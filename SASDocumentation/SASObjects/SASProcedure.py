import re
from itertools import chain

from .SASDataObjectParser import SASDataObjectParser


class SASProcedure(SASDataObjectParser):
    '''
    SAS Procedure Class

    This class represents all SAS procedures, except PROC SQL. They are defined as a
    list of inputs, outputs and a procedure type which is the word after proc in the
    raw code.

    Attributes:

        Inputs: List of DataObjects that are inputs to this step
        Outputs: List of DataObjects that are outputs from this step
        Procedure: SAS Procedure type

        StartLine: The inital line in the parent code where this appears
        Endline: The final line of the datastatement


    '''

    def __init__(self, rawStr, startLine):

        SASDataObjectParser.__init__(self)

        self.startLine = startLine
        self.endLine = rawStr.count('\n') + startLine

        self.rawStr = rawStr
        self.procedure = re.findall(
            r'proc (.*?)[\s;]', self.rawStr, self.regexFlags)[0]
        self.id = 'proc {} on '.format(self.procedure)

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
                self.inputs.append(
                    self.parseDataObjects(
                        input,
                        startLine=self.startLine,
                        endLine=self.endLine))

        if len(rawOutputs) > 0:
            for output in rawOutputs:
                self.outputs.append(
                    self.parseDataObjects(
                        output,
                        startLine=self.startLine,
                        endLine=self.endLine))

        self.inputs = list(chain(*self.inputs))
        self.outputs = list(chain(*self.outputs))

        self.id = 'proc {} on {}'.format(self.procedure, self.inputs[0])

    # def __str__(self):
    #     return ','.join([_.__str__ for _ in self.outputs])

    # def __repr__(self):
    #     return ','.join([_.__repr__ for _ in self.outputs])


class SASProcSQL(SASDataObjectParser):
    '''
    SAS Proc SQL Class

    This class represents the PROC SQL statment. It is largely identical to the
    SASProcedure class except for handling the rawInput and rawOutputs from the code.

    Attributes:

        Inputs: List of DataObjects that are inputs to this step
        Outputs: List of DataObjects that are outputs from this step
        Procedure: SAS Procedure type

        StartLine: The inital line in the parent code where this appears
        Endline: The final line of the datastatement
    '''

    def __init__(self, rawStr, startLine):

        SASDataObjectParser.__init__(self)

        self.startLine = startLine
        self.endLine = rawStr.count('\n') + startLine

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
                self.inputs.append(
                    self.parseDataObjects(
                        input,
                        startLine=self.startLine,
                        endLine=self.endLine))

        if len(rawOutputs) > 0:
            for output in rawOutputs:
                self.outputs.append(
                    self.parseDataObjects(
                        output,
                        startLine=self.startLine,
                        endLine=self.endLine))

        self.inputs = list(chain(*self.inputs))
        self.outputs = list(chain(*self.outputs))

    # def __str__(self):
    #     return ','.join([_.__str__ for _ in self.outputs])

    # def __repr__(self):
    #     return ','.join([_.__repr__ for _ in self.outputs])
