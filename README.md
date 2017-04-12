# Lingcorpora
[![Build Status](https://travis-ci.org/alexeykosh/lingcorpora.py.svg?branch=master)](https://travis-ci.org/alexeykosh/lingcorpora.py) [![Build status](https://ci.appveyor.com/api/projects/status/a9yljmk5g6fkgj33?svg=true)](https://ci.appveyor.com/project/alexeykosh/lingcorpora-py) [![PyPI version](https://badge.fury.io/py/lingcorpora.svg)](https://badge.fury.io/py/lingcorpora)

This package includes API for 
* [National Corpus of Russian Language](http://www.ruscorpora.ru)
* [National Corpus of Polish](http://nkjp.pl)
* [Das Wortauskunftssystem zur deutschen Sprache in Geschichte und Gegenwart](https://www.dwds.de/r)

R version of this package by George Moroz is located [here](https://github.com/agricolamz/lingcorpora.R)

## Instalation

If you want to install our package, please tap the following command in Terminal:

```bash
pip install lingcorpora
```

Or:

```bash
sudo pip install lingcorpora
```

If you had Python 3 and Python 2, tap:

```bash
pip3 install lingcorpora
```

Or (for Linux users):

```bash
sudo pip3 install lingcorpora
```


For import it in your project, tap:

```python
import lingcorpora
```

## Usage
All these functions are using the following arguments:
* query – the actual query (wordform, or regular expression, if corpus supports it)
* corpus - the subcorpus where you want to search (it differs from corpora to corpora)
* tag - ```True``` or ```False ``` by default it is ```False```, when it is ```True```, it shows you morphological tags
* n_results - the actual quantity of the results (by default it is 10)
* kwic - ```True``` or ```False ```, shows in kwic format (by default it is ```True```)
* write - ```True``` or ```False ```, writes results to an csv file (by default it is ```False```)

###### rus_search function
```python
>>> print(lingcorpora.rus_search('дядя'))
                                                left  center  \
0                                Ой какие нехорошие    дяди    
1                    Её работа (Елена Андреевна) в "   Дяде    
2                                      Когда войдёт    дядя    
3                       и К. Раппопорт в спектакле "   Дядя    
4                   Во-первых, нет уверенности, что    дядя    
5           Коляем Коляичем с пистолетом.  (Смотри "   Дядю    
6            из ваших близких, например двоюродного    дяди    
7          земским врачам.  "Надо быть милосердным,    дядя    
8                                        Мои отец и    дядя    
9  волновавшейся о неизвестном местонахождении св...   дяди    

                                          right  
0                   позвали их на баррикады.     
1             Ване" Льва Додина, без сомнения    
2                    Ваня с осенними розами и    
3                    Ваня" ― К. Раппопорт и С    
4             Вася, съевший собаку на ремонте    
5            Ваню")  . Автор уверяет, что его    
6                , до 40 лет был тромбофлебит    
7         …"   Дача― деревянная, но крепкая.     
8  , правда, всегда говорили, что обязательно    
9      ", пришлась к новогоднему столу ложкой    

```

###### pol_search function

```python
>>> print(lingcorpora.pol_search('tata'))
                                left  center  \
0      pieczołowicie, jak kiedyś mój   tata    
1              ojcem ani wymówek, że   tata    
2        że ten dzidziuś to wykapany   tata    
3                    za sobą. - Czyj   tata    
4                m mężczyznę. Był to   tata    
5   tracić takich pieniędzy. Nianiek   tata    
6                   .. - zdziwił się   tata    
7                dziadków na wieś, a   tata    
8                    . - Kto to jest   tata    
9                            - No...   tata    

                                 right  
0    . Noemi przyrządziła pyszny obiad  
1                  jest zbyt surowy, a  
2                    ! - usłyszałam za  
3                ? - nie zrozumiał mąż  
4         Rafałka. Siedział na urlopie  
5        Rafałka nie uznawał. Wiedział  
6         Rafałka. Dwie mamy spojrzały  
7   Rafałka zabrał rodzinę do stadniny  
8        Rafałka? - zainteresowała się  
9                     Rafałka. - Aha -  
```

```python
>>> print(lingcorpora.pl_search('powstanie' , tag=True, n_results=15))
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

###### deu_search function

```python
>>> print(lingcorpora.deu_search(query='Muther'))
                                                left  center  \
0       Da meint er schon etwas Großes zu thun, w...  Muther
1                        Dann wird der Mann, der      Muther
2       Und schon sehe ich den Besten, der seit l...  Muther
3       Wer von den Lesern, die neulich den Schar...  Muther
4       Vor wenigen Tagen hat nun auch der Kunstw...  Muther
5       - Von der unter dem Titel Die Kunst " im ...  Muther
6       Manet und sein Kreis wird von Julius Meye...  Muther
7       Sie ist schwer gekränkt und klagt, man en...  Muther
8       Zur Frühstückstafel beim Kaiser waren gel...  Muther
9       Ferner führte er die Verteidigung in zahl...  Muther

                                               right
0       - in dessen in jungen Jahren geschaffenem...
1       als Plagiator missachtet, zum - Plagiator...
2                   , sich hier acclimatisieren.
3       aus den Bildern eines jungen Herrn Schles...
4                           , Ruskin »gefeiert«.
5       herausgegebenen Sammlung illustrirter Mon...
6       zum Gegenstande einer geistvollen Untersu...
7      , die Künstlergenossenschaft schlecht beha...
8       , Hauptleute Lannert , Nachtigall u. Majo...
9       . Weitere viel besprochene Prozesse betra...

