from corpora import *
from params_container import Container
import csv


functions = {'bam': bam_corpus}


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class Session:
    def __init__(self):
        self.successful = []
        self.unsuccessful = []
        self.all = []


class Query(Container):
    def __init__(self,session,language,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.session = session
        self.language = language
        

    def search(self):
        downloader = functions[self.language].Downloader(**vars(self))
        self.results = downloader.download_all()
        
        if not self.results:
            print ('%s_search: nothing found for "%s"' % (self.language,self.query))
        if self.kwic:
            self.cols = ['index','left','center','right']
        else:
            self.results = [[''.join(x)] for x in self.results]
            self.cols = ['index','result']
            
        self.session.all.append(self)
        if self.results:
            self.session.successful.append(self)
        else:
            self.session.unsuccessful.append(self)
            
        return self.results


    def write_results(self,filename=None):
        not_allowed = '/\\?%*:|"<>'
        query = ''.join([x if x not in not_allowed else 'na' for x in self.query])
        if filename is None:
            filename = '%s_results_%s.csv' % (self.language, query)
        with open(filename,'w',encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow(self.cols)
            for i,x in enumerate(self.results):
                writer.writerow([i]+x)


