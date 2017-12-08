class Container:
    def __init__(self,query,subcorpus=None,tag=False,nLeft=None,
                 nRight=None,mode=None,numResults=100,kwic=True):
        self.language = language
        self.query = query
        self.subcorpus = subcorpus
        self.tag = tag
        self.nLeft = nLeft
        self.nRight = nRight
        self.mode = mode
        self.numResults = numResults
        self.results = []
        self.kwic = kwic
