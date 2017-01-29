import urllib.request
import re
import argparse
import sys
from bs4 import BeautifulSoup
import pandas as pd


def f(x):
    return x[0] + x[1] + x[2]


def create_request(needs):
    corpora = needs[0]
    request = needs[1]
    case = needs[2]
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&spd=&' \
          'text=lexgramm&mode=%s&sort=gr_tagging&lang=ru&nodia=1&parent1=0&level1=0&lex1=%s&gramm1=%s&sem1=&sem-m' \
          'od1=sem&sem-mod1=sem2&flags1=&m1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&sem2=&sem-mod2=sem&se' \
          'm-mod2=sem2&flags2=&m2=&out=%s'
    common_url = url % (corpora, request, case, 'kwic')
    return common_url


def get_all_pages(common_url, results):
    pages = results // 10
    k = 0
    massive_of_links = []
    while k < pages:
        page = common_url + '&p=' + str(k)
        massive_of_links.append(page)
        k += 1
    return massive_of_links


def get_table(urls, n_results, write, kwic):
    center_right_list = []
    gram_list =[]
    center_list = []
    right_list = []
    left_list = []
    for url in urls:
        soup_url = urllib.request.urlopen(url)
        soup = BeautifulSoup(soup_url, 'lxml')
        for center_right in soup.select('tr > td > nobr'):
            center_right_list.append(center_right.text)
        for left in soup.select('tr > td > div > nobr'):
            left_list.append(left.text)
    center_list = center_right_list[0::2]
    right_list = center_right_list[1::2]
    if n_results == '':
        n_results = int(len(right_list))
    d = {"center": center_list[:n_results], "right": right_list[:n_results], "left": left_list[:n_results]}
    s = pd.DataFrame(d, columns=["left", "center", "right"])
    if write is True:
        file = open('ru_table.csv', 'w')
        s.to_csv(file, encoding='utf-8')
        file.close()
    else:
        pass
    if kwic is False:
        file = open('ru_table.csv', 'w')
        s = s.apply(f, axis=1)
        s.to_csv(file, encoding='utf-8')
    else:
        pass
    return s


def main(query, corpus='main', tag='', n_results=10, write=False, kwic=True):
    needs = [corpus]
    request = urllib.request.quote(query.encode('windows-1251'))
    needs.append(request)
    case = urllib.request.quote(tag.encode('windows-1251'))
    needs.append(case)
    common_ur = create_request(needs)
    return get_table(get_all_pages(common_ur, n_results), n_results, write, kwic)


if __name__ == "__main__":
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('tag', type=str)
    parser.add_argument('n_results', type=int)
    parser.add_argument('write', type=bool)
    parser.add_argument('kwic', type=bool)
    args = parser.parse_args(args)
    main(corpus, query, tag, n_results, write, kwic)


