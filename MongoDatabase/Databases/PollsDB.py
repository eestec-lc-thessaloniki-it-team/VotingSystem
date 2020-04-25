from typing import Optional, List

from MongoDatabase.Wrappers.PollWrapper import PollWrapper
from model.Poll import Poll
from model.Poll import getPollFromJson
from bson import ObjectId


class PollsDB:
    def __init__(self, client):
        self.client = client
        self.db = self.client.pollsDB

    def _findPollById(self, poll_id: str) -> Optional[Poll]:
        """
        Finds a poll with poll_id
        :param poll_id
        :return: Poll object
        """
        try:
            jsonReturned = self.db.find_one({"_id": ObjectId(poll_id)})
            if jsonReturned:
                object = getPollFromJson(jsonReturned)
                return object
            return None
        except:
            return None

    def createPoll(self, question: str, options: List[str], named: bool, unique: bool, user_id: str) -> PollWrapper:
        """
        Creates a new Poll
        :param user
        :param question
        :param options
        :param named
        :param unique
        :param session_id
        :return: PollWrapper
        """
        try:
            poll: Poll = Poll(question, options, named, unique, user_id)
            poll_id = str(self.db.insert_one(poll.makeJson()).inserted_id)
            return PollWrapper(poll, poll_id, found=True, userFound=True, operationDone=True)
        except:
            return PollWrapper(None, None, found=False, userFound=False, operationDone=False)

    def getPollById(self, poll_id: str) -> PollWrapper:
        """
        Gets a Poll with poll_id
        :param poll_id
        :return: PollWrapper
        """
        try:
            poll: Poll = self._findPollById(poll_id)
            if poll:
                return PollWrapper(poll, poll_id, found=True, userFound=True, operationDone=True)
            return PollWrapper(poll, poll_id, found=False, userFound=True, operationDone=False)
        except:
            return PollWrapper(None, None, found=False, userFound=True, operationDone=False)

    def deletePollById(self, poll_id: str) -> PollWrapper:
        """
        Delete the poll with the given poll_id
        :param poll_id:
        :return:
        """
        _poll = self._findPollById(poll_id)
        if not _poll:
            return PollWrapper(None, None, found=False, userFound=False, operationDone=False)
        try:
            returned = self.db.delete_many({"_id": ObjectId(poll_id)})
            return PollWrapper(None, None, found=False, userFound=False, operationDone=bool(returned.deleted_count))
        except:
            return PollWrapper(None, None, found=True, userFound=False, operationDone=False)
