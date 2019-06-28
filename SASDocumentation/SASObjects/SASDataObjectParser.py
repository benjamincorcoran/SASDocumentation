import re

from .SASBaseObject import SASBaseObject
from .SASDataObject import SASDataObject


class SASDataObjectParser(SASBaseObject):
    '''
    SAS Data Object Parser Class

    Factory for creating DataObjects from text string
    '''

    def __init__(self):
        SASBaseObject.__init__(self)

    def parseDataObjects(self, objectText, startLine=None, endLine=None):
        '''
        Takes object text and parses out Data Objects

        Parameters:
            objectText - Raw text with DataObject defined within
            startLine (optional) - Starting line of specified text
            endLine (optional) - Ending line of specified text

        Returns:
            list - List of validated SASDataObjects found in objectText
        '''

        rawObjectList = self.splitDataObjects(objectText)
        
        objectList = []

        for dataObject in rawObjectList:
            library = dataObject[0]
            dataset = re.findall(
                r'([^(]+)[.]*', dataObject[1], self.regexFlags)
            if len(dataset) == 0:
                dataset=''
            else:
                dataset=dataset[0]
            condition = re.findall(r'\((.*)\)', dataObject[1], self.regexFlags)

            if len(library) > 0:
                library = library
            else:
                library = None
            if len(condition) > 0:
                condition = condition[0]
            else:
                condition = None
            if len(dataset) > 0:
                objectList.append(
                    SASDataObject(
                        library,
                        dataset,
                        condition,
                        startLine,
                        endLine))

        return objectList
