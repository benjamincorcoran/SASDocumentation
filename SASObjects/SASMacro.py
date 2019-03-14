import re

from .SASArgument import SASArgument

class SASMacro(object):
    '''
    SAS Macro Class
    
    Creates an object with the following properties

        Name: Name of the Macro given
        Arguments: List of SASArgument Objects
        DocString: Documentation String for the argument.
        Help: Help statement if present in the macro 
    '''

    def __init__(self,rawStr):
        
        reFlags = re.DOTALL|re.IGNORECASE

        predoc = re.findall('((?:\/\*.*\*\/\s*))?%macro.*?%mend',rawStr,reFlags)
        head = re.findall('(%macro.*?;)',rawStr,reFlags)[0]
        body = re.findall('%macro.*?;(.*)',rawStr,reFlags)[0]

        self.name = re.findall('%macro ([^\(;]*)',head,reFlags)[0]

        self.arguments = []
        argsLine = re.findall('\((.*\))',head,reFlags)  
        
        if len(argsLine)>0:
            self.getArgs(argsLine[0])

        if len(predoc) > 0 and len(predoc[0])>0:
            self.docString=re.sub('\*|\t|\/','',predoc[0])
        else:
            docString = re.findall('((?:\/\*.*?\*\/\s*)+)',body,reFlags)
            if len(docString) > 0:
                self.getDocString(docString[0])
            else:
                self.docString='No doc string'
            

        helpString = re.findall('%if.*?help.*?;(.*?)%end',body,reFlags)
        if len(helpString) > 0:
            self.getHelp(helpString[0])
        else:
            self.help=''

    def getArgs(self, argStr):
        args = re.findall('(.*?(?:\/\*.*?\*\/)?)(?:\s*,\s*|\s*\))',argStr)
        for arg in args:
            self.arguments.append(SASArgument(arg))
    
    def getDocString(self,docString):
        docString = re.sub('\/|\*|\t| {2,}','',docString)
        self.docString=docString

    def getHelp(self, helpString):
        helpString = '\n'.join(re.findall('%put(.*?);',helpString,flags=re.IGNORECASE))
        self.help=re.sub('\t| {2,}',' ',helpString)


    def __str__(self):
        _ = '{}\n - About: {}\n - {} Arguments: {}'.format(self.name,self.docString,len(self.arguments),self.arguments)
        # if len(self.arguments)>0:
        #     for arg in self.arguments:
        #         _ +='\n\n' + arg.__str__()
        return _
    
    def __repr__(self):
        return self.name

