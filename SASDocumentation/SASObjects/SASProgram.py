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

    This class represents an entire .sas program. Seperating out macros, datasteps and
    procedures into predefined python objects. Included are several functions to read
    different aspects of the code correctly.

    Attributes:

        Name: Name of the SAS Program
        Filename: Filename of the SAS Program
        FilePath: Absolute file path of the SAS Program
        LastUpdated: Current time
        FileSize: Size of SAS Programfile
        Macros: List of SAS Macros

        Libnames: Two lists of defined SAS and SQL libnames
        Datasteps: List of all datasteps found the in code
        Procedures: list of all procedure found in the code

        Inputs: List of all inputs in the code
        Outputs: List of all outputs in the code

        rawComments: a list of all comment blocks within the code
        unCommentedCode: a version of the code with all comments/put
                         statements removed.


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

        try:
            with open(self.filePath) as f:
                self.rawProgram = f.read()
        except PermissionError:
            print("Do not have permissions to read {}".format(self.filePath))
            self.rawProgram="Do not have permissions to read {}".format(self.filePath)


        self.rawComments = self.parse('commentBlock', self.rawProgram)
        if len(self.rawComments) > 0:
            self.about = re.sub(r'\*|\t|\/', '', self.rawComments[0])
        else:
            self.about = None

        self.unCommentedProgram = self.SASRegexDict['commentBlock'].sub(
            '', self.rawProgram)
        self.unCommentedProgram = self.SASRegexDict['commentLine'].sub(
            '', self.unCommentedProgram)
        self.unCommentedProgram = self.SASRegexDict['putStatement'].sub(
            '', self.unCommentedProgram)

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

        self.getUniqueDataObjects()

    def getUniqueDataObjects(self):
        '''
        Create a list of unique data items based on name and library
        and a list of tuples denoting the lines where they occur.

        Returns:
            dict - DataItem library,dataset tupple -> linestart,lineend tupple list
        '''
        self.uniqueDataItems = {}
        for ds in self.inputs + self.outputs:
            dsKey = (ds.library.upper(), ds.dataset.upper())
            if dsKey in self.uniqueDataItems:
                self.uniqueDataItems[dsKey].append((ds.startLine, ds.endLine))
            else:
                self.uniqueDataItems[dsKey] = [(ds.startLine, ds.endLine)]
        for key, linepairs in self.uniqueDataItems.items():
            self.uniqueDataItems[key] = sorted(
                list(set(linepairs)), key=lambda x: x[0])

    def findLine(self, str):
        '''
        Find the line number of a given string.
        Parameters:
            str - String to search for in the code

        Returns:
            int - Line number for string
        '''
        start = re.findall(r"^[\s\\\*\/]*([^\n]*)", str, re.IGNORECASE)[0]
        prevLines = re.findall(
            "^(.*)" + re.escape(start),
            self.rawProgram,
            re.DOTALL | re.IGNORECASE)
        if len(prevLines) == 0:
            print("Unable to find first line due to inline comment.")
            return 0
        else:
            return re.findall(
                "^(.*)" + re.escape(start),
                self.rawProgram,
                re.DOTALL | re.IGNORECASE)[0].count('\n') + 1

    def readMacros(self, rawMacros):
        '''
        Read and process list of rawStrings into Objects

        Returns:
            list - List of Objects
        '''
        for macroStr in rawMacros:
            self.macros.append(SASMacro(macroStr, self.findLine(macroStr)))

    def readLibnames(self, rawLibnames, libType):
        '''
        Read and process list of rawStrings into Objects

        Returns:
            list - List of Objects
        '''
        for libnameStr in rawLibnames:
            if libType == 'SAS':
                self.libnames['SAS'].append(SASLibname(
                    libnameStr, self.findLine(libnameStr)))
            elif libType == 'SQL':
                self.libnames['SQL'].append(SASSQLLibname(
                    libnameStr, self.findLine(libnameStr)))

    def readIncludes(self, rawIncludes):
        '''
        Read and process list of rawStrings into Objects

        Returns:
            list - List of Objects
        '''
        for includeStr in rawIncludes:
            self.includes.append(
                SASInclude(
                    includeStr,
                    self.findLine(includeStr)))

    def readDatasteps(self, rawDatasteps):
        '''
        Read and process list of rawStrings into Objects

        Returns:
            list - List of Objects
        '''
        for datastepStr in rawDatasteps:
            self.datasteps.append(
                SASDatastep(
                    datastepStr,
                    self.findLine(datastepStr)))

    def readProcedures(self, rawProcedures):
        '''
        Read and process list of rawStrings into Objects

        Returns:
            list - List of Objects
        '''
        for procedureStr in rawProcedures:
            if len(re.findall('proc sql', procedureStr, self.regexFlags)) > 0:
                self.procedures.append(
                    SASProcSQL(
                        procedureStr,
                        self.findLine(procedureStr)))
            else:
                self.procedures.append(
                    SASProcedure(
                        procedureStr,
                        self.findLine(procedureStr)))

    def getInputs(self):
        '''
        Find all input objects from datasteps and procedures

        Returns:
            list - List of input objects
        '''
        for datastep in self.datasteps:
            for input in datastep.inputs:
                self.inputs.append(input)
        for proc in self.procedures:
            for input in proc.inputs:
                self.inputs.append(input)

    def getOutputs(self):
        '''
        Find all output objects from datasteps and procedures

        Returns:
            list - List of output objects
        '''
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
