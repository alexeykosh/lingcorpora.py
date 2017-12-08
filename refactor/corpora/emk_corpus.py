from requests import get
from bs4 import BeautifulSoup
import csv
from params_container import Container
import sys
import unittest
import argparse
from html import unescape
import os
   

class PageParser:
    def __init__(self,query,subcorpus):
        self.query = query
        self.subcorpus = subcorpus
        self.page = None
        self.occurrences = 0
        self.pagenum = 1

    def get_results(self):
        """
        create a query url and get results for one page
        """
        params = {
            "corpname": self.subcorpus,
            "iquery": self.query,
            "fromp": self.pagenum
        }
        r = get('http://maslinsky.spb.ru/emk/run.cgi/first',params)
        return unescape(r.text)


    def parse_page(self):
        """
        find results (and total number of results) in the page code
        """
        soup = BeautifulSoup(self.page, 'lxml')
        res = soup.find('table')
        res = res.find_all('tr')
        if self.pagenum == 1:
            self.occurrences = int(soup.select('strong[data-num]')[0].text)
        return res


    def parse_results(self,results):
        """
        find hit and its left and right contexts
        in the extracted row of table
        """
        parsed_results = []
        for i in range(len(results)):
            lc = ' '.join([x.text.strip()
                                for x in results[i].select('td.lc span.nott')])
            kw = results[i].select('td.kw span.nott')[0].text.strip()
            if kw != self.query:
                kw = query + ' (' + kw + ')'
            rc = ' '.join([x.text.strip()
                                for x in results[i].select('td.rc span.nott')])
            parsed_results.append([lc,kw,rc]) 
        return parsed_results

    def extract_results(self):
        self.page = self.get_results()
        rows = self.parse_page()
        parsed_results = self.parse_results(rows)
        return parsed_results
    

class Downloader(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.per_page = 20
        if self.subcorpus is None:
            self.subcorpus = 'cormani-brut-lat'
            
    def download_all(self):
        """
        get information and hits from first page and iterate until
        all hits are collected or maximum set by user is achieved
        """
        parser = PageParser(self.query,self.subcorpus)
        try:
            first = parser.extract_results()
        except:
            return []
        results = first
        final_total = min(self.numResults,parser.occurrences)
        pages_to_get = len(list(range(self.per_page+1,final_total+1,self.per_page)))
        for i in range(pages_to_get):
            parser.pagenum = i
            results += parser.extract_results()
        if len(results) > final_total:
            results = results[:final_total]
        return results

#rewrite
class TestMethods(unittest.TestCase):
    def test1(self):
        self.assertTrue(get_results(query='tuma',corpus='cormani-brut-lat',page=1))

    def test2(self):
        self.assertIs(list,type(main(query='ߛߐ߬ߘߐ߲߬',corpus='cormani-brut-nko')))
    
    def test3(self):
        r = main(query='ߛߐ߬ߘߐ߲߬',corpus='cormani-brut-nko',write=True,kwic=False)
        filelist = os.listdir()
        self.assertIn('emk_search_ߛߐ߬ߘߐ߲߬.csv',filelist)
        os.remove('emk_search_ߛߐ߬ߘߐ߲߬.csv')

    

if __name__ == '__main__':
    unittest.main()
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str)
    parser.add_argument('corpus', type=str)
    parser.add_argument('tag', type=bool)
    parser.add_argument('n_results', type=int)
    parser.add_argument('kwic', type=bool)
    parser.add_argument('write', type=bool)
    args = parser.parse_args(args)
    main(**vars(args))
