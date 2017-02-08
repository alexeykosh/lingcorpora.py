from requests import post, get
from bs4 import BeautifulSoup
import pandas as pd
import sys
import argparse


def not_kwic(x):
    return x[0] + x[1] + x[2]


def get_results(query, corpus, n_results, tag):
    if tag is True:
        tag_variable = 'slt'
    else:
        tag_variable = 's'
    settings_params = {'show_in_match': tag_variable,
                       'show_in_context': tag_variable,
                       'left_context_width': '5',
                       'right_context_width': '5',
                       'wide_context_width': '50',
                       'results_per_page': n_results,
                       'next': '/poliqarp/' + corpus + '/query/'}
    s = post(url='http://nkjp.pl/poliqarp/settings/', data=settings_params)
    user_agent = {'Host': 'nkjp.pl',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:51.0) Gecko/20100101 Firefox/51.0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                  'Accept-Encoding': 'gzip, deflate',
                  'Referer': 'http://nkjp.pl/poliqarp',
                  'Cookie': 'sessionid=' + str(s.cookies.get('sessionid')),
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1'}
    post(url='http://nkjp.pl/poliqarp/query/', headers=user_agent, data={'query': query, 'corpus': 'nkjp300'})
    r = get(url='http://nkjp.pl/poliqarp/nkjp300/query/', headers=user_agent)
    return r


def kwic_results(page, write, kwic):
    left_list = []
    right_list = []
    center_list = []
    soup = BeautifulSoup(page.text, 'lxml')
    for left in soup.select('.left'):
        left_list.append(left.text)
    for center in soup.select('span > a'):
        center_list.append(center.text)
    for right in soup.select('.right'):
        right_list.append(right.text)
    left_list = [s.strip('\n') for s in left_list]
    center_list = [s.strip('\n') for s in center_list]
    right_list = [s.strip('\n') for s in right_list][1::2]
    d = {"center": center_list, "left": left_list, "right": right_list}
    s = pd.DataFrame(d, columns=["left", "center", "right"])
    if kwic is False:
        s = s.apply(not_kwic, axis=1)
    else:
        pass
    if write is True:
        file = open('table.csv', 'w')
        s.to_csv(file, encoding='utf-8')
        file.close()
    else:
        pass
    if s.empty:
        print('Something went wrong: please try again!')
    else:
        return s


def main(query, corpus='nkjp300', n_results=10, write=False, kwic=True, tag=False):
    page = get_results(query, corpus, n_results, tag)
    results = kwic_results(page, write, kwic)
    return results


if __name__ == '__main__':
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()  # ru_corpora(corpora = 'main')
    parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('n_results', type=int)
    parser.add_argument('write', type=int)
    parser.add_argument('kwic', type=int)
    parser.add_argument('tag', type=int)
    args = parser.parse_args(args)
    main(corpus, query, n_results, write, kwic, tag)


