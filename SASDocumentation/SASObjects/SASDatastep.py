import re

from .SASDataObjectParser import SASDataObjectParser


class SASDatastep(SASDataObjectParser):
    '''
    SAS Datastep Object

    Creates an object with the following properties

        Inputs: List of DataObjects that are inputs to this step
        Outputs: List of DataObjects that are outputs from this step
        Head: Headline of datastep
        Body: Body of datastep

        StartLine (optional): The inital line in the parent code where this appears
        Endline (optional): The final line of the datastatement

    This object represents an entire SAS Datastep. Each input and output being a SASDataObject
    and such having the properties of a library, dataset name and condition where applicable
    '''

    def __init__(self, rawStr, startLine):

        SASDataObjectParser.__init__(self)

        self.startLine = startLine
        self.endLine = rawStr.count('\n') + startLine

        self.head = self.parse('datastepHead', rawStr)[0]
        self.body = self.parse('datastepBody', rawStr)[0]

        rawOutputs = re.findall(r'data (.*?;)', self.head, self.regexFlags)
        rawInputs = re.findall(r'(?:[\s]+set\s+|[;\s]+merge\s+)(.*?;)',
                               self.body, self.regexFlags)

        if len(rawInputs) > 0:
            rawInputs = re.sub(r'end=.*?[\s;]', '',
                               rawInputs[0], self.regexFlags)
            self.inputs = self.parseDataObjects(
                rawInputs, startLine=self.startLine, endLine=self.endLine)
        else:
            self.inputs = []
        if len(rawOutputs) > 0:
            self.outputs = self.parseDataObjects(
                rawOutputs[0], startLine=self.startLine, endLine=self.endLine)
        else:
            self.inputs = []

    # def __str__(self):
    #     return ','.join([_.__str__ for _ in self.outputs])

    # def __repr__(self):
    #     return ','.join([_.__repr__ for _ in self.outputs])
