import re
import os
import datetime

from .SASBaseObject import SASBaseObject
from .SASMacro import SASMacro
from .SASLibname import SASLibname, SASSQLLibname
from .SASInclude import SASInclude
from .SASDatastep import SASDatastep
from .SASProcedure import SASProcedure, SASProcSQL


class SASProgram(SASBaseObject):
    '''
    SAS Program Class

    Creates an object with the following properties

        Name: Name of the SAS Program
        Filename:
        FilePath:
        LastUpdated:
        Macros:
        Arguments: List of SASArgument Objects
        DocString: Documentation String for the argument.
    '''

    def __init__(self, file):

        SASBaseObject.__init__(self)

        self.name = os.path.basename(file)
        self.fileName = os.path.basename(file)
        self.filePath = os.path.abspath(file)

        st = os.stat(file)

        self.fileSize = st[6]
        self.LastUpdated = datetime.datetime.fromtimestamp(st[8])

        self.macros = []
        self.libnames = {'SAS': [], 'SQL': []}
        self.includes = []
        self.datasteps = []
        self.procedures = []

        self.inputs = []
        self.outputs = []

        with open(self.filePath) as f:
            self.rawProgram = f.read()

        self.rawComments = self.parse('commentBlock', self.rawProgram)
        if len(self.rawComments) > 0:
            self.about = re.sub(r'\*|\t|\/', '', self.rawComments[0])
            self.about = re.sub('(?<!\n)\n(?!\n)', '\n\n', self.about)
        else:
            self.about = None

        self.unCommentedProgram = self.SASRegexDict['commentBlock'].sub(
            '', self.rawProgram)

        rawMacros = self.parse('macro', self.rawProgram)
        if len(rawMacros) > 0:
            self.readMacros(rawMacros)

        rawLibnames = self.parse('libname', self.rawProgram)
        if len(rawLibnames) > 0:
            self.readLibnames(rawLibnames, 'SAS')

        rawSQLLibnames = self.parse('sqllibname', self.rawProgram)
        if len(rawSQLLibnames) > 0:
            self.readLibnames(rawSQLLibnames, 'SQL')

        rawIncludes = self.parse('include', self.rawProgram)
        if len(rawIncludes) > 0:
            self.readIncludes(rawIncludes)

        rawDatasteps = self.parse('datastep', self.unCommentedProgram)
        if len(rawDatasteps) > 0:
            self.readDatasteps(rawDatasteps)

        rawProcedures = self.parse('procedure', self.unCommentedProgram)
        if len(rawProcedures) > 0:
            self.readProcedures(rawProcedures)

        self.getInputs()
        self.getOutputs()

        self.uniqueDataItems = [x.split('#/#') for x in list(set([ds.library.upper(
        ) + '#/#' + ds.dataset.upper() for ds in self.inputs + self.outputs]))]

    def findLine(self,str):
        start = re.findall("^[\s\\\*\/]*([^\n]*)",str,re.IGNORECASE)[0]
        return re.findall("^(.*)"+re.escape(start),self.rawProgram,re.DOTALL|re.IGNORECASE)[0].count('\n')+1

    def readMacros(self, rawMacros):
        for macroStr in rawMacros:
            self.macros.append(SASMacro(macroStr,self.findLine(macroStr)))

    def readLibnames(self, rawLibnames, libType):
        for libnameStr in rawLibnames:
            if libType == 'SAS':
                self.libnames['SAS'].append(SASLibname(libnameStr,self.findLine(libnameStr)))
            elif libType == 'SQL':
                self.libnames['SQL'].append(SASSQLLibname(libnameStr,self.findLine(libnameStr)))

    def readIncludes(self, rawIncludes):
        for includeStr in rawIncludes:
            self.includes.append(SASInclude(includeStr,self.findLine(includeStr)))

    def readDatasteps(self, rawDatasteps):
        for datastepStr in rawDatasteps:
            self.datasteps.append(SASDatastep(datastepStr,self.findLine(datastepStr)))

    def readProcedures(self, rawProcedures):
        for procedureStr in rawProcedures:
            if len(re.findall('proc sql', procedureStr, self.regexFlags)) > 0:
                self.procedures.append(SASProcSQL(procedureStr,self.findLine(procedureStr)))
            else:
                self.procedures.append(SASProcedure(procedureStr,self.findLine(procedureStr)))

    def getInputs(self):
        for datastep in self.datasteps:
            for input in datastep.inputs:
                self.inputs.append(input)
        for proc in self.procedures:
            for input in proc.inputs:
                self.inputs.append(input)

    def getOutputs(self):
        for datastep in self.datasteps:
            for output in datastep.outputs:
                self.outputs.append(output)
        for proc in self.procedures:
            for output in proc.outputs:
                self.outputs.append(output)

    def __str__(self):
        _ = '{}\n - {} macro(s)\n - {} libnames\n - {} includes'.format(
            self.fileName, len(
                self.macros), len(
                self.libnames), len(
                self.includes))
        return _

    def __repr__(self):
        return self.fileName
