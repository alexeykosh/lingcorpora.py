from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import sys
import argparse
from html import unescape


def get_results(query,start,n,lang,mode,n_left,n_right):
    """
    create a query url and get results for one page
    """
    params = {'q': query,
              'start': start,
              'num': n,
              'index':'FullIndex',
              'outputFormat':'HTML',
              'encoding':'UTF-8',
              'maxLeftLength':n_left,
              'maxRightLength':n_right,
              'orderStyle':'score',
              'dir':lang,
              'scopestr':'' # subcorpus: TO DO
              }
    if mode == 'simple':
        r = get('http://ccl.pku.edu.cn:8080/ccl_corpus/search',params)
    if mode == 'pattern':
        r = get('http://ccl.pku.edu.cn:8080/ccl_corpus/pattern',params)
    return unescape(r.text)


def parse_page(page,first=False):
    """
    find results (and total number of results) in the page code
    """
    soup = BeautifulSoup(page, 'lxml')
    res = soup.find('table',align='center')
    if res:
        res = res.find_all('tr')
    else:
        return [],0
    if first:
        num_res = int(soup.find('td',class_='totalright').find('b').text)
        return res, num_res
    return res

    
def parse_results(results):
    """
    find hit and its left and right contexts
    in the extracted row of table
    """
    for i in range(len(results)):
        results[i] = results[i].select('td[align]')
        results[i] = [x.text.strip() for x in results[i]]
    return results
        

def download_all(query,results_wanted,n_left,n_right,lang,mode):
    """
    get information and hits from first page and iterate until
    all hits are collected or maximum set by user is achieved
    """
    per_page = 50
    all_res = []
    first = get_results(query,0,per_page,lang,mode,n_left,n_right)
    first_res,total_res = parse_page(first,True)
    all_res += parse_results(first_res)
    n_results = min(total_res,results_wanted)
    for i in range(per_page,n_results,per_page):
        page = get_results(query,i,per_page,lang,mode,n_left,n_right)
        all_res += parse_results(parse_page(page))
    return all_res


def write_results(query,results,n_results,kwic,write):
    """
    get results ready for output - pandas DataFrame
    and csv file if needed
    """
    not_allowed = '/\\?%*:|"<>'
    if kwic:
        if not results:
            d = {key:[] for key in ["left","center","right"]}
        else:
            d = {"left": [x[0] for x in results[:n_results]],
                 "center": [x[1] for x in results[:n_results]],
                 "right": [x[2] for x in results[:n_results]]}
        s = pd.DataFrame(d, columns=["left", "center", "right"])
    else:
        not_kwic = [''.join(x) for x in results[:n_results]]
        s = pd.DataFrame({"result":not_kwic}, columns=["result"])
        print(s.head())
    if write:
        query = ''.join([x if x not in not_allowed else 'na' for x in query])
        with open('zho_results_'+query+'.csv','w',encoding='utf-8-sig') as f:
            s.to_csv(f,sep=';')
    return s

    
def main(query,corpus='xiandai',mode='simple',n_results=10,
         n_left=30,n_right=30,write=False,kwic=True):
    """
    main function
    
    Args:
        query: a query to search by
        corpus: 'xiandai' (modern Chinese) or 'dugai' (ancient Chinese)
        mode: 'simple' or 'pattern'
              (they differ in syntax, read instructions in the corpus)
        n_results: desired number of results (10 by default)
        n_left: length of left context (in chars, max=40)
        n_right: length of right context (in chars,max=40)
        write: whether to write into csv file or not
        kwic: whether to write into file in kwic format or not

    Return:
        pandas DataFrame and csv file is written if specified
    """
    if not query:
        return 'Empty query'
    results = download_all(query,n_results,n_left,n_right,corpus,mode)
    res_df = write_results(query,results,n_results,kwic,write)
    return res_df

if __name__ == '__main__':
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str)
    parser.add_argument('corpus', type=str)
    parser.add_argument('mode', type=str)
    parser.add_argument('n_results', type=int)
    parser.add_argument('n_left', type=int)
    parser.add_argument('n_right', type=int)
    parser.add_argument('write', type=int)
    parser.add_argument('kwic', type=int)
    args = parser.parse_args(args)
    main(query, corpus, mode, n_results, n_left, n_right, write, kwic)
    