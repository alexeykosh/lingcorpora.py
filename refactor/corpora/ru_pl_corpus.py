from params_container import Container
from requests import post
from bs4 import BeautifulSoup


class PageParser:
    def __init__(self, query, subcorpus, numResults, targetLanguage):
        self.query = query
        self.page = None
        self.subcorpus = subcorpus
        self.numResults = numResults
        if targetLanguage is None:
            raise ValueError('Please, pass the targetLanguage argument. It migth be \'ru\' or \'pl\'.')
        else:
            self.targetLanguage = targetLanguage

        if self.targetLanguage is 'pl':
            self.language = 'ru'
        else:
            self.language = 'pl'


    def get_page(self):

        params = {'string' + self.language: self.query + '+',
                  'limit' + self.language.title(): self.numResults}

        for corpus in self.subcorpus:
            params[corpus] = 'on'

        s = post('http://pol-ros.polon.uw.edu.pl/searchresults/searchw'+self.language+'.php', params=params)
        return s

    def get_results(self):
        original = []
        translation = []
        soup = BeautifulSoup(self.page.text, 'lxml')
        for orig in soup.select('.resultsleftcol'):
            original.append(orig.text)
        for tran in soup.select('.resultsrightcol'):
            translation.append(tran.text)

        s = [[original[i], translation[i]] for i in range(len(original))]
        return s

    def extract_results(self):
        self.page = self.get_page()
        parsed_results = self.get_results()
        return parsed_results


class Downloader(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.subcorpus is None:
            self.subcorpus = ['1', '2', '3', '4', '5', '6', 'russian', 'foreign', 'polish']

    def download_all(self):
        parser = PageParser(self.query, self.subcorpus, self.numResults, self.targetLanguage)
        try:
            return parser.extract_results()
        except:
            return []


if __name__ == '__main__':
    #unittest.main()
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('subcorpus', type=str)
    parser.add_argument('numResults', type=int)
    parser.add_argument('targetLanguage', type=int)
    parser.add_argument('kwic', type=bool)
    parser.add_argument('write', type=bool)
    args = parser.parse_args(args)
    main(**vars(args))