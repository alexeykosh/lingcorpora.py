# Lingcorpora

This package includes API for 
* [National Corpus of Russian Language](http://www.ruscorpora.ru)
* [National Corpus of Polish](http://nkjp.pl)

## Instalation

If you want to install our package, please tap the following command in Terminal:

```bash
pip install git+https://github.com/alexeykosh/lingcorpora.py
```

For import it in your project, tap:

```python
import lingcorpora
```
R version of this package by George Moroz is located [here](https://github.com/agricolamz/lingcorpora.R)

## Usage


```python
>>> import lingcorpora
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
>>> import lingcorpora
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
