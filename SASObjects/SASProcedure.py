import re

from .SASBaseObject import SASBaseObject
from .SASDataObject import SASDataObject

class SASProcedure(SASBaseObject):
    
    def __init__(self,rawStr):
  
        SASBaseObject.__init__(self)

        self.rawStr = rawStr

        self.procedure = re.findall(r'proc (.*?)[\s;]',self.rawStr,self.regexFlags)[0]
        
        rawOutputs = re.findall(r'out=(.*?[;\(/])',self.rawStr,self.regexFlags)
        rawInputs = re.findall(r'data=(.*?(?:;|out=))',self.rawStr,self.regexFlags)
        
        if len(rawInputs)>0:   
            self.inputs = self.parseDataObjects(rawInputs[0])
        else:
            self.inputs = []
        if len(rawOutputs)>0:
            self.outputs = self.parseDataObjects(rawOutputs[0])
        else:
            self.outputs = []
  

    def parseDataObjects(self,objectText):
        rawObjectList = self.splitDataObjects(objectText)
        rawObjectList = [ _ for _ in rawObjectList if len(_)>0]

        objectList = []
        
        for dataObject in rawObjectList:
            dataObject = re.sub('/.*[\s;]','',dataObject)
            dataObject = re.sub('&.*?\.','',dataObject)
            
            library = re.findall(r'(.*?)\.',dataObject,self.regexFlags)
            dataset = re.findall(r'(?:.*?\.)?([^(]+)[.]*',dataObject,self.regexFlags)
            condition = re.findall(r'\((.*)\)',dataObject,self.regexFlags)
            
            if len(library) > 0:
                library = library[0]
            else:
                library = None
            if len(condition) > 0:
                condition = condition[0]
            else:
                condition = None
            if len(dataset) > 0:
                objectList.append(SASDataObject(library,dataset[0],condition))

        return objectList

    # def __str__(self):
    #     return ','.join([_.__str__ for _ in self.outputs])

    # def __repr__(self):
    #     return ','.join([_.__repr__ for _ in self.outputs])

