import re

from .SASDataObjectParser import SASDataObjectParser


class SASDatastep(SASDataObjectParser):

    def __init__(self, rawStr):

        SASDataObjectParser.__init__(self)

        self.head = self.parse('datastepHead', rawStr)[0]
        self.body = self.parse('datastepBody', rawStr)[0]

        rawOutputs = re.findall(r'data (.*?;)', self.head, self.regexFlags)
        rawInputs = re.findall(r'(?:set |merge )(.*?;)',
                               self.body, self.regexFlags)

        if len(rawInputs) > 0:
            rawInputs = re.sub(r'end=.*?[\s;]', '',
                               rawInputs[0], self.regexFlags)
            self.inputs = self.parseDataObjects(rawInputs)
        else:
            self.inputs = []
        if len(rawOutputs) > 0:
            self.outputs = self.parseDataObjects(rawOutputs[0])
        else:
            self.inputs = []

    # def __str__(self):
    #     return ','.join([_.__str__ for _ in self.outputs])

    # def __repr__(self):
    #     return ','.join([_.__repr__ for _ in self.outputs])
