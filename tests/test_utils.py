import unittest
import sys
sys.path.append("../stackexapi")
from utils import AnswersUtils
# from stackexapi.utils import AnswersUtils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.utils = AnswersUtils(self.init_answers())

    @staticmethod
    def init_answers():
        js = []

        data1 = dict()
        data1["question_id"] = 48029650
        data1["is_accepted"] = True
        data1["score"] = 0

        js.append(data1)
        data2 = dict()
        data2["question_id"] = 48022650
        data2["is_accepted"] = False
        data2["score"] = 3
        js.append(data2)

        return js

    def test_get_accepted_answers(self):
        self.assertEqual(len(self.utils.get_accepted_answers()), 1)

    def test_get_score_of_answers(self):
        self.assertEqual(self.utils.get_score_of_answers(self.init_answers()), 3)

    def test_get_total_number_of_accepted_answers(self):
        self.assertEqual(self.utils.get_total_number_of_accepted_answers(), 1)

    def test_get_avg_score_of_accepted_answers(self):
        self.assertEqual(self.utils.get_avg_score_of_accepted_answers(), 0.0)

    def test_get_avg_answer_count_per_question(self):
        self.assertEqual(self.utils.get_avg_answer_count_per_question(), 1.0)


if __name__ == '__main__':
    unittest.main()