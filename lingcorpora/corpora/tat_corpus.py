from .arkhangelskiy_corpora import PageParser

language = 'tatar'
results = 'http://web-corpora.net/TatarCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'туган'},
             'test_multi_query': {'query': ['туган', 'мәхәббәт']}
             }

__doc__ = \
    """
    
API for Tatar corpus (http://web-corpora.net/TatarCorpus/).
    
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
