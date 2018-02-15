from oop_template import Session, Query
import collections
import warnings

class Manager:
    def __init__(self):
        self.session = Session()

        
    def search(self,language,*args,**kwargs):
        queryObject = Query(self.session,language,*args,**kwargs)
        queryObject.search()
        return queryObject
 
 
    def search_bunch(self,language,query,*args,**kwargs):
        queryObjects = []
        if not isinstance(query, collections.Sequence):
            raise TypeError('A sequence-type variable should be passed to this function. For a single query, use "search" function.')
        else:
            if isinstance(query, str):
                warnings.warn('A string was passed for a "query" argument. For a single query, use "search" function.')
            for q in query:
                queryObjects.append(self.search(language,q,*args,**kwargs))
        return queryObjects

        
    def write_results(self,query=None,filename=None):
        if query is None and self.session.all:
            query = self.session.all[-1]
        elif not self.session.all:
            print('Query list is empty. Please make a query first.')
        query.write_results(filename)

    #to do: redo unsuccessful, cashing?

#a = Manager()
#b = a.search_bunch('deu',['Mutter','Vater'])
#print(b[0].results[:5],b[1].results[:5],sep='\n')
