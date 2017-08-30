from requests import get
from bs4 import BeautifulSoup
import csv
import sys
import unittest
import argparse
from html import unescape
from copy import deepcopy
import os
   
        
def get_results(query,corpus,page):
    """
    create a query url and get results for one page
    """
    params = {
        "corpname": corpus,
        "iquery": query,
        "fromp": page
    }
    r = get('http://maslinsky.spb.ru/emk/run.cgi/first',params)
    return unescape(r.text)


def parse_page(page,first=False):
    """
    find results (and total number of results) in the page code
    """
    soup = BeautifulSoup(page, 'lxml')
    res = soup.find('table')
    res = res.find_all('tr')
    if first:
        num_res = int(soup.select('strong[data-num]')[0].text)
        return res, num_res
    return res


def parse_results(results,query):
    """
    find hit and its left and right contexts
    in the extracted row of table
    """
    parsed_results = []
    for i in range(len(results)):
        lc = ' '.join([x.text.strip()
                            for x in results[i].select('td.lc span.nott')])
        kw = results[i].select('td.kw span.nott')[0].text.strip()
        if kw != query:
            kw = query + ' (' + kw + ')'
        rc = ' '.join([x.text.strip()
                            for x in results[i].select('td.rc span.nott')])
        parsed_results.append([lc,kw,rc]) 
    return parsed_results


def download_all(query,num_res,corpus):
    """
    get information and hits from first page and iterate until
    all hits are collected or maximum set by user is achieved
    """
    per_page = 20
    try:
        first,total = parse_page(get_results(query,corpus,1),first=True)
    except:
        return []
    results = parse_results(first,query)
    final_total = min(total,num_res)
    pages_to_get = len(list(range(per_page+1,final_total+1,per_page)))
    for i in range(pages_to_get):
        one_page = parse_page(get_results(query,corpus,i))
        one_res = parse_results(one_page,query)
        results += one_res
    if len(results) > final_total:
        results = results[:final_total]
    return results


def write_results(query,results,cols):
    """
    write csv
    """
    not_allowed = '/\\?%*:|"<>'
    query = ''.join([x if x not in not_allowed else '_na_' for x in query])
    with open('emk_search_'+query+'.csv','w',encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(cols)
        for i,x in enumerate(results):
            writer.writerow([i]+x)


def main(query,corpus='cormani-brut-lat',tag=False,
         n_results=10,kwic=True,write=False):
    """
    main function
    
    Args:
        query: a query to search by
        corpus: a subcorpus ('cormani-brut-lat' by default)
        tag: whether to provide grammatical information (irrelevant here)
        n_results: desired number of results (10 by default)
        kwic: whether to write into file in kwic format or not
        write: whether to write into csv file or not
        
    Return:
        list of row lists and csv file is written if specified
        
    """
    results = download_all(query,n_results,corpus)
    if not results:
        print ('emk_search: nothing found for "%s"' % (query))
    if kwic:
        cols = ['index','left','center','right']
    else:
        results = [[''.join(x)] for x in results]
        cols = ['index','result']
    if write:
        write_results(query,results,cols)
    return results


class TestMethods(unittest.TestCase):
    def test1(self):
        self.assertTrue(get_results(query='tuma',corpus='cormani-brut-lat',page=1))

    def test2(self):
        self.assertIs(list,type(main(query='ߛߐ߬ߘߐ߲߬',corpus='cormani-brut-nko')))
    
    def test3(self):
        r = main(query='ߛߐ߬ߘߐ߲߬',corpus='cormani-brut-nko',write=True,kwic=False)
        filelist = os.listdir()
        self.assertIn('emk_search_ߛߐ߬ߘߐ߲߬.csv',filelist)
        os.remove('emk_search_ߛߐ߬ߘߐ߲߬.csv')

    

if __name__ == '__main__':
    unittest.main()
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str)
    parser.add_argument('corpus', type=str)
    parser.add_argument('tag', type=bool)
    parser.add_argument('n_results', type=int)
    parser.add_argument('kwic', type=bool)
    parser.add_argument('write', type=bool)
    args = parser.parse_args(args)
    main(**vars(args))
