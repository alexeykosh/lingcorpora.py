import requests
from bs4 import BeautifulSoup
from ..params_container import Container
from ..target import Target
import re

TEST_QUERIES = {'test_single_query': 'skyne',
                'test_multi_query': ['skyne', 'kanon']
                }

__doc__ = \
"""
    
API for Danish corpus (https://ordnet.dk/korpusdk_en/concordance).
    
Args:
    query: str or List([str]): query or queries (currently only search by forms of the word is available)
    numResults: int: number of results wanted (100 by default)
    
Main function: extract
Returns:
    A generator of Target objects.

"""


class PageParser(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.punc = re.compile("[.-\[\]:\";,!?']")
        self.__pagenum = 1
        self.__page = None
        self.__occurrences = 0
        self.__session = requests.Session()
        
    def get_first_page(self):
        params = {'query': self.query,
                  'search': 'Search',
                  'tag': 'lemma'}
        response = self.__session.get('http://ordnet.dk/korpusdk_en/concordance/action', params=params)
        return response


    def get_page(self):
        params = {'page': self.__pagenum}
        page = requests.get('http://ordnet.dk/korpusdk_en/concordance/result/navigate',
                            params=params, cookies=self.__session.cookies)
        return page


    def extract_one_res(self,sen):
        left_part = ''
        right_part = ''
        for word in sen.select('.left-context-cell'):
           left_part = left_part + ' ' + word.select('a')[0].text
        for word in sen.select('.right-context-cell'):
            right_part = right_part + ' ' + word.select('a')[0].text
        center_part = sen.select('.conc_match')[0].a.text.strip()
        left_part, right_part = left_part.strip(), right_part.strip()
        if self.punc.search(center_part[1:]) is not None:
            right_part = center_part[self.punc.search(center_part[1:]).start()+1:].strip() + ' ' + right_part
            center_part = center_part[0:self.punc.search(center_part[1:]).start()+1].strip()
        idx = (len(left_part) + 1, len(left_part) + 1 + len(center_part))
        text = left_part + ' ' + center_part + ' ' + right_part
        t = Target(text,idx,'',[])
        return t        
        
        
    def get_results_page(self):
        soup = BeautifulSoup(self.__page.text, 'lxml')
        if self.__pagenum == 1:
            occur = soup.select('.value')[0].text
            self.__occurrences = int(occur[(occur.find('of') + 2):(occur.find('occur'))].strip())
            #self.__occurrences = 5000
            if self.__occurrences > 49:
                self.__occurrences -= 1
        p = soup.select('.conc_table')[0]
        return p.select('tr[onmouseover]')


    def extract(self):
        n = 0
        self.__page = self.get_first_page()
        if self.__page.status_code == 200:
            results = self.get_results_page()
            final_total = min(self.numResults,self.__occurrences)
            num_page = final_total // 50 + 1
            while n < final_total and n < len(results):
                yield self.extract_one_res(results[n])
                n += 1
            for i in range(2, num_page + 1):
                r = 0
                self.__pagenum = i
                self.__page = self.get_page()
                results = self.get_results_page()
                while n < final_total and r < len(results):
                    yield self.extract_one_res(results[r])
                    n += 1
                    r += 1
