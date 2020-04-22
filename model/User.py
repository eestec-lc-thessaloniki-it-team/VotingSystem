import secrets
import hashlib, binascii, os


class User:
    def __init__(self, name, mail, password):
        self.name = name
        self.mail = mail
        self.password = self._hashPassword(password)
        self.createSessionId()

    def makeJson(self):
        # TODO:
        pass
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

def getUserFromJson(json):
    #Todo: it
    pass