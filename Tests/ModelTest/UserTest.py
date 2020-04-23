import unittest
from model.User import User, getUserFromJson


class UserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User('Tasos', 'mail@mail.mail', 'kodikos')
        self.unhashed = 'kodikos'
        self.json = {'name': 'Tasos', 'mail': 'mail@mail.mail', 'password': self.user.password,
                     'session_id': self.user.session_id}
        self.json_no_session_id = {'name': 'Tasos', 'mail': 'mail@mail.mail', 'password': self.user.password}

    def test_create_user(self):
        self.assertEqual(self.json.get("name"), self.user.name)
        self.assertEqual(self.json.get("mail"), self.user.mail)
        self.assertTrue(self.user.verify_password(self.unhashed))

    def test_makeJson(self):
        self.assertEqual(self.json, self.user.makeJson())

    def test_getUserFromJson(self):
        self.assertEqual(self.user, getUserFromJson(self.json))

        with self.assertRaises(Exception, msg="Fields name, mail and password are needed"):
            getUserFromJson({})

        no_id = getUserFromJson(self.json_no_session_id)
        self.assertEqual(self.json_no_session_id.get("name"), no_id.name)
        self.assertEqual(self.json_no_session_id.get("mail"), no_id.mail)
        self.assertTrue(self.json_no_session_id.get("password"), no_id.password)

    def test_verify_password(self):
        self.assertTrue(self.user.verify_password(self.unhashed))
        self.assertFalse(self.user.verify_password("lathos"))


if __name__ == '__main__':
    unittest.main()
