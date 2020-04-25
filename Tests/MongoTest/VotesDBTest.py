import unittest

from MongoDatabase.MongoDB import MongoDB
from MongoDatabase.Wrappers.PollWrapper import PollWrapper
from MongoDatabase.Wrappers.UserWrapper import UserWrapper
from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from model.Poll import Poll
from model.User import User


class VotesDBTest(unittest.TestCase):
    def setUp(self) -> None:
        # get connection, add 2 users, 2 polls, 1 vote for the first
        self.connection = MongoDB()
        self.user: User = User("mavroudo", "mail@mail.mail", "1234")
        self.user2: User = User("charis", "charis@mail.mail", "12345")

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

    def test_get_all_votes(self):
        # create vote has been tested in setUp and deleteVote in tearDown
        # get all votes for an incorrect pollId
        votesWrapper: VotesWrapper = self.connection.votesDB.getAllVotes("123456", named=True)
        self.assertFalse(votesWrapper.operationDone)
        # get all votes from the first poll id, named=True
        votesWrapper: VotesWrapper = self.connection.votesDB.getAllVotes(self.poll_id, named=True)
        self.assertTrue(votesWrapper.operationDone)
        self.assertTrue(votesWrapper.found)
        self.assertEqual(len(votesWrapper.votes), 2)
        self.assertTrue(votesWrapper.votes.get(0)[0], self.user_id)
        self.assertTrue(votesWrapper.votes.get(1)[0], self.user_id2)
        # get all votes from the second poll, named=False
        votesWrapper2: VotesWrapper = self.connection.votesDB.getAllVotes(self.poll_id2, named=False)
        self.assertTrue(votesWrapper2.operationDone)
        self.assertEqual(len(votesWrapper2.votes),2)
        self.assertEqual(votesWrapper2.votes.get(0),1)
        self.assertEqual(votesWrapper2.votes.get(1),1)

    def tearDown(self) -> None:
        # delete users, poll, votes
        user: UserWrapper = self.connection.userDB.deleteUser(self.user.mail)
        self.assertTrue(user.operationDone)
        user2: UserWrapper = self.connection.userDB.deleteUser(self.user2.mail)
        self.assertTrue(user2.operationDone)
        poll = self.connection.pollsDB.deletePollById(poll_id=self.poll_id)
        self.assertTrue(poll.operationDone)
        self.assertTrue(self.connection.votesDB.deleteVote(self.poll_id))


if __name__ == '__main__':
    unittest.main()
