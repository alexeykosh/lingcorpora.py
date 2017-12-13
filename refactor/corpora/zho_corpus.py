from params_container import Container
from requests import get
from bs4 import BeautifulSoup
import sys
import argparse
from html import unescape
import csv
import unittest


class PageParser:
    def __init__(self,query,n,subcorpus,mode,nLeft,nRight):
        self.query = query
        self.numResults = n
        self.subcorpus = subcorpus
        self.mode = mode
        self.nLeft = nLeft
        self.nRight = nRight
        self.page = None
        self.occurrences = 0
        self.pagenum = 1
        
    def get_results(self):
        """
        create a query url and get results for one page
        """
        params = {'q': self.query,
                  'start': self.pagenum,
                  'num': self.numResults,
                  'index':'FullIndex',
                  'outputFormat':'HTML',
                  'encoding':'UTF-8',
                  'maxLeftLength':self.nLeft,
                  'maxRightLength':self.nRight,
                  'orderStyle':'score',
                  'dir':self.subcorpus,
                  'scopestr':'' # text selection: TO DO?
                  }
        if self.mode == 'simple':
            r = get('http://ccl.pku.edu.cn:8080/ccl_corpus/search',params)
        if self.mode == 'pattern':
            r = get('http://ccl.pku.edu.cn:8080/ccl_corpus/pattern',params)
        return unescape(r.text)


    def parse_page(self):
        """
        find results (and total number of results) in the page code
        """
        soup = BeautifulSoup(self.page, 'lxml')
        res = soup.find('table',align='center')
        if res:
            res = res.find_all('tr')
        else:
            return []
        if self.pagenum == 0:
            self.occurrences = int(soup.find('td',class_='totalright').find('b').text)
        return res

        
    def parse_results(self,results):
        """
        find hit and its left and right contexts
        in the extracted row of table
        """
        for i in range(len(results)):
            results[i] = results[i].select('td[align]')
            results[i] = [x.text.strip() for x in results[i]]
        return results

    def extract_results(self):
        self.page = self.get_results()
        rows = self.parse_page()
        parsed_results = self.parse_results(rows)
        return parsed_results

        
class Downloader(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.per_page = 50
        if self.subcorpus is None:
            self.subcorpus = 'xiandai'
        if self.mode is None:
            self.mode = 'simple'
        if self.nLeft is None:
            self.nLeft = 30
        if self.nRight is None:
            self.nRight = 30
        
            
    def download_all(self):
        """
        get information and hits from first page and iterate until
        all hits are collected or maximum set by user is achieved
        """
        parser = PageParser(self.query,self.numResults,self.subcorpus,
                            self.mode,self.nLeft,self.nRight)
        all_res = parser.extract_results()
        n_results = min(self.numResults,parser.occurrences)
        for i in range(self.per_page,n_results,self.per_page):
            parser.pagenum = i
            all_res += parser.extract_results()
        if len(all_res) > self.numResults:
            all_res = all_res[:self.numResults]
        return all_res


# rewrite
class TestMethods(unittest.TestCase):
    def test1(self):
        self.assertTrue(parse_page(get_results(query='古代汉',start=0,n=50,lang='xiandai',
                                               mode='simple',n_left=30,n_right=30)))

    def test2(self):
        self.assertIs(list, type(download_all(query='古代汉',results_wanted=10,n_left=30,
                                              n_right=30,lang='xiandai',mode='simple')))
       

if __name__ == '__main__':
    unittest.main()
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str)
    parser.add_argument('corpus', type=str)
    parser.add_argument('mode', type=str)
    parser.add_argument('n_results', type=int)
    parser.add_argument('n_left', type=int)
    parser.add_argument('n_right', type=int)
    parser.add_argument('kwic', type=bool)
    parser.add_argument('write', type=bool)
    args = parser.parse_args(args)
    main(**vars(args))
