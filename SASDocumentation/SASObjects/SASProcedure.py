import re
from itertools import chain

from .SASDataObjectParser import SASDataObjectParser


class SASProcedure(SASDataObjectParser):

    def __init__(self, rawStr, startLine):

        SASDataObjectParser.__init__(self)

        self.startLine = startLine
        self.endLine = rawStr.count('\n')+startLine

        self.rawStr = rawStr
        self.procedure = re.findall(
            r'proc (.*?)[\s;]', self.rawStr, self.regexFlags)[0]

        rawOutputs = re.findall(
            r'out\s*=\s*(.*?[;\(/])', self.rawStr, self.regexFlags)
        rawInputs = re.findall(
            r'data\s*=\s*(.*?(?:;|out\s*=|outfile\s*=))',
            self.rawStr,
            self.regexFlags)

        self.inputs = []
        self.outputs = []

        if len(rawInputs) > 0:
            for input in rawInputs:
                self.inputs.append(self.parseDataObjects(input, startLine=self.startLine, endLine=self.endLine))

        if len(rawOutputs) > 0:
            for output in rawOutputs:
                self.outputs.append(self.parseDataObjects(output, startLine=self.startLine, endLine=self.endLine))

        self.inputs = list(chain(*self.inputs))
        self.outputs = list(chain(*self.outputs))
        
    # def __str__(self):
    #     return ','.join([_.__str__ for _ in self.outputs])

    # def __repr__(self):
    #     return ','.join([_.__repr__ for _ in self.outputs])


class SASProcSQL(SASDataObjectParser):

    def __init__(self, rawStr, startLine):

        SASDataObjectParser.__init__(self)

        self.startLine = startLine
        self.endLine = rawStr.count('\n')+startLine

        self.rawStr = rawStr
        self.procedure = re.findall(
            r'proc (.*?)[\s;]', self.rawStr, self.regexFlags)[0]

        rawOutputs = re.findall(
            r'create table\s*(.*?)\sas', self.rawStr, self.regexFlags)
        rawInputs = re.findall(
            r'(?:from|join)\s+([^()]*?)\s', self.rawStr, self.regexFlags)

        self.inputs = []
        self.outputs = []

        if len(rawInputs) > 0:
            for input in rawInputs:
                self.inputs.append(self.parseDataObjects(input, startLine=self.startLine, endLine=self.endLine))

        if len(rawOutputs) > 0:
            for output in rawOutputs:
                self.outputs.append(self.parseDataObjects(output, startLine=self.startLine, endLine=self.endLine))

        self.inputs = list(chain(*self.inputs))
        self.outputs = list(chain(*self.outputs))

    # def __str__(self):
    #     return ','.join([_.__str__ for _ in self.outputs])

    # def __repr__(self):
    #     return ','.join([_.__repr__ for _ in self.outputs])
