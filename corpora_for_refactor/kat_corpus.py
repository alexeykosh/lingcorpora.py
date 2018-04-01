from params_container import Container
import requests
from bs4 import BeautifulSoup
import csv
import sys
import argparse
import unittest
import os


class PageParser:
    def __init__(self,query):
        self.query = query
        self.pagenum = 0
        self.page = None
        self.occurrences = 0
        self.session = requests.Session()
        
    def get_first_page(self):
        data = {'exact_word': self.query,
                'op': 'Search',
                'form_build_id': 'form-hMOF3mG0n7lwL6LmHrPi9vZCcaLbsZmCAco4z8vALT4',
                'form_id': 'sw_exact_word_search_form'}
        params = {'q': 'search-words'}
        response = self.session.post('http://corpora.iliauni.edu.ge/', params=params, data=data)
        return response


    def get_page(self):
        params = {'page': str(self.pagenum),
                  'q':	'search-words'}
        page = requests.get('http://corpora.iliauni.edu.ge/', params=params, cookies=self.session.cookies)
        return page


    def get_results_page(self):
        res = []
        soup = BeautifulSoup(self.page.text, 'lxml')
        if self.pagenum == 0:
            occur = soup.select('.mtavruli')[0].string
            self.occurrences = int(occur.split(' ')[2])
        table = soup.select('.result_table')[0]
        for sen in table.select('tr'):
            left_part = ''
            right_part = ''
            for word in sen.select('.left_side'):
                if word.string:
                    left_part = left_part + ' ' + word.string
            for word in sen.select('.right_side'):
                if word.string:
                    right_part = right_part + ' ' + word.string
            res.append([left_part.strip(),sen.select('.found_word')[0].string.strip(),right_part.strip()])
        return res


    def extract_results(self):
        if self.pagenum == 0:
            self.page = self.get_first_page()
        else:
            self.page = self.get_page()
        parsed_results = self.get_results_page()
        return parsed_results


class Downloader(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def download_all(self):
        parser = PageParser(self.query)
        try:
            first = parser.extract_results()
        except:
            return []
        results = first
        final_total = min(self.numResults,parser.occurrences)
        num_page = (final_total + 9) // 10
        for i in range(1, num_page):
            parser.pagenum = i
            results += parser.extract_results()
        if len(results) > final_total:
            results = results[:final_total]
        parser.session.close()
        return results




#rewrite
class TestMethods(unittest.TestCase):
    def test1(self):
        self.assertEqual(('<Response [200]>'), str(get_first_page(query='დედა', corpus='vah', n_results=100)))

    def test2(self):
        self.assertIs(list, type(get_results(first_page=get_first_page(query='დედა', corpus='vah', n_results=100),
                                             write=False, kwic=True, query='დედა', n_results=100)))

    def test3(self):
        main('დედა', 'vah', 'False', '100', 'False', 'True')
        filelist = os.listdir()
        self.assertIn('vah_search_დედა.csv', filelist)
        os.remove('vah_search_დედა.csv')


if __name__ == '__main__':
    unittest.main()
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str)
    parser.add_argument('corpus', type=str)
    parser.add_argument('tag', type=str)
    parser.add_argument('n_results', type=str)
    parser.add_argument('kwic', type=str)
    parser.add_argument('write', type=str)
    args = parser.parse_args(args)
    print(args)
    main(**vars(args))
