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
        Finds a user with mail
        :param mail
        :return: User object
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
        Gets user with session_id
        :param session_id
        :return: user object, user_id
        """
        try:
            jsonReturned = self.db.find_one({"session_id": session_id})
            if jsonReturned:
                object = getUserFromJson(jsonReturned)
                return object, str(jsonReturned["_id"])
            else:
                return None, ""
        except:
            return None, ""

    def createNewUser(self, name: str, mail: str, password: str) -> UserWrapper:
        """
        Creates a user with name, mail and password
        :param name
        :param mail
        :param password
        :return: UserWrapper
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
        Returns a UserWrapper with mail and password
        :param mail
        :param password
        :return: UserWrapper
        """
        user: User = self._findUserByMail(mail)
        if not user:
            return UserWrapper(None, found=False, userFound=False, operationDone=False)
        if user.verify_password(password):
            user.createSessionId()  # This will update session id
            return self.updateUser(user)
        return UserWrapper(None, found=True, userFound=True,
                           operationDone=False)

    def updateUser(self, newUser: User) -> UserWrapper:
        """
        Saves the new instance in the database
        :param newUser
        :return: UserWrapper
        """
        try:
            returned = self.db.update_one({"mail": newUser.mail}, {'$set': newUser.makeJson()})
            return UserWrapper(newUser, found=True, userFound=True, operationDone=bool(returned.matched_count))
        except:
            return UserWrapper(newUser, found=False, userFound=False, operationDone=False)

    def deleteUser(self, mail: str) -> UserWrapper:
        """
        Deletes a User with inserted mail
        :param mail:
        :return: UserWrapper
        """
        _user = self._findUserByMail(mail)
        if not _user:
            return UserWrapper(None, found=False, userFound=False, operationDone=False)
        try:
            returned = self.db.delete_many({'mail': mail})
            return UserWrapper(None, found=False, userFound=False, operationDone=bool(returned.deleted_count))
        except:
            return UserWrapper(None, found=False, userFound=False, operationDone=False)

    def fillUsernames(self, votesWrapper: VotesWrapper) -> VotesWrapper:
        """
        Gets the user_ids for everyone and change it with their names from the database
        :param votesWrapper:
        :return: VotesWrapper
        """
        if votesWrapper.votes:
            for option,userList in votesWrapper.votes.items():
                if type(userList) is not list:
                    raise ValueError("Dict must contain only list values")
            votesDict = {option:list() for option in votesWrapper.votes}
            for option, userList in votesWrapper.votes.items():
                votesDict[option] = [getUserFromJson(self.db.find_one({"_id": ObjectId(user_id)})).name for user_id in userList]
            return VotesWrapper(votesWrapper.lastTimestamp, votesDict, found=votesWrapper.found,
                                userFound=votesWrapper.userFound, operationDone=votesWrapper.operationDone)
        return VotesWrapper(votesWrapper.lastTimestamp, {}, found=False, userFound=False, operationDone=False)