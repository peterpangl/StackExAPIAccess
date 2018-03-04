from __future__ import division


class AnswersUtils(object):

    def __init__(self, answers):
        """ Assign the answers from the API Request to the object"""

        self.all_answers = answers

    def get_accepted_answers(self):
        """ Returns the accepted answers from a list of answers"""

        accepted_answers = []

        for x in self.all_answers:
            if x['is_accepted']:
                accepted_answers.append(x)

        return accepted_answers

    @staticmethod
    def get_score_of_answers(answers):
        """ Counts the score of the given answers """

        score = 0
        for x in answers:
            score += x['score']

        return score

    def get_total_number_of_accepted_answers(self):
        """ Return the total number of accepted answers """

        return len(self.get_accepted_answers())

    def get_avg_score_of_accepted_answers(self):
        """ Return the average score of the accepted answers"""

        accepted_answers = self.get_accepted_answers()
        if accepted_answers < 1:
            return 0

        score = self.get_score_of_answers(accepted_answers)

        return round((score / len(accepted_answers)), 1)

    def get_avg_answer_count_per_question(self):
        """ Return the average count per question """

        answer_count_per_question = set()
        for x in self.all_answers:
            answer_count_per_question.add(x['question_id'])

        return round((len(self.all_answers) / len(answer_count_per_question)), 1)

    def get_top_ten_answers_ids(self):
        """ Find the ids of the ten answers with the highest score """

        sorted_list = sorted(self.all_answers, key=lambda x: x['score'], reverse=True)
        return [x['answer_id'] for x in sorted_list[:10]]

    @staticmethod
    def get_comment_count_of_answers(comments, comments_per_id):
        """ Return the comment count for each answer of an answer set """

        for x in comments:
            if x['post_id'] in comments_per_id:
                comments_per_id[x['post_id']] += 1

        return comments_per_id

    @staticmethod
    def initialize_comments_per_ids(answers_ids):
        """ Init comments in order to be included also the 0 ones """

        return {x: 0 for x in answers_ids}
