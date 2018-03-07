# python3
# coding=<UTF-8>


from collections import Iterable
import warnings
from time import sleep
from tqdm import tqdm
from result import Result
from corpora import *


functions = {#'rus': rus_corpus,
              'bam': bam_corpus
}


class Query:
    def __init__(self, language, sleep_time=1, sleep_each=5):
        """
        sleep_time: int: sleeping time in seconds
        sleep_each: int: sleep after each `sleep_each` request
        """
        
        self.language = language
        self.__corpus = functions[self.language] 
        self.search.__func__.__doc__ = self.__corpus.__doc__
        
        self.results = list()
        self.unsuccessful = list()
        self.__warn = 'Nothing found for query "%s".\n' \
                      'Unsuccessful queries are available via Query.unsuccessful'
        self.__pbar_desc = 'Query "%s"'
        self.__type_except = 'Argument `query` must be of type <str> or iterable, got <%s>'

        if sleep_each < 1:
            raise ValueError('Argument `sleep_each` must  be >= 1')
            
        self.sleep_each = sleep_each
        self.sleep_time = sleep_time

    def search(self, query, *args, **kwargs):
        """      
        for arguments see `params_container.Container`
        __________
        
        pbar bad behaviour if found < numResults
        pbar dies if interrupted
        verbose might be more stable
        we want to add param "progress=['bar', 'verbose']", dont we
        """
        
        if isinstance(query, str):
            query = [query]
        
        if not isinstance(query, Iterable):
            raise TypeError(self.__type_except % type(query))
        
        for q in query:
            _r = Result(q)
            parser = self.__corpus.PageParser(q, *args, **kwargs)
            q_desc = self.__pbar_desc % q

            if args:
                progress_total = args[0]
            elif 'numResults' in kwargs:
                progress_total = kwargs['numResults']
            else:
                progress_total = 100           
            for t in tqdm(parser.extract(),
                          total=progress_total,
                          unit='docs',
                          desc=q_desc):
                _r.add(t)
                if _r.N % self.sleep_each == 0:
                    sleep(self.sleep_time)
            
            self.results.append(_r)
            if _r.N == 0:
                warnings.warn(self.__warn % q)
                self.unsuccessful.append(q)
            
        return self.results
