import unittest

from MongoDatabase.MongoDB import MongoDB
from MongoDatabase.Wrappers.PollWrapper import PollWrapper
from MongoDatabase.Wrappers.UserWrapper import UserWrapper
from model.Poll import Poll
from model.User import User


class PollsDBTest(unittest.TestCase):

    def setUp(self) -> None:
        # get connection, create a user, get its session_id, create a Poll object
        self.connection = MongoDB()
        self.user: User = User("mavroudo", "mail@mail.mail", "1234")

        userWrapper: UserWrapper = self.connection.userDB.createNewUser(self.user.name, self.user.mail,
                                                                        self.user.password)
        self.assertIsNotNone(userWrapper.object)
        self.assertIsNotNone(userWrapper.object.session_id)
        self.session_id = userWrapper.object.session_id
        # get user id from session_id
        (user, user_id) = self.connection.userDB.getUserWithSessionId(self.session_id)

        self.assertIsNotNone(user)
        self.assertNotEqual(user_id, "")
        self.poll: Poll = Poll("how cool are we?", ["A lot", "A lot but second", "same as 2"], named=True, unique=True,
                               creator_user_id=user_id)
        pollWrapper: PollWrapper = self.connection.pollsDB.createPoll(self.poll.question, self.poll.options,
                                                                      self.poll.named, self.poll.unique, user_id)
        self.assertTrue(pollWrapper.operationDone)
        self.assertIsNotNone(pollWrapper.object)
        self.poll_id = pollWrapper.pollId

    def test_get_poll_by_id(self):
        #create and delete are tested in setUp and tear down respectively

        # ask for a poll_id that does not exist
        pollWrapper: PollWrapper = self.connection.pollsDB.getPollById("12345567788")
        self.assertIsNone(pollWrapper.object)
        self.assertFalse(pollWrapper.found)
        self.assertFalse(pollWrapper.operationDone)
        # ask for the poll that is inside
        pollWrapper: PollWrapper = self.connection.pollsDB.getPollById(self.poll_id)
        print(pollWrapper.makeJson())
        self.assertTrue(pollWrapper.operationDone)
        self.assertIsNotNone(pollWrapper.object)
        poll = pollWrapper.object
        self.assertEqual(poll.question, self.poll.question)

    def tearDown(self) -> None:
        # delete user and poll
        user: UserWrapper = self.connection.userDB.deleteUser(self.user.mail)
        self.assertTrue(user.operationDone)
        poll = self.connection.pollsDB.deletePollById(poll_id=self.poll_id)
        self.assertTrue(poll.operationDone)


if __name__ == '__main__':
    unittest.main()
