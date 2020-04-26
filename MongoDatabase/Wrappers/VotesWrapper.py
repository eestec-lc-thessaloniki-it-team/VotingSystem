class VotesWrapper:

    def __init__(self, lastTimestamp, votes, named=False, found=False, userFound=False, operationDone=False):
        self.lastTimestamp = lastTimestamp
        self.votes = votes
        self.named = named
        self.found = found
        self.userFound = userFound
        self.operationDone = operationDone

    def makeJson(self):
        return {
            "lastTimestamp": self.lastTimestamp,
            "votes": self.votes,
            "named": self.named,
            "found": self.found,
            "userFound": self.userFound,
            "operationDone": self.operationDone
        }
