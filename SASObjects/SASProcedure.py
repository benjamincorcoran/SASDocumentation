import re

from .SASDataObjectParser import SASDataObjectParser

class SASProcedure(SASDataObjectParser):
    
    def __init__(self,rawStr):
  
        SASDataObjectParser.__init__(self)

        self.rawStr = rawStr


        self.procedure = re.findall(r'proc (.*?)[\s;]',self.rawStr,self.regexFlags)[0]
        
        rawOutputs = re.findall(r'out\s*=\s*(.*?[;\(/])',self.rawStr,self.regexFlags)
        rawInputs = re.findall(r'data\s*=\s*(.*?(?:;|out\s*=|outfile\s*=))',self.rawStr,self.regexFlags)
        
        if len(rawInputs)>0:  
            self.inputs = self.parseDataObjects(rawInputs[0])
        else:
            self.inputs = []
        if len(rawOutputs)>0:
            self.outputs = self.parseDataObjects(rawOutputs[0])
        else:
            self.outputs = []
  



    # def __str__(self):
    #     return ','.join([_.__str__ for _ in self.outputs])

    # def __repr__(self):
    #     return ','.join([_.__repr__ for _ in self.outputs])

