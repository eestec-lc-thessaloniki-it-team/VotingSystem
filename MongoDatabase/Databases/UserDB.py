from typing import Optional

from MongoDatabase.Wrappers.UserWrapper import UserWrapper
from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from model.User import User


class UserDB:
    def __init__(self, client):
        self.client = client
        self.db = self.client.userDB
        pass

    def _findUserByMail(self, mail: str) -> Optional[User]:
        """

        :param mail:
        :return:
        """
        pass

    def getUserWithSessionId(self, session_id: str) -> (Optional[User], str):
        """

        :param session_id:
        :return: the user object, the user_id from mongo
        """
        pass

    def createNewUser(self, name: str, mail: str, password: str) -> UserWrapper:
        """
        :param name:
        :param mail:
        :param password:
        :return:
        """
        # TODO: check if mail already exists
        user: User = User(name, mail, password)
        # Todo: persist it to database
        return UserWrapper()

    def logInUser(self, mail: str, password: str) -> UserWrapper:
        """

        :param mail:
        :param password:
        :return:
        """
        user: User = self._findUserByMail(mail)
        # TODO: check if user is not None else return found=false
        if user.verify_password(password):
            user.createSessionId()  # This will update session id
            return self.updateUser(user)
        # Todo: return userWrapper with operation=false
        return UserWrapper

    def updateUser(self, newUser: User) -> UserWrapper:
        """
        Save the new instance in the database and return in wrapper
        :param newUser:
        :return:
        """
        # TODO: persist new user in database
        # TODO: check if everything is ok and return it
        return UserWrapper

    def fillUsernames(self, votesWrapper: VotesWrapper) -> VotesWrapper:
        """
        This function will get the user_ids for everyone and change it with their names from the database
        :param votesWrapper:
        :return: Return the wrapper that now contain the names
        """
        return VotesWrapper()
