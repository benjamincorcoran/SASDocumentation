import re

class SASDataObject(object):
    
    def __init__(self,library,dataset,condition):

       
        self.dataset = dataset
    
        if library is None:
            self.library = 'work'
        else:
            self.library = library

        if condition is None:
            self.condition = ''
        else:
            self.condition = condition

        self._str = '{}.{}'.format(self.library,self.dataset)
   
    def __str__(self):
        return self._str
    
    def __repr__(self):
        return self._str