# python3
# coding=<UTF-8>

import warnings
from collections import Iterable, deque
from time import sleep

from tqdm import tqdm

from .result import Result
from .functions import functions


class Corpus:
    """The object of this class should be instantiated for each corpus. Search is conducted via search method
    
    Attributes:
        language: str: in most cases,
            Language ISO 639-3 code for the corpus with combined codes for parallel corpora.
            List of available corpora with corresponding codes:
           ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
           ┃ Code         ┃   Corpus                                                      ┃
           ┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
           ┃ bam          ┃   Corpus Bambara de Reference                                 ┃
           ┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
           ┃ emk          ┃   Maninka Automatically Parsed corpus                         ┃
           ┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
           ┃ rus          ┃   National Corpus of Russian Language                         ┃
           ┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
           ┃ rus_parallel ┃   Parallel subcorpus of National Corpus of Russian Language   ┃
           ┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
           ┃ zho          ┃   Center of Chinese Linguistics corpus                        ┃
           ┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

        sleep_time: int, optional, default 1:
            The length of pause between requests to the corpus (in seconds).
            It is required to avoid blocking and corpus breakdown.
        sleep_each: int, optional, default 5:
            The number of requests after which a pause is required.
        doc: str:
            Documentation for chosen corpus (after instance creation).
        results: list:
            List of all Result objects, each returned by search method.
        failed: list:
            List of Result objects where nothing was found.
    """

    def __init__(self, language, verbose=True):
        """
        language: str: language alias
        verbose: bool: enable tqdm progressbar
        """
        
        self.language = language
        self.verbose = verbose
        self.corpus = functions[self.language] 
        self.doc = self.corpus.__doc__
        self.gr_tags_info = self.corpus.__dict__.get('GR_TAGS_INFO')

        self.results = list()
        self.failed = deque(list())
        
        self.warn_str = 'Nothing found for query "%s"'
        self.pbar_desc = '"%s"'
    
    def __getattr__(self, name):
        if name.lower() == 'r':
            return self.results
        
        raise AttributeError("<Corpus> object has no attribute '%s'" % name)

    def __to_multisearch_format(self, arg, arg_name, len_multiplier=1):
        """
        pack <str> or List[str] `arg` to multisearch format
        """
        
        if isinstance(arg, str):
            arg = [arg] * len_multiplier
        
        if not isinstance(arg, Iterable):
            raise TypeError(
                'Argument `%s` must be of type <str> or iterable[str], got <%s>'
                % (arg_name, type(arg))
            )
            
        return arg

    def get_gr_tags_info(self):
        return self.gr_tags_info

    def search(self, query, *args, **kwargs):
        """
        query: str: query
        for arguments see `params_container.Container`
        """

        query = self.__to_multisearch_format(arg=query, arg_name='query')
        gr_tags = kwargs.get('gr_tags', [None] * len(query))
        gr_tags = self.__to_multisearch_format(
            arg=gr_tags,
            arg_name='gr_tags',
            len_multiplier=len(query)
        )

        if len(query) != len(gr_tags):
            raise ValueError('`query`, `gr_tags` length mismatch')

        results = []
        
        for q, c_gr_tags in zip(query, gr_tags):
            kwargs['gr_tags'] = c_gr_tags            
            parser = self.corpus.PageParser(q, *args, **kwargs)
            result_obj = Result(self.language, parser.__dict__)
                
            for target in tqdm(
                parser.extract(),
                total=parser.n_results,
                unit='docs',
                desc=self.pbar_desc % q,
                disable=not self.verbose
            ):
                result_obj.add(target)
            
            if result_obj:
                results.append(result_obj)
            
            else:
                warnings.warn(self.warn_str % q)
                self.failed.append(result_obj)
        
        self.results.extend(results)
        
        return results

    def retry_failed(self):
        """
        Apply `.search()` to failed queries stored in `.failed`
        """
        
        if self.failed:
            n_rounds = len(self.failed)
            retrieved = []
            
            for _ in range(n_rounds):
                r_failed = self.failed.popleft()
                
                # List[<Result>]
                results_new = self.search(
                    r_failed.query,
                    **r_failed.params
                )
                
                if results_new:
                    retrieved.append(results_new[0])
            
            return retrieved
        
    def reset_failed(self):
        """
        Reset `.failed`
        """
        
        self.failed = deque(list())
