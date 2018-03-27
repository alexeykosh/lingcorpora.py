# Documentation

**The package is under reconstruction. Documentation applies to new release only. For old version, see the main page.**
**The documentation is in development.**

Welcome to `lingcorpora`'s documentation. In order to get started, see [Installation](#installation) and then proceed to [Quickstart](#quickstart). For parameter description, see [Making queries](#making-queries). To obtain description of our `Target` and `Result` objects, go to [Working with results](#working-with-results).

* [Installation](#installation)
* [Quickstart](#quickstart)
* [Making queries](#making-queries)
  * [Corpora](#corpora)
* [Working with results](#working-with-results)

## Installation

To install `lingcorpora`, type in the terminal:
```
pip install lingcorpora
```
lingcorpora has dependencies on:
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* [lxml](http://lxml.de)
* [requests](http://docs.python-requests.org/en/master/)
* [tqdm](https://github.com/tqdm/tqdm)

`lingcorpora` will install these packages during installation. If you have troubles with installing dependencies, check Installation section in the documentation of the according packages.

## Quickstart

To search in any corpus, you need to create an instance of `Query` object and use method `search`:
```python
>>> from lingcorpora import Query
>>> rus_query = Query('rus')
>>> rus_results = rus_query.search('мешок', numResults = 10)
Query "мешок": 100%|##########| 10/10 [00:04<00:00,  2.22docs/s]
>>> rus_results
[Result(query=мешок, N=10, params={'nLeft': None, 'numResults': 10, 'ana': False, 'start': 0, 'query': 'мешок', 'targetLanguage': None, 'mode': None, 'subcorpus': '', 'kwic': True, 'tag': False, 'nRight': None, 'writingSystem': None})]
```

All results are stored in the `Result` object. `Result` is the list of `Target` objects. To print the data, you can use the following code:
```python
>>> for result in rus_results:
        for target in result:
            print(target.text)

		
 [lafet, nick]   «Считают, что если они кому-нибудь отсыпят мешок золота, то можно всех пригласить? 
 [Hamlet, nick]   ещё добрые преподы, которым просто некогда, и которые за мешок с пивом лихо ставили не самые плохие оценки всей группе ^ Но, но, но… 
 ))) И мешо́к для сменки Немо, и рюкза́к, и пена́лы-ру́чки-тетра́дки. 
 Мо́жешь испо́льзовать мешо́к многокра́тно, прости́рывая по́сле ка́ждой ва́рки с мы́лом, но то́лько не в стира́льном порошке́. 
 И э́тот мешо́к ― как ска́терть-самобра́нка; в нём всё прибыва́ет оре́хов. 
 Наверняка пойдёт на дно, как мешо́к с песко́м!" 
  Капита́н-шеф-по́вар побежа́л бы́ло на́ но́с, что́бы увести́ Эле-Фантика Но как раз в э́тот миг налете́л девя́тый вал и, подсте́гиваемый урага́ном, ру́хнул, как девятиэтажный дом, то́чно на слонёнка - ослепи́л, оглуши́л, закрути́л в водоворо́те и снёс за борт, как большо́й мешо́к с песко́м. 
  8. 39. Древнегре́ческий учёный Аристотель для доказа́тельства невесо́мости во́здуха взве́шивал пусто́й ко́жаный мешо́к и тот же мешо́к, напо́лненный во́здухом. 
  8. 39. Древнегре́ческий учёный Аристотель для доказа́тельства невесо́мости во́здуха взве́шивал пусто́й ко́жаный мешо́к и тот же мешо́к, напо́лненный во́здухом. 
  8. 39. Потому́ что вес мешка́ с во́здухом увели́чивался на сто́лько, на ско́лько увели́чивалась выта́лкивающая си́ла, де́йствующая со стороны́ во́здуха на разду́тый мешо́к. 
```


## Making queries

### Corpora

## Working with results
