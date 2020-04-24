import unittest

from MongoDatabase.MongoDB import MongoDB
from MongoDatabase.Wrappers.UserWrapper import UserWrapper
from model.User import User


class UserDBTest(unittest.TestCase):

    def setUp(self) -> None:
        self.connection = MongoDB()  # this will connect to mongo
        self.user1 = User("mavroudo", "mavroudo@mail.mail", "1234")
        self.user2_same_mail = User("mavroudo2", "mavroudo@mail.mail", "4567")
        self.user3 = User("kalliopi", "k@mail.mail", "789")
        userWrapper: UserWrapper = self.connection.userDB.createNewUser(self.user1.name, self.user1.mail,
                                                                        self.user1.password)
        self.assertTrue(userWrapper.operationDone)

    def test_create_new_user(self):
        # check added user with same mail
        userWrapper: UserWrapper = self.connection.userDB.createNewUser(self.user2_same_mail.name,
                                                                        self.user2_same_mail.mail,
                                                                        self.user2_same_mail.password)
        self.assertEqual(userWrapper.object, None)
        self.assertEqual(userWrapper.userFound, True)
        self.assertEqual(userWrapper.operationDone, False)

        # check added a new one
        userWrapper: UserWrapper = self.connection.userDB.createNewUser(self.user3.name, self.user3.mail,
                                                                        self.user3.password)
        self.assertEqual(userWrapper.operationDone, True)
        self.assertEqual(userWrapper.userFound, False)
        userSaved = userWrapper.object
        self.assertEqual(userSaved.name, self.user3.name)
        self.assertIsNotNone(userSaved.session_id)
        self.assertNotEqual(userSaved.password, self.user3.password)

        # delete user3 that added in
        self.connection.userDB.deleteUser(self.user3.mail)

    def test_log_in_user(self):
        # only user1 is saved
        # try to log in with user 3
        userWrapper: UserWrapper = self.connection.userDB.logInUser(self.user3.mail, self.user3.password)
        self.assertIsNone(userWrapper.object)
        self.assertFalse(userWrapper.operationDone)
        self.assertFalse(userWrapper.found)
        # try to log in with correct mail but wrong password
        userWrapper: UserWrapper = self.connection.userDB.logInUser(self.user2_same_mail.mail,
                                                                    self.user2_same_mail.password)
        self.assertFalse(userWrapper.operationDone)
        self.assertTrue(userWrapper.found)  # found but not correct
        self.assertIsNone(userWrapper.object)
        # try to log in with correct credentials, will also test update user
        userWrapper: UserWrapper = self.connection.userDB.logInUser(self.user1.mail, self.user1.password)
        self.assertTrue(userWrapper.operationDone)
        self.assertTrue(userWrapper.found)
        userSaved: User = userWrapper.object
        self.assertEqual(userSaved.name, self.user1.name)

    def test_get_user_with_session_id(self):
        # try to get user with wrong session_id
        (user, user_id) = self.connection.userDB.getUserWithSessionId("ThatsWrongSessionID")
        self.assertIsNone(user)
        self.assertEqual(user_id, "")
        # try with correct session_id
        userWrapper: UserWrapper = self.connection.userDB.logInUser(self.user1.mail, self.user1.password)
        userSaved: User = userWrapper.object
        self.assertIsNotNone(userSaved)
        (user, user_id) = self.connection.userDB.getUserWithSessionId(userSaved.session_id)
        self.assertEqual(user.name, self.user1.name)
        self.assertNotEqual(user_id, "")

    def test_update_user(self):
        # Test i want to change the name
        userWrapper: UserWrapper = self.connection.userDB.updateUser(
            User("mavroudo_best", self.user1.mail, self.user1.password))
        self.assertNotEqual(userWrapper.object.password, "1234")  # it has been hashed
        self.assertIsNotNone(userWrapper.object.session_id)
        # Trying to log in with mail and password and check the name if changed
        userWrapper1: UserWrapper = self.connection.userDB.logInUser(self.user1.mail, self.user1.password)
        self.assertEqual(userWrapper1.object.name,"mavroudo_best")
        self.assertNotEqual(userWrapper1.object.session_id,userWrapper.object.session_id)
        self.assertEqual(userWrapper.object.password,userWrapper1.object.password)

    def test_fill_user_names(self):
        pass

    def tearDown(self) -> None:
        userWrapper: UserWrapper = self.connection.userDB.deleteUser(self.user1.mail)
        self.assertTrue(userWrapper.operationDone)
