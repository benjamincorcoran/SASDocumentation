import re

from .SASDataObject import SASDataObject

class SASDatastep(object):
    
    def __init__(self,rawStr):
  
        reFlags = re.DOTALL|re.IGNORECASE
        
        self.dataObjects = []
 
        rawObjects = re.findall(r'data ([^=].*?);',rawStr,reFlags)[0].split(' ')

        for dataObject in rawObjects:
            
            dataObjectDef=re.findall('([^\( ]*)',dataObject)[0]
            dataObjectDef=dataObjectDef.split('.')

            if len(dataObjectDef) == 1:
                if dataObjectDef[0].upper()!='_NULL_':
                    self.dataObjects.append(SASDataObject('work',dataObjectDef[0]))     
            else:
                self.dataObjects.append(SASDataObject(dataObjectDef[0],''.join(dataObjectDef[1:])))   
        

    # def __str__(self):
    #     return self.dataObjects

    # def __repr__(self):
    #     return self.dataObjects
