from requests import get, post
from collections import OrderedDict
from bs4 import BeautifulSoup
import re


def get_results():
    parametres = OrderedDict([('shuffle', '1'),
                             ('reload', ''),
                             ('corpname', 'omezeni/syn2015'),
                             ('queryselector', 'iqueryrow'),
                             ('iquery', 'tata'),
                             ('lemma', ''),
                             ('lpos', ''),
                             ('phrase', ''),
                             ('word', ''),
                             ('wpos', ''),
                             ('char', ''),
                             ('cql', ''),
                             ('default_attr', 'word'),
                             ('fc_lemword_window_type', 'left'),
                             ('fc_lemword_wsize', '1'),
                             ('fc_lemword', ''),
                             ('fc_lemword_type', 'all'),
                             ('fc_pos_window_type', 'left'),
                             ('fc_pos_wsize', '1'),
                             ('fc_pos_type', 'all'),
                             ('sca_doc.title', ''),
                             ('sca_doc.author', ''),
                             ('sca_doc.translator', '')])
    user_agent ={'Host': 'kontext.korpus.cz',
                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:51.0) Gecko/20100101 Firefox/51.0',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                 'Accept-Encoding': 'gzip, deflate, br',
                 'Referer': 'https://kontext.korpus.cz/first_form',
                 'Cookie': 'kontextsid=039f6dd8ea91c436130493c03f4591444bd06e57',
                 'Connection': 'keep-alive',
                 'Upgrade-Insecure-Requests': '1'}
    page = get(url='https://kontext.korpus.cz/first', params=parametres, headers=user_agent, allow_redirects=True)
    page1 = get('https://kontext.korpus.cz/view?ctxattrs=word&attr_vmode=visible&pagesize=40&refs=%3Ddoc.title&q=~Vl7hvlEv&viewmode=kwic&attrs=word&corpname=omezeni%2Fsyn2015&structs=p%2Cg%2Cerr%2Ccorr&attr_allpos=kw')
    soup = BeautifulSoup(page1.text, 'lxml')
    print(soup.prettify())


def main():
    get_results()


if __name__ == '__main__':
    main()

