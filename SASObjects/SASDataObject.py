import re

class SASDataObject(object):
    
    def __init__(self,library,dataset,condition):

       
        self.dataset = re.sub('\s','',dataset)
    
        if library is None:
            self.library = 'work'
        else:
            self.library = re.sub('\s','',library)

        if condition is None:
            self.condition = ''
        else:
            self.condition = condition

        self.id = '{}.{}'.format(self.library,self.dataset)
   
    def __str__(self):
        return self.id
    
    def __repr__(self):
        return self.id