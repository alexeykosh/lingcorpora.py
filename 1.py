import urllib.request
from bs4 import BeautifulSoup


def create_request():
    word = input("слово: ")
    request = urllib.request.quote(word.encode('windows-1251'))
    corpora = input("корпус: ")
    case = input("грамм признаки: ") #типа через запятую %2
    case = case.replace(",", "%2C")
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&spd=&text=lexgramm&mode=%s&sort=gr_tagging&lang=ru&nodia=1&parent1=0&level1=0&lex1=%s&gramm1=%s&sem1=&sem-mod1=sem&sem-mod1=sem2&flags1=&m1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&sem2=&sem-mod2=sem&sem-mod2=sem2&flags2=&m2=&out=%s'
    common_url = url % (corpora, request, case, 'kwic')
    return common_url


def get_table(url):
    url = urllib.request.urlopen(url)
    soup = BeautifulSoup(url, 'lxml')
    res = soup.findAll("table")[1]
    res = str(res)
    Html_file = open("table.html", "a")
    Html_file.write(res)
    Html_file.close()


def main():
    get_table(create_request())

if __name__ == "__main__":
    main()

    #page = requests.get(url)
    #tree = html.fromstring(page.content)
    #left_part = tree.xpath('/table/tr/td[1]|/table/tr/td[3]')
    #print(left_part)


#http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=&spp=&spd=&text=lexform&mode=paper&sort=gr_tagging&lang=ru&req=%(здесь типа запрос)