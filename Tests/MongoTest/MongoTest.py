import unittest

from MongoDatabase.MongoDB import MongoDB
from MongoDatabase.Wrappers.PollWrapper import PollWrapper
from MongoDatabase.Wrappers.UserWrapper import UserWrapper
from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from model.Poll import Poll
from model.User import User


class MongoTest(unittest.TestCase):
    """
    The ultimate test after everything wasted, check the responses before moving to Flask
    """

    def setUp(self) -> None:
        # get connection, 2 users, 2 polls (named/unnamed), 4 votes, third user for testing the logIn
        self.connection = MongoDB()
        self.user: User = User("mavroudo", "mail@mail.mail", "1234")
        self.user2: User = User("charis", "charis@mail.mail", "12345")
        self.user3: User = User("Stef", "stef@mail.mail", "asdf")

        userWrapper: UserWrapper = self.connection.userDB.createNewUser(self.user.name, self.user.mail,
                                                                        self.user.password)
        self.assertIsNotNone(userWrapper.object)
        self.assertIsNotNone(userWrapper.object.session_id)
        self.session_id = userWrapper.object.session_id
        userWrapper2: UserWrapper = self.connection.userDB.createNewUser(self.user2.name, self.user2.mail,
                                                                         self.user2.password)
        self.assertIsNotNone(userWrapper2.object)
        self.assertIsNotNone(userWrapper2.object.session_id)
        self.session_id2 = userWrapper.object.session_id

        # get user id from session_id
        (user, self.user_id) = self.connection.userDB.getUserWithSessionId(self.session_id)
        self.assertIsNotNone(user)
        self.assertNotEqual(self.user_id, "")
        (user2, self.user_id2) = self.connection.userDB.getUserWithSessionId(self.session_id2)
        self.assertIsNotNone(user2)
        self.assertNotEqual(self.user_id2, "")
        # add polls
        self.poll: Poll = Poll("how cool are we?", ["A lot", "A lot but second", "same as 2"], named=True, unique=True,
                               creator_user_id=self.user_id)
        pollWrapper: PollWrapper = self.connection.pollsDB.createPoll(self.poll.question, self.poll.options,
                                                                      self.poll.named, self.poll.unique, self.user_id)
        self.assertTrue(pollWrapper.operationDone)
        self.assertIsNotNone(pollWrapper.object)
        self.poll_id = pollWrapper.pollId

        self.poll2_noNamed: Poll = Poll("how cool are we?", ["A lot", "A lot but second", "same as 2"], named=False,
                                        unique=True,
                                        creator_user_id=self.user_id)
        pollWrapper2: PollWrapper = self.connection.pollsDB.createPoll(self.poll2_noNamed.question,
                                                                       self.poll2_noNamed.options,
                                                                       self.poll2_noNamed.named,
                                                                       self.poll2_noNamed.unique, self.user_id)
        self.assertTrue(pollWrapper2.operationDone)
        self.assertIsNotNone(pollWrapper2.object)
        self.poll_id2 = pollWrapper2.pollId
        # add 2 votes for each
        voteWrapper: VotesWrapper = self.connection.votesDB.createVote(self.user_id, self.poll_id, self.poll.named, 0)
        self.assertTrue(voteWrapper.operationDone)
        voteWrapper: VotesWrapper = self.connection.votesDB.createVote(self.user_id2, self.poll_id, self.poll.named, 1)
        self.assertTrue(voteWrapper.operationDone)
        voteWrapper: VotesWrapper = self.connection.votesDB.createVote(self.user_id, self.poll_id2,
                                                                       self.poll2_noNamed.named, 0)
        self.assertTrue(voteWrapper.operationDone)
        voteWrapper: VotesWrapper = self.connection.votesDB.createVote(self.user_id2, self.poll_id2,
                                                                       self.poll2_noNamed.named, 1)
        self.assertTrue(voteWrapper.operationDone)

    def test_log_in(self):
        """
        Charis trying to logIn, first forgets mail, then forgets password, then does it correct
        """
        userWrapper: UserWrapper = self.connection.logIn("forget@mail.com", "12345")
        self.assertFalse(userWrapper.operationDone)
        self.assertFalse(userWrapper.userFound)
        userWrapper: UserWrapper = self.connection.logIn(self.user2.mail, "forgotPass")
        self.assertTrue(userWrapper.userFound)
        self.assertFalse(userWrapper.operationDone)
        userWrapper: UserWrapper = self.connection.logIn(self.user2.mail, self.user2.password)
        self.assertTrue(userWrapper.operationDone)
        self.assertIsNotNone(userWrapper.object)
        self.assertIsNotNone(userWrapper.object.session_id)

    def test_register(self):
        """
        A new user, user3 is trying to register to our system. First uses a mail that has used before, but then
        creates a new user successfully
        """
        userWrapper: UserWrapper = self.connection.register(self.user3.name, self.user.mail, self.user3.password)
        self.assertFalse(userWrapper.operationDone)
        self.assertTrue(userWrapper.userFound)
        userWrapper: UserWrapper = self.connection.register(self.user3.name, self.user3.mail, self.user3.password)
        self.assertTrue(userWrapper.operationDone)
        self.assertIsNotNone(userWrapper.object)

        # delete it afterwards
        userWrapper: UserWrapper = self.connection.userDB.deleteUser(self.user3.mail)
        self.assertTrue(userWrapper.operationDone)

    def test_create_poll(self):
        """
        User1 will try to create a poll. First he is not connected, so no session_id is given. Then complete it
        :return:
        """
        poll: Poll = Poll("how cool are we?", ["A lot", "A lot but second", "same as 2"], named=False,
                          unique=True,
                          creator_user_id=self.user_id)
        pollWrapper: PollWrapper = self.connection.createPoll(poll.question, poll.options, poll.named, poll.unique, "")
        self.assertFalse(pollWrapper.operationDone)
        self.assertFalse(pollWrapper.userFound)

        pollWrapper: PollWrapper = self.connection.createPoll(poll.question, poll.options, poll.named, poll.unique,
                                                              self.session_id)
        self.assertTrue(pollWrapper.operationDone)
        self.assertTrue(pollWrapper.userFound)
        self.assertEqual(pollWrapper.object.question,poll.question)

    def tearDown(self) -> None:
        user: UserWrapper = self.connection.userDB.deleteUser(self.user.mail)
        self.assertTrue(user.operationDone)
        user2: UserWrapper = self.connection.userDB.deleteUser(self.user2.mail)
        self.assertTrue(user2.operationDone)
        poll = self.connection.pollsDB.deletePollById(poll_id=self.poll_id)
        self.assertTrue(poll.operationDone)
        self.assertTrue(self.connection.votesDB.deleteVote(self.poll_id))
        poll2 = self.connection.pollsDB.deletePollById(poll_id=self.poll_id2)
        self.assertTrue(poll2.operationDone)
        self.assertTrue(self.connection.votesDB.deleteVote(self.poll_id2))


if __name__ == '__main__':
    unittest.main()
