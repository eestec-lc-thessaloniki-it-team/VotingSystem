import unittest
from model.Poll import *


class PollTesting(unittest.TestCase):

    def setUp(self):

        self.poll = Poll("Do you like our voting system?", ["Yes", "Of course", "absolutely"], True, True, "001")
        self.json = {'question': 'Do you like our voting system?', 'options': ['Yes', 'Of course', 'absolutely'],
                     'named': True, 'unique': True, 'creator_user_id': '001'}

    def test_create_poll(self):
        self.assertEqual(self.poll.question, "Do you like our voting system?")
        self.assertEqual(self.poll.options, ["Yes", "Of course", "absolutely"])
        self.assertEqual(self.poll.named, True)
        self.assertEqual(self.poll.unique, True)
        self.assertEqual(self.poll.creator_user_id, "001")

    def test_makeJson(self):
        self.assertDictEqual(self.poll.makeJson(), self.json)

    def test_getPollFromJson(self):
        self.assertEqual(getPollFromJson(self.json), self.poll)



if __name__ == '__main__':
    unittest.main()