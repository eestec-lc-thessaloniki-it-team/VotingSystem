from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from model.Vote import Vote
from model.Vote import getVoteFromJson


class VotesDB:
    def __init__(self, client):
        self.client = client
        self.db = self.client.votesDB

    def createVote(self, user_id: str, poll_id: str, named: bool, chosen_option: int) -> VotesWrapper:
        """
        Creates a new Vote with user_id, poll_id and option selected
        :param user_id
        :param poll_id
        :param chosen_option
        :return: VotesWrapper
        """
        try:

            vote: Vote = Vote(user_id, poll_id, chosen_option)  # timestamp will be created automatically
            self.db.insert_one(vote.makeJson())
            return self.getAllVotes(poll_id, named)
        except:
            return VotesWrapper(None, {})

    def getAllVotes(self, poll_id: str, named: bool, after_timestamp=0) -> VotesWrapper:
        """
        Gets all the votes for this poll_id, divided into options.
        :param poll_id
        :param after_timestamp
        :return: VotesWrapper
        """
        try:

            if after_timestamp:
                voteList = [getVoteFromJson(voteJson) for voteJson in
                            self.db.find({"timestamp": {"$gt": after_timestamp}})
                            if getVoteFromJson(voteJson).poll_id == poll_id]
            else:
                voteList = [getVoteFromJson(voteJson) for voteJson in self.db.find()
                            if getVoteFromJson(voteJson).poll_id == poll_id]
            if not voteList:
                return VotesWrapper(0, {}, named=named, found=False, userFound=False, operationDone=False)
            latestTimestamp = 0
            for vote in voteList:
                if vote.timestamp > latestTimestamp:
                    latestTimestamp = vote.timestamp
            voteDict = {vote.chosen_option: list() for vote in voteList}
            for vote in voteList:
                voteDict[vote.chosen_option].append(vote.user_id)
            if not named:
                voteDict = {option: len(userlist) for option, userlist in voteDict.items()}
            # get the last timestamp
            return VotesWrapper(latestTimestamp, voteDict, named=named, found=True, userFound=True,
                                operationDone=True)
        except:
            return VotesWrapper(None, {})

    def deleteVote(self, poll_id):
        """
        Deletes a vote with poll_id
        :param poll_id
        :return: boolean
        """
        return bool(self.db.delete_many({"poll_id": poll_id}).deleted_count)
