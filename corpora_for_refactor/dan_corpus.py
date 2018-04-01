import requests
from bs4 import BeautifulSoup
from params_container import Container
import csv
import sys
import argparse
import re
import unittest
import os


class PageParser:
    def __init__(self,query):
        self.query = query
        self.pagenum = 1
        self.page = None
        self.occurrences = 0
        self.session = requests.Session()
        
    def get_first_page(self):
        params = {'query': self.query,
                  'search': 'Search',
                  'tag': 'lemma'}
        response = self.session.get('http://ordnet.dk/korpusdk_en/concordance/action', params=params)
        return response


    def get_page(self):
        params = {'page': self.pagenum}
        page = requests.get('http://ordnet.dk/korpusdk_en/concordance/result/navigate',
                            params=params, cookies=self.session.cookies)
        return page


    def get_results_page(self):
        res = []
        soup = BeautifulSoup(self.page.text, 'lxml')
        if self.pagenum == 1:
            occur = soup.select('.value')[0].string
            self.occurrences = int(occur[(occur.find('of') + 2):(occur.find('occur'))].strip())
            if self.occurrences > 49:
                self.occurrences -= 1
        punc = re.compile("[.-\[\]:\";,!?']")
        p = soup.select('.conc_table')[0]
        for sen in p.select('tr[onmouseover]'):
            loc_res = []
            left_part = ''
            right_part = ''
            for word in sen.select('.left-context-cell'):
                left_part = left_part + ' ' + word.select('a')[0].string
            for word in sen.select('.right-context-cell'):
                right_part = right_part + ' ' + word.select('a')[0].string
            center_part = sen.select('.conc_match')[0].a.string
            loc_res.append(left_part.strip())
            if punc.search(center_part[1:]):
                loc_res.append(center_part[0:punc.search(center_part[1:]).start()].strip())
                loc_res.append(center_part[punc.search(center_part[1:]).start():].strip() + right_part.strip())
            else:
                loc_res.append(center_part.strip())
                loc_res.append(right_part.strip())
            res.append(loc_res)
        return res


    def extract_results(self):
        if self.pagenum == 1:
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
        if min(parser.occurrences, self.numResults) > 49:
            num_page = final_total // 50 + 1
        else:
            num_page = 1
        for i in range(2, num_page + 1):
            parser.pagenum = i
            results += parser.extract_results()
        if len(results) > final_total:
            results = results[:final_total]
        parser.session.close()
        return results



#rewrite
class TestMethods(unittest.TestCase):
    def test1(self):
        self.assertEqual(('<Response [200]>'), str(get_first_page(query='pyjamas')))

    def test2(self):
        self.assertIs(list, type(get_results(first_page=get_first_page(query='pyjamas'),
                                             write=False, kwic=True, query='pyjamas', n_results=100)))

    def test3(self):
        main('danish', 'pyjamas', 'False', '100', 'False', 'True')
        filelist = os.listdir()
        self.assertIn('danish_search_pyjamas.csv', filelist)
        os.remove('danish_search_pyjamas.csv')


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
    main(**vars(args))
