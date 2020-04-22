from typing import List


class Poll:
    def __init__(self, question: str, options: List[str], named: bool, unique: bool, creator_user_id: str):
        self.question = question
        self.options = options
        self.named = named
        self.unique = unique
        self.creator_user_id = creator_user_id
    def makeJson(self):
        #Todo: it
        pass

def getPollFromJson(json):
    #Todo: it
    pass