# python3
# coding=<UTF-8>


class Container:
    def __init__(self, query='', numResults=100, kwic=True, nLeft=None, nRight=None,
                 subcorpus=None, tag=False, ana=False, targetLanguage=None,
                 mode=None, start=0):
        self.query = query
        self.numResults = numResults
        self.kwic = kwic
        self.nLeft = nLeft
        self.nRight = nRight
        self.targetLanguage = targetLanguage
        self.subcorpus = subcorpus
        self.tag = tag
        self.ana = ana
        self.targetLanguage = targetLanguage
        self.mode = mode
        self.start = start
