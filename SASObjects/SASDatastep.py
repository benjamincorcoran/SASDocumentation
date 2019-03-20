import re

from SASBaseObject import SASBaseObject
from SASDataObject import SASDataObject

class SASDatastep(SASBaseObject):
    
    def __init__(self,rawStr):
  
        SASBaseObject.__init__(self)

        self.head = self.parse('datastepHead',rawStr)[0]
        self.body = self.parse('datastepBody',rawStr)[0]

        rawOutputs = re.findall(r'data (.*?);',self.head,self.regexFlags)[0]
        rawInputs = re.findall(r'(?:set |merge )(.*?);',self.body,self.regexFlags)[0]

        self.inputs = self.parseDataObjects(rawInputs)
        self.outputs = self.parseDataObjects(rawOutputs)

        print(self.inputs,self.outputs)
        
    def parseDataObjects(self,objectText):
        rawObjectList = self.SASRegexDict['dataObject'].split(objectText)
        rawObjectList = [ _ for _ in rawObjectList if len(_)>0]

        objectList = []

        for dataObject in rawObjectList:
            library = re.findall(r'(.*)\.',dataObject,self.regexFlags)
            dataset = re.findall(r'(?:.*\.)?([^(]+)',dataObject,self.regexFlags)[0]
            condition = re.findall(r'\((.*)\)',dataObject,self.regexFlags)
            
            if len(library) > 0:
                library = library[0]
            else:
                library = None
            if len(condition) > 0:
                condition = condition[0]
            else:
                condition = None

            objectList.append(SASDataObject(library,dataset,condition))

        return objectList

            


    # def __str__(self):
    #     return self.dataObjects

    # def __repr__(self):
    #     return self.dataObjects

if __name__ == "__main__":
    test = '''data a.d b e.c(where=);
    set d e(where=) f;
    run;'''

    SASDatastep(test)