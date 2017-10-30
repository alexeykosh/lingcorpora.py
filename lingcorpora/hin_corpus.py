from requests import get
from bs4 import BeautifulSoup
import csv
import re
import os
import sys
import argparse
import unittest


def get_page(query, n_results, start):
    """
    create a query url and return a page with results
    """
    params = {'word': query,
              'limit': n_results,
              'start': start,
              'submit': 'Search'}
    s = get('http://www.cfilt.iitb.ac.in/~corpus/hindi/find.php', params=params)
    return s


def get_results(page):
    """
    parse the page and get results
    """
    num = re.compile('\d+')
    sentence_list = []
    center_list = []
    left_list = []
    right_list = []
    soup = BeautifulSoup(page.text, 'lxml')
    for sentence in soup.select('tr[bgcolor*="f"] td'):
        if not num.match(sentence.text):
            sentence_list.append(sentence.text)
    for center in soup.select('td font a[target]'):
        if not num.match(center.text):
            center_list.append(center.text)
    for i in range(len(sentence_list)):
        res = sentence_list[i].split(center_list[i])
        left_list.append(res[0])
        right_list.append(res[1])
    s = [[left_list[i].strip(), center_list[i].strip(), right_list[i].strip()] for i in range(len(left_list))]
    return s


def write_results(query, results, cols):
    """
    write csv
    """
    not_allowed = '/\\?%*:|"<>'
    query = ''.join([x if x not in not_allowed else '_na_' for x in query])
    with open('hin_search_' + str(query) + '.csv', 'w', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(cols)
        for i, x in enumerate(results, start=1):
            writer.writerow([i]+x)


def main(query, n_results, start, kwic=True, write=False):
    """
       main function

       Args:
           query: a query to search by
           n_results: desired number of results (10 by default)
           start: from which number to start searching (0 by default)
           kwic: whether to write into file in kwic format or not (True by default)
           write: whether to write into csv file or not (False by default)

       Return:
           list of row lists and csv file is written if specified

    """
    results = get_results(get_page(query, n_results, start))
    if not results:
        print('hin_search: nothing found for "{}"'.format(query))
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
        self.assertEqual('<Response [200]>', str(get_page(query='कुत्ते', n_results=50, start=0)))

    def test2(self):
        self.assertIs(list, type(get_results(get_page(query='कुत्ते', n_results=50, start=0))))

    def test3(self):
        results = main(query='कुत्ते', n_results=10, start=0, kwic=True, write=True)
        filelist = os.listdir('.')
        self.assertIn('hin_search_कुत्ते.csv', filelist)
        os.remove('hin_search_कुत्ते.csv')


if __name__ == '__main__':
    unittest.main()
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='hin_corpus.py')
    parser.add_argument('query', type=str)
    parser.add_argument('n_results', type=int, default=10)
    parser.add_argument('start', type=int, default=0)
    parser.add_argument('kwic', type=bool, default=True)
    parser.add_argument('write', type=bool, default=False)
    args = parser.parse_args(args)
    main(**vars(args))
