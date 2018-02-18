# python3

import os
import re
from lxml import etree
import urllib.request as ur
from time import sleep
from collections import Iterable


class Container:
    def __init__(self,query,subcorpus=None,tag=False,nLeft=None,
                 nRight=None,mode=None,numResults=100,kwic=True,
                 session=None, language=None, targetLanguage=None, start=0):
        self.language = language
        self.targetLanguage = targetLanguage
        self.query = query
        self.subcorpus = subcorpus
        self.tag = tag
        self.nLeft = nLeft
        self.nRight = nRight
        self.mode = mode
        self.numResults = numResults
        self.kwic = kwic
        self.start = start


class Downloader(Container):
    def __init__(self, seed=None, *args,**kwargs):
        super().__init__(*args,**kwargs)
        if seed is None:
            self.seed = ''
        else:
            self.seed = seed
            
        if self.nLeft is None:
            self.nLeft = 10
        
        if self.nRight is None:
            self.nRight = 10
            
    def download_all(self):
        self.parser = PageParser(query=self.query, subcorpus=self.subcorpus,
                                 numResults=self.numResults, nLeft=self.nLeft,
                                 nRight=self.nRight, tag=self.tag, seed=self.seed)
        return self.parser.extract_results()


class Result:
    def __init__(self, query=None):
        self.results = list()
        self.N = 0
        self.query = query
    
    def add(self, x):
        self.results.append(x)
        self.N += 1
    
    def __str__(self):
        return 'Result(%s, %s)' % (self.query, self.N)
        
    __repr__ = __str__
    
    def export_csv(self):
        pass
    
    def clear(self):
        self.results = list()


class Target:
    def __init__(self, text, idxs, meta, tags):
        """
        text: list
        idxs: target idxs in text
        """
        self.text = text
        self.idxs = idxs
        self.meta = meta
        self.tags = tags
        
    def __str__(self):
        return 'Target(%s, %s)' % (', '.join([self.text[i] for i in self.idxs]).strip(), self.meta)

    __repr__ = __str__
    
    def to_text(self):
        try:
            return ''.join(self.text).strip()
        except TypeError:
            return ''.join(['_NONE_' if x is None else x for x in self.text]).strip()
    
    def kwic(self, l, r):
        out = list()
        for idx in self.idxs:
            _l = idx
            _r = idx
            l_cnt = 0
            r_cnt = 0
            l_res = ''
            r_res = ''
            l_flag = False
            r_flag = False
            
            while not l_flag:
                _l -= 1
                if _l <= 0:
                    l_flag = True
                if re.search('\w', self.text[_l]) is not None:
                    l_cnt += 1
                    if l_cnt >= l:
                        l_flag = True
                l_res = self.text[_l] + l_res
            
            while not r_flag:
                _r += 1
                if _r >= len(self.text) - 1:
                    r_flag = True
                if re.search('\w', self.text[_r]) is not None:
                    r_cnt += 1
                    if r_cnt >= r:
                        r_flag = True
                r_res += self.text[_r]
            
            out.append((l_res, r_res))
        
        return [('%s\t%s\t%s' % (out[i][0], self.text[idx], out[i][1])).strip() \
                for i, idx in enumerate(self.idxs)]

    
class PageParser:
    def __init__(self, query, subcorpus, numResults, nLeft, nRight, tag, seed=''):
        self.query = query
        self.page = None
        self.subcorpus = subcorpus
        self.numResults = numResults
        self.nLeft = nLeft
        self.nRight = nRight
        self.tag = tag
        self.seed = seed
        self.__custom_init()
    
    def __custom_init(self):
        self.R = Result(self.query)
        self.__temp = 'temptree.xml'
        self.__xpath = '/page/searchresult/body/result/document'
        self.__dpp = 100
        self.__stop_flag = False
        self.__c_page = 0
        self.__targets_seen = 0
        self.__sleep_time = 1
        self.__sleep_each = 5
        
        if self.subcorpus is None:
            self.subcorpus = ''
            
        self.__dom = 'http://search1.ruscorpora.ru/dump.xml?'
        self.__post = 'env=%s&mode=%s&text=%s&sort=%s&seed=%s&dpp=%s&mycorp=%s&req=%s&p=%s'

    def __get_ana(word):
        _ana = dict()
        for ana in word.findall('ana'):
            # iter over values of current ana of target (lex, sem, m, ...)
            for ana_type in ana.findall('el'):
                _ana[ana_type.attrib['name']] = [x.text for x in ana_type.findall('el-group/el-atom')]
        return _ana        

    def __parse_docs(self, docs, analyses=True):
        """
        a generator over documents tree
        """
        # iter over docs
        for i, doc in enumerate(docs):
            _meta = doc.attrib['title']
            # iter over examples in *doc*
            for snip in doc.getchildren()[1:]:
                _text = list()
                _idx = 0
                _target_idxs = list()
                _ana = dict()
                # iter over words in cur example
                for word in snip.getchildren():
                    if word.tag == 'text':
                        _text.append(word.text)
                        _idx += 1
                    if len(word.attrib) > 0:
                        _text.append(word.attrib['text'])
                        # process target
                        if word.attrib.get('target') is not None:
                            _target_idxs.append(_idx)
                            if analyses:
                                _ana = self.__get_ana(word)
                        _idx += 1
                if _target_idxs:
                    yield _text, _target_idxs, _meta, _ana
                else:
                    continue
        
    def get_page(self):
        """
        return documents tree
        """
        params = ('alpha',
                  'main',
                  'lexform',
                  'gr_tagging',
                  self.seed,
                  self.__dpp,
                  self.subcorpus,
                  ur.quote(self.query),
                  self.__c_page
                 )
        post = self.__post % (params)
        ur.urlretrieve(self.__dom + post, self.__temp)
        raw_tree = etree.parse(self.__temp)
        os.remove(self.__temp)
        return raw_tree

    def get_results(self):
        docs_tree = self.page.xpath(self.__xpath)
        
        if len(docs_tree) < 1:
            raise EnvironmentError('empty page')
        
        for doc in self.__parse_docs(docs_tree, analyses=self.tag):
            t = Target(*doc)  
            for c_example in t.idxs:
                self.__targets_seen += 1
                if self.__targets_seen <= self.numResults:
                    self.R.add(t)
                else:
                    self.__stop_flag = True
                    return

    def extract_results(self):
        """
        solve return for multiple targets in single kwic
        """
        while not self.__stop_flag:
            # print('parsing page: %s' % (self.__c_page + 1))
            try:
                # print('collecting results ...')
                self.page = self.get_page()
                self.get_results()
                # print('successfully collected: %s\n' % self.R.N)
            except EnvironmentError:
                # print('EMPTY page', (self.__c_page + 1))
                self.__stop_flag = True
            
            if (self.__c_page + 1) % self.__sleep_each == 0:
                # print('sleeping %s s. at page: %s' % (self.__sleep_time, self.__c_page))
                sleep(self.__sleep_time)
            
            self.__c_page += 1
        
        return [t.kwic(self.nLeft, self.nRight)[0].split('\t') for t in self.R.results]
