#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Alexey Koshevoy

from requests import post
from requests import get
from bs4 import BeautifulSoup
import csv


class NothingFound(Exception):
    """This exception will rise, when nothing is found"""
    pass


class QueryArgs:

    def __init__(self, query: str, corpus: str='nkjp300', tag: bool=False,
                 n_results: int=10, kwic: bool=True, write: bool=False):
        self.query = query
        self.corpus = corpus
        self.tag = tag
        self.n_results = n_results
        self.kwic = kwic
        self.write = write


class HtmlPage:

    def __init__(self):

        if args.tag is True:
            tag_variable = 'slt'
        else:
            tag_variable = 's'

        self.data = {'show_in_match': tag_variable,
                     'show_in_context': tag_variable,
                     'left_context_width': '5',
                     'wide_context_width': '50',
                     'results_per_page': args.n_results,
                     'next': '/poliqarp/{}/query/'.format(args.corpus)}

    def create_user_agent(self):

        """Create User-Agent dictionary
        This method collects cookies from nkjp.pl and then insert the
        sessionid parameter into User-Agent for future requests
        @return: User-Agent dictionary
        """
        s = post(url='http://nkjp.pl/poliqarp/settings/', data=self.data)

        if s.status_code != 200:
            raise ConnectionError('There is something with connection. '
                                  'Please try again later.')

        user_agent = {'Host': 'nkjp.pl',
                      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.'
                                    '10; rv:51.0) Gecko/20100101 Firefox/51.0',
                      'Accept': 'text/html,application/xhtml+xml,application/'
                                'xml;q=0.9,*/*;q=0.8',
                      'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                      'Accept-Encoding': 'gzip, deflate',
                      'Referer': 'http://nkjp.pl/poliqarp',
                      'Cookie': 'sessionid={}'.format(s.cookies.
                                                      get('sessionid')),
                      'Connection': 'keep-alive',
                      'Upgrade-Insecure-Requests': '1'}

        return user_agent

    def post_and_get(self):

        """

        @return:
        """
        user_agent = self.create_user_agent()

        post(url='http://nkjp.pl/poliqarp/query/', headers=user_agent,
             data={'query': args.query, 'corpus': args.corpus})
        html_page = get(url='http://nkjp.pl/poliqarp/nkjp300/query/',
                        headers=user_agent)
        return html_page


class ResultTable(HtmlPage):

    def __init__(self):
        HtmlPage.__init__(self)
        self.soup = BeautifulSoup(self.post_and_get().text, 'lxml')

    def get_lr_parts(self):

        """Extract left and right parts from table
        This method extracts left and right parts from table, then cleans the
        results

        @return: list of lists, which contains all rows
        """
        left_list = []
        right_list = []

        for left in self.soup.select('.left'):
            left_list.append(left.text)
        for right in self.soup.select('.right'):
            right_list.append(right.text)

        if not right_list:
            raise NothingFound('pol_search: nothing found for "{}"'.
                               format(args.query))

        left_list = [s.strip('\n') for s in left_list]
        right_list = [s.strip('\n') for s in right_list]

        center_list = right_list[0::2]
        right_list = right_list[1::2]

        all_rows = [[left_list[i], center_list[i], right_list[i]]
                    for i in range(len(left_list))]

        return all_rows

    def deal_with_args(self):

        """Deal with user arguments
        This function transform list of all rows due to user preferences

        @return: user-wanted list of lists, which contains all rows
        """

        all_rows = self.get_lr_parts()

        if not args.kwic:
            all_rows = [[' '.join(x)] for x in all_rows]

        return all_rows


class CsvTable:

    def __init__(self):
        self.all_results = ResultTable().deal_with_args()

    @staticmethod
    def write_results(query, results, cols):

        not_allowed = '/\\?%*:|"<>'

        query = ''.join([x if x not in not_allowed else '_na_' for x in query])

        with open('pol_search_' + str(query) + '.csv', 'w',
                  encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow(cols)

            for i, x in enumerate(results):
                writer.writerow([i]+x)

    def write_to_csv(self):

        if args.kwic:
            cols = ['index','left','center','right']
        else:
            cols = ['index','results']

        self.write_results(args.query, self.all_results, cols)


if __name__ == '__main__':
    args = QueryArgs(query='Tata', write=True)

    if args.write:
        CsvTable().write_to_csv()
    else:
        ResultTable().get_lr_parts()
