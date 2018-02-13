# Lingcorpora
[![Build Status](https://travis-ci.org/alexeykosh/lingcorpora.py.svg?branch=master)](https://travis-ci.org/alexeykosh/lingcorpora.py) [![Build status](https://ci.appveyor.com/api/projects/status/a9yljmk5g6fkgj33?svg=true)](https://ci.appveyor.com/project/alexeykosh/lingcorpora-py) [![PyPI version](https://badge.fury.io/py/lingcorpora.svg)](https://badge.fury.io/py/lingcorpora)[![codecov](https://codecov.io/gh/alexeykosh/lingcorpora.py/branch/master/graph/badge.svg)](https://codecov.io/gh/alexeykosh/lingcorpora.py) [![DOI](https://zenodo.org/badge/115459241.svg)](https://zenodo.org/badge/latestdoi/115459241)


This package includes API for 
* [National Corpus of Russian Language](http://www.ruscorpora.ru)
* [National Corpus of Polish](http://nkjp.pl)
* [Das Wortauskunftssystem zur deutschen Sprache in Geschichte und Gegenwart](https://www.dwds.de/r)
* [Center of Chinese Linguistics corpus](http://ccl.pku.edu.cn:8080/ccl_corpus/index.jsp)
* [Corpus Bambara de Reference](http://maslinsky.spb.ru/bonito/run.cgi/first_form)
* [Maninka Automatically Parsed corpus](http://maslinsky.spb.ru/emk/run.cgi/first_form)

R version of this package by George Moroz is located [here](https://github.com/agricolamz/lingcorpora.R)

## Installation

If you want to install our package, please type the following command in Terminal:

```bash
pip install lingcorpora
```

Or:

```bash
sudo pip install lingcorpora
```

If you had Python 3 and Python 2, type:

```bash
pip3 install lingcorpora
```

Or (for Linux users):

```bash
sudo pip3 install lingcorpora
```


To import it in your project, type:

```python
import lingcorpora
```

**Note:** this package does not require [Pandas](http://pandas.pydata.org) to be installed. <br>
The output of functions is a list of occurences, which are in turn are also lists. The output can be used as an input to a Pandas DataFrame (see examples below).

## Usage

### rus_search, pol_search, deu_search, bam_search, emk_search
All these functions are using the following arguments:
* query – the actual query (wordform, or regular expression, if corpus supports it)
* corpus - the subcorpus where you want to search (it differs from corpora to corpora)
* tag - ```True``` or ```False ``` by default it is ```False```, when it is ```True```, it shows you morphological tags where they are present
* n_results - the actual quantity of the results (by default it is 10)
* kwic - ```True``` or ```False ```, shows in kwic format (by default it is ```True```)
* write - ```True``` or ```False ```, writes results to an csv file (by default it is ```False```)

### zho_search
This function has the following arguments:

* query - a query to search by (regular expressions are supported, read instructions in the corpus (in Chinese))
* corpus - 'xiandai' (modern Chinese, by default) or 'dugai' (ancient Chinese)
* mode - 'simple' (default) or 'pattern' (they differ in syntax, read instructions in the corpus (in Chinese))
* n_results - desired number of results (10 by default)
* n_left - length of left context (in chars, max = 40, 30 by default)
* n_right - length of right context (in chars, max = 40, 30 by default)
* write - ```True``` or ```False ```, writes results to an csv file (by default it is ```False```)
* kwic - ```True``` or ```False ```, shows in kwic format (by default it is ```True```)


## Output examples
### bam_search
```python
>>> output = lingcorpora.bam_search(query='súngurun', corpus='corbama-net-tonal')
>>> print(output)
[["y' à bìla sunguru dɔ́ dè kàn .", 'súnguru', "nìn tɛ́ fóyì kɛ́ , n' à wúlila à"],
["dén nìn mìnɛ k' à ɲími , k' ò bɛ́na", 'súngurunninw', 'lɔ̀gɔbɛ ò kàna sɔ̀n kà tág
a túlon'], ['kà tága só . kàbini ò dón ,', 'súngurunw', 'tɛ́ sɔ̀n kà bɔ́ ò ká dùgu 
lá kà tága'], ['tága túlon kɛ́ dùgu wɛ́rɛ lá , sísan', 'súngurun', 'dɔw , ò bɛ́ dòn
móbili lá kà tága'], ['díya bɛ́ bán . 172 ) ní fɛ́n wɛ́rɛ má', 'súngurunya', 'sà , 
síjɛtigiya nà à sà . 173 ) tìle'], ['bìlakoroba fàga jóona , à bólo nà dá', 'sún
gurun', 'sín ná . 402 ) « ní Ála má ń sònya'], ['bóloɲɛ fɔ́lɔ tɛ́ mɔ̀gɔɲumandun yé 
. 948 )', 'súngurunba', 'bóloɲɛ fɔ́lɔ tɛ́ mɔ̀gɔɲumandun yé . 949'], ["mùsokɔrɔnin y
é wɔ̀lɔgɛn ná , ò y' à sɔ̀rɔ à", 'súngurunma', 'dè yé dɔ́ mìnɛ . 959 ) ò yé sìrakwà
ma'], ['à ɲɛ́dɔn dè ? 1017 ) kámalenba dè bɛ́', 'súngurunba', 'sìyɔrɔ dɔ́n . 1018 )
kànu bɛ́ npògotigi'], ["2792 ) mɔ̀gɔ t' à fɔ́ wáliden mà « í", 'súngurunba', "! » ,
í tá bɛ́ í bólo , í t' ò lában"]]
>>> import pandas
>>> print(pandas.DataFrame(output, columns=['left','center','right']))
                                                left         center  \
0                 y' à bìla sunguru dɔ́ dè kàn .       súnguru   
1          dén nìn mìnɛ k' à ɲími , k' ò bɛ́na  súngurunninw   
2                  kà tága só . kàbini ò dón ,     súngurunw   
3          tága túlon kɛ́ dùgu wɛ́rɛ lá , sísan      súngurun   
4          díya bɛ́ bán . 172 ) ní fɛ́n wɛ́rɛ má    súngurunya   
5        bìlakoroba fàga jóona , à bólo nà dá      súngurun   
6        bóloɲɛ fɔ́lɔ tɛ́ mɔ̀gɔɲumandun yé . 948 )    súngurunba   
7  mùsokɔrɔnin yé wɔ̀lɔgɛn ná , ò y' à sɔ̀rɔ à    súngurunma   
8          à ɲɛ́dɔn dè ? 1017 ) kámalenba dè bɛ́    súngurunba   
9           2792 ) mɔ̀gɔ t' à fɔ́ wáliden mà « í    súngurunba   

                                          right  
0        nìn tɛ́ fóyì kɛ́ , n' à wúlila à  
1        lɔ̀gɔbɛ ò kàna sɔ̀n kà tága túlon  
2   tɛ́ sɔ̀n kà bɔ́ ò ká dùgu lá kà tága  
3       dɔw , ò bɛ́ dòn móbili lá kà tága  
4    sà , síjɛtigiya nà à sà . 173 ) tìle  
5     sín ná . 402 ) « ní Ála má ń sònya  
6     bóloɲɛ fɔ́lɔ tɛ́ mɔ̀gɔɲumandun yé . 949  
7  dè yé dɔ́ mìnɛ . 959 ) ò yé sìrakwàma  
8    sìyɔrɔ dɔ́n . 1018 ) kànu bɛ́ npògotigi  
9   ! » , í tá bɛ́ í bólo , í t' ò lában 
```

### pol_search (with tags)

```python
>>> import pandas
>>> output = lingcorpora.pl_search('powstanie' , tag=True, n_results=15))
>>> print(pandas.DataFrame(output, columns=['left','center','right']))
                                                left       center  \
0   . [.:interp] Aż [aż:qub] na [na:prep:acc] siłę...   powstanie    
1    czy [czy:qub] taki [taki:adj:sg:nom:m3:pos] k...   powstanie    
2    dwudziestu [dwadzieścia:num:pl:gen:m3:congr] ...   powstanie    
3    koło [koło:prep:gen] Suchowoli [Suchowoli:ign...   powstanie    
4    po [po:prep:loc] kilku [kilka:num:pl:gen:m3:c...   powstanie    
5    i [i:conj] opadało [opadać:praet:sg:n:imperf]...   powstanie    
6    tego [ten:adj:sg:gen:m3:pos], [,:interp] co [...   powstanie    
7    humanitarnie [humanitarnie:adv:pos] niesłycha...   powstanie    
8    uran [uran:subst:sg:nom:m3] i [i:conj] wielki...   powstanie    
9    popiołów [popiół:subst:pl:gen:m3] Bytu [byt:s...   powstanie    
10   co [co:subst:sg:acc:n] pan [pan:subst:sg:nom:...   powstanie    
11   ta [ten:adj:sg:nom:f:pos] dziura [dziura:subs...   powstanie    
12   istnienia [istnieć:ger:sg:gen:n:imperf:aff] m...   powstanie    
13   koledzy [kolega:subst:pl:nom:m1] chcą [chcieć...   powstanie    
14   szmaragdowo [szmaragdowy:adja]- [-:interp]błę...   powstanie    

                                                right  
0    i [i:conj] gniew [gniew:subst:sg:nom:m3] stra...  
1   , [,:interp] zadecydujemy [zadecydować:fin:pl:...  
2    i [i:conj] własną [własny:adj:sg:acc:f:pos] j...  
3    car [car:subst:sg:nom:m1] majątek [majątek:su...  
4    nowy [nowy:adj:sg:nom:m3:pos] mit [mit:subst:...  
5   . [.:interp] Potem [potem:adv] coraz [coraz:ad...  
6   . [.:interp] Pieniądze [pieniądz:subst:pl:nom:...  
7    ( [(:interp]wot [wot:ign], [,:interp] kak [ka...  
8   ! [!:interp] Ja [ja:ppron12:sg:nom:m1:pri] aut...  
9   ! [!:interp] Cudowny [cudowny:adj:sg:nom:m3:po...  
10   to [to:pred] trochę [trochę:adv]. [.:interp]....  
11  ? [?:interp] – [–:interp] Tak [tak:adv:pos]. [...  
12  . [.:interp]. [.:interp]. [.:interp] Zobacz [z...  
13  ? [?:interp] Albo [albo:conj] za [za:prep:acc]...  
14   na [na:prep:acc] deskach [deska:subst:pl:loc:...  
```
