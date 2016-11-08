import urllib.request
from bs4 import BeautifulSoup
import re


def inputs():
    needs = []
    corpora = input("корпус: ")
    needs.append(corpora)
    word = input("слово: ")
    request = urllib.request.quote(word.encode('windows-1251'))
    needs.append(request)
    case = input("грамм признаки: ")  # типа через запятую %2
    case = case.replace(",", "%2C")
    needs.append(case)
    return needs


def create_request(needs):
    corpora = needs[0]
    request = needs[1]
    case = needs[2]
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&spd=&text=lexgramm&mode=%s&sort=gr_tagging&lang=ru&nodia=1&parent1=0&level1=0&lex1=%s&gramm1=%s&sem1=&sem-mod1=sem&sem-mod1=sem2&flags1=&m1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&sem2=&sem-mod2=sem&sem-mod2=sem2&flags2=&m2=&out=%s'
    common_url = url % (corpora, request, case, 'kwic') #&p= что-то там
    print(common_url)
    return common_url


def get_page_numbers(common_url):
    common_url=common_url.replace('=kwic','')
    where_to_find = urllib.request.urlopen(common_url)
    text = where_to_find.read().decode('windows-1251')
    q_regex = r'<span class="stat-number">(.*)<\/span>.*документов'
    num_of_pages = re.findall(q_regex, text)[1]
    num_of_pages = num_of_pages.replace(' ', '')
    if num_of_pages == 0:
        num_of_pages = 1
    print(num_of_pages)


def get_all_pages(common_url):
    k = 1
    massive_of_links = []
    while k < 10:
        page = common_url + '&p=' + str(k)
        massive_of_links.append(page)
        k += 1
    return massive_of_links


def get_table(urls):
    html_file = open("table.html", "w")
    for url in urls:
        soup_url = urllib.request.urlopen(url)
        soup = BeautifulSoup(soup_url, 'lxml')
        res = soup.findAll("table")[1]
        res = str(res)
        html_file.write(res)
    html_file.close()


def main():
    common_ur = create_request(inputs())
    get_page_numbers(common_ur)
    get_table(get_all_pages(common_ur))


if __name__ == "__main__":
    main()

    #page = requests.get(url)
    #tree = html.fromstring(page.content)
    #left_part = tree.xpath('/table/tr/td[1]|/table/tr/td[3]')
    #print(left_part)


#http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=&spp=&spd=&text=lexform&mode=paper&sort=gr_tagging&lang=ru&req=%(здесь типа запрос)