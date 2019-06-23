# python3
# coding=<UTF-8>

import os
import re

from lxml.etree import parse
from urllib.request import quote

from ..params_container import Container
from ..target import Target
from ..exceptions import EmptyPageException


__author__ = 'akv17'

__doc__ = \
"""
API for National Corpus of Russian (http://ruscorpora.ru/index.html)

Args:
    query: str or List([str]): query or queries (currently only exact search by word or phrase is available)
    num_results: int: number of results wanted (100 by default)
    kwic: boolean: kwic format (True) or a sentence (False) (True by default)
    get_analysis: boolean: whether to collect grammatical tags for target word or not (False by default)
    subcorpus: str: subcorpus ('main' by default).
                    Valid: ['main', 'syntax', 'paper', 'regional', 'school',
                            'dialect', 'poetic', 'spoken', 'accent', 'murco',
                            'multiparc', 'old_rus', 'birchbark', 'mid_rus', 'orthlib']

Main method: extract

Returns:
    A generator over Target objects.
"""

GR_TAGS_INFO = \
"""
Часть речи
    существительное: S
    прилагательное: A
    числительное: NUM
    числприл: ANUM
    глагол: V
    наречие: ADV
    предикатив: PRAEDIC
    вводное слово: PARENTH
    местсущ: SPRO
    местприл: APRO
    местпредикатив: PRAEDICPRO
    местоименное наречие: ADVPRO
    предлог: PR
    союз: CONJ
    частица: PART
    междометие: INTJ

Падеж
    именительный: nom
    звательный: voc
    родительный: gen
    родительный 2: gen2
    дательный: dat
    винительный: acc
    винительный 2: acc2
    творительный: ins
    предложный: loc
    предложный 2: loc2
    счётная форма: adnum

Наклонение / Форма
    изъявительное: indic
    повелительное: imper
    повелительное 2: imper2
    инфинитив: inf
    причастие: partcp
    деепричастие: ger

Степень / Краткость
    сравнительная: comp
    сравнительная 2: comp2
    превосходная: supr
    полная форма: plen
    краткая форма: brev

Время
    настоящее: praes
    будущее: fut
    прошедшее: praet

Переходность
    переходный: tran
    непереходный: intr

Число
    единственное: sg
    множественное: pl

Лицо
    первое: 1p
    второе: 2p
    третье: 3p

Прочее
    цифровая запись: ciph
    аномальная форма: anom
    искаженная форма: distort
    инициал: INIT
    сокращение: abbr
    несклоняемое: 0
    топоним: topon

Имена собственные
    фамилия: famn
    имя: persn
    отчество: patrn

Род
    мужской: m
    женский: f
    средний: n
    общий: mf

Залог
    действительный: act
    страдательный: pass
    медиальный: med

Одушевленность
    одушевленное: anim
    неодушевленное: inan

Вид
    совершенный: pf
    несовершенный: ipf
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
        self.__request_gr = 'env=alpha&nodia=1&mode=%s&text=lexgramm&sort=gr_tagging&seed=%s&dpp=%s&lex1=%s&gramm1=%s&p=%s'

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
                        yield text, idxs, meta, ana[i], self.gr_tags

                else:
                    continue
        
    def __get_page(self, page_num):
        """
        return: etree of the page
        """

        if self.gr_tags is not None:
            arguments = (self.subcorpus,
                         self.__seed,
                         self.__dpp,
                         quote(self.query),
                         quote(self.gr_tags),
                         page_num
            )

        else:
            arguments = (self.subcorpus,
                         self.__seed,
                         self.__dpp,
                         quote(self.query),
                         page_num
            )

        request = self.__request_gr if self.gr_tags is not None else self.__request
        request = request % (arguments)
        
        return parse(self.__url + request)

    def __get_results(self, page):
        docs_tree = page.xpath(self.__xpath)
        
        if not docs_tree:
            raise EmptyPageException
    
        for doc in self.__parse_docs(docs_tree, self.get_analysis):
            self.__targets_seen += 1
            
            if self.__targets_seen <= self.n_results:
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
            