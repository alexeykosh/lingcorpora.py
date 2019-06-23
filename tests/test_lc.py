import sys
import os
import unittest

from modulefinder import ModuleFinder
from random import randint
from collections import Iterable

sys.path.insert(0, os.path.abspath('..'))
from lingcorpora.corpus import Corpus, functions

__author__ = 'akv17'
__doc__ = 'unittest based routine for testing modules in `lingcorpora/corpora`'


class TestLangFunc(unittest.TestCase):

    """
    test given module for:
        - 0. valid fetch data
        - 1. processing single query
        - 2. matching number of results to the desired one
        - 3. processing multi query
        - 4. docstring
        - 5. using local scope only
        - 6. using legit dependencies only
    """

    def set_env(self, func, lang):
        """
        pass module to test as `func` <callable>, `lang` <str>
        """
        self.func = func
        self.lang = lang
        self.corp = Corpus(self.lang, verbose=False)
        self.fetch_data = None
        self.pre_globals_len = len(globals())

    def test_fetch_data(self):
        """
        *** ALWAYS TO BE RUN PRIMARILY ***

        assert that fetch data is valid
        set as `self.fetch` if valid
        """

        var = 'TEST_DATA'
        self.assertIn(var, self.func.__dict__)
        self.assertIsInstance(self.func.__dict__.get(var), dict)
        self.assertIn('test_single_query', self.func.__dict__[var].keys())
        self.assertIsInstance(self.func.__dict__[var].get('test_single_query'), dict)
        self.assertIsInstance(self.func.__dict__[var]['test_single_query'].get('query'), str)
        self.assertIn('test_multi_query', self.func.__dict__[var].keys())
        self.assertIsInstance(self.func.__dict__[var].get('test_multi_query'), dict)
        self.assertIsInstance(self.func.__dict__[var]['test_multi_query'].get('query'), Iterable)
        self.assertIsInstance(self.func.__dict__[var]['test_multi_query']['query'][0], str)

        TestLangFunc.fetch_data = self.func.__dict__[var]

    def test_single_query(self):
        kwargs = self.fetch_data['test_single_query']
        kwargs['n_results'] = randint(1, 5)

        parser = self.func.PageParser(**kwargs)
        
        res = list(parser.extract())

        self.assertGreater(len(res), 0)

        for t in res:
            l, r = t.idxs

            assert t.text[l:r].lower() == parser.query.lower(), \
                    '`%s` does not match query `%s`' % (t.text[l:r], parser.query)

        del kwargs, parser

    def test_n_results(self):
        kwargs = self.fetch_data['test_single_query']
        kwargs['n_results'] = randint(1, 5)

        parser = self.func.PageParser(**kwargs)

        res = list(parser.extract())

        assert len(res) == kwargs['n_results'], \
                'expected %s, got %s' % (kwargs['n_results'], len(res))

        del kwargs, parser, res

    def test_multi_query(self):
        kwargs = self.fetch_data['test_multi_query']
        kwargs['n_results'] = randint(1, 5)

        result_obj = self.corp.search(**kwargs)

        self.assertEqual(
            len(result_obj),
            len(kwargs['query']),
            'expected %s, got %s' % (len(kwargs['query']), len(result_obj))
        )

        del kwargs, result_obj
        
    def test_docstring(self):
        self.assertIn('__doc__', self.func.__dict__)
        self.assertIsInstance(self.func.__doc__, str)

    def test_local_scope_only(self):
        kwargs = self.fetch_data['test_single_query']
        kwargs['n_results'] = randint(1, 5)

        result_obj = self.corp.search(**kwargs)

        post_globals_len = len(globals())

        self.assertEqual(
            self.pre_globals_len,
            post_globals_len
        )

        del kwargs, result_obj

    def test_dependencies(self):
        # EXTREMELY SLOW

        path = os.path.join(
            os.pardir,
            'lingcorpora',
            'corpora',
            '%s_corpus.py' % self.lang
        )

        core_path = os.path.join(
            os.pardir,
            'lingcorpora',
            'corpus.py',
        )

        mf = ModuleFinder()
        mf.run_script(core_path)
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

    failures = []
    funcs_to_test = FUNCS_TO_TEST if funcs_to_test is None else funcs_to_test
    tests_to_run = TESTS_TO_RUN if tests_to_run is None else tests_to_run

    stream = sys.stderr if stream is None else stream

    log_header = '\n%s\nTESTING: %s_corpus.py\n%s\n\n'

    runner = unittest.TextTestRunner(stream, verbosity=verbosity)

    for lang, func in funcs_to_test.items():
        stream.write(log_header % ('*' * 20, lang, '*' * 20))

        suite = unittest.TestSuite()
        routine = TestLangFunc
        routine.set_env(routine, func, lang)

        runner.run(routine('test_fetch_data'))

        if routine.fetch_data is not None:
            for test in tests_to_run:
                suite.addTest(routine(test))

            test_res = runner.run(suite)
            failures.extend(test_res.failures)
            
    stream.close()

    return bool(failures)


if __name__ == '__main__':
    FUNCS_TO_TEST = functions
    TESTS_TO_RUN = [
        'test_single_query',
        'test_n_results',
        'test_multi_query',
        'test_docstring',
        'test_local_scope_only',
        # 'test_dependencies'
    ]

    return run()
