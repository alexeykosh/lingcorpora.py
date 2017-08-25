from requests import post
from bs4 import BeautifulSoup
import csv
import sys
import argparse
import unittest
import os

def get_page(query, corpus, n_results):
    params = {'corpus': corpus,
              'date-end':'1999',
              'date-start':'1900',
              'format':'kwic',
              'genre': 'Belletristik',
              'genre': 'Wissenschaft',
              'genre': 'Gebrauchsliteratur',
              'genre': 'Zeitung',
              'limit': n_results,
              'q': query,
              'sort':	'date_asc'}
    s = post('https://www.dwds.de/r', params=params)
    return s


def get_results(page, write, kwic, query, n_results):
    left_list = []
    right_list = []
    center_list = []
    soup = BeautifulSoup(page.text, 'lxml')
    for left in soup.select('.ddc-kwic-ls'):
        left_list.append(left.text)
    for center in soup.select('.ddc-kwic-kw.ddc-hl'):
        center_list.append(center.text)
    for right in soup.select('.ddc-kwic-rs'):
        right_list.append(right.text)
    s = [[left_list[i].strip(),center_list[i].strip(),right_list[i].strip()]
               for i in range(len(left_list))]
    if not s:
        print ('deu_search: nothing found for "%s"' % (query))    
    if not kwic:
        s = [[' '.join(x)] for x in s]
    if write:
        if not kwic:
            cols = ['index','results']
        else:
            cols = ['index','left','center','right']
        write_results(query,s,cols)
    return s


def write_results(query,results,cols):
    """
    write csv
    """
    not_allowed = '/\\?%*:|"<>'
    query = ''.join([x if x not in not_allowed else '_na_' for x in query])
    with open('deu_search_' + str(query) + '.csv','w',encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(cols)
        for i,x in enumerate(results):
            writer.writerow([i]+x)


class TestMethods(unittest.TestCase):
    def test1(self):
        self.assertEqual(('<Response [200]>'), str(get_page(query='bezug', n_results='100', corpus='kern')))

    def test2(self):
        self.assertIs(list, type(get_results(page=get_page(query='bezug',corpus='kern',n_results='100'),
                                             write=False, kwic=True,query='bezug', n_results='100')))

    def test3(self):
        r = main('Mutter',kwic=False,write=True)
        filelist = os.listdir()
        self.assertIn('deu_search_Mutter.csv',filelist)
        os.remove('deu_search_Mutter.csv')


def main(query, corpus='kern', n_results=10, kwic=True, write=False):
    page = get_page(query, corpus, n_results)
    results = get_results(page, write, kwic, query, n_results)
    return results


if __name__ == '__main__':
    unittest.main()
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('n_results', type=int)
    parser.add_argument('kwic', type=bool)
    parser.add_argument('write', type=bool)
    args = parser.parse_args(args)
    main(**vars(args))
