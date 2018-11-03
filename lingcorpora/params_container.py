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
                 analysis=False,
                 gr_tags=None,
                 query_language=None,
                 start=0,
                 writing_system=None
    ):

        self.query = query
        self.n_results = n_results
        self.kwic = kwic
        self.n_left = n_left
        self.n_right = n_right
        self.query_language = query_language
        self.subcorpus = subcorpus
        self.analysis = analysis
        self.gr_tags = gr_tags
        self.start = start
        self.writing_system = writing_system
