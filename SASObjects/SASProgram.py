import re 
import os 
import datetime

from .SASMacro import SASMacro
from .SASLibname import SASLibname
from .SASInclude import SASInclude

class SASProgram(object):
    '''
    SAS Macro Class
    
    Creates an object with the following properties

        Name: Name of the SAS Program
        Filename:
        FilePath:
        LastUpdated:
        Macros:
        Arguments: List of SASArgument Objects
        DocString: Documentation String for the argument.
    '''

    def __init__(self,file):
        
        reFlags = re.DOTALL|re.IGNORECASE

        self.name = os.path.basename(file).replace('.sas','')
        self.fileName = os.path.basename(file)
        self.filePath = os.path.abspath(file)

        st = os.stat(file)

        self.fileSize = st[6]
        self.LastUpdated = datetime.datetime.fromtimestamp(st[8])

        self.macros = []
        self.libnames = []
        self.includes = []


        with open(self.filePath) as f:
            self.rawProgram = f.read()

        rawAbout = re.findall('(\/\*.*?\*\/(?!\s*[\/\*]))',self.rawProgram,reFlags)
        if len(rawAbout) > 0:
            self.about=re.sub('\*|\t|\/','',rawAbout[0])
        else:
            self.about=None

        rawMacros = re.findall('(?:\/\*[^;]*\*\/\s*)?%macro.*?%mend',self.rawProgram,reFlags)
        if len(rawMacros) > 0:
            self.readMacros(rawMacros)

        rawLibnames = re.findall(r"libname .{0,8} ['\"\(][^'\"\(\)]*?['\"\)]\s*;",self.rawProgram,reFlags)
        if len(rawLibnames) > 0:
            self.readLibnames(rawLibnames)
        
        rawIncludes= re.findall(r"include ['\"].*?['\"]",self.rawProgram,reFlags)
        if len(rawIncludes) > 0:
            self.readIncludes(rawIncludes)

    def readMacros(self,rawMacros):
        for macroStr in rawMacros:
            self.macros.append(SASMacro(macroStr))

    def readLibnames(self, rawLibnames):
        for libnameStr in rawLibnames:
            self.libnames.append(SASLibname(libnameStr))
    
    def readIncludes(self, rawIncludes):
        for includeStr in rawIncludes:
            self.includes.append(SASInclude(includeStr))

    def __str__(self):
        _ = '{}\n - {} macro(s)\n - {} libnames\n - {} includes'.format(self.fileName,len(self.macros),len(self.libnames),len(self.includes))
        return _

    def __repr__(self):
        return self.fileName