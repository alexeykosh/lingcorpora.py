from ..params_container import Container
from ..target import Target
from requests import get
from bs4 import BeautifulSoup


TEST_DATA = {'test_single_query': {'query': 'къырым'},
             'test_multi_query': {'query': ['къырым', 'озюни']}
            }


__doc__ = \
    """
    
API for Crimean Tatar corpus (http://korpus.juls.savba.sk:8080/manatee.ks/do_query?corpname=qirim).
    
Args:
    query: str or List([str]): query or queries
    n_results: int: number of results wanted (100 by default)
    kwic: boolean: kwic format (True) or a sentence (False) (True by default)
    start: int: index of the first query appearance to be shown (0 by default)
    
Main function: extract
Returns:
    A generator of Target objects.

"""


class PageParser(Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__page = None
        self.__pagenum = 0

    def get_page(self):
        """
        create a query url and return a page with results
        """
        params = {'query': self.query,
                  'corpname': 'qirim',
                  'start': self.__pagenum}
        s = get('http://korpus.juls.savba.sk:8080/manatee.ks/do_query', params=params)
        return s.text

    def __get_target(self, l, word, r):
        text = '%s %s %s' % (l, word, r)
        idxs = (len(l) + 2, len(l) + 1 + len(word))
        meta = ''
        tags = {}
        return Target(text, idxs, meta, tags)

    def __parse_page(self):
        """
        parse the page
        """
        left_list = []
        center_list = []
        right_list = []
        soup = BeautifulSoup(self.__page, 'lxml')
        for left in soup.select('td[class="lc"]'):
            left_list.append(left.text)
        for center in soup.select('td[class="kwic"]'):
            center_list.append(center.text)
        for right in soup.select('td[class="rc"]'):
            right_list.append(right.text)
        res = [self.__get_target(l, c, r) for l, c, r in zip(
            left_list, center_list, right_list)]
        return res

    def __extract_results(self):
        self.__page = self.get_page()
        parsed_results = self.__parse_page()
        return parsed_results

    def extract(self):
        """
        get information and hits from first page and iterate until
        all hits are collected or the maximum set by user is achieved
        """
        output_counter = 0
        for i in range(0, self.n_results, 10):
            try:
                self.__pagenum = i
                results = self.__extract_results()
                j = 0
                while output_counter < self.n_results and j < len(results):
                    yield results[j]
                    output_counter += 1
                    j += 1
            except:
                pass
