import re

from .SASDataObject import SASDataObject

class SASDatastep(object):
    
    def __init__(self,rawStr):
  
        reFlags = re.DOTALL|re.IGNORECASE
        
        self.dataObjects = []

        rawObjects = re.findall('data (.*?);',rawStr,reFlags)[0].split(' ')
        for dataObject in rawObjects:
            dataObjectDef=(re.findall('(?:(.*)\.)?([^\(]*)',dataObject)[0])
            if dataObjectDef[1].upper()!='_NULL_':
                self.dataObjects.append(SASDataObject(dataObjectDef[0],dataObjectDef[1]))     
        

    # def __str__(self):
    #     return self.dataObjects

    # def __repr__(self):
    #     return self.dataObjects
