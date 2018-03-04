# -*- coding: utf-8 -*-
import sys
import urllib2
import json
import gzip
from datetime import datetime
from StringIO import StringIO
from utils import AnswersUtils


class StackExApiRequest(object):
    """
    Class with methods for accessing the StackExchange API and return results.
    """

    def __init__(self, site):
        """
        Init the object with which stack exchange api and which api version
        :type site: basestring
        """

        self.site = site
        self.version = '2.2'

    @staticmethod
    def do_api_request(url):
        """ Make the API request, get the response and deflate them if needed. Return the json data """

        req = urllib2.Request(url)
        req.add_header('Accept-encoding', 'gzip,deflate')

        opener = urllib2.build_opener()
        resp = opener.open(req)

        if resp.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(resp.read())
            resp = gzip.GzipFile(fileobj=buf)

        return json.loads(resp.read())

    def get_url_answers(self, page, from_date, to_date):
        """ Prepare and return the url for the answers api request """

        url = 'https://api.stackexchange.com/' + self.version + \
              '/answers?page=' + str(page) + '&fromdate=' + from_date + '&todate=' + to_date + '&site=' + self.site
        return url

    def get_url_comments_on_answers(self, page, ids, from_date, to_date):
        """ Prepare and return the url fpr the comments on answers api request """

        url = 'https://api.stackexchange.com/' + self.version + \
              '/answers/' + ids + '/comments?page=' + str(page) + '&fromdate=' + from_date + '&todate=' + \
              to_date + '&site=' + self.site

        return url

    @staticmethod
    def convert_to_unix_time(date_time):
        """ Converts date/time to unix time as needed for the API query fields """

        dt = datetime.strptime(date_time.replace("'", ""), "%Y-%m-%d %H:%M:%S")
        return (dt - datetime(1970, 1, 1)).total_seconds()

    def fetch_answers(self, from_date, to_date):
        """ Get answers from the site """

        from_date = str(int(self.convert_to_unix_time(from_date)))
        to_date = str(int(self.convert_to_unix_time(to_date)))

        page = 1
        answers_data = self.do_api_request(self.get_url_answers(page, from_date, to_date))
        answers = list(answers_data['items'])

        while answers_data['has_more']:
            page += 1
            answers_data = self.do_api_request(self.get_url_answers(page, from_date, to_date))
            answers.extend(answers_data['items'])

        return answers

    def fetch_comments_on_answers(self, ids, from_date, to_date):
        """ Get comments on answers """

        from_date = str(int(self.convert_to_unix_time(from_date)))
        to_date = str(int(self.convert_to_unix_time(to_date)))

        page = 1
        comments_data = self.do_api_request(self.get_url_comments_on_answers(page, ids, from_date, to_date))
        comments = list(comments_data['items'])

        while comments_data['has_more']:
            page += 1
            comments_data = self.do_api_request(self.get_url_comments_on_answers(page, ids, from_date, to_date))
            comments.extend(comments_data['items'])

        return comments


def main(arg_list):

    # command inputs
    from_dt = 2
    to_dt = 4

    # set the stack ex site
    which_site = "stackoverflow"
    stack_ex_query = StackExApiRequest(which_site)

    answers = stack_ex_query.fetch_answers(arg_list[from_dt], arg_list[to_dt])

    answers_utils = AnswersUtils(answers)
    number_of_accepted_answers = answers_utils.get_total_number_of_accepted_answers()

    avg_score_of_accepted_answers = answers_utils.get_avg_score_of_accepted_answers()

    avg_answer_count_per_question = answers_utils.get_avg_answer_count_per_question()

    sorted_answers_ids = answers_utils.get_top_ten_answers_ids()
    ids = ';'.join(map(str, sorted_answers_ids))

    comments = stack_ex_query.fetch_comments_on_answers(ids, arg_list[from_dt], arg_list[to_dt])
    comments_per_answer = answers_utils.get_comment_count_of_answers(comments,
                                                                     answers_utils.initialize_comments_per_ids(
                                                                                            sorted_answers_ids))

    # Collect and return the output in json
    data = dict()
    data['total_accepted_answers'] = number_of_accepted_answers
    data['accepted_answers_average_score'] = avg_score_of_accepted_answers
    data['average_answers_per_question'] = avg_answer_count_per_question
    data['top_ten_answers_comment_count'] = comments_per_answer

    # dump the result
    print json.dumps(data, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: stackstats --since '2018-01-01 10:00:00' --until '2018-01-01 11:30:00' [--output-format json]"
        exit()
    main(sys.argv)
