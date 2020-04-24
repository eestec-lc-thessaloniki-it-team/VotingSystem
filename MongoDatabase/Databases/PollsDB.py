from typing import Optional, List
from model.Poll import Poll
from model.User import User
from MongoDatabase.Wrappers.PollWrapper import PollWrapper
from model.Poll import getPollFromJson

class PollsDB:
    def __init__(self, client):
        self.client = client
        self.db = self.client.pollsDB

    def _findPollById(self, poll_id: str) -> Optional[Poll]:
        """

        :param poll_id:
        :return:
        """
        try:
            jsonReturned = self.db.find_one({"_id":poll_id})
            if jsonReturned:
                object = getPollFromJson(jsonReturned)
                return object
            return None
        except:
            return None


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
        try:
            poll:Poll=Poll(question,options,named,unique,user_id)
            poll_id = str(self.db.insert_one(poll.makeJson()).inserted_id)
            return PollWrapper(poll, poll_id, found=True, userFound=True, operationDone=True)
        except:
            return PollWrapper(None, "", found=False, userFound=False, operationDone=False)

    def getPollById(self, poll_id: str) -> PollWrapper:
        """
        :param poll_id:
        :return:
        """
        try:
            poll: Poll = self._findPollById(poll_id)
            # TODO: wrap it in a wrapper
            # Todo: if poll_id don't exist send found=false
            if poll:
                return PollWrapper(poll, poll_id, found=True, userFound=True, operationDone=True)
            return PollWrapper(poll, poll_id, found=False, userFound=False, operationDone=False)
        except:
            return PollWrapper(None, "", found=False, userFound=False, operationDone=False)

