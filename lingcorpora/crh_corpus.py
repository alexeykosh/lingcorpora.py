from requests import get
from bs4 import BeautifulSoup
import csv
import re
import os
import sys
import argparse
import unittest


def get_page(query):
    """
    create a query url and return a page with results
    """
    params = {'query': query,
              'corpname': 'qirim'}
    s = get('http://korpus.juls.savba.sk:8080/manatee.ks/do_query', params=params)
    return s


def parse_page(link, left_list, center_list, right_list, n_results):
    """
    parse the page
    """
    s = get(link)
    soup = BeautifulSoup(s.text, 'lxml')
    for left in soup.select('td[class="lc"]'):
        if len(left_list) < n_results:
            left_list.append(left.text)
    for center in soup.select('td[class="kwic"]'):
        if len(center_list) < n_results:
            center_list.append(center.text)
    for right in soup.select('td[class="rc"]'):
        if len(right_list) < n_results:
            right_list.append(right.text)
    return left_list, center_list, right_list


def get_results(page, n_results):
    """
    get results and return them
    """
    soup = BeautifulSoup(page.text, 'lxml')
    left_list = []
    center_list = []
    right_list = []
    link = 'http://korpus.juls.savba.sk:8080/manatee.ks/{}'.format(soup.find('a', "navigation")['href'])
    param_start = re.compile('&start=\d+?&')
    for i in range(0, n_results-1, 10):
        link = param_start.sub('&start={}&'.format(i), link)
        left_list, center_list, right_list = parse_page(link, left_list, center_list, right_list, n_results)
    s = [[left_list[i].strip(), center_list[i].strip(), right_list[i].strip()] for i in range(len(left_list))]
    return s


def write_results(query, results, cols):
    """
    write csv
    """
    not_allowed = '/\\?%*:|"<>'
    query = ''.join([x if x not in not_allowed else '_na_' for x in query])
    with open('crh_search_' + str(query) + '.csv', 'w', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(cols)
        i = 1
        for x in results:
            writer.writerow([i]+x)
            i += 1


def main(query, n_results=10, kwic=True, write=False):
    """
       main function

       Args:
           query: a query to search by
           n_results: desired number of results (10 by default)
           kwic: whether to write into file in kwic format or not (True by default)
           write: whether to write into csv file or not (False by default)

       Return:
           list of row lists and csv file is written if specified

    """
    results = get_results(get_page(query),  n_results)
    if not results:
        print('crh_search: nothing found for "{}"'.format(query))
    if not kwic:
        results = [[' '.join(x)] for x in results]
    if write:
        if not kwic:
            cols = ['index', 'results']
        else:
            cols = ['index', 'left', 'center', 'right']
        write_results(query, results, cols)
    return results


class TestMethods(unittest.TestCase):

    def test1(self):
        self.assertEqual('<Response [200]>', str(get_page(query='къырым')))

    def test2(self):
        self.assertIs(list, type(get_results(get_page(query='къырым'),
                                             n_results=50)))

    def test3(self):
        results = main(query='къырым', n_results=30, kwic=True, write=True)
        filelist = os.listdir('.')
        self.assertIn('crh_search_къырым.csv', filelist)
        os.remove('crh_search_къырым.csv')

if __name__ == '__main__':
    unittest.main()
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='crh_corpus.py')
    parser.add_argument('query', type=str)
    parser.add_argument('n_results', type=int, default=10)
    parser.add_argument('kwic', type=bool, default=True)
    parser.add_argument('write', type=bool, default=False)
    args = parser.parse_args(args)
    main(**vars(args))
