#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Alexey Koshevoy

from params_container import Container
from requests import get, post
from bs4 import BeautifulSoup
import sys
import argparse
from html import unescape
import csv
import unittest
import os


class PageParser:
    def __init__(self, query, subcorpus='nkjp300', tag=False, write=False,
                 kwic=True, occurrences=10):
        """
        This function posts data in order to get cookies and then get the
        results
        :param query: actual query for the corpus
        :param subcorpus: subcorpus (if exists)
        :param tag: show tags
        """
        self.query = query
        self.tag = tag
        self.subcorpus = subcorpus
        self.page = None
        self.occurrences = occurrences
        self.write = write
        self.kwic = kwic

    def get_results(self):

        if self.tag is True:
            tag_variable = 'slt'
        else:
            tag_variable = 's'

        settings_params = {'show_in_match': tag_variable,
                           'show_in_context': tag_variable,
                           'left_context_width': '5',
                           'right_context_width': '5',
                           'wide_context_width': '50',
                           'results_per_page': self.occurrences,
                           'next': '/poliqarp/' + self.subcorpus + '/query/'}

        send_cookies = post(url='http://nkjp.pl/poliqarp/settings/',
                            data=settings_params)

        user_agent = {'Host': 'nkjp.pl',
                      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.'
                                    '10; rv:51.0) Gecko/20100101 Firefox/51.0',
                      'Accept': 'text/html,application/xhtml+xml,application/'
                                'xml;q=0.9,*/*;q=0.8',
                      'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                      'Accept-Encoding': 'gzip, deflate',
                      'Referer': 'http://nkjp.pl/poliqarp',
                      'Cookie': 'sessionid=' + str(send_cookies.cookies.get
                                                   ('sessionid')),
                      'Connection': 'keep-alive',
                      'Upgrade-Insecure-Requests': '1'}

        post(url='http://nkjp.pl/poliqarp/query/', headers=user_agent,
             data={'query': self.query, 'corpus': 'nkjp300'})

        results = get(url='http://nkjp.pl/poliqarp/nkjp300/query/',
                headers=user_agent)

        return results

    def parse_results(self):

        """
        :return: list of lists of lines
        """
        page = self.get_results()

        left_list = []
        right_list = []
        center_list = []
        soup = BeautifulSoup(page.text, 'lxml')

        for left in soup.select('.left'):
            left_list.append(left.text)
        for center in soup.select('span > a'):
            center_list.append(center.text)
        for right in soup.select('.right'):
            right_list.append(right.text)

        left_list = [s.strip('\n') for s in left_list]
        center_list = [s.strip('\n') for s in center_list]
        right_list = [s.strip('\n') for s in right_list][1::2]

        s = [[left_list[i], center_list[i], right_list[i]] for i in
             range(len(left_list))]

        if not s:
            print('pol_search: nothing found for "%s"' % (self.query))

        if not self.kwic:
            s = [[' '.join(x)] for x in s]

        if self.write:
            if self.kwic:
                cols = ['index', 'results']
            else:
                cols = ['index', 'left', 'center', 'right']
            self.write_results(self.query, s, cols)

        return s

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
                writer.writerow([i] + x)

if __name__ == '__main__':
    a = PageParser(query='tata')
    print(a.parse_results())
