from datetime import datetime


class Vote:
    def __init__(self, user_id: str, poll_id: str, chosen_option: int):
        self.user_id = user_id
        self.poll_id = poll_id
        self.chosen_option = chosen_option
        self.timestamp = datetime.now()
    def makeJson(self):
        #Todo: it
        pass

def getVoteFromJson(json):
    #Todo: it
    pass
