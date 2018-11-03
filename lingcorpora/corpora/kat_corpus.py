from ..params_container import Container
from ..target import Target
import requests
from bs4 import BeautifulSoup


TEST_DATA = {'test_single_query': {'query': 'წელი'},
             'test_multi_query': {'query': ['წამს', 'დეიდა']}
            }
            

__doc__ = \
"""
    
API for Georgian monolingual corpus (http://corpora.iliauni.edu.ge).
    
Args:
    query: str or List([str]): query or queries (currently only exact search by word is available)
    n_results: int: number of results wanted (100 by default)
    
Main function: extract
Returns:
    A generator of Target objects.

"""

class PageParser(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.__pagenum = 0
        self.__page = None
        self.__occurrences = 0
        self.__session = requests.Session()
        
    def get_first_page(self):
        data = {'exact_word': self.query,
                'op': 'Search',
                'form_build_id': 'form-hMOF3mG0n7lwL6LmHrPi9vZCcaLbsZmCAco4z8vALT4',
                'form_id': 'sw_exact_word_search_form'}
        params = {'q': 'search-words'}
        response = self.__session.post('http://corpora.iliauni.edu.ge/', params=params, data=data)
        return response


    def get_page(self):
        params = {'page': str(self.__pagenum),
                  'q':	'search-words'}
        page = requests.get('http://corpora.iliauni.edu.ge/', params=params, cookies=self.__session.cookies)
        return page


    def get_results_page(self):
        res = []
        soup = BeautifulSoup(self.__page.text, 'lxml')
        if self.__pagenum == 0:
            occur = soup.select('.mtavruli')[0].string
            self.__occurrences = int(occur.split(' ')[2])
        table = soup.select('.result_table')[0]
        return table.select('tr')

        
    def extract_one_res(self,sen):
        left_part = ''
        right_part = ''
        for word in sen.select('.left_side'):
            if word.string:
                left_part = left_part + ' ' + word.string
        for word in sen.select('.right_side'):
            if word.string:
                right_part = right_part + ' ' + word.string
        left_part, center_part, right_part = left_part.strip(), \
                                             sen.select('.found_word')[0].string.strip(), \
                                             right_part.strip()
        idx = (len(left_part) + 1, len(left_part) + 1 + len(center_part))
        text = left_part + ' ' + center_part + ' ' + right_part
        t = Target(text,idx,'',[])
        return t

        
    def extract(self):
        n = 0
        self.__page = self.get_first_page()
        if self.__page.status_code == 200:
            results = self.get_results_page()
            final_total = min(self.n_results, self.__occurrences)
            num_page = (final_total + 9) // 10
            while n < final_total and n < len(results):
                yield self.extract_one_res(results[n])
                n += 1
            for i in range(1, num_page):
                r = 0
                self.__pagenum = i
                self.__page = self.get_page()
                results = self.get_results_page()
                while n < final_total and r < len(results):
                    yield self.extract_one_res(results[r])
                    n += 1
                    r += 1

