# import sys
# sys.path.insert(0, "C:\\Users\\fotin\\OneDrive\\Documents\\VotingSystem")
from typing import Optional

from MongoDatabase.Wrappers.UserWrapper import UserWrapper
from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from model.User import User
from bson import ObjectId
from model.User import getUserFromJson


class UserDB:
    def __init__(self, client):
        self.client = client
        self.db = self.client.userDB

    def _findUserByMail(self, mail: str) -> Optional[User]:
        """

        :param mail:
        :return:
        """
        jsonReturned = self.db.find_one({"mail": mail})
        object = getUserFromJson(jsonReturned)
        return object

    def getUserWithSessionId(self, session_id: str) -> (Optional[User], str):
        """

        :param session_id:
        :return: the user object, the user_id from mongo
        """
        jsonReturned = self.db.find_one({"session_id": session_id})
        object = getUserFromJson(jsonReturned)
        return (object, str(jsonReturned["_id"]))
        

    def createNewUser(self, name: str, mail: str, password: str) -> UserWrapper:
        """
        :param name:
        :param mail:
        :param password:
        :return:
        """
        # TODO: check if mail already exists
        user: User = User(name, mail, password)
        self.db.insert_one(user.makeJson())
        # Todo: persist it to database
        return UserWrapper(user, True, True, True)

    def logInUser(self, mail: str, password: str) -> UserWrapper:
        """

        :param mail:
        :param password:
        :return:
        """
        user: User = self._findUserByMail(mail)
        # TODO: check if user is not None else return found=false
        if user is None:
            return UserWrapper(None)
        if user.verify_password(password):
            user.createSessionId()  # This will update session id
            return self.updateUser(user)
        # Todo: return userWrapper with operation=false
        return UserWrapper(user, True, True, False)

    def updateUser(self, newUser: User) -> UserWrapper:
        """
        Save the new instance in the database and return in wrapper
        :param newUser:
        :return:
        """
        # TODO: persist new user in database
        # TODO: check if everything is ok and return it
        returned = self.db.update_one({"mail": newUser.mail}, {'$set': newUser.makeJson()})
        return UserWrapper(newUser, True, True, bool(returned.matched_count))

    def fillUsernames(self, votesWrapper: VotesWrapper) -> VotesWrapper:
        """
        This function will get the user_ids for everyone and change it with their names from the database
        :param votesWrapper:
        :return: Return the wrapper that now contain the names
        """
        return VotesWrapper()
