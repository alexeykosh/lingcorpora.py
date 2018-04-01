# python3
# coding=<UTF-8>

import re
import csv


class Result:
    def __init__(self, language, query_params):
        """
        language: str: language
        query_params: dict: __dict__ of used parser
        """
        self.results = list()
        self.N = 0
        self.lang = language
        self.query = query_params['query']
        self.params = {k: query_params[k] \
                      for k in query_params \
                      if k[0] != '_' and k not in ['page', 'query']
                     }
                      
        self.__header = ('index', 'text')
        self.__kwic_header = ('index', 'left', 'center', 'right')
        self.__not_allowed = '/\\?%*:|"<>'
    
    def add(self, x):
        self.results.append(x)
        self.N += 1
    
    def __str__(self):
        return 'Result(query=%s, N=%s, params=%s)' \
                % (self.query,
                   self.N,
                   self.params
                  )
    
    __repr__ = __str__
    
    def __iter__(self):
        return iter(self.results)
        
    def __getitem__(self,key):
        return self.results[key]
        
    def __setitem__(self,key,val):
        self.results[key] = val

    def __delitem__(self, key):
        del self.results[key]
    
    def export_csv(self, filename=None, header=True, sep=';'):
        if filename is None:
            filename = '%s_%s_results.csv' \
                        % (self.lang,
                           re.sub(self.__not_allowed, '', self.query)
                          )
        
        with open(filename,'w',encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=sep, quotechar='"',
                                quoting=csv.QUOTE_MINIMAL, lineterminator='\n'
                               )
            
            if self.params['kwic']:
                if header:
                    writer.writerow(self.__kwic_header)
                
                nLeft = self.params['nLeft'] 
                nRight = self.params['nRight']
                
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
