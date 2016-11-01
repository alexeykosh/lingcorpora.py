import urllib.request
from lxml import html
import requests


def create_request():
    word = input("Введите ваше слово: ")
    request = urllib.request.quote(word.encode('windows-1251'))
    return request


def search_word(x):
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&spd=&text=lexgramm&mode=main&sort=gr_tagging&lang=ru&nodia=1&parent1=0&level1=0&lex1=%s&gramm1=&sem1=&sem-mod1=sem&sem-mod1=sem2&flags1=&m1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&sem2=&sem-mod2=sem&sem-mod2=sem2&flags2=&m2=&out=kwic' %x
    return url

def final_result (url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    left_part = tree.xpath('/table/tr/td[1]|/table/tr/td[3]')
    print(left_part)



def main():
    search_data(create_request())

if __name__ == "__main__":
    main()




#http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=&spp=&spd=&text=lexform&mode=paper&sort=gr_tagging&lang=ru&req=%(здесь типа запрос)