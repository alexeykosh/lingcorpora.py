from ..params_container import Container
from ..target import Target
from requests import get
from bs4 import BeautifulSoup
import re


__doc__ = \
"""
    
API for Estonian corpus (http://www.cl.ut.ee/korpused/kasutajaliides/index.php).
    
Args:
    query: str or List([str]): query or queries (currently only exact search by word is available)
    numResults: int: number of results wanted (100 by default)
    subcorpus: str: subcorpus. Available options: see below values and their meanings ('1990_ajalehed_26_08_04' by default). To use several subcorpora, list them with semicolon, e.g. '1990_ajalehed_26_08_04;EE_10_09_2004'.
    
Main function: extract
Returns:
    A generator of Target objects.

Available subcorpora:
    1990_ajalehed_26_08_04: 1990d - ajakirjandus [865 tuhat]
    EE_10_09_2004: Eesti Ekspress 1996-2001 [7,2 miljonit]
    Maaleht: Maaleht 2001-2004 [5,3 miljonit]
    Postimees_1995: Postimees 1995
    Postimees_1996: Postimees 1996
    Postimees_1997: Postimees 1997
    Postimees_1998: Postimees 1998
    Postimees_1999: Postimees 1999
    Postimees_2000: Postimees 2000
    Postimees_Extra: Postimees Extra
    epl_1995: Eesti Päevaleht 1995
    epl_1996: Eesti Päevaleht 1996
    epl_1997: Eesti Päevaleht 1997
    epl_1998: Eesti Päevaleht 1998
    epl_1999: Eesti Päevaleht 1999
    epl_2000: Eesti Päevaleht 2000
    epl_2001: Eesti Päevaleht 2001
    epl_2002: Eesti Päevaleht 2002
    epl_2003: Eesti Päevaleht 2003
    epl_2004: Eesti Päevaleht 2004
    epl_2005: Eesti Päevaleht 2005
    epl_2006: Eesti Päevaleht 2006
    epl_2007: Eesti Päevaleht 2007
    sloleht_1997: SLÕhtuleht 1997
    sloleht_1998: SLÕhtuleht 1998
    sloleht_1999: SLÕhtuleht 1999
    sloleht_2000: SLÕhtuleht 2000
    sloleht_2001: SLÕhtuleht 2001
    sloleht_2002: SLÕhtuleht 2002
    sloleht_2003: SLÕhtuleht 2003
    sloleht_2004: SLÕhtuleht 2004
    sloleht_2005: SLÕhtuleht 2005
    sloleht_2006: SLÕhtuleht 2006
    sloleht_2007: SLÕhtuleht 2007
    valga: Ajaleht Valgamaalane [2,5 miljonit]
    le: Ajaleht Lääne Elu [1,8 miljonit]
    Kroonika: Seltskonnaajakiri Kroonika [960 tuhat]
    1980_aja: 1980d - ajakirjandus (baas) [175 tuhat]
    1970_aja: 1970d - ajakirjandus [168 tuhat]
    1960_aja: 1960d - ajakirjandus [201 tuhat]
    1950_aja: 1950d - ajakirjandus [242 tuhat]
    1930_aja: 1930d - ajakirjandus [117 tuhat]
    1910_aja: 1910d - ajakirjandus [182 tuhat]
    1900_aja: 1900d - ajakirjandus [171 tuhat]
    1890_aja: 1890d - ajakirjandus [193 tuhat]
    1990_ilu_26_08_04: 1990d - ilukirjandus (katkendid) [602 tuhat]
    segailu_5_10_2008: 1990d - ilukirjandus [5,6 miljonit]
    1980_ilu: 1980d - ilukirjandus (baas) [250 tuhat]
    1970_ilu: 1970d - ilukirjandus [257 tuhat]
    1960_ilu: 1960d - ilukirjandus [132 tuhat]
    1950_ilu: 1950d - ilukirjandus [66 tuhat]
    1930_ilu: 1930d - ilukirjandus [252 tuhat]
    1910_ilu: 1910d - ilukirjandus [247 tuhat]
    1900_ilu: 1900d - ilukirjandus [64 tuhat]
    1890_ilu: 1890d - ilukirjandus [155 tuhat]
    1980_tea: 1980d - teadustekst [160 tuhat]
    horisont: Ajakiri Horisont 1996-2003 [260 tuhat]
    arvutitehnika: Ajakiri Arvutitehnika ja Andmetöötlus 1999-2005 [625 tuhat]
    doktor: Doktoritööd [2,3 miljonit]
    Eesti_Arst_2002: Ajakiri Eesti Arst 2002 [249 tuhat]
    Eesti_Arst_2003: Ajakiri Eesti Arst 2003 [244 tuhat]
    Eesti_Arst_2004: Ajakiri Eesti Arst 2004 [217 tuhat]
    agraar: Agraarteadus 2001-2006 [298 tuhat]
    jututoad: Jututoad [7 miljonit]
    uudisgrupid: Uudisgrupid [8 miljonit]
    foorumid: Foorumid [5 miljonit]
    kommentaarid: Kommentaarid [2 miljonit]
    riigikogu: Riigikogu stenogrammid 1995 - 2001 [13 miljonit]
    1980_muu: 1980d - muud tekstid [415 tuhat]
    teadusartiklid: Mitmesugused Teadusartiklid 1995-2007 [1,3 miljonit]
    akp: Asutawa Kogu protokollid [2 miljonit]
    
"""

class PageParser(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.__page = None
        self.p = re.compile('[ .-:;,!?]')
        if self.subcorpus is None:
            self.subcorpus = '1990_ajalehed_26_08_04'

    def get_page(self):
        params = {'otsisona': self.query,
                  'subcorp': self.subcorpus.split(';'),
                  'kontekst': '0',
                  'lause_arv':	'0'}
        s = get('http://www.cl.ut.ee/korpused/kasutajaliides/konk.cgi.et', params=params)
        return s


    def find_right_part(self, elem, right_part):
        right_part = right_part + elem.string + elem.next_sibling
        if elem.next_sibling.next_sibling.name != 'br':
            right_part = self.find_right_part(elem.next_sibling.next_sibling, right_part)
        return right_part


    def find_left_part(self, elem, left_part):
        left_part = elem.previous_sibling + elem.string + left_part
        if elem.previous_sibling.previous_sibling.name != 'hr':
            left_part = self.find_left_part(elem.previous_sibling.previous_sibling, left_part)
        return left_part


    def extract(self):
        s = 0
        self.__page = self.get_page()
        soup = BeautifulSoup(self.__page.text, 'lxml')
        strong = soup.select('strong')
        if strong:
            for elem in strong:
                right_part = elem.next_sibling
                left_part = elem.previous_sibling
                center_part = elem.string
                if elem.next_sibling.next_sibling.name != 'br':
                    right_part = self.find_right_part(elem.next_sibling.next_sibling, right_part)
                if elem.previous_sibling.previous_sibling.name != 'hr':
                    left_part = self.find_left_part(elem.previous_sibling.previous_sibling, left_part)
                    
                left_part, center_part, right_part = left_part.split('    ', maxsplit=1)[1].strip(),\
                                                     center_part + right_part[0:self.p.search(right_part).start()].strip(), \
                                                     right_part[self.p.search(right_part).start():].strip()
                idx = (len(left_part) + 1, len(left_part) + 1 + len(center_part))
                text = left_part + ' ' + center_part + ' ' + right_part
                t = Target(text,idx,'',[])
                yield t
                s += 1
                if s == self.numResults:
                    break
