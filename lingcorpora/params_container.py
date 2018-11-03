# python3
# coding=<UTF-8>


"""
PARAMS DESCRIPTION HERE 
"""


class Container:
    def __init__(self,
                 query,
                 n_results=100,
                 kwic=True,
                 n_left=None,
                 n_right=None,
                 subcorpus=None,
                 get_analysis=False,
                 gr_tags=None,
                 query_language=None,
                 start=0,
                 writing_system=None
    ):
        """
        Two arguments are universal:
        query: str or list[str]: query or queries
        n_results: int, optional, default 100: number of results wanted
        
        Other depend on the corpus:
        kwic: boolean, optional, default True: kwic format (True) or a sentence (False)
        n_left: int, optional: number of words / symbols (corpus-specific) in the left context
        n_right: int, optional: number of words / symbols (corpus-specific) in the right context
        subcorpus: str, optional: subcorpus to search in
        get_analysis: boolean, optional, default False: whether to download grammatical information if the corpus is annotated
        gr_tags: tags for grammar search
        query_language: str: for parallel corpora, language of the query
        start: int, optional, default 0: result index to start from
        writing_system: str, optional: writing system of results
        """
        self.query = query
        self.n_results = n_results
        self.kwic = kwic
        self.n_left = n_left
        self.n_right = n_right
        self.query_language = query_language
        self.subcorpus = subcorpus
        self.get_analysis = get_analysis
        self.gr_tags = gr_tags
        self.start = start
        self.writing_system = writing_system
