from requests import post, get
from bs4 import BeautifulSoup
import pandas as pd
import sys
import argparse
import unittest


def get_results():
    params = {'f':	'd',
              'ks': 'ca',
              'met': 'kon',
              'mova':	'en',
              'xxx': 'шагьар',
              'qp': '100'}
    s = post('http://baltoslav.eu/avar/', params=params)
    return s


def get_kwic(url):
    texts = []
    soup = BeautifulSoup(url.text, 'lxml')
    for example in soup.select('.cyry'): # add types of encoding
        texts.append(example.text)
    center_word = soup.select('.cyry > b')
    print(center_word)
    d = {"center": texts}
    s = pd.DataFrame(d, columns=["center"])


def main():
    url = get_results()
    get_kwic(url)


if __name__ == '__main__':
    main()