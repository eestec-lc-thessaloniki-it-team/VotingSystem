from typing import Optional, List
from model.Poll import Poll
from model.User import User
from MongoDatabase.Wrappers.PollWrapper import PollWrapper


class PollsDB:
    def __init__(self, client):
        self.client = client
        self.db = self.client.pollsDB

    def _findPollById(self, poll_id: str) -> Optional[Poll]:
        """

        :param poll_id:
        :return:
        """
        pass

    def createPoll(self, question: str, options: List[str], named: bool, unique: bool, user_id: str) -> PollWrapper:
        """
        :param user:
        :param question:
        :param options:
        :param named:
        :param unique:
        :param session_id:
        :return:
        """
        # TODO: persist it in the database and return the proper wrapper
        # TODO: if something went wrong return operationsDone=false
        poll:Poll=Poll(question,options,named,unique,user_id)
        return PollWrapper

    def getPollById(self, poll_id: str) -> PollWrapper:
        """
        :param poll_id:
        :return:
        """
        poll: Poll = self._findPollById(poll_id)
        # TODO: wrap it in a wrapper
        return PollWrapper()
