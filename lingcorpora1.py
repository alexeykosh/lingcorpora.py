import urllib.request, re, argparse, sys, os
from bs4 import BeautifulSoup


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
    while k < 10:
        page = common_url + '&p=' + str(k)
        massive_of_links.append(page)
        k += 1
    return massive_of_links


def get_table(urls):  # тут вытаскиваем таблицу (сделал до 10 страниц чтобы не нагружать корпус)
    n = 1
    if os.path.exists("table.html"): #тут как-то научится вытаскивать количество файлов из названия
        html_file = open("table" + str(n) + ".html", "w")  # если множественные запросы чтобы создавал несколько фыайлов пока хз как сделать
        n += 1
    else:
        html_file = open("table.html", "w")
    for url in urls:
        soup_url = urllib.request.urlopen(url)
        soup = BeautifulSoup(soup_url, 'lxml')
        res = soup.findAll("table")[1]
        res = str(res)
        html_file.write(res)
    html_file.close()


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('corpora', type=str)
    parser.add_argument('word', type=str)
    parser.add_argument('case', type=str)
    args = parser.parse_args(args)
    needs = [args.corpora]
    request = urllib.request.quote(args.word.encode('windows-1251'))
    needs.append(request)
    case = args.case.replace(",", "%2C")
    needs.append(case)
    common_ur = create_request(needs)
    get_page_numbers(common_ur)
    get_table(get_all_pages(common_ur))


if __name__ == "__main__":
    main(sys.argv[1:])



