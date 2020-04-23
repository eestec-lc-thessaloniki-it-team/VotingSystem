from model.User import *


class UserWrapper:

    def __init__(self, object: User, found=False, userFound=False, operationDone=False):
        self.object = object
        self.found = found
        self.userFound = userFound
        self.operationDone = operationDone
