# import sys
# sys.path.append("C:\\Users\\fotin\\OneDrive\\Documents\\VotingSystem")
from datetime import datetime
from typing import List

from pymongo import MongoClient

from MongoDatabase.Databases.PollsDB import PollsDB
from MongoDatabase.Databases.UserDB import UserDB
from MongoDatabase.Databases.VotesDB import VotesDB
from MongoDatabase.Wrappers.PollWrapper import PollWrapper
from MongoDatabase.Wrappers.UserWrapper import UserWrapper
from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from MongoDatabase.user import *  # get credentials


class MongoDB:
    """
    Will contain a function for connecting to db and then one of the other 3 objects from the same package
    """

    def __init__(self, database="lcThessalonikiVoting"):
        url = """mongodb://{}:{}@116.203.85.249/{}""".format(username, password, database)
        self.client = MongoClient(url, authSource="admin")[database]
        self.userDB = UserDB(self.client.lcThessaloniki)
        self.pollsDB = PollsDB(self.client.lcThessaloniki)
        self.votesDB = VotesDB(self.client.lcThessaloniki)

    def logIn(self, mail: str, password: str) -> UserWrapper:
        """
        Returns a user with mail and password.
        :param mail:
        :param password:
        :return: UserWrapper
        """
        return self.userDB.logInUser(mail, password)

    def register(self, name: str, mail: str, password: str) -> UserWrapper:
        """
        Returns a user with name, mail and password.
        :param name:
        :param mail:
        :param password:
        :return: UserWrapper
        """
        return self.userDB.createNewUser(name, mail, password)

    def createPoll(self, question: str, options: List[str], named: bool, unique: bool, session_id: str) -> PollWrapper:
        """
        Checks if user exists. Creates a new poll.
        :param question:
        :param options:
        :param named:
        :param unique:
        :param session_id:
        :return: PollWrapper
        """
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        if user is None:
            return PollWrapper(None, "", found=False, userFound=False, operationDone=False)
        return self.pollsDB.createPoll(question, options, named, unique, user_id)

    def getPollById(self, poll_id: str, session_id: str) -> PollWrapper:
        """
        Checks if user exists. Gets a poll with poll_id.
        :param poll_id:
        :param session_id:
        :return: PollWrapper
        """
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        if user is None:
            return PollWrapper(None, "", found=False, userFound=False, operationDone=False)
        return self.pollsDB.getPollById(poll_id)

    def vote(self, poll_id: str, chosen_option: int, session_id: str) -> VotesWrapper:
        """
        Checks if user exists. Creates a VotesWrapper.
        :param poll_id:
        :param chosen_option:
        :param session_id:
        :return: VotesWrapper
        """
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        if user is None:
            return VotesWrapper("", {}, named=False, found=False, userFound=False, operationDone=False)
        poll: PollWrapper = self.pollsDB.getPollById(poll_id)
        if not poll.found:
            return VotesWrapper("", {}, named=False, found=False, userFound=True, operationDone=False)
        if not self.checkIfValidVote(session_id=session_id, poll_id=poll_id):
            return VotesWrapper("", named=poll.object.named, found=True, userFound=True, operationDone=False)
        votesWrapper: VotesWrapper = self.votesDB.createVote(user_id, poll_id, poll.object.named,
                                                             chosen_option)
        if votesWrapper.named:
            return self.userDB.fillUsernames(votesWrapper)
        else:
            return votesWrapper

    def mvotes(self, poll_id: str, chosen_option: [], session_id: str):
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        if user is None:
            return VotesWrapper("", {}, named=False, found=False, userFound=False, operationDone=False)
        poll: PollWrapper = self.pollsDB.getPollById(poll_id)
        if not poll.found:
            return VotesWrapper("", {}, named=False, found=False, userFound=True, operationDone=False)
        votesWrapper: VotesWrapper = None
        for choice in chosen_option:
            votesWrapper = self.votesDB.createVote(user_id, poll_id, poll.object.named,
                                                   choice) #return the last one
        if votesWrapper.named:
            return self.userDB.fillUsernames(votesWrapper)
        else:
            return votesWrapper

    def results(self, poll_id: str, after_timestamp, session_id: str):
        """
        Checks if user exists. Gets all votes for this poll_id, divided into options.
        :param poll_id:
        :param after_timestamp:
        :param session_id:
        :return:
        """
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        if user is None:
            return VotesWrapper("", {}, named=False, found=False, userFound=False, operationDone=False)
        poll: PollWrapper = self.pollsDB.getPollById(poll_id)
        if not poll.found:
            return VotesWrapper("", {}, named=False, found=False, userFound=True, operationDone=False)
        # makeTimestamp
        if after_timestamp != 0:
            dateTimeObject = datetime.strptime(after_timestamp, "%Y-%m-%d %H:%M:%S.%f")
            votesWrapper: VotesWrapper = self.votesDB.getAllVotes(poll_id, poll.object.named,
                                                                  dateTimeObject.timestamp())
        else:
            votesWrapper: VotesWrapper = self.votesDB.getAllVotes(poll_id, poll.object.named, 0)
        votesWrapper.lastTimestamp = str(datetime.fromtimestamp(votesWrapper.lastTimestamp))
        if not votesWrapper.named or len(votesWrapper.votes) == 0:
            return votesWrapper
        else:
            return self.userDB.fillUsernames(votesWrapper)

    def checkIfValidSessionId(self, session_id: str) -> bool:
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        return user is not None

    def checkIfValidVote(self, session_id: str, poll_id: str) -> bool:
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        pollWrapper: PollWrapper = self.pollsDB.getPollById(poll_id)
        if user is None or pollWrapper.object is None:
            return False
        if self.votesDB.getVote(user_id, poll_id) is not None:
            return False
        return True

# PRINT TESTS
#
# my_db = MongoDB()
# user1 = User("user1","mail1","sdaeas")
# user2 = User("user2","mail2","ssdaxs")
# user3 = User("user3","mail3","sdgdas")
#
# user1_id = my_db.userDB.db.insert_one(user1.makeJson()).inserted_id
# user2_id = my_db.userDB.db.insert_one(user2.makeJson()).inserted_id
# user3_id = my_db.userDB.db.insert_one(user3.makeJson()).inserted_id
#
# vote1 = my_db.votesDB.createVote(str(user1_id),"1",1)
# vote2 = my_db.votesDB.createVote(str(user2_id),"1",0)
# vote3 = my_db.votesDB.createVote(str(user3_id),"1",2)
# vote4 = my_db.votesDB.createVote(str(user3_id),"1",3)
# vote5 = my_db.votesDB.createVote(str(user3_id),"1",1)
# vote6 = my_db.votesDB.createVote(str(user3_id),"1",0)
#
# wrapper = my_db.votesDB.getAllVotes("1",True)
# print(wrapper.votes)
#
# wrapper = my_db.userDB.fillUsernames(wrapper)
# print(wrapper.votes)
#
# my_db.votesDB.db.drop()
# my_db.userDB.db.drop()
