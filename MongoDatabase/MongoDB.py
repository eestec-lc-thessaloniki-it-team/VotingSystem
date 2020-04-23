# import sys
# sys.path.append("C:\\Users\\fotin\\OneDrive\\Documents\\VotingSystem")
from datetime import datetime
from typing import List
from pymongo import MongoClient
from model.User import User
from MongoDatabase.user import * # get credentials
from MongoDatabase.Databases.UserDB import UserDB
from MongoDatabase.Databases.PollsDB import PollsDB
from MongoDatabase.Databases.VotesDB import VotesDB
from MongoDatabase.Wrappers.UserWrapper import UserWrapper
from MongoDatabase.Wrappers.PollWrapper import PollWrapper
from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from model.Vote import getVoteFromJson, Vote  # TODO DELETE



class MongoDB:
    """
        Will contain a function for connecting to db and then one of the other 3 objects from the same package
    """

    def __init__(self, database="lcThessalonikiVoting"):
        url = """mongodb://{}:{}@116.203.85.249/{}""".format(username, password, database)  # TODO: fill with credentials
        self.client = MongoClient(url, authSource="admin")[database]  # TODO: fill with credentials
        self.userDB = UserDB(self.client.lcThessaloniki)
        self.pollsDB = PollsDB(self.client.lcThessaloniki)
        self.votesDB = VotesDB(self.client.lcThessaloniki)

    def logIn(self, mail: str, password: str) -> UserWrapper:
        return self.userDB.logInUser(mail, password)

    def register(self, name: str, mail: str, password: str) -> UserWrapper:
        return self.userDB.createNewUser(name, mail, password)

    def createPoll(self, question: str, options: List[str], named: bool, unique: bool, session_id: str) -> PollWrapper:
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        # TODO: check if user is not none, if is is return userFound=False
        return self.pollsDB.createPoll(question, options, named, unique, user_id)

    def getPollById(self, poll_id: str, session_id: str) -> PollWrapper:
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        # TODO: check if user is not none, if is is return userFound=False
        return self.pollsDB.getPollById(poll_id)

    def vote(self, poll_id: str, chosen_option: int, session_id: str) -> VotesWrapper:
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        # TODO: check if user is not none, if is is return userFound=False
        votesWrapper: VotesWrapper = self.votesDB.createVote(poll_id, user_id, chosen_option)
        if votesWrapper.named:
            return self.userDB.fillUsernames(votesWrapper)
        else:
            return votesWrapper

    def results(self, poll_id: str, after_timestamp,session_id: str):
        (user, user_id) = self.userDB.getUserWithSessionId(session_id)
        # TODO: check if user is not none, if is is return userFound=False
        votesWrapper: VotesWrapper=self.votesDB.getAllVotes(poll_id,after_timestamp)
        if votesWrapper.named:
            return self.userDB.fillUsernames(votesWrapper)
        else:
            return votesWrapper

# my_db = MongoDB()
# my_db.votesDB.db.drop()