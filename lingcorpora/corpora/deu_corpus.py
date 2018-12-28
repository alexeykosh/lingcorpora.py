from ..params_container import Container
from ..target import Target
from requests import post
from bs4 import BeautifulSoup

TEST_DATA = {'test_single_query': {'query': 'bezug'},
             'test_multi_query': {'query': ['bezug', 'Mutter']}
            }

__author__ = 'alexeykosh, ustya-k'
__doc__ = \
    """
    
API for German corpus (https://www.dwds.de).
    
Args:
    query: str or List([str]): query or queries
    n_results: int: number of results wanted (100 by default)
    kwic: boolean: kwic format (True) or a sentence (False) (True by default)
    subcorpus: str: subcorpus. Available options: 'kern' (by default),
                                'tagesspiegel', 'zeit', 'public', 'blogs',
                                'dingler', 'untertitel', 'spk', 'bz', 'dta',
                                'korpus21'.
    
Main function: extract
Returns:
    A generator of Target objects.

"""


class PageParser(Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__page = None
        if self.subcorpus is None:
            self.subcorpus = 'kern'

    def __get_page(self):
        params = {'corpus': self.subcorpus,
                  'date-end': '1999',
                  'date-start': '1900',
                  'format': 'kwic',
                  'genre': 'Belletristik',
                  'genre': 'Wissenschaft',
                  'genre': 'Gebrauchsliteratur',
                  'genre': 'Zeitung',
                  'limit': self.n_results,
                  'q': self.query,
                  'sort': 'date_asc'}
        s = post('https://www.dwds.de/r', params=params)
        return s

    def __new_target(self, left, word, right):
        text = '%s %s %s' % (left, word, right)
        idxs = (len(left) + 2, len(left) + len(word))
        meta = ''
        tags = {}
        return Target(text, idxs, meta, tags)

    def __get_results(self):
        left_list = []
        right_list = []
        center_list = []
        soup = BeautifulSoup(self.__page.text, 'lxml')
        for left in soup.select('.ddc-kwic-ls'):
            left_list.append(left.text)
        for center in soup.select('.ddc-kwic-kw.ddc-hl'):
            center_list.append(center.text)
        for right in soup.select('.ddc-kwic-rs'):
            right_list.append(right.text)

        s = [self.__new_target(l, w, r) for l, w, r in zip(
            left_list, center_list, right_list)]
        return s

    def __extract_results(self):
        self.__page = self.__get_page()
        parsed_results = self.__get_results()
        return parsed_results

    def extract(self):
        parsed_results = self.__extract_results()
        for res in parsed_results:
            yield res
