from model.Poll import *

class PollWrapper:

    def __init__(self, object: Poll, pollId, found = False, userFound = False, operationDone = False):
        self.object = object
        self.pollId = pollId
        self.found = found
        self.userFound = userFound
        self.operationDone = operationDone