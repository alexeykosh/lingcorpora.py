# python3
# coding=<UTF-8>

import os
import re

from lxml.etree import parse
from urllib.request import quote

from ..params_container import Container
from ..target import Target
from ..exceptions import EmptyPageException


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


TEST_DATA = {'test_single_query': {'query': 'фонема'},
             'test_multi_query': {'query': ['фонема', 'морфема']}
            }


class PageParser(Container):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__stop_flag = False
        self.__page_num = 0
        self.__targets_seen = 0
        
        self.subcorpus = self.subcorpus if self.subcorpus is not None else 'main' 
        self.__seed = ''
        self.__xpath = '/page/searchresult/body/result/document'
        self.__dpp = 100
            
        self.__url = 'http://search1.ruscorpora.ru/dump.xml?'
        self.__request = 'env=alpha&nodia=1&mode=%s&text=lexform&sort=gr_tagging&seed=%s&dpp=%s&req=%s&p=%s'

    def __get_ana(self, word):
        """
        Word's analysis parser
        """
        
        ana = dict()
        for _ana in word.findall('ana'):

            # iter over values of current ana of target (lex, sem, m, ...)
            for ana_type in _ana.findall('el'):
                ana[ana_type.attrib['name']] = [x.text for x in ana_type.findall('el-group/el-atom')]

        return ana       

    def __parse_docs(self, docs, analysis=True):
        """
        A generator over etree of documents
        """
        
        # iter over docs
        for doc in docs:
            meta = doc.attrib['title']

            # iter over snippets in *doc*
            for snip in doc.getchildren()[1:]:
                text = str()
                _len = 0
                target_idxs = list()
                ana = list()

                # iter over words in cur example
                for word in snip.getchildren():
                    
                    # nonalpha and unknown tokens
                    if word.tag == 'text':
                        text += word.text
                        _len += len(word.text)
                        continue

                    # lexical tokens
                    if word.attrib:
                        text += word.attrib['text']

                        # process target
                        if word.attrib.get('target') is not None:
                            target_idxs.append((_len, _len + len(word.attrib['text'])))
                            ana.append(self.__get_ana(word) if analysis else dict())

                        _len += len(word.attrib['text'])

                if target_idxs:
                    for i, idxs in enumerate(target_idxs):
                        yield text, idxs, meta, ana[i]

                else:
                    continue
        
    def __get_page(self, page_num):
        """
        return: etree of the page
        """
        params = (self.subcorpus,
                  self.__seed,
                  self.__dpp,
                  quote(self.query),
                  page_num,
                 )

        request = self.__request % (params)
        
        return parse(self.__url + request)

    def __get_results(self, page):
        docs_tree = page.xpath(self.__xpath)
        
        if not docs_tree:
            raise EmptyPageException
    
        for doc in self.__parse_docs(docs_tree, self.tag):
            self.__targets_seen += 1
            
            if self.__targets_seen <= self.numResults:
                yield Target(*doc) 
            
            else:
                self.__stop_flag = True
                return
    
    def extract(self):
        """
        A streamer to Corpus
        """
        while not self.__stop_flag:
            try:
                page = self.__get_page(self.__page_num)
                yield from self.__get_results(page)
                self.__page_num += 1
                
            except EmptyPageException:
                self.__stop_flag = True
            