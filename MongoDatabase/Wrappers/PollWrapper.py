from model.Poll import *


class PollWrapper:

    def __init__(self, object: Poll, pollId, found=False, userFound=False, operationDone=False):
        self.object = object
        self.pollId = pollId
        self.found = found
        self.userFound = userFound
        self.operationDone = operationDone

    def makeJson(self):
        json={
            "poll_id": self.pollId,
            "found": self.found,
            "userFound": self.userFound,
            "operationDone": self.operationDone,
            "object": self.object.makeJson()
        }
        del json['object']['creator_user_id'] #no need to give user id
        return json
