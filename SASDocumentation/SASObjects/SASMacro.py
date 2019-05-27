import re

from .SASArgument import SASArgument


class SASMacro(object):
    '''
    SAS Macro Class
    
    This class represents a SAS Macro function, primarly an attempt to
    fit the SAS Macro into a python class/function documentation structure.

    Attributes:

        Name: Name of the Macro given
        Arguments: List of SASArgument Objects
        DocString: Documentation String for the argument.
        Help: Help statement if present in the macro

    '''

    def __init__(self, rawStr, startLine):

        reFlags = re.DOTALL | re.IGNORECASE

        head = re.findall('(%macro.*?;)', rawStr, reFlags)[0]
        body = re.findall('%macro.*?;(.*)', rawStr, reFlags)[0]

        self.name = re.findall(r'%macro ([^\(;]*)', head, reFlags)[0]
        self.id = '%{}'.format(self.name)

        self.startLine = startLine
        self.endLine = rawStr.count('\n') + startLine

        self.arguments = []
        argsLine = re.findall(r'\((.*\))', head, reFlags)

        if len(argsLine) > 0:
            self.getArgs(argsLine[0])

        docString = re.findall(r'\/\*.*?\*\/(?!\s*[\/\*])', body, reFlags)
        if len(docString) > 0:
            self.getDocString(docString[0])
        else:
            self.docString = 'No doc string'

        helpString = re.findall('%if.*?help.*?;(.*?)%end', body, reFlags)
        if len(helpString) > 0:
            self.getHelp(helpString[0])
        else:
            self.help = ''

    def getArgs(self, argStr):
        '''
        Find all arguements in the macro definition line.

        Parameters:
            argStr - String containing defined arguments

        Returns:
            list - List of SASArgument Objects
        '''
        args = re.findall(r'(.*?(?:\/\*.*?\*\/)?)(?:\s*,\s*|\s*\))', argStr)
        for arg in args:
            self.arguments.append(SASArgument(arg))

    def getDocString(self, docString):
        '''
        Clean the doc string defintion of the macro

        Parameters:
            docString - String containing macro docstring

        Returns:
            list - Docstring with comment delimiters removed
        '''
        docString = re.sub(r'\/|\*|\t| {2,}', '', docString)
        self.docString = docString

    def getHelp(self, helpString):
        '''
        Clean the help string defintion of the macro

        Parameters:
            helpString - String containing macro helpString

        Returns:
            list - Docstring with %put statments removed
        '''
        helpString = '\n'.join(
            re.findall(
                '%put(.*?);',
                helpString,
                flags=re.IGNORECASE))
        self.help = re.sub('\t| {2,}', ' ', helpString)

    def __str__(self):
        _ = '{}\n - About: {}\n - {} Arguments: {}'.format(
            self.name, self.docString, len(self.arguments), self.arguments)
        # if len(self.arguments)>0:
        #     for arg in self.arguments:
        #         _ +='\n\n' + arg.__str__()
        return _

    def __repr__(self):
        return self.name
