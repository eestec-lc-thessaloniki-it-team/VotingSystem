import unittest
from model.Vote import Vote


class VoteTest(unittest.TestCase):

    def test_create_vote(self):
        vote = Vote("1234", "1234", 2)
        print(vote.timestamp)
        self.assertEqual(vote.user_id, "1234")

if __name__ == '__main__':
    unittest.main()