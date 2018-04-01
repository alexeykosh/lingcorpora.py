from params_container import Container
from requests import get
from bs4 import BeautifulSoup
import re
from html import unescape

global results_url
results_url = 'http://web-corpora.net/TatarCorpus/search/results.php'


class PageParser:

    def __init__(self, query, subcorpus, tag, nLeft, nRight, per_page=100):
        self.query = query
        self.tag = tag
        self.subcorpus = subcorpus
        self.page = None
        self.occurrences = None
        self.pagenum = 1
        self.nLeft = nLeft
        self.nRight = nRight
        self.per_page = per_page
        self.__get_sid()

    def __get_sid(self):
        params = {
            "fullsearch": self.query,

            "occurences_per_page": self.per_page,
            "contexts_output_language": "tatar",
            "search_language": "tatar",
            "subcorpus": self.subcorpus,
            "interface_language": "en",
            "sentences_per_enlarged_occurrence": "1",
            "contexts_layout": "basic",
            "show_gram_info": int(self.tag),
            "subcorpus_query": ""
        }
        res = get(results_url, params)
        self.sid = re.search('sid=([0-9]+)', res.text).group(1)

    def get_results(self):
        params = {"sid": self.sid,
                  "page": self.pagenum,
                  "search_language": "tatar"}
        res = get(results_url, params)
        return unescape(res.text)

    def parse_page(self):
        soup = BeautifulSoup(self.page, 'lxml')
        occs = re.search('FOUND(.*?)MATCHES', soup.text)
        self.occurrences = int(occs.group(1).replace(' ', ''))
        contexts = soup.find(id="contexts_div")
        res = list(contexts.find_all('table', recursive=False))
        return res

    def parse_results(self, results):
        parsed_results = []
        for i in range(len(results)):
            context = self.__parse_context(results[i])
            if len(context) != 0:
                parsed_results.append(context)
        return parsed_results

    def __parse_context(self, context):
        res_context = list(context.find_all('tr', recursive=False))[1]
        res_text, word_index = self.__get_text(res_context)
        if word_index is None:
            return []
        left_context = ' '.join(
            res_text[min(0, word_index - self.nLeft):word_index])
        right_context = ' '.join(
            res_text[word_index + 1:word_index + self.nRight + 1])
        word = res_text[word_index]['word']
        if self.tag:
            word += ' ' + res_text[word_index]['tag']
        return [left_context, word, right_context]

    def __get_tag(self, tag_text):
        brkts = '?:(\'(.*?)\',?)+'
        # [lemmas], [PoS], [tags]
        regex = re.search('popup\(this,\[.*?\],\[(.*?)], \[(.*?)\]', tag_text)
        try:
            pos = re.findall("'(.*?)'", regex.group(1))
            tags = re.findall("'(.*?)'", regex.group(2))
        except AttributeError:
            pos = ''
            tags = ''
        tag_lines = ['(%s, %s)' % (i, j) for i, j in zip(pos, tags)]
        tag = ' OR '.join(tag_lines)
        return tag

    def __get_text(self, res_context):
        res_text_tagged = list(res_context.find_all('span'))
        res_text = []
        word_index = None
        for w in res_text_tagged:
            if 'class' in w.attrs and 'result1' in w.attrs['class']:
                word = {}
                word['word'] = w.text
                word['tag'] = self.__get_tag(w.attrs['onmouseover'])
                word_index = len(res_text)
            else:
                word = w.text
            res_text.append(word)
        return res_text, word_index

    def extract_results(self):
        self.page = self.get_results()
        rows = self.parse_page()
        parsed_results = self.parse_results(rows)
        return parsed_results


class Downloader(Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.per_page = 100

        if self.subcorpus is None:
            self.subcorpus = ''

        if self.nLeft is None:
            self.nLeft = 5

        if self.nRight is None:
            self.nRight = 5

    def download_all(self):
        results = []
        self.parser = PageParser(query=self.query, subcorpus=self.subcorpus,
                                 tag=self.tag,
                                 nLeft=self.nLeft, nRight=self.nRight,
                                 per_page=self.per_page)
        while (self.parser.occurrences is None) or
        (len(results) < self.numResults and
                self.parser.occurrences > len(results)):
            self.parser.pagenum = len(results) / self.per_page + 1
            results += self.parser.extract_results()
        return results[:self.numResults]
