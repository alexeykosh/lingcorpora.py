# python3
# coding=<UTF-8>

import re


class Result:
    def __init__(self, query):
        """
        results: list: list of type Target
        N: int: len(self.results)
        query: str: query
        """
        self.results = list()
        self.N = 0
        self.query = query
        self.q_prm = {k: query.parser.__dict__[k] \
                      for k in query.parser.__dict__ \
                      if k[0] != '_' and k != 'page'
                     }
                      
        self.__header = ('index', 'text')
        self.__kwic_header = ('index', 'left', 'center', 'right')
        self.__not_allowed = '/\\?%*:|"<>'
    
    def add(self, x):
        self.results.append(x)
        self.N += 1
    
    def __str__(self):
        return 'Result(query=%s, N=%s, params=%s)' % (self.q_prm['query'],
                                                      self.N,
                                                      self.q_prm
                                                     )
    
    __repr__ = __str__
    
    def __iter__(self):
        return iter(self.results)
    
    def export_csv(self, filename=None, header=True, sep=';'):
        if filename is None:
            filename = '%s_%s_results.csv' \
                        % (self.query.language,
                           re.sub(self.__not_allowed, '', self.q_prm['query'])
                          )
        
        with open(filename,'w',encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=sep, quotechar='"',
                                quoting=csv.QUOTE_MINIMAL, lineterminator='\n'
                               )
            
            if self.q_prm['kwic']:
                if header:
                    writer.writerow(self.__kwic_header)
                
                nLeft = self.q_prm['nLeft'] 
                nRight = self.q_prm['nRight']
                
                if nLeft is None:
                    nLeft = 10
                    
                if nRight is None:
                    nRight = 10
                    
                for i, t in enumerate(self.results):
                    writer.writerow((i + 1, *t.kwic(nLeft, nRight)))
            
            else:
                if header:
                    writer.writerow(self.__header)
                
                for i, t in enumerate(self.results):
                    writer.writerow((i + 1, t.text))
                    
    def clear(self):
        self.results = list()
