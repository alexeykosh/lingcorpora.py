from .arkhangelskiy_corpora import PageParser

language = 'buryat'
results = 'http://web-corpora.net/BuryatCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'хөөшхэ'},
             'test_multi_query': {'query': ['хөөшхэ', 'дурлаха']}
             }

__author__ = 'ustya-k'
__doc__ = \
    """
    
API for Buryat corpus (http://web-corpora.net/BuryatCorpus/search/).
    
Args:
    query: str or List([str]): query or queries
    n_results: int: number of results wanted (100 by default)
    kwic: boolean: kwic format (True) or a sentence (False) (True by default)
    get_analysis: boolean: tags shown (True) or not (False)
    
Main function: extract
Returns:
    A generator of Target objects.

"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
