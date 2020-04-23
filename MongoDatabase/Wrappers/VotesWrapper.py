from model.Vote import *


class VotesWrapper:

    def __init__(self, lastTimestamp, votes, named=False, found=False, userFound=False, operationDone=False):
        self.lastTimestamp = lastTimestamp
        self.votes = votes
        self.named = named
        self.found = found
        self.userFound = userFound
        self.operationDone = operationDone
