import re

class SASDataObject(object):
    
    def __init__(self,library,name):
  
        self.name = name
        self.library = library

        if self.library != '':
            self._str = '{}.{}'.format(self.library,self.name)
        else:
            self._str = self.name

    def __str__(self):
        return self._str
    
    def __repr__(self):
        return 