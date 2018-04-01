# python3
# coding=<UTF-8>

import os
import re
from lxml import etree
import urllib.request as ur

from params_container import Container
from target import Target


__author__ = 'akv_17'
__doc__ = \
"""
API for National Corpus of Russian (http://ruscorpora.ru/index.html)

Args:
    query: str or List([str]): query or queries (currently only exact search by word or phrase is available)
    numResults: int: number of results wanted (100 by default)
    kwic: boolean: kwic format (True) or a sentence (False) (True by default)
    tag: boolean: whether to collect grammatical tags for target word or not (False by default)
    subcorpus: str: subcorpus ('main' by default).
                    Valid: ['main', 'syntax', 'paper', 'regional', 'school',
                            'dialect', 'poetic', 'spoken', 'accent', 'murco',
                            'multiparc', 'old_rus', 'birchbark', 'mid_rus', 'orthlib']
    
Main method: extract

Returns:
    A generator over Target objects.
"""


class PageParser(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.subcorpus is None:
            self.subcorpus = 'main'
        
        self.__seed = ''
        self.__temp = 'temptree.xml'
        self.__xpath = '/page/searchresult/body/result/document'
        self.__dpp = 100
        self.__stop_flag = False
        self.__c_page = 0
        self.__targets_seen = 0
        self.__nodia = 1
            
        self.__dom = 'http://search1.ruscorpora.ru/dump.xml?'
        self.__post = 'env=%s&mode=%s&text=%s&sort=%s&seed=%s&dpp=%s&req=%s&p=%s&nodia=%s'

    def __get_ana(self, word):
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
                    _text = str()
                    _idx = 0
                    _target_idxs = list()
                    _ana = list()
                    # iter over words in cur example
                    for word in snip.getchildren():
                        if word.tag == 'text':
                            _text += word.text
                            _idx += len(word.text)
                        
                        if len(word.attrib) > 0:
                            _text += word.attrib['text']
                            # process target
                            if word.attrib.get('target') is not None:
                                _target_idxs.append((_idx, _idx + len(word.attrib['text'])))
                                if analyses:
                                    _ana.append(self.__get_ana(word))
                                    
                            _idx += len(word.attrib['text'])
                            
                    if _target_idxs:
                        for i, ixs in enumerate(_target_idxs):
                            if analyses:
                                yield _text, ixs, _meta, _ana[i]
                            else:
                                yield _text, ixs, _meta, _ana
                    else:
                        continue
        
    def get_page(self):
        """
        return documents tree
        """
        params = ('alpha',
                  self.subcorpus,
                  'lexform',
                  'gr_tagging',
                  self.__seed,
                  self.__dpp,
                  ur.quote(self.query),
                  self.__c_page,
                  self.__nodia
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
            self.__targets_seen += 1
            if self.__targets_seen <= self.numResults:
                yield Target(*doc) 
            else:
                self.__stop_flag = True
                return
    
    def extract(self):
        """
        streamer to Query
        """
        while not self.__stop_flag:
            try:
                self.page = self.get_page()
                yield from self.get_results()

            except EnvironmentError:
                self.__stop_flag = True
            
            self.__c_page += 1
            
