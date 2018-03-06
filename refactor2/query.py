# python3
# coding=<UTF-8>


from collections import Iterable
import warnings
from time import sleep
from tqdm import tqdm
from result import Result
# import rus_corpus_oop


# functions = {'rus': rus_corpus_oop}
functions = {}


class Query:
    def __init__(self, language):
        self.language = language
        self.__corpus = functions[self.language] 
        # self.search.__func__.__doc__ = self.__corpus.__doc__
        
        self.results = list()
        self.unsuccessful = list()
        self.__warn = 'Nothing found for query "%s".\n' \
                      'Unsuccessful queries are available via Query.unsuccessful'
        self.__pbar_desc = 'Query "%s"'
        self.__type_except = 'Argument `query` must be of type <str> or iterable, got <%s>'

    def search(self, query, sleep_time=1, sleep_each=5, *args, **kwargs):
        """
        sleep_time: int: sleeping time in seconds
        sleep_each: int: sleep after each `sleep_each` request
        
        for more arguments see `params_container.Container`
        
        __________
        
        pbar bad behaviour if found < numResults
        pbar dies if interrupted
        verbose might be more stable
        we want to add param "progress=['bar', 'verbose']", dont we
        """
        if sleep_each < 1:
            raise ValueError('Argument `sleep_each` must  be >= 1')
        
        if isinstance(query, str):
            query = [query]
        
        if not isinstance(query, Iterable):
            raise TypeError(self.__type_except % type(query))
        
        for q in query:
            _r = Result(q)
            parser = self.__corpus.PageParser(query=q, *args, **kwargs)
            q_desc = self.__pbar_desc % q
            
            for t in tqdm(parser.extract(),
                          total=kwargs['numResults'],
                          unit='docs',
                          desc=q_desc):
                _r.add(t)
                if _r.N % sleep_each == 0:
                    sleep(sleep_time)
            
            self.results.append(_r)
            if _r.N == 0:
                warnings.warn(self.__warn % q)
                self.unsuccessful.append(q)
            
        return self.results
