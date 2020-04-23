from datetime import datetime


class Vote:
    def __init__(self, user_id: str, poll_id: str, chosen_option: int):
        self.user_id = user_id
        self.poll_id = poll_id
        self.chosen_option = chosen_option
        self.timestamp = datetime.now()

    def __eq__(self, other):
        return(
            self.user_id == other.user_id and self.poll_id == other.poll_id and
            self.chosen_option == other.chosen_option and self.timestamp == other.timestamp
        )


    def makeJson(self):
        dict = {
            "user_id": self.user_id,
            "poll_id": self.poll_id,
            "chosen_option": self.chosen_option,
            "timestamp": self.timestamp
        }
        return dict

def getVoteFromJson(json) -> Vote:
    if "user_id" in json and "poll_id" in json and "chosen_option" in json and "timestamp" in json:
        new_vote = Vote(json.get("user_id"), json.get("poll_id"), json.get("chosen_option"))
        new_vote.timestamp = json.get("timestamp")
        return new_vote
    else:
        raise Exception("Fields name, mail and password are needed")


