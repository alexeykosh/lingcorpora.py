from requests import post
from bs4 import BeautifulSoup
import pandas as pd
import sys
import argparse


def not_kwic(x):
    return x[0] + x[1] + x[2]


def get_results(query, corpus, n_results):
    user_agent = {'Host': 'nkjp.pl',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:50.0) Gecko/20100101 Firefox/50.0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                  'Accept-Encoding': 'gzip, deflate',
                  'Referer': 'http://nkjp.pl/poliqarp/nkjp300/query/',
                  'Cookie': 'sessionid=6d0dd51c95e77b5b16c6b6057a011555',  # сюда присылать куки из другого запроса
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1'}
    settings_params = {'show_in_match': 'slt',
                       'show_in_context': 's',
                       'left_context_width': '5',
                       'right_context_width': '5',
                       'wide_context_width': '50',
                       'results_per_page': n_results,
                       'next': '/poliqarp/' + corpus + '/query/'}
    post(url='http://nkjp.pl/poliqarp/settings/', headers=user_agent, data=settings_params)
    r = post(url='http://nkjp.pl/poliqarp/query/', headers=user_agent, data={'query': query, 'corpus': 'nkjp300'})
    return r


def kwic_results(page, write, kwic):
    a = 1
    left_list = []
    right_list = []
    center_list = []
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.findAll('table')[0]
    for left in table.select('.left'):
        left_list.append(left.text)
    for center in table.select('span > a'):
        center_list.append(center.text)
    for right in table.select('.right'):
        right_list.append(right.text)
    left_list = [s.strip('\n') for s in left_list]
    center_list = [s.strip('\n') for s in center_list]
    right_list = [s.strip('\n') for s in right_list][1::2]
    d = {"center": center_list, "left": left_list, "right": right_list}
    s = pd.DataFrame(d, columns=["left", "center", "right"])
    if write is True:
        file = open('table.csv', 'w')
        s.to_csv(file, encoding='utf-8')
        file.close()
    else:
        pass
    if kwic is False:
        file = open('table.csv', 'w')
        s = s.apply(not_kwic, axis=1)
        s.to_csv(file, encoding='utf-8')
    else:
        pass
    return s


def main(query, corpus='nkjp300', n_results=10, write=False, kwic=True):
    page = get_results(query, corpus, n_results)
    results = kwic_results(page, write, kwic)
    return results


if __name__ == '__main__':
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()  # ru_corpora(corpora = 'main')
    parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('tag', type=str)
    parser.add_argument('n_results', type=int)
    parser.add_argument('write', type=int)
    parser.add_argument('kwic', type=int)
    args = parser.parse_args(args)
    main(corpus, query, tag, n_results, write, kwic)
