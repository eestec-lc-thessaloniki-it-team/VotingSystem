from model.User import *


class UserWrapper:

    def __init__(self, object: User, found=False, userFound=False, operationDone=False):
        self.object = object
        self.found = found
        self.userFound = userFound
        self.operationDone = operationDone

    def makeJson(self):
        json = {
            "found": self.found,
            "userFound": self.userFound,
            "operationDone": self.operationDone,
            "object": self.object.makeJson()
        }
        del json['object']['password']
        return json
