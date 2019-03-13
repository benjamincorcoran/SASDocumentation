import re

from .SASArgument import SASArgument

class SASMacro(object):
    '''
    SAS Macro Class
    
    Creates an object with the following properties

        Name: Name of the Macro given
        Arguments: List of SASArgument Objects
        DocString: Documentation String for the argument.
    '''

    def __init__(self,rawStr):
        
        reFlags = re.DOTALL|re.IGNORECASE

        initLine = re.findall('(%macro.*?;)',rawStr,reFlags)[0]
        codeBody = re.findall('%macro.*?;(.*)',rawStr,reFlags)[0]

        self.name = re.findall('%macro ([^\(;]*)',initLine,reFlags)[0]

        self.arguments = []
        argsLine = re.findall('\((.*\))',initLine,reFlags)  
        
        if len(argsLine)>0:
            self.getArgs(argsLine[0])

        docString = re.findall('((?:\/\*.*?\*\/\s*)+)',codeBody,reFlags)

        if len(docString) > 0:
            self.getDocString(docString[0])
        else:
            self.docString='No doc string'

    def getArgs(self, argStr):
        args = re.findall('(.*?(?:\/\*.*?\*\/)?)(?:,|\s*\))',argStr)
        for arg in args:
            self.arguments.append(SASArgument(arg))
    
    def getDocString(self,docString):
        docString = re.sub('\/|\*','',docString)
        self.docString=docString

    def __str__(self):
        _ = '{}\n - About: {}\n - {} Arguments: {}'.format(self.name,self.docString,len(self.arguments),self.arguments)
        # if len(self.arguments)>0:
        #     for arg in self.arguments:
        #         _ +='\n\n' + arg.__str__()
        return _
    
    def __repr__(self):
        return self.name

