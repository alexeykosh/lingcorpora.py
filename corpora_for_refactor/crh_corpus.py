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
    def __init__(self,query):
        self.query = query
        self.page = None
        self.pagenum = 0
        
    def get_page(self):
        """
        create a query url and return a page with results
        """
        params = {'query': self.query,
                  'corpname': 'qirim',
                  'start':self.pagenum}
        s = get('http://korpus.juls.savba.sk:8080/manatee.ks/do_query', params=params)
        return s.text


    def parse_page(self):
        """
        parse the page
        """
        left_list = []
        center_list = []
        right_list = []
        soup = BeautifulSoup(self.page, 'lxml')
        for left in soup.select('td[class="lc"]'):
            left_list.append(left.text)
        for center in soup.select('td[class="kwic"]'):
            center_list.append(center.text)
        for right in soup.select('td[class="rc"]'):
            right_list.append(right.text)
        res = [[l.strip(),c.strip(),r.strip()] for l,c,r in zip(left_list, center_list, right_list)]
        return res

    def extract_results(self):
        self.page = self.get_page()
        parsed_results = self.parse_page()
        return parsed_results

    
class Downloader(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def download_all(self):
        """
        get information and hits from first page and iterate until
        all hits are collected or the maximum set by user is achieved
        """
        s = []
        parser = PageParser(self.query)
        for i in range(0, self.numResults-1, 10):
            try:
                parser.pagenum = i
                s += parser.extract_results()
            except:
                return []
        if len(s) > self.numResults:
            s = s[:self.numResults]
        return s
        

# rewrite
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
