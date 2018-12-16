from .arkhangelskiy_corpora import PageParser

language = 'greek'
results = 'http://web-corpora.net/GreekCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'γάτα'},
             'test_multi_query': {'query': ['γάτα', 'αγάπη']}
             }

__doc__ = \
    """
    
API for Modern Greek corpus (http://web-corpora.net/GreekCorpus/search/).
    
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
