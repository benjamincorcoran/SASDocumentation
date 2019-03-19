import re 
import os 
import datetime

from .SASBaseObject import SASBaseObject
from .SASMacro import SASMacro
from .SASLibname import SASLibname
from .SASInclude import SASInclude
from .SASDatastep import SASDatastep

class SASProgram(SASBaseObject):
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

        SASBaseObject.__init__(self)
        
        self.name = os.path.basename(file)
        self.fileName = os.path.basename(file)
        self.filePath = os.path.abspath(file)

        st = os.stat(file)

        self.fileSize = st[6]
        self.LastUpdated = datetime.datetime.fromtimestamp(st[8])

        self.macros = []
        self.libnames = []
        self.includes = []
        self.datasets = []


        with open(self.filePath) as f:
            self.rawProgram = f.read()

        self.rawComments = self.parseSASObject('commentBlock',self.rawProgram)
        if len(self.rawComments) > 0:
            self.about=re.sub('\*|\t|\/','',self.rawComments[0])
        else:
            self.about=None

        self.unCommentedProgram = self.SASRegexDict['commentBlock'].sub('',self.rawProgram)

        rawMacros = self.parseSASObject('macro',self.rawProgram)
        if len(rawMacros) > 0:
            self.readMacros(rawMacros)

        rawLibnames = self.parseSASObject('libname',self.rawProgram)
        if len(rawLibnames) > 0:
            self.readLibnames(rawLibnames)
        
        rawIncludes = self.parseSASObject('include',self.rawProgram)
        if len(rawIncludes) > 0:
            self.readIncludes(rawIncludes)

        rawDatasteps = self.parseSASObject('datastep',self.unCommentedProgram)
        if len(rawDatasteps) > 0:
            self.readDatasteps(rawDatasteps)

    def readMacros(self,rawMacros):
        for macroStr in rawMacros:
            self.macros.append(SASMacro(macroStr))

    def readLibnames(self, rawLibnames):
        for libnameStr in rawLibnames:
            self.libnames.append(SASLibname(libnameStr))
    
    def readIncludes(self, rawIncludes):
        for includeStr in rawIncludes:
            self.includes.append(SASInclude(includeStr))
    
    def readDatasteps(self, rawDatasteps):
        for datastepStr in rawDatasteps:
            datastep = (SASDatastep(datastepStr))
            for dataset in datastep.dataObjects:
                self.datasets.append(dataset)


    def __str__(self):
        _ = '{}\n - {} macro(s)\n - {} libnames\n - {} includes'.format(self.fileName,len(self.macros),len(self.libnames),len(self.includes))
        return _

    def __repr__(self):
        return self.fileName