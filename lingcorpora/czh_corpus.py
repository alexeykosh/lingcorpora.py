from requests import get, post


def get_results():
    parametres = {'shuffle': '1',
                  'reload': '',
                  'corpname': 'omezeni%2Fsyn2015',
                  'queryselector': 'iqueryrow',
                  'iquery': 'pozor',
                  'lemma': '',
                  'lpos': '',
                  'phrase': '',
                  'word': '',
                  'wpos': '',
                  'char': '',
                  'cql': '',
                  'default_attr': 'word',
                  'fc_lemword_window_type': 'left',
                  'fc_lemword_wsize': '1',
                  'fc_lemword': '',
                  'fc_lemword_type': 'all',
                  'fc_pos_window_type': 'left',
                  'fc_pos_wsize': '1',
                  'fc_pos_type': 'all',
                  'sca_doc.title': '',
                  'sca_doc.author': '',
                  'sca_doc.translator': ''}
    user_agent ={'Host': 'kontext.korpus.cz',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:51.0) Gecko/20100101 Firefox/51.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate, br',
               'Referer': 'https://kontext.korpus.cz/first_form',
               'Cookie': 'kontextsid=039f6dd8ea91c436130493c03f4591444bd06e57',
               'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1'}
    r = get(url='https://kontext.korpus.cz', data=parametres)
    print(r.url)


def main():
    get_results()

if __name__ == '__main__':
    main()

