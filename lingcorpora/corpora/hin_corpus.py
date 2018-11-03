from ..params_container import Container
from ..target import Target
from requests import get
from bs4 import BeautifulSoup
import re

# has errors exporting results with words with diacritics on the end

TEST_DATA = {'test_single_query': {'query': 'कुत्ते'},
             'test_multi_query': {'query': ['कुत्ते', 'हाय']}
            }

__doc__ = \
    """
    
API for Hindi corpus (http://www.cfilt.iitb.ac.in/~corpus/hindi/find.php).
    
Args:
    query: str or List([str]): query or queries
    num_results: int: number of results wanted (100 by default)
    kwic: boolean: kwic format (True) or a sentence (False) (True by default)
    start: int: index of the first query appearance to be shown (0 by default)
    
Main function: extract
Returns:
    A generator of Target objects.

"""


class PageParser(Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = None
        if self.start is None:
            self.start = 0

    def __get_page(self):
        """
        create a query url and return a page with results
        """
        params = {'word': self.query,
                  'limit': self.num_results,
                  'start': self.start,
                  'submit': 'Search'}
        s = get('http://www.cfilt.iitb.ac.in/~corpus/hindi/find.php', params=params)
        return s

    def __new_target(self, left, word, right):
        text = '%s %s %s' % (left, word, right)
        idxs = (len(left) + 1, len(left) + len(word) + 1)
        meta = ''
        tags = {}
        return Target(text, idxs, meta, tags)

    def __get_results(self):
        """
        parse the page and get results
        """
        num = re.compile('\d+')
        sentence_list = []
        center_list = []
        left_list = []
        right_list = []
        soup = BeautifulSoup(self.page.text, 'lxml')
        for sentence in soup.select('tr[bgcolor*="f"] td'):
            if not num.match(sentence.text):
                sentence_list.append(sentence.text)
        for center in soup.select('td font a[target]'):
            if not num.match(center.text):
                center_list.append(center.text)
        for i in range(len(sentence_list)):
            res = sentence_list[i].split(center_list[i])
            left_list.append(res[0])
            right_list.append(res[1])
        s = [self.__new_target(l, w, r) for l, w, r in zip(
            left_list, center_list, right_list)]
        return s

    def __extract_results(self):
        self.page = self.__get_page()
        parsed_results = self.__get_results()
        return parsed_results

    def extract(self):
        parsed_results = self.__extract_results()
        for res in parsed_results:
            yield res
