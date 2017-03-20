import requests
from bs4 import BeautifulSoup


def get_words():
    list_words = []
    s = requests.get(url = 'https://en.wikibooks.org/wiki/Polish/List_of_words')
    soup = BeautifulSoup(s.text, 'lxml')
    for word in soup.select('ul > li > b'):
        list_words.append(word.text)
    print(list_words)


def main():
    get_words()

if __name__ == '__main__':
    main()