import urllib.request, re, argparse, sys, os, csv
from bs4 import BeautifulSoup
import pandas as pd


def create_request(needs): # создаем ссылку поиска
    corpora = needs[0]
    request = needs[1]
    case = needs[2]
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&spd=&text=lexgramm&mode=%s&sort=gr_tagging&lang=ru&nodia=1&parent1=0&level1=0&lex1=%s&gramm1=%s&sem1=&sem-mod1=sem&sem-mod1=sem2&flags1=&m1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&sem2=&sem-mod2=sem&sem-mod2=sem2&flags2=&m2=&out=%s'
    common_url = url % (corpora, request, case, 'kwic') #&p= что-то там
    print("url", common_url)
    return common_url


def get_page_numbers(common_url): # тут я получаю количество страниц
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
    print("pages", num_of_pages)


def get_all_pages(common_url): # тут у нас ссылки на все страницы
    k = 0
    massive_of_links = []
    while k < 1:
        page = common_url + '&p=' + str(k)
        massive_of_links.append(page)
        k += 1
    return massive_of_links


def get_table(urls):  # тут вытаскиваем таблицу (сделал до 10 страниц чтобы не нагружать корпус)
    html_file = open("table.html", "w")
    for url in urls:
        right_part = []
        center =[]
        soup_url = urllib.request.urlopen(url)
        soup = BeautifulSoup(soup_url, 'lxml')
        table = soup.findAll('table')[1]
        center_list = []
        right_list = []
        left_list = []
        for row2 in table.find_all("span", {"class": "b-wrd-expl g-em"}):
            center = row2.text
            center_list.append(center)
        for row in table.find_all("table", {"style": "table-layout:fixed"}):
            for row1 in row.find_all("div", {"align": "right"}):
                right_part = row1.text
                right_list.append(right_part)
            for row3 in row.find_all("nobr"):
                left_part = row3.text
                left_list.append(left_part)
        left_list = left_list[1::2] #убрать закорючки
        normal_left_list = [s[:-9]for s in left_list]
        d = {"center" : center_list, "left" : right_list, "right" : normal_left_list}
        s = pd.DataFrame(d, columns=["left", "center", "right"])
        print(s)
# columns=['left', 'center'])

def main(corpus, query, tag):
    needs = [corpus]
    request = urllib.request.quote(query.encode('windows-1251'))
    needs.append(request)
    case = tag.replace(",", "%2C")
    needs.append(case)
    common_ur = create_request(needs)
    get_page_numbers(common_ur)
    get_table(get_all_pages(common_ur))


if __name__ == "__main__":
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()  # ru_corpora(corpora = 'main')
    parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('tag', type=str)
    args = parser.parse_args(args)
    main(corpus, query, tag)



