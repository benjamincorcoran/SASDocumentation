import re

from .SASBaseObject import SASBaseObject


class SASDataObject(SASBaseObject):

    def __init__(self, library, dataset, condition, startLine=None, endLine=None):

        SASBaseObject.__init__(self)

        self.dataset = re.sub(r'\s', '', dataset)
        self.startLine = startLine
        self.endLine = endLine

        if library is None:
            self.library = 'work'
        else:
            self.library = re.sub(r'\s', '', library)

        if condition is None:
            self.condition = ''
        else:
            self.condition = condition

        self.id = '{}.{}'.format(self.library, self.dataset)

    def isNull(self):
        if len(re.findall(r'_null_', self.dataset, self.regexFlags)) > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id
