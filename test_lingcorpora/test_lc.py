import sys
import os
import unittest
import pickle
from modulefinder import ModuleFinder
from random import randint
from tqdm import tqdm

sys.path.insert(0, os.path.abspath('..'))
from lingcorpora.corpus import Corpus, functions


__author__ = 'akv17'
__doc__ = \
"""
unittest based routine for testing modules in `lingcorpora/corpora` 
"""


class TestLangFunc(unittest.TestCase):

    """
    test given module for:
        - 0. valid fetch data
        - 1. processing single query
        - 2. matching number of results to the desired one
        - 3. processing multi query
        - 4. docstring
        - 5. exploiting local scope only
        - 6. exploiting legit dependencies only
    """

    def set_env(self, func, lang):
        """
        pass module to test as `func` <callable>, `lang` <str>
        """
        self.func = func
        self.lang = lang
        self.corp = Corpus(self.lang, verbose=False)
        self.fetch_data = None

    def test_fetch_data(self):
        """
        *** ALWAYS TO BE RUN PRIMARILY ***

        assert that fetch data is valid
        set as `self.fetch` if valid
        """

        _var = 'TEST_QUERIES'
        self.assertIn(_var, self.func.__dict__)
        self.assertIsInstance(self.func.__dict__.get(_var), dict)
        self.assertIn('test_single_query', self.func.__dict__.get(_var).keys())
        self.assertIsInstance(self.func.__dict__.get(_var).get('test_single_query'), str)
        self.assertIn('test_multi_query', self.func.__dict__.get(_var).keys())
        self.assertIsInstance(self.func.__dict__.get(_var).get('test_multi_query'), list)
        self.assertIsInstance(self.func.__dict__.get(_var).get('test_single_query')[0], str)

        TestLangFunc.fetch_data = self.func.__dict__.get(_var)

    def test_single_query(self):
        query = self.fetch_data.get('test_single_query')

        parser = self.func.PageParser(query=query,
                                      numResults=3
                                      )

        for t in parser.extract():
            l, r = t.idxs
            assert t.text[l:r].lower() == query.lower(), \
                '`%s` does not match query `%s`' % (t.text[l:r], query)

        del parser

    def test_num_results(self):
        query = self.fetch_data.get('test_single_query')
        numResults = randint(1, 5)

        parser = self.func.PageParser(query=query,
                                      numResults=numResults
                                      )

        res = list(parser.extract())

        assert len(res) == numResults, 'expected %s, got %s' % (numResults, len(res))

        del parser, res

    def test_multi_query(self):
        query = self.fetch_data.get('test_multi_query')

        R = self.corp.search(query=query,
                             numResults=1
                             )

        self.assertEqual(len(R), len(query), 'expected %s, got %s' % (len(query), len(R)))

        for q, r in zip(query, R):
            self.assertEqual(q, r.query, '`%s` does not match query `%s`' % (r.query, q))

        del R
        
    def test_docstring(self):
        self.assertIn('__doc__', self.func.__dict__)
        self.assertIsInstance(self.func.__doc__, str)

    def test_local_scope_only(self):
        query = self.fetch_data.get('test_single_query')

        pre_globals_len = len(globals())

        R = self.corp.search(query=query,
                             numResults=1
                             )

        post_globals_len = len(globals())

        self.assertEqual(pre_globals_len,
                         post_globals_len
                         )

        del R

    def test_dependencies(self):
        """
        EXTREMELY SLOW
        """

        path = os.path.join('..',
                            'lingcorpora',
                            'corpora',
                            '%s_corpus.py' % self.lang
                            )

        core_path = os.path.join('..',
                                 'lingcorpora',
                                 'corpus.py',
                                 )

        # legit_deps = pickle.load(open('dependencies.pickle', 'rb'))

        mf = ModuleFinder()

        mf.run_script(init_path)
        legit_deps = set(mf.modules.keys())

        mf.run_script(path)
        deps = set(mf.modules.keys())

        self.assertEqual(len(deps.difference(legit_deps)), 0)
        
        del deps, legit_deps
            

def run(funcs_to_test=None, tests_to_run=None, stream=None, verbosity=2):
    """
    run testing routine
    args:
        - funcs_to_test: dict: {lang_name <str>: lang_func <callable>}
                                      of language processing modules to test
                                      if None `corpus.functions` passed
        - tests_to_run: list[<str>]: list of tests to run
                                              if None `TESTS_TO_RUN` passed
        - stream: file-like: stream to verbose to
                                  if None `sys.stderr` passed
        - verbosity: int: verbosity mode
    """
    
    if funcs_to_test is None:
        funcs_to_test = FUNCS_TO_TEST

    if tests_to_run is None:
        tests_to_run = TESTS_TO_RUN

    if stream is None:
        stream = sys.stderr

    log_header = '\n%s\nTESTING: %s_corpus.py\n%s\n\n'

    runner = unittest.TextTestRunner(stream, verbosity=verbosity)

    for LANG, FUNC in funcs_to_test.items():
        stream.write(log_header % ('*' * 20, LANG, '*' * 20))

        suite = unittest.TestSuite()
        routine = TestLangFunc

        routine.set_env(routine, FUNC, LANG)

        runner.run(routine('test_fetch_data'))

        if routine.fetch_data is not None:
            for _test in tests_to_run:
                suite.addTest(routine(_test))

            runner.run(suite)
            
    stream.close()

if __name__ == '__main__':
    # FUNCS_TO_TEST = functions
    FUNCS_TO_TEST = {'rus': functions['rus']}
    TESTS_TO_RUN = ['test_single_query',
                    'test_num_results',
                    'test_multi_query',
                    'test_docstring',
                    'test_local_scope_only',
                    # 'test_dependencies'
                    ]

    run()
