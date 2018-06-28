# python3
# coding=<UTF-8>

from collections import Iterable
import warnings
from time import sleep
from tqdm import tqdm
from .result import Result
from .corpora import *


functions = {
             'rus': rus_corpus,
             'bam': bam_corpus,
             'emk': emk_corpus,
             'zho': zho_corpus,
             'rus_parallel': rus_parallel_corpus,
             'dan': dan_corpus,
             'est': est_corpus,
             'kat': kat_corpus,
             'crh': crh_corpus,
             'tat': tat_corpus,
             'deu': deu_corpus,
             'slk': slk_corpus,
             'hin': hin_corpus
            }


class Corpus:
    def __init__(self, language, verbose=True, sleep_time=1, sleep_each=5):
        """
        language: str: language alias
        verbose: bool: tqdm progressbar
        sleep_time: int: sleeping time in seconds
        sleep_each: int: sleep after each `sleep_each` request
        """
        
        self.language = language
        self.verbose = verbose
        self.__corpus = functions[self.language] 
        self.doc = self.__corpus.__doc__
        
        self.results = list()
        self.failed = list()
        self.__retry_flag = False
        
        self.__warn = 'Nothing found for query "%s".\n' \
                      'Call `retry_failed` method to retry failed queries'
        self.__pbar_desc = '"%s"'
        self.__type_except = 'Argument `query` must be of type <str> or iterable, got <%s>'

        if sleep_each < 1:
            raise ValueError('Argument `sleep_each` must  be >= 1')
            
        self.sleep_each = sleep_each
        self.sleep_time = sleep_time

    def search(self, query, *args, **kwargs):
        """
        query: str: query
        for arguments see `params_container.Container`
        """
        
        if isinstance(query, str):
            query = [query]
        
        if not isinstance(query, Iterable):
            raise TypeError(self.__type_except % type(query))
            
        if args:
            progress_total = args[0]
        elif 'numResults' in kwargs:
            progress_total = kwargs['numResults']
        else:
            progress_total = 100
        
        _results = list()
        
        for q in query:
            self.parser = self.__corpus.PageParser(q, *args, **kwargs)
            _r = Result(self.language, self.parser.__dict__)
            q_desc = self.__pbar_desc % q
                
            for t in tqdm(self.parser.extract(),
                          total=progress_total,
                          unit='docs',
                          desc=q_desc,
                          disable=abs(-1 + self.verbose)):
                _r.add(t)
                if _r.N % self.sleep_each == 0:
                    sleep(self.sleep_time)
            
            _results.append(_r)
            if _r.N < 1:
                warnings.warn(self.__warn % q)
                if not self.__retry_flag:
                    self.failed.append(_r)
        
        if not self.__retry_flag:
            self.results.extend(_results)
        
        return _results

    def retry_failed(self):
        """
        Calls `.search()` for failed queries stored in `.failed`
        
        ISSUE:
        if `_r` got successfully retrieved here,
        its empty `Result` is still left in `Corpus.results` 
        """
        if self.failed:
            self.__retry_flag = True
            _pos = list()
            _neg = list()
            
            for r in self.failed:
                _r = self.search(r.query, **r.params)[0]
                if _r.N > 0:
                    _pos.append(_r)
                else:
                    _neg.append(_r)
            
            self.failed = _neg[:]
            self.results.extend(_pos)
            self.__retry_flag = False
            
            return _pos
        
        else:
            return []
