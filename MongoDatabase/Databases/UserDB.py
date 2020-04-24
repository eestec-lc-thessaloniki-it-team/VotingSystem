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
        :return: the user with this email or None if not found
        """
        try:
            jsonReturned = self.db.find_one({"mail": mail})
            if jsonReturned:
                object = getUserFromJson(jsonReturned)
                return object
            return None
        except:
            return None

    def getUserWithSessionId(self, session_id: str) -> (Optional[User], str):
        """

        :param session_id:
        :return: the user object, the user_id from mongo
        """
        jsonReturned = self.db.find_one({"session_id": session_id})
        if jsonReturned:
            object = getUserFromJson(jsonReturned)
            return object, str(jsonReturned["_id"])
        else:
            return None, ""

    def createNewUser(self, name: str, mail: str, password: str) -> UserWrapper:
        """
        :param name:
        :param mail:
        :param password:
        :return:
        """
        _user = self._findUserByMail(mail)
        if _user:
            return UserWrapper(None, found=True, userFound=True,
                               operationDone=False)  # Dont return saved user when find it in db

        user: User = User(name, mail, password)
        self.db.insert_one(user.makeJson())
        return UserWrapper(user, found=False, userFound=False, operationDone=True)

    def logInUser(self, mail: str, password: str) -> UserWrapper:
        """

        :param mail:
        :param password:
        :return:
        """
        user: User = self._findUserByMail(mail)
        if not user:
            return UserWrapper(None, found=False, userFound=False, operationDone=False)
        if user.verify_password(password):
            user.createSessionId()  # This will update session id
            return self.updateUser(user)
        return UserWrapper(None, found=True, userFound=True,
                           operationDone=False)  # Don't return it if gave wrong password

    def updateUser(self, newUser: User) -> UserWrapper:
        """
        Save the new instance in the database and return in wrapper
        :param newUser:
        :return:
        """
        try:
            returned = self.db.update_one({"mail": newUser.mail}, {'$set': newUser.makeJson()})
            return UserWrapper(newUser, found=True, userFound=True, operationDone=bool(returned.matched_count))
        except:
            return UserWrapper(newUser, found=False, userFound=False, operationDone=False)

    def deleteUser(self, mail: str) -> UserWrapper:
        _user = self._findUserByMail(mail)
        if not _user:  # didnt find it
            return UserWrapper(None, found=False, userFound=False, operationDone=False)
        try:
            returned = self.db.delete_many({'mail': mail})
            return UserWrapper(None, found=False, userFound=False, operationDone=bool(returned.deleted_count))
        except:
            return UserWrapper(None, found=False, userFound=False, operationDone=False)

    def fillUsernames(self, votesWrapper: VotesWrapper) -> VotesWrapper:
        """
        This function will get the user_ids for everyone and change it with their names from the database
        :param votesWrapper:
        :return: Return the wrapper that now contain the names
        """
        return VotesWrapper()
