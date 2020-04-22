import unittest
from model.User import User, getUserFromJson


class UserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User('Tasos', 'mail@mail.mail', 'kodikos')
        self.json = {'name': 'Tasos', 'mail': 'mail@mail.mail', 'password': self.user.password,
                     'session_id': self.user.session_id}

    def test_create_user(self):
        self.assertEqual(self.json.get("name"), self.user.name)
        self.assertEqual(self.json.get("mail"), self.user.mail)
        self.assertTrue(self.user.verify_password("kodikos"))

    def test_makeJson(self):
        self.assertEqual(self.json, self.user.makeJson())

    def test_getUserFromJson(self):
        self.assertEqual(self.user, getUserFromJson(self.json))


if __name__ == '__main__':
    unittest.main()
