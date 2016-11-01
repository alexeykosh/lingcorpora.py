import urllib.request
import re



def create_request():
    word = input("Введите ваше слово: ")
    request = urllib.request.quote(word.encode('windows-1251'))
    return request


def search_data(x):
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=&spp=&spd=&text=lexform&mode=paper&sort=gr_tagging&lang=ru&req=%s' %x
    print(url)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('windows-1251')
    download_smth = re.findall(r'<a href="(\/download-excel.*?)\" onclick.*?', html)
    url_dwnld = (download_smth[0])


def main():
    search_data(create_request())

if __name__ == "__main__":
    main()




#http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=&spp=&spd=&text=lexform&mode=paper&sort=gr_tagging&lang=ru&req=%(здесь типа запрос)