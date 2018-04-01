from params_container import Container
from requests import post
from bs4 import BeautifulSoup
import csv
import sys
import argparse
import unittest
import os


class PageParser:
    def __init__(self,query,subcorpus,numResults):
        self.query = query
        self.page = None
        self.subcorpus = subcorpus
        self.numResults = numResults
        
    def get_page(self):
        params = {'corpus': self.subcorpus,
                  'date-end':'1999',
                  'date-start':'1900',
                  'format':'kwic',
                  'genre': 'Belletristik',
                  'genre': 'Wissenschaft',
                  'genre': 'Gebrauchsliteratur',
                  'genre': 'Zeitung',
                  'limit': self.numResults,
                  'q': self.query,
                  'sort': 'date_asc'}
        s = post('https://www.dwds.de/r', params=params)
        return s

    def get_results(self):
        left_list = []
        right_list = []
        center_list = []
        soup = BeautifulSoup(self.page.text, 'lxml')
        for left in soup.select('.ddc-kwic-ls'):
            left_list.append(left.text)
        for center in soup.select('.ddc-kwic-kw.ddc-hl'):
            center_list.append(center.text)
        for right in soup.select('.ddc-kwic-rs'):
            right_list.append(right.text)
        s = [[left_list[i].strip(),center_list[i].strip(),right_list[i].strip()]
                   for i in range(len(left_list))]
        return s

    def extract_results(self):
        self.page = self.get_page()
        parsed_results = self.get_results()
        return parsed_results


class Downloader(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.subcorpus is None:
            self.subcorpus = 'kern'

    def download_all(self):
        parser = PageParser(self.query,self.subcorpus,self.numResults)
        try:
            return parser.extract_results()
        except:
            return []
        
    
# rewrite
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




if __name__ == '__main__':
    unittest.main()
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('tag', type=bool)
    parser.add_argument('n_results', type=int)
    parser.add_argument('kwic', type=bool)
    parser.add_argument('write', type=bool)
    args = parser.parse_args(args)
    main(**vars(args))
