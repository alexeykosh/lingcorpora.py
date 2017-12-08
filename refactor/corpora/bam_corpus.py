from params_container import Container
from requests import get
from bs4 import BeautifulSoup
import sys
import argparse
from html import unescape
import csv
import unittest
import os

class PageParser:
    def __init__(self,query,subcorpus,tag):
        self.query = query
        self.tag = tag
        self.subcorpus = subcorpus
        self.page = None
        self.occurrences = 0
        self.pagenum = 1
        
    def get_results(self):
        params = {
            "corpname": self.subcorpus,
            "iquery": self.query,
            "fromp": self.pagenum
        }
        """
        create a query url and get results for one page
        """
        r = get('http://maslinsky.spb.ru/bonito/run.cgi/first',params)
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
            lc = ' '.join([x.text.strip() for x in results[i].select('td.lc span.nott')])
            kws = results[i].select('td.kw div.token')
            final_kws = []
            for kw in kws:
                tag = kw.select('div.aline')
                tag = '; '.join([x.text.strip() for x in tag if x.text.strip()])
                if self.tag and tag and self.subcorpus == 'corbama-net-tonal':
                    text_kw = kw.select('span.nott')[0].text.strip() +' ('+tag+')'
                else:
                    text_kw = kw.select('span.nott')[0].text.strip()
                final_kws.append(text_kw)
            rc = ' '.join([x.text.strip() for x in results[i].select('td.rc span.nott')])
            parsed_results.append([lc,' '.join(final_kws),rc])
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
        if self.subcorpus == None:
            self.subcorpus = 'corbama-net-non-tonal'
    
    def download_all(self):
        """
        get information and hits from first page and iterate until
        all hits are collected or the maximum set by user is achieved
        """
        parser = PageParser(self.query,self.subcorpus,self.tag)
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


class TestMethods(unittest.TestCase):
    def test1(self):
        self.assertTrue(download_all(query='jamana',num_res=10,corpus='corbama-net-non-tonal',tags=False))

    def test2(self):
        r = main(query='kɔ́nɔ',corpus='corbama-net-tonal',tag=True,write=True)
        filelist = os.listdir()
        self.assertIn('bam_search_kɔ́nɔ.csv',filelist)
        os.remove('bam_search_kɔ́nɔ.csv')

        
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
