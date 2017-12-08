from oop_template import Session, Query

class Manager:
    def __init__(self):
        self.session = Session()

    def search(self,language,*args,**kwargs):
        queryObject = Query(self.session,language,*args,**kwargs)
        queryObject.search()
        return queryObject

    def write_results(self,query=None,filename=None):
        if query is None and self.session.all:
            query = self.session.all[-1]
        elif not self.session.all:
            print('Query list is empty. Please make a query first.')
        query.write_results(filename)

    #to do: redo unsuccessful, cashing?

a = Manager()
b = a.search('bam','jamana')
a.write_results(b)
