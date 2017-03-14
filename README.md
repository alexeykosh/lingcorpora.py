# Lingcorpora [![Build Status](https://travis-ci.org/alexeykosh/lingcorpora.py.svg?branch=master)](https://travis-ci.org/alexeykosh/lingcorpora.py) [![Build status](https://ci.appveyor.com/api/projects/status/a9yljmk5g6fkgj33?svg=true)](https://ci.appveyor.com/project/alexeykosh/lingcorpora-py)

This package includes API for 
* [National Corpus of Russian Language](http://www.ruscorpora.ru)
* [National Corpus of Polish](http://nkjp.pl)

R version of this package by George Moroz is located [here](https://github.com/agricolamz/lingcorpora.R)

## Instalation

If you want to install our package, please tap the following command in Terminal:

```bash
pip install git+https://github.com/alexeykosh/lingcorpora.py
```

Or:

```bash
sudo pip install git+https://github.com/alexeykosh/lingcorpora.py
```

If you had Python 3 and Python 2, tap:

```bash
pip3 install git+https://github.com/alexeykosh/lingcorpora.py
```

Or (for Linux users):

```bash
sudo pip3 install git+https://github.com/alexeykosh/lingcorpora.py
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

###### Rus_search function
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

###### Pol_search function

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
>>> print(lingcorpora.pl_search('powstanie' , tag=True, n_results=100))
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
