---
output:
  html_document:
    theme: lumen
    highlight: tango
    toc: yes
    toc_position: right
    toc_float: yes
    smooth_scroll: false
    number_sections: true
---

# What's new

## Production
* * *
Release date (expected): March 2018


## Development
* * *

### 01.04.2018
* Bug fixes
* Finalizing docs

### 31.03.2018
* Target and Result adjusted for parallel corpora (Maria Terekhina, Artyom Kopetskiy)
* Query renamed to Corpus (Katya Gerasimenko)
* Preparing package for release (Maria Terekhina)

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
