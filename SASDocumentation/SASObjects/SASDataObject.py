import re

from .SASBaseObject import SASBaseObject


class SASDataObject(SASBaseObject):
    '''
    SAS Data Object Class

    Creates an object with the following properties

        Library: Name of Library
        Dataset: Name of Dataset
        Condition: Any inline conditions applied to the dataset
        StartLine (optional): The inital line in the parent code where this appears
        Endline (optional): The final line of the datastatement

    This object exists as a definition for a SASDataset. Not a 'Data' statement 
    but any reference to a dataset that exists in a piece of SAS Code. Including 
    any inline conditions and libraries. 
    '''
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
        '''
        Check if the self is a _null_ dataset
       
        Returns:
            bool - True if _null_
        '''        
        if len(re.findall(r'_null_', self.dataset, self.regexFlags)) > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id
