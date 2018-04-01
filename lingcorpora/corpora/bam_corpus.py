from params_container import Container
from requests import get
from bs4 import BeautifulSoup
from html import unescape
from target import Target


__doc__ = \
"""
    
API for Bamana corpus (http://maslinsky.spb.ru/bonito/index.html).
    
Args:
    query: str or List([str]): query or queries (currently only exact search by word or phrase is available)
    numResults: int: number of results wanted (100 by default)
    kwic: boolean: kwic format (True) or a sentence (False) (True by default)
    tag: boolean: whether to collect grammatical tags for target word or not (False by default, available only for corbama-net-non-tonal subcorpus)
    subcorpus: str: subcorpus. Available options: 'corbama-net-non-tonal', 'corbama-net-tonal', 'corbama-brut' ('corbama-net-non-tonal' by default)
    
Main function: extract
Returns:
    A generator of Target objects.

"""



class PageParser(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.subcorpus is None:
            self.subcorpus = 'corbama-net-non-tonal'
        if self.kwic:
            self.__viewmode = 'kwic'
        else:
            self.__viewmode = 'sen'
            
        self.__page = None
        self.__pagenum = 1

        
    def get_results(self):
        params = {
            "corpname": self.subcorpus,
            "iquery": self.query,
            "fromp": self.__pagenum,
            "viewmode": self.__viewmode
        }
        """
        create a query url and get results for one page
        """
        r = get('http://maslinsky.spb.ru/bonito/run.cgi/first',params)
        return unescape(r.text)


    def parse_page(self):
        """
        find results (and total number of results) in the page code
        """
        soup = BeautifulSoup(self.__page, 'lxml')
        if soup.select('div#error'):
            return []
        res = soup.find('table')
        res = res.find_all('tr')
        if self.__pagenum == 1:
            self.numResults = min(int(soup.select('strong[data-num]')[0].text),self.numResults)
        return res

        
    def extract_kws(self,kws):
        final_kws = []
        tags = []
        for kw in kws:
            text_kw = kw.select('span.nott')[0].text.strip()
            tag = kw.select('div.aline')
            tag = [x.text.strip() for x in tag if x.text.strip()]
            if self.tag and self.subcorpus == 'corbama-net-non-tonal':
                tags.append({'lemma': tag[0], 'tag': tag[1], 'gloss': tag[2]})
            final_kws.append(text_kw)
        final_kws = ' '.join(final_kws)
        return final_kws, tags


    def parse_kwic_result(self,result):
        """
        find hit and its left and right contexts
        in the extracted row of table
        """
        lc = ' '.join([x.text.strip() for x in result.select('td.lc span.nott')])
        kws = result.select('td.kw div.token')
        final_kws,tags = self.extract_kws(kws)
        rc = ' '.join([x.text.strip() for x in result.select('td.rc span.nott')])
        
        idx = (len(lc) + 1, len(lc) + 1 + len(final_kws))
        text = lc + ' ' + final_kws + ' ' + rc
        t = Target(text,idx,'',tags)
        return t
 
 
    def parse_sen_result(self,result):
        sentence = result.select('td.par  ')[0]
        text = ''
        if self.subcorpus == 'corbama-net-non-tonal':
            for ch in sentence.children:
                if ch.name is not None:
                    if 'token' in ch['class']:
                        w = ch.select('span.nott')[0].text.strip()
                        text += w + ' '
                    elif ch.name == 'span':
                        kws = ch.select('div.token')
                        final_kws,tags = self.extract_kws(kws)
                        idx = (len(text),len(text)+len(final_kws))
                        text += final_kws + ' '
        else:
            lc = sentence.select('span.nott')[0].string.strip()
            rc = sentence.select('span.nott')[-1].string.strip()
            kws = sentence.select('div.token')
            final_kws,tags = self.extract_kws(kws)
            idx = (len(lc) + 1, len(lc) + 1 + len(final_kws))
            text = lc + ' ' + final_kws + ' ' + rc
        t = Target(text.strip(),idx,'',tags)
        return t
        

    def extract(self):
        n = 0
        while n < self.numResults:
            self.__page = self.get_results()
            rows = self.parse_page()
            if not rows:
                break
            r = 0
            while n < self.numResults and r < len(rows):
                if self.kwic:
                    yield self.parse_kwic_result(rows[r])
                else:
                    yield self.parse_sen_result(rows[r])
                n += 1
                r += 1
            self.__pagenum += 1
