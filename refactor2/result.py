# python3
# coding=<UTF-8>


class Result:
    def __init__(self, query=None):
        """
        results: list: list of type Target
        N: int: len(self.results)
        query: str: query
        """
        self.results = list()
        self.N = 0
        self.query = query
    
    def add(self, x):
        self.results.append(x)
        self.N += 1
    
    def __str__(self):
        return 'Result(%s, %s)' % (self.query, self.N)
        
    __repr__ = __str__
    
    def export_csv(self):
        pass
    
    def clear(self):
        self.results = list()
        