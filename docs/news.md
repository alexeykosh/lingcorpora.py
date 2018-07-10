# What's new

## Production
* * *

### 01.04.2018
`lingcorpora`, version 1.1

* 5 corpora, including a parallel one
* `Corpus` object for searching, storing results and retrying failed queries
* `Result` object for storing all results and export to `csv`
* `Target` object for managing occurrences

[Documentation](https://lingcorpora.github.io/lingcorpora.py/docs.html)


## Development
* * *

### 8.07.2018
* Russian-polish parallel corpus refactored

### 10.06.2018
* Georgian, Estonian and Danish corpora refactored (Katya Gerasimenko)


### 04.04.2018
* First tests added (Artyom Kopetskiy)

### 01.04.2018
* Bug fixes
* Finalizing docs

### 31.03.2018
* Target and Result adjusted for parallel corpora (Maria Terekhina, Artyom Kopetskiy)
* Query renamed to Corpus (Katya Gerasimenko)
* Preparing package for release (Maria Terekhina)
* Retry function added (Artyom Kopetskiy)
* Docs added to all corpora

### 27.03.2018
* Docs starting to emerge (Katya Gerasimenko)
* Docstring fixed (Artyom Kopetskiy)
* `search` return fixed (Artyom Kopetskiy)

### 25.03.2018
* Parallel Russian corpus added (Maria Terekhina)

### 07.03.2018
* New architecture added (Artyom Kopetskiy)
* Bamana, Maninka and Chinese corpora refactored (Katya Gerasimenko)
  * Target objects
  * Generator
  * More adequate kwic-sentence distinction

### 28.02.2018
* Tatar corpus added (Ustya Kosheleva)

### 26.02.2018
* Improvements to the architecture prototype (Artyom Kopetskiy)
  * fewer wrapper objects (change Query, remove Manager)
  * add objects for results
  * change specific corpora API structure
* Rus_corpus API improvement (Artyom Kopetskiy)
