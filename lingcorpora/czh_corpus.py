from requests import get
from bs4 import BeautifulSoup


def get_results():
    params = {'char': '',
              'corpname': 'omezeni/syn2015',
              'cql': '',
              'default_attr': 'word',
              'fc_lemword': '',
              'fc_lemword_type': 'all',
              'fc_lemword_window_type': 'left',
              'fc_lemword_wsize': '1',
              'fc_pos_type': 'all',
              'fc_pos_window_type': 'left',
              'fc_pos_wsize': '1',
              'iquery': 'stat',
              'lemma': '',
              'lpos': '',
              'phrase': '',
              'queryselector': 'iqueryrow',
              'reload': '',
              'sca_doc.author': '',
              'sca_doc.title': '',
              'sca_doc.translator': '',
              'shuffle': '1',
              'word': '',
              'wpos': ''}
#    user_agent = {'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                  'Accept-Encoding': 'gzip, deflate, br',
#                  'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#                  'Connection': 'keep-alive',
#                  'Cookie': 'kontextsid=09d6b61955f36432b6a48c4fb988edf6e60f26bc',
#                  'Host': 'kontext.korpus.cz',
#                  'Referer': 'https://kontext.korpus.cz/first_form',
#                  'Upgrade-Insecure-Request': '1',
#                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:51.0) Gecko/20100101 Firefox/51.0'}
    post1 = get(url='https://kontext.korpus.cz/' ,data=params)
    print(post1.text)


def main():
    get_results()

if __name__ == '__main__':
    main()

