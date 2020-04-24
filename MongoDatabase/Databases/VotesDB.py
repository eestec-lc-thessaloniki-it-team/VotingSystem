from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from model.Vote import Vote
from model.Vote import getVoteFromJson

class VotesDB:
    def __init__(self, client):
        self.client = client
        self.db = self.client.votesDB

    def createVote(self, poll_id: str, user_id: str, chosen_option: int) -> VotesWrapper:
        try:
            vote: Vote = Vote(poll_id, user_id, chosen_option)  # timestamp will be created automatically
            self.db.insert_one(vote.makeJson())
            return self.getAllVotes(poll_id)
        except:
            return VotesWrapper(None, {})

    def getAllVotes(self, poll_id: str, named: bool, after_timestamp=0) -> VotesWrapper:
        """

        :param poll_id:
        :param after_timestamp:
        :return: All the votes for this poll_id, divided into options. If named is true then pass into the wrapper
        the user_id, else pass only the numbers. Make sure to set named in wrapper
        """
        try:

            if after_timestamp:
                voteList = [getVoteFromJson(voteJson) for voteJson in
                            self.db.find({"timestamp": {"$gt": after_timestamp}})
                            if getVoteFromJson(voteJson).poll_id == poll_id]
            else:
                voteList = [getVoteFromJson(voteJson) for voteJson in self.db.find()
                            if getVoteFromJson(voteJson).poll_id == poll_id]

            voteDict = {vote.chosen_option: list() for vote in voteList}
            for vote in voteList:
                voteDict[vote.chosen_option].append(vote.user_id)
            if not named:
                voteDict = {option: len(userlist) for option, userlist in voteDict.items()}
            return VotesWrapper(after_timestamp, voteDict, named=named, found=True, userFound=True,
                                operationDone=True)  # TODO: named? you get it from poll_id -> pollDB
        except:
            return VotesWrapper(None, {})

    def deleteVote(self, poll_id):
        return bool(self.db.delete_many({"poll_id":poll_id}).deleted_count)
