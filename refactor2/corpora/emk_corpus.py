from requests import get
from bs4 import BeautifulSoup
from params_container import Container
from html import unescape
from target import Target


__doc__ = \
"""
    
API for Maninka corpus (http://maslinsky.spb.ru/emk/run.cgi/first_form).
    
Args:
    query: list: queries (currently only exact search by word or phrase is available)
    numResults: int: number of results wanted (100 by default)
    kwic: boolean: kwic format (True) or a sentence (False) (True by default)
    subcorpus: str: subcorpus. Available options: 'cormani-brut-lat', 'corbama-brut-nko' ('cormani-brut-lat' by default)
    writingSystem: str: writing system for examples. Available options: 'nko', 'latin'. Bug: only 'latin' for 'corbama-brut-nko' subcorpus. 
    
Main function: extract
Returns:
    A generator of Target objects.

"""

class PageParser(Container):
    """
    TODO: 
    tackle emerging latin in nko subcorp
    view funcs (tags, context length)
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.subcorpus is None:
            self.subcorpus = 'cormani-brut-lat'
        if self.writingSystem is None or self.subcorpus.endswith(self.writingSystem[:3]):
            self.writingSystem = ''
        if self.kwic:
            self.viewmode = 'kwic'
        else:
            self.viewmode = 'sen'
            
        self.page = None
        self.pagenum = 1
        
 
    def get_results(self):
        """
        create a query url and get results for one page
        """
        params = {
            "corpname": self.subcorpus,
            "iquery": self.query,
            "fromp": self.pagenum,
            "viewmode": self.viewmode,
            "attrs": self.writingSystem,
            "ctxattrs": self.writingSystem
        }
        r = get('http://maslinsky.spb.ru/emk/run.cgi/first',params)
        return unescape(r.text)


    def parse_page(self):
        """
        find results (and total number of results) in the page code
        """
        soup = BeautifulSoup(self.page, 'lxml')
        if soup.select('div#error'):
            return []
        res = soup.find('table')
        res = res.find_all('tr')
        if self.pagenum == 1:
            self.numResults = min(int(soup.select('strong[data-num]')[0].text),self.numResults)
        return res      
        
   
    def parse_result(self,result):
        if self.kwic:
            lc = ' '.join([x.text.strip() for x in result.select('td.lc span.nott')]).strip()
            rc = ' '.join([x.text.strip() for x in result.select('td.rc span.nott')]).strip()
        else:
            lc = result.select('span.nott')[0].string.strip()
            rc = result.select('span.nott')[-1].string.strip()
        final_kws = result.select('div.token span.nott')[0].string.strip()
        idx = (len(lc), len(lc) + 1 + len(final_kws))
        text = lc + ' ' + final_kws + ' ' + rc
        t = Target(text.strip(),idx,'',[])
        return t

        
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
            self.pagenum += 1
