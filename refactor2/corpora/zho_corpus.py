from params_container import Container
from requests import get
from bs4 import BeautifulSoup
from html import unescape
from target import Target


__doc__ = \
"""
    
API for Chinese corpus (http://ccl.pku.edu.cn:8080/ccl_corpus/).
    
Args:
    query: list: queries (currently only exact search by word or phrase is available)
    numResults: int: number of results wanted (100 by default)
    subcorpus: str: subcorpus. Available options: ‘xiandai’ (modern Chinese) or ‘dugai’ (ancient Chinese) ('xiandai' by default)
    mode: str: ‘simple’ (default) or ‘pattern’ (regular expressions, description here (in Chinese): http://ccl.pku.edu.cn:8080/ccl_corpus/CCLCorpus_Readme.html)
    nLeft, nRight: int: context lenght (in symbols, 30 by default)
    
Main function: extract
Returns:
    A generator of Target objects.

"""


class PageParser(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.per_page = 50
        self.pagenum = 0
        if self.subcorpus is None:
            self.subcorpus = 'xiandai'
        if self.mode is None:
            self.mode = 'simple'
        if self.nLeft is None:
            self.nLeft = 30
        if self.nRight is None:
            self.nRight = 30

            
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
            self.numResults = min(self.numResults,int(soup.find('td',class_='totalright').find('b').text))
        return res

        
    def parse_result(self,result):
        """
        find hit and its left and right contexts
        in the extracted row of table
        """
        result = result.select('td[align]')
        result = [x.text.strip() for x in result]
        text = ''.join(result)
        idxs = (len(result[0]),len(result[0])+len(result[1]))
        return Target(text,idxs,'',[])

        
    def extract(self):
        n = 0
        while n < self.numResults:
            self.page = self.get_results()
            rows = self.parse_page()
            if not rows:
                break
            r = 0
            while n < self.numResults and r < len(rows):
                yield self.parse_result(rows[r])
                n += 1
                r += 1
            self.pagenum += self.per_page

