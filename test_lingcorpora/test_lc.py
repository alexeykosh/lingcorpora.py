import sys
import os
import unittest
import pickle
from modulefinder import ModuleFinder

sys.path.insert(0, os.path.abspath('..'))
from lingcorpora.corpus import Corpus, functions


__author__ = 'akv17'
__doc__ = \
"""
unittest based routine for testing `lingcorpora`
i.e. language processing modules in `lingcorpora/corpora` 
"""


class TestLangFunc(unittest.TestCase):

    """
    test given language processing module for:
        - 1. processing single query
        - 2. matching number or results to desired one
        - 3. processing multiple query
        - 4. docstring availability
        - 5. exploiting local scope only
        - 6. exploiting legit dependencies only
    """

    def set_env(self, func, lang):
        """
        pass language processing module to test 
        as `func` <callable>, `lang` <str>
        """
        self.func = func
        self.lang = lang
        self.corp = Corpus(self.lang)
    
    def test_single_query(self):
        case = 'test_single_query'
        self.assertIn(case, self.func.__dict__)
        self.func.test_single_query()

    def test_num_results(self):
        case =  'test_num_results'
        self.assertIn(case, self.func.__dict__)
        self.func.test_num_results()

    def test_multi_query(self):
        case =  'test_multi_query'
        self.assertIn(case, self.func.__dict__)
        query = self.func.test_multi_query()
        R = self.corp.search(query=query,
                             numResults=1
                             )

        self.assertEqual(len(R), len(query))

        for q, r in zip(query, R):
            self.assertEqual(q, r.query)

        del R
        
    def test_docstring(self):
        case = '__doc__'
        self.assertIn(case, self.func.__dict__)
        self.assertIsInstance(self.func.__doc__, str)

    def test_local_scope_only(self):
        case = 'test_local_scope_only'
        query = self.func.test_multi_query()[0]
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
        path = os.path.join('lingcorpora',
                            'corpora',
                            '%s_corpus.py' % self.lang
                            )
        legit_deps = pickle.load(open('dependencies.pickle', 'rb'))
        
        mf = ModuleFinder()
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
        - vebosity: int: verbosity mode
    """
    
    if funcs_to_test is None:
        funcs_to_test = FUNCS_TO_TEST

    if tests_to_run is None:
        tests_to_run = TESTS_TO_RUN

    if stream is None:
        stream = sys.stderr

    log_header = '%s\nTESTING: %s_corpus.py\n%s\n\n'

    runner = unittest.TextTestRunner(stream, verbosity=verbosity)

    for LANG, FUNC in funcs_to_test.items():
        stream.write(log_header % ('=' * 20, LANG, '=' * 20))

        suite = unittest.TestSuite()
        routine = TestLangFunc

        for _test in tests_to_run:
            suite.addTest(routine(_test))

        routine.set_env(routine, FUNC, LANG)

        runner.run(suite)
            
    stream.close()

if __name__ == '__main__':
    #FUNCS_TO_TEST = functions
    FUNCS_TO_TEST = {'rus': functions['rus']}
    TESTS_TO_RUN = ['test_single_query',
                    'test_num_results',
                    'test_multi_query',
                    'test_docstring',
                    'test_local_scope_only',
                    'test_dependencies'
                    ]

    run()
