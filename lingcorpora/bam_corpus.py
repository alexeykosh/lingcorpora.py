from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import sys
import argparse
from html import unescape


def get_results(query,corpus,page):
    """
    create a query url and get results for one page
    """
    params = {
        "corpname": corpus,
        "iquery": query,
        "fromp": page
    }
    r = get('http://maslinsky.spb.ru/bonito/run.cgi/first',params)
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


def parse_results(results,tags):
    """
    find hit and its left and right contexts
    in the extracted row of table
    """
    parsed_results = []
    for i in range(len(results)):
        lc = results[i].select('td.lc span.nott')[0].text.strip()
        kws = results[i].select('td.kw div.token')
        final_kws = []
        for kw in kws:
            tag = kw.select('div.aline')
            tag = '; '.join([x.text.strip() for x in tag if x.text.strip()])
            if tags:
                text_kw = kw.select('span.nott')[0].text.strip() +' ('+tag+')'
            else:
                text_kw = kw.select('span.nott')[0].text.strip()
            final_kws.append(text_kw)
        rc = results[i].select('td.rc span.nott')[0].text.strip()
        parsed_results.append([lc,' '.join(final_kws),rc])
    return parsed_results


def download_all(query,num_res,corpus,tags):
    """
    get information and hits from first page and iterate until
    all hits are collected or maximum set by user is achieved
    """
    per_page = 20
    try:
        first,total = parse_page(get_results(query,corpus,1),first=True)
    except:
        return None
    results = parse_results(first,tags)
    final_total = min(total,num_res)
    pages_to_get = len(list(range(per_page+1,final_total+1,per_page)))
    for i in range(pages_to_get):
        one_page = parse_page(get_results(query,corpus,i))
        one_res = parse_results(one_page,tags)
        results += one_res
    if len(results) > final_total:
        results = results[:final_total]
    return results


def write_results(query,results,kwic,write):
    """
    get results ready for output - pandas DataFrame
    and csv file if needed
    """
    if kwic:
        res_table = pd.DataFrame(results,columns=['left','center','right'])
    else:
        results = [[' '.join(x)] for x in results]
        res_table = pd.DataFrame(results,columns=['results'])
    if write:
        with open('bam_results_'+query+'.csv','w',encoding='utf-8-sig') as f:
            res_table.to_csv(f,sep=';')
    return res_table


def main(query,corpus='corbama-net-non-tonal',tag=False,
         n_results=10,kwic=True,write=False):
    """
    main function
    
    Args:
        query: a query to search by
        corpus: a subcorpus ('corbama-net-non-tonal' by default)
        tag: whether to provide grammatical information 
        n_results: desired number of results (10 by default)
        kwic: whether to write into file in kwic format or not
        write: whether to write into csv file or not
        
    Return:
        pandas DataFrame and csv file is written if specified
        
    """
    results = download_all(query,n_results,corpus,tag)
    if results is None:
        results = [['','nothing found','']]
    res_df = write_results(query,results,kwic,write)
    return res_df


if __name__ == '__main__':
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str)
    parser.add_argument('corpus', type=str)
    parser.add_argument('tag', type=int)
    parser.add_argument('kwic', type=int)
    parser.add_argument('write', type=int)
    args = parser.parse_args(args)
    main(query, corpus, tag, n_results, kwic, write)
