import urllib.request, re, argparse, sys, os, csv
from bs4 import BeautifulSoup
import pandas as pd


def f(x):
    return x[0] + x[1] + x[2]

def create_request(needs): # создаем ссылку поиска
    corpora = needs[0]
    request = needs[1]
    case = needs[2]
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&spd=&text=lexgramm&mode=%s&sort=gr_tagging&lang=ru&nodia=1&parent1=0&level1=0&lex1=%s&gramm1=%s&sem1=&sem-mod1=sem&sem-mod1=sem2&flags1=&m1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&sem2=&sem-mod2=sem&sem-mod2=sem2&flags2=&m2=&out=%s'
    common_url = url % (corpora, request, case, 'kwic')  # &p= что-то там
    return common_url


def get_page_numbers(common_url):  # тут я получаю количество страниц
    common_url=common_url.replace('=kwic','')
    where_to_find = urllib.request.urlopen(common_url)
    text = where_to_find.read().decode('windows-1251')
    q_regex = r'Найдено <span class="stat-number">(\d+ \d+|\d+[ ]?[\d+]?)'
    num_of_pages = re.findall(q_regex, text)
    num_of_pages = str(num_of_pages)
    num_of_pages = num_of_pages.replace(' ', '')
    num_of_pages = num_of_pages.replace('\'', '')
    num_of_pages = num_of_pages.replace('[', '')
    num_of_pages = num_of_pages.replace(']', '')
    num_of_pages = int(num_of_pages) // 10 + 1


def get_all_pages(common_url, results): # тут у нас ссылки на все страницы
    pages = results // 10
    k = 0
    massive_of_links = []
    while k < pages:
        page = common_url + '&p=' + str(k)
        massive_of_links.append(page)
        k += 1
    return massive_of_links


def get_table(urls, n_results, write, kwic):  # тут вытаскиваем таблицу (сделал до 10 страниц чтобы не нагружать корпус)
    center_list = []  # если вынести то проблемы видимо с тем что элемент каждый второй подумать как исправить
    right_list = []
    left_list = []
    normal_left_list = []
    for url in urls:
        soup_url = urllib.request.urlopen(url)
        soup = BeautifulSoup(soup_url, 'lxml')
        table = soup.findAll('table')[1]
        for row0 in table.find_all("td", {"align": "left"}):
            for row1 in row0.find_all("span", {"class": "b-wrd-expl g-em"}):
                center = row1.text
                center_list.append(center)
        for row2 in table.find_all("table", {"style": "table-layout:fixed"}):
            for row3 in row2.find_all("div", {"align": "right"}):
                right_part = row3.text
                right_list.append(right_part)
            for row4 in row2.find_all("nobr"):
                left_part = row4.text
                left_list.append(left_part)
        normal_left_list = left_list[1::2]
    normal_left_list = [s[:-9]for s in normal_left_list]
    if n_results == '':
        n_results = int(len(right_list))
    d = {"center": center_list[:n_results], "left": right_list[:n_results], "right": normal_left_list[:n_results]}
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
    request = urllib.request.quote(query.encode('windows-1251')) #  тут надо как-то научится кодировать еще и скобочки и прочее
    needs.append(request)
    case = urllib.request.quote(tag.encode('windows-1251'))
    needs.append(case)
    common_ur = create_request(needs)
    get_page_numbers(common_ur)
    return get_table(get_all_pages(common_ur, n_results), n_results, write, kwic)


if __name__ == "__main__":
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()  # ru_corpora(corpora = 'main')
    parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('tag', type=str)
    parser.add_argument('n_results', type=int)
    parser.add_argument('write', type=bool)
    parser.add_argument('kwic', type=bool)
    args = parser.parse_args(args)
    main(corpus, query, tag, n_results, write, kwic)


