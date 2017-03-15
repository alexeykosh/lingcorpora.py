from requests import post
from bs4 import BeautifulSoup
import pandas as pd
import sys
import argparse


def not_kwic(x):
    return x[0] + x[1] + x[2]


def get_page(query, corpus, n_results):
    params = {'corpus': corpus,
              'date-end':'1999',
              'date-start':'1900',
              'format':'kwic',
              'genre': 'Belletristik',
              'genre': 'Wissenschaft',
              'genre': 'Gebrauchsliteratur',
              'genre': 'Zeitung',
              'limit': n_results,
              'q': query,
              'sort':	'date_asc'}
    s = post('https://www.dwds.de/r', params=params)
    return s


def get_results(page, write, kwic, query, n_results):
    left_list = []
    right_list = []
    center_list = []
    soup = BeautifulSoup(page.text, 'lxml')
    for left in soup.select('.ddc-kwic-ls'):
        left_list.append(left.text)
    for center in soup.select('.ddc-kwic-kw.ddc-hl'):
        center_list.append(center.text)
    for right in soup.select('.ddc-kwic-rs'):
        right_list.append(right.text)
    left_list = [s.strip('\n') for s in left_list]
    center_list = [s.strip('\n') for s in center_list]
    right_list = [s.strip('\n') for s in right_list]
    d = {"center": center_list, "left": left_list, "right": right_list}
    s = pd.DataFrame(d, columns=["left", "center", "right"])
    if kwic is False:
        s = s.apply(not_kwic, axis=1)
    else:
        pass
    if write is True:
        file = open('table' + str(query) + str(n_results) + '.csv', 'w')
        s.to_csv(file, encoding='utf-8')
        file.close()
    else:
        pass
    return s


def main(query, corpus='kern', n_results=10, write=False, kwic=True):
    page = get_page(query, corpus, n_results)
    results = get_results(page, write, kwic, query, n_results)
    return results


if __name__ == '__main__':
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('n_results', type=int)
    parser.add_argument('write', type=int)
    parser.add_argument('kwic', type=int)
    args = parser.parse_args(args)
    main(corpus, query, n_results, write, kwic)