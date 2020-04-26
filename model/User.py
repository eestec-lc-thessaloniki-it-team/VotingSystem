import secrets
import hashlib, binascii, os


class User:
    def __init__(self, name, mail, password):
        self.name = name
        self.mail = mail
        self.password = self._hashPassword(password)
        self.createSessionId()

    def __eq__(self, other):
        if self.name == other.name and self.mail == other.mail and self.password == other.password \
                and self.session_id == other.session_id:
            return True
        return False

    def makeJson(self):
        json = {
            "name": self.name,
            "mail": self.mail,
            "password": self.password,
            "session_id": self.session_id
        }
        return json

    def _hashPassword(self, password) -> str:
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, provided_password) -> bool:
        """Verify a stored password against one provided by user"""
        salt = self.password[:64]
        stored_password = self.password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def createSessionId(self):
        self.session_id = secrets.token_urlsafe(16)


def getUserFromJson(json) -> User:
    # password expected to be already hashed
    if "name" in json and "mail" in json and "password" in json:
        user = User(json.get("name"), json.get("mail"), json.get("password"))
        user.password = json.get("password")
        if "session_id" in json: # new session_id generated if not given in json
            user.session_id = json.get("session_id")
        return user
    else:
        raise Exception("Fields name, mail and password are needed")
