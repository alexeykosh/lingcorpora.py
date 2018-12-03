# -*- coding: utf-8 -*-
# Uses python 3.7.1


import re
import requests
from bs4 import BeautifulSoup
from ..params_container import Container
from ..target import Target


# control of the number of results is senseless for now in this dictionary

__author__ = 'Pandaklez'
__doc__ = \
    """
    API for Spreadthesign sign language dictionary (https://www.spreadthesign.com/)
    Args:
        query: str or List([str]): query or queries (only exact search by word is available)
        subcorpus: str or List([str]): target sign language. ('ru.ru' by default)
                                       Valid (use abbreviations): {'Russian': 'ru.ru', 'Swedish': 'sv.se',
                                       'American English': 'en.us', 'British English': 'en.gb',
                                       'Mexican Spanish': 'es.mx', 'Czech': 'cs.cz', 'Lithuanian': 'lt.lt',
                                       'Spanish': 'es.es', 'Portuguese': 'pt.pt', 'Japanese': 'ja.jp',
                                       'German': 'de.de', 'French': 'fr.fr', 'Turkish': 'tr.tr',
                                       'Portuguese (Brasil)': 'pt.br', 'Italian': 'it.it', 'Polish': 'pl.pl',
                                       'Icelandic': 'is.is', 'German (Austria)': 'de.at', 'Estonian': 'et.ee',
                                       'Latvian': 'lv.lv', 'English (India)': 'en.in', 'Bulgarian': 'bg.bg',
                                       'Chinese': 'zh.hans.cn', 'Urdu': 'ur.pk', 'Croatian': 'hr.hr',
                                       'Russian (Belarus)': 'ru.by'}
        query_language: str: language of the 'query'. Same languages as for 'subcorpus' argument are valid.
        variants: boolean: Enable to see variants of one sign (if exist). False by default.
        only_link: boolean: Enable if you want videos to be downloaded. False by default.
                            If you don't want to download videos use links from Target.transl.
        sentences: boolean: In some cases you can search for the whole sentences be a word. False by default.
    Main method: extract
    Returns:
        A generator over Target objects.
    """

TEST_DATA = {'test_single_query': {'query': 'собака', 'query_language': "ru.ru", 'subcorpus': "uk.ua"},
             'test_multi_query': {'query': ['moon', 'T-shirt'], 'query_language': "en.us", 'subcorpus': "en.us"}
             }

class PageParser(Container):

    def __init__(self, *args, **kwargs):
        self.only_link = kwargs.pop("only_link", True)
        self.variants = kwargs.pop("variants", False)
        self.sentences = kwargs.pop("sentences", False)
        super().__init__(*args, **kwargs)

        if not isinstance(self.query, list) and not isinstance(self.query, str):
            raise TypeError("Query should be a string or a list of strings")

        if self.query_language is None:
            raise ValueError('Please specify query language')

        if not isinstance(self.query_language, str):
            raise TypeError("Language of the query should be a string \n Available languages can be seen in docstring")

        if not isinstance(self.subcorpus, list) and not isinstance(self.subcorpus, str):
            raise TypeError("Subcorpus should be a string or a list of strings \n Available languages can be seen in docstring")

        if self.subcorpus is None:
            self.subcorpus = "ru.ru"

    def get_page(self, lang, word):
        url_address = "http://www.spreadthesign.com/" + self.query_language + "/search/?cls=2&q=" + word
        r = requests.get(url_address)
        res = re.search('id=\"result-(.*)\"', str(BeautifulSoup(r.content, features="lxml", from_encoding=r.encoding)))
        num = res.group(1)

        url_ad = "http://www.spreadthesign.com/" + self.query_language +\
                 "-to-" + lang + "/word/" + num + "/0/?q=" + word
        r1 = requests.get(url_ad)
        soup = BeautifulSoup(r1.content, features="lxml", from_encoding=r.encoding)
        try:
            link = soup.video['src']
        except TypeError:
            raise TypeError("There is no sign {} for {} sign language".format(word, lang))

        # take into account a possibility of 4 variants for one sign
        links = []
        if self.variants is True:
            link_compare = 'link'
            prev = 'link'
            for j in range(1, 3):
                if link_compare is not None:
                    link_compare = self.get_variants(soup, j, word, link, prev, lang)
                    if self.only_link is False:
                        self.save_video(link_compare, word, lang, var=j)
                    prev = link_compare
                    links.append(link_compare)
            return links

        if self.only_link is False:
            self.save_video(link, word, lang)
        return link

    def save_video(self, link, word, lang, var=0):
        file_name = 'video_' + word + '_' + lang + str(var) + '.mp4'
        r = requests.get(link, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    def get_variants(self, soup, var, word, prev_link, prevprev_link, lang):
        res = re.search('id=\"result-(.*)\"', str(soup))
        num = res.group(1)
        url_address2 = "http://www.spreadthesign.com/" + lang + "/word/" + num + "/" + word + "/" + str(var) + "/?q="
        r2 = requests.get(url_address2)
        soup2 = BeautifulSoup(r2.content, features="lxml", from_encoding=r2.encoding)
        link2 = soup2.video['src']
        if link2 == prev_link or link2 == prevprev_link:
            return None
        return link2

    def get_multiple_results(self):
        if isinstance(self.subcorpus, list) and isinstance(self.query, list):
            for lang in self.subcorpus:
                for word in self.query:
                    if self.variants is True:
                        links = self.get_page(lang, word)  # list
                        for el in links:
                            yield Target(word, (0,len(el)), None, None, transl=el)
                    else:
                        link = self.get_page(lang, word)  # str
                        yield Target(word, (0, len(link)), None, None, transl=link)

        if isinstance(self.subcorpus, list) and isinstance(self.query, str):
            for lang in self.subcorpus:
                word = self.query
                if self.variants is True:
                    links = self.get_page(lang, word)  # list
                    for el in links:
                        yield Target(word, (0,len(word)), None, None, transl=el)
                else:
                    link = self.get_page(lang, word)  # str
                    yield Target(word, (0, len(word)), None, None, transl=link)

        if isinstance(self.query, list) and isinstance(self.subcorpus, str):
            for word in self.query:
                lang = self.subcorpus
                if self.variants is True:
                    links = self.get_page(lang, word)  # list
                    for el in links:
                        yield Target(word, (0,len(word)), None, None, transl=el)
                else:
                    link = self.get_page(lang, word)  # str
                    yield Target(word, (0, len(word)), None, None, transl=link)

    def get_single_results(self):
        link = self.get_page(self.subcorpus, self.query)
        return Target(self.query, (0, len(self.query)), None, None, transl=link)

    def get_sentences(self):
        if not isinstance(self.query, str):
            raise TypeError("Word should be a string for sentences search")

        if not isinstance(self.subcorpus, str):
            raise TypeError("Target language name should be a string for sentences search")

        if self.query_language != self.subcorpus:
            raise Exception("Language of the query and target language should be the same")

        language = self.query_language
        word = self.query

        address = "http://www.spreadthesign.com/" + language + "/search/?cls=1&q=" + word
        req = requests.get(address)
        further_links = re.findall('/sentence/(.*)\" c', req.text)

        for urll in further_links:
            urll = "http://www.spreadthesign.com/" + language + "/sentence/" + urll
            r = requests.get(urll)
            soup = BeautifulSoup(r.content, features="lxml")
            link = soup.video['src']
            if self.only_link is False:
                self.save_video(link, word, language)
            yield Target(word, (0, len(word)), None, None, transl=link)

    def extract(self):
        if self.sentences is True:
            yield from self.get_sentences()
        if isinstance(self.query, str) and isinstance(self.subcorpus, str):
            yield self.get_single_results()
        else:
            yield from self.get_multiple_results()
