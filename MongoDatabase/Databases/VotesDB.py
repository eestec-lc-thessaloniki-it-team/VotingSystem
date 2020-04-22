from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from model.User import User
from model.Vote import Vote


class VotesDB:
    def __init__(self, client):
        self.client = client
        self.db = self.client.votesDB

    def createVote(self, poll_id: str, user_id: str, chosen_option: int) -> VotesWrapper:
        vote: Vote = Vote(poll_id, user_id, chosen_option) #timestamp will be created automatically
        # Todo: persist to database
        return self.getAllVotes(poll_id)
        pass

    def getAllVotes(self, poll_id: str, after_timestamp="") -> VotesWrapper:
        """

        :param poll_id:
        :param after_timestamp:
        :return: All the votes for this poll_id, divided into options. If named is true then pass into the wrapper
        the user_id, else pass only the numbers . Make sure to set named in wrapper
        """
        if after_timestamp =="":
            #Todo: get them all
            pass
        else:
            #Todo: only the ones after the timestamp
            pass
