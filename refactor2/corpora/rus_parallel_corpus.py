# python3
# coding=<UTF-8>

from lxml import etree
import urllib.request as ur

from params_container import Container
from target import Target


__author__ = 'akv_17, maria-terekhina'
__doc__ = \
"""
API for parallel subcorpus of National Corpus of Russian (http://ruscorpora.ru/search-para-en.html)
Args:
    query: str or List([str]): query or queries (currently only exact search by word or phrase is available)
    numResults: int: number of results wanted (100 by default)
    kwic: boolean: kwic format (True) or a sentence (False) (True by default)
    tag: boolean: whether to collect grammatical tags for target word or not (False by default)
    subcorpus: str: subcorpus ('rus' by default - search query over all subcorpora).
                    Valid: ['rus', 'eng', 'bel', 'bul', 'bua', 'esp', 'ita',
                            'zho', 'lav', 'ger', 'pol', 'ukr',
                            'fra', 'sve', 'est']
    queryLanguage: str: language of the 'query'
    
Main method: extract
Returns:
    A generator over Target objects.
"""


class PageParser(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.subcorpus is None:
            self.subcorpus = 'rus'

        if self.queryLanguage is None:
            raise ValueError('Please specify query language')

        self.__seed = ''
        self.__temp = 'temptree.xml'
        self.__xpath = '/page/searchresult/body/result/document'
        self.__dpp = 100
        self.__stop_flag = False
        self.__c_page = 0
        self.__targets_seen = 0
            
        self.__dom = 'http://search1.ruscorpora.ru/dump.xml?'
        self.__post = 'mycorp=%s&text=%s&mode=%s&sort=%s&env=%s&req=%s&p=%s'

    def __get_ana(self, word):
        _ana = dict()
        for ana in word.findall('ana'):
            # iter over values of current ana of target (lex, sem, m, ...)
            for ana_type in ana.findall('el'):
                _ana[ana_type.attrib['name']] = [x.text for x in ana_type.findall('el-group/el-atom')]
        return _ana        

    def __parse_docs(self, docs, ql, analyses=True):
            """
            a generator over documents tree
            """
            # iter over docs
            for i, doc in enumerate(docs):
                _meta = doc.attrib['title']

                # iter over pairs in *doc*
                for para in doc.getchildren()[1:]:
                    _text = str()
                    _transl = str()
                    _idx = 0
                    _target_idxs = list()
                    _ana = list()
                    _lang = str()

                    # iter over examples in *para*
                    for snip in para.getchildren():
                        # iter over words in cur example
                        for word in snip.getchildren():
                            if word.tag == 'text':

                                if snip.attrib['language'] == ql[:-1]:
                                    _text += word.text
                                    _idx += len(word.text)
                                else:
                                    _transl += word.text

                                if snip.attrib['language'] != 'ru':
                                    _lang = snip.attrib['language']

                            if len(word.attrib) > 0:
                                # process target
                                if word.attrib.get('target') is not None:
                                    _target_idxs.append((_idx, _idx + len(word.attrib['text'])))
                                    if analyses:
                                        _ana.append(self.__get_ana(word))

                                if snip.attrib['language'] == ql[:-1]:
                                    _text += word.attrib['text']
                                    _idx += len(word.attrib['text'])
                                else:
                                    _transl += word.attrib['text']

                                if snip.attrib['language'] != 'ru':
                                    _lang = snip.attrib['language']

                    if _target_idxs:
                        for i, ixs in enumerate(_target_idxs):
                            if analyses:
                                yield _text, ixs, _meta, _ana[i], _transl, _lang
                            else:
                                yield _text, ixs, _meta, _ana, _transl, _lang
                    else:
                        continue
        
    def get_page(self):
        """
        return documents tree
        """
        params = ('%28lang%3A%22'+self.subcorpus+'%22+%7C+lang_trans%3A%22'+self.subcorpus+'%22%29',
                  'lexform',
                  'para',
                  'gr_tagging',
                  'alpha',
                  ur.quote(self.query),
                  self.__c_page)

        post = self.__post % (params)
        return etree.parse(self.__dom + post)

    def get_results(self):
        docs_tree = self.page.xpath(self.__xpath)

        if len(docs_tree) < 1:
            raise EnvironmentError('empty page')
    
        for doc in self.__parse_docs(docs_tree, self.queryLanguage, analyses=self.tag):
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
