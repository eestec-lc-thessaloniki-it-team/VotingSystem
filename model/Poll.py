from typing import List, Optional


class Poll:
    def __init__(self, question: str, options: List[str], named: bool, unique: bool, creator_user_id: str):
        self.question = question
        self.options = options
        self.named = named
        self.unique = unique
        self.creator_user_id = creator_user_id

    def __eq__(self, other):
        return (
                self.question == other.question and self.options == other.options and self.named == other.named and
                self.unique == other.unique and self.creator_user_id == other.creator_user_id
        )

    def makeJson(self):
        dict = {
            "question": self.question,
            "options": self.options,
            "named": self.named,
            "unique": self.unique,
            "creator_user_id": self.creator_user_id
        }
        return dict


def getPollFromJson(json) -> Poll:
    if "question" in json and "options" in json and "named" in json and "unique" in json and "creator_user_id" in json:
        new_poll = Poll(json.get("question"), json.get("options"), json.get("named"), json.get("unique"),
                        json.get("creator_user_id"))
        return new_poll
    else:
        raise Exception("Fields name, mail and password are needed")
