import unittest

import requests


class FLaskTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.basic_url = "http://127.0.0.1:5000/"

    def testResultsNamed(self):
        response = requests.post(self.basic_url + "login",
                                 json={"password": "1234", "mail": "mymail@mail.mail"})
        self.session_id = response.json().get("wrapper").get("object").get("session_id")
        response = requests.post(self.basic_url + "create-poll", json={
            "question": "hi", "options": ["1", "2"], "named": "true", "unique": "true", "session_id": self.session_id
        })
        self.poll_id = response.json().get("id")

        response = requests.post(self.basic_url+"vote",json={
            "id":self.poll_id,"session_id":self.session_id,"chosen_option":0
        })

        response2=requests.post(self.basic_url+"results?id="+self.poll_id, json={
            "last_timestamp":0,"session_id":self.session_id
        })
        print(response2)
        print("hi")
