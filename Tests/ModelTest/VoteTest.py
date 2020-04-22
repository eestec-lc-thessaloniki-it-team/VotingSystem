import unittest
from model.Vote import*


class VoteTest(unittest.TestCase):

    def setUp(self):
        self.vote = Vote("1234", "5678", 2)
        self.json = { 'user_id': '1234', 'poll_id': '5678', 'chosen_option': 2, 'timestamp': self.vote.timestamp}



    def test_create_vote(self):
        self.assertEqual(self.vote.user_id, "1234")
        self.assertEqual(self.vote.poll_id, "5678")
        self.assertEqual(self.vote.chosen_option, 2)
        print(self.vote.timestamp)

    def test_makeJson(self):
        self.assertDictEqual(self.vote.makeJson(), self.json)

    def test_getVoteFromJson(self):
        self.assertEqual(getVoteFromJson(self.json), self.vote)


if __name__ == '__main__':
    unittest.main()