from params_container import Container
from requests import get
from bs4 import BeautifulSoup
import csv
import re
import os
import sys
import argparse
import unittest


class PageParser:
    def __init__(self,query,numResults,start):
        self.query = query
        self.numResults = numResults
        self.page = None
        self.start = start


    def get_page(self):
        """
        create a query url and return a page with results
        """
        params = {'word': self.query,
                  'limit': self.numResults,
                  'start': self.start,
                  'submit': 'Search'}
        s = get('http://www.cfilt.iitb.ac.in/~corpus/hindi/find.php', params=params)
        return s


    def get_results(self):
        """
        parse the page and get results
        """
        num = re.compile('\d+')
        sentence_list = []
        center_list = []
        left_list = []
        right_list = []
        soup = BeautifulSoup(self.page.text, 'lxml')
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


    def extract_results(self):
        self.page = self.get_page()
        parsed_results = self.get_results()
        return parsed_results


class Downloader(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def download_all(self):
        """
        get information and hits from first page and iterate until
        all hits are collected or the maximum set by user is achieved
        """
        parser = PageParser(self.query,self.numResults,self.start)
        try:
            return parser.extract_results()
        except:
            return []
        
# rewrite
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
