# python3
# coding=<UTF-8>


class Container:
    def __init__(self, query, numResults=100, kwic=True, nLeft=None, nRight=None,
                 subcorpus=None, tag=False, queryLanguage=None,
                 start=0, writingSystem=None):
        self.query = query
        self.numResults = numResults
        self.kwic = kwic
        self.nLeft = nLeft
        self.nRight = nRight
        self.queryLanguage = queryLanguage
        self.subcorpus = subcorpus
        self.tag = tag
        self.start = start
        self.writingSystem = writingSystem
