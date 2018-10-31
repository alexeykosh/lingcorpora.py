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
        
        self.lang = language
        self.query = query_params['query']
        self.params = {k: query_params[k] \
                       for k in query_params \
                       if not k.startswith('_') and k not in ['page', 'query']
        }
        
        self.results = list()
        self.N = 0
                      
        self.__header = ('index', 'text')
        self.__kwic_header = ('index', 'left', 'center', 'right')
        self.__not_allowed = '/\\?%*:|"<>'
    
    def __str__(self):
        return 'Result(query=%s, N=%s, params=%s)' \
                % (self.query,
                   self.N,
                   self.params
        )
    
    __repr__ = __str__
    
    def __bool__(self):
        return True if self.N > 0 else False
    
    def __iter__(self):
        return iter(self.results)
    
    def __getattr__(self, name):
        if name.lower() == 'r':
            return self.results
        
        raise AttributeError("'Result' object has no attribute '%s'" % name)
        
    def __getitem__(self,key):
        return self.results[key]
        
    def __setitem__(self,key,val):
        self.results[key] = val

    def __delitem__(self, key):
        del self.results[key]
        
    def add(self, x):
        self.results.append(x)
        self.N += 1
    
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
                
                nLeft = self.params['nLeft'] if self.params['nLeft'] is not None else 10 
                nRight = self.params['nRight'] if self.params['nRight'] is not None else 10
                    
                for i, t in enumerate(self.results):
                    writer.writerow((i + 1, *t.kwic(nLeft, nRight)))
            
            else:
                if header:
                    writer.writerow(self.__header)
                
                for i, t in enumerate(self.results):
                    writer.writerow((i + 1, t.text))
                    
    def clear(self):
        del self.results
        self.results = list()
