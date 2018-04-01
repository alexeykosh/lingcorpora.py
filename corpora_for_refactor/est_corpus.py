from params_container import Container
from requests import get
from bs4 import BeautifulSoup
import re
import csv
import sys
import argparse
import unittest
import os

'''
Available subcorpora:
              'subcorp': 'Maaleht',
              'subcorp': 'postimees_kokku',
              'subcorp': 'valga',
              'subcorp': 'le',
              'subcorp': 'luup',
              'subcorp': 'Kroonika',
              'subcorp': '1980_aja',
              'subcorp': '1970_aja',
              'subcorp': '1960_aja',
              'subcorp': '1950_aja',
              'subcorp': '1930_aja',
              'subcorp': '1910_aja',
              'subcorp': '1900_aja',
              'subcorp': '1890_aja',
              'subcorp': 'epl_1995',
              'subcorp': 'epl_1996',
              'subcorp': 'epl_1997',
              'subcorp': 'epl_1998',
              'subcorp': 'epl_1999',
              'subcorp': 'epl_2000',
              'subcorp': 'epl_2001',
              'subcorp': 'epl_2002',
              'subcorp': 'epl_2004',
              'subcorp': 'epl_2005',
              'subcorp': 'epl_2006',
              'subcorp': 'epl_2007',
              'subcorp': 'sloleht_1997',
              'subcorp': 'sloleht_1998',
              'subcorp': 'sloleht_1999',
              'subcorp': 'sloleht_2000',
              'subcorp': 'sloleht_2001',
              'subcorp': 'sloleht_2002',
              'subcorp': 'sloleht_2003',
              'subcorp': 'sloleht_2004',
              'subcorp': 'sloleht_2006',
              'subcorp': 'sloleht_2007',
              'subcorp': '1990_ilu_26_08_04',
              'subcorp': 'segailu_5_10_2008',
              'subcorp': '1980_ilu',
              'subcorp': '1970_ilu',
              'subcorp': '1960_ilu',
              'subcorp': '1950_ilu',
              'subcorp': '1930_ilu',
              'subcorp': '1910_ilu',
              'subcorp': '1900_ilu',
              'subcorp': '1890_ilu',
              'subcorp': '1980_tea',
              'subcorp': 'horisont',
              'subcorp': 'arvutitehnika',
              'subcorp': 'doktor',
              'subcorp': 'Eesti_Arst_2002',
              'subcorp': 'Eesti_Arst_2003',
              'subcorp': 'Eesti_Arst_2004',
              'subcorp': 'agraar',
              'subcorp': 'jututoad',
              'subcorp': 'uudisgrupid',
              'subcorp': 'foorumid',
              'subcorp': 'kommentaarid',
              'subcorp': 'riigikogu',
              'subcorp': '1980_muu',
              'subcorp': 'teadusartiklid',
              'subcorp': 'akp',
'''

class PageParser:
    def __init__(self,query,subcorpus,numResults):
        self.query = query
        self.subcorpus = subcorpus
        self.page = None
        self.occurrences = 0
        self.numResults = numResults
        self.pagenum = 1

    def get_page(self):
        params = {'otsisona': self.query,
                  'subcorp': self.subcorpus,
                  'kontekst': '0',
                  'lause_arv':	'0'}
        s = get('http://www.cl.ut.ee/korpused/kasutajaliides/konk.cgi.et', params=params)
        return s


    def find_right_part(self, elem, right_part):
        right_part = right_part + elem.string + elem.next_sibling
        if elem.next_sibling.next_sibling.name != 'br':
            right_part = self.find_right_part(elem.next_sibling.next_sibling, right_part)
        return right_part


    def find_left_part(self, elem, left_part):
        left_part = elem.previous_sibling + elem.string + left_part
        if elem.previous_sibling.previous_sibling.name != 'hr':
            left_part = self.find_left_part(elem.previous_sibling.previous_sibling, left_part)
        return left_part


    def get_results(self):
        #corpus = []
        s = []
        p = re.compile('[ .-:;,!?]')
        soup = BeautifulSoup(self.page.text, 'lxml')
        strong = soup.select('strong')
        if strong:
            for elem in strong:
                right_part = elem.next_sibling
                left_part = elem.previous_sibling
                center_part = elem.string
                if elem.next_sibling.next_sibling.name != 'br':
                    right_part = self.find_right_part(elem.next_sibling.next_sibling, right_part)
                if elem.previous_sibling.previous_sibling.name != 'hr':
                    left_part = self.find_left_part(elem.previous_sibling.previous_sibling, left_part)
                #corpus.append(left_part.split('    ', maxsplit=1)[0])
                s.append([left_part.split('    ', maxsplit=1)[1].strip(),
                          center_part + right_part[0:p.search(right_part).start()].strip(),
                          right_part[p.search(right_part).start():].strip()])
                if len(s) == self.numResults:
                    break
            return s


    def extract_results(self):
        self.page = self.get_page()
        parsed_results = self.get_results()
        return parsed_results


class Downloader(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.per_page = 20
        if self.subcorpus is None:
            self.subcorpus = '1990_ajalehed_26_08_04'
    
    def download_all(self):
        parser = PageParser(self.query,self.subcorpus,self.numResults)
        try:
            results = parser.extract_results()
        except:
            return []
        return results


#rewrite
class TestMethods(unittest.TestCase):
    def test1(self):
        self.assertEqual(('<Response [200]>'), str(get_page(query='keele')))

    def test2(self):
        self.assertIs(list, type(get_results(page=get_page(query='keele'),
                                             write=False, kwic=True, query='keele', n_results=100)))

    def test3(self):
        main('eesti', 'keele', 'False', '100', 'False', 'True')
        filelist = os.listdir()
        self.assertIn('eesti_search_keele.csv', filelist)
        os.remove('eesti_search_keele.csv')


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
