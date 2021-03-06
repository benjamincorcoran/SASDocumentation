import re


class SASBaseObject(object):
    '''
    SAS Base Object Class

    This object exists as the base object for most SAS objects 
    and several functions for processing SAS program text in to 
    SASObjects correctly.


    Attributes:
        regexFlags: Global regex flags
        SASRegexDict:  Identifies elements of the SAS program 
        SASKeywords: List of SAS reserved keywords

    '''

    def __init__(self):

        self.regexFlags = re.DOTALL | re.IGNORECASE

        self.SASRegexDict = {
            'commentBlock': re.compile(
                r'\/\*.*?\*\/(?!\s*[\/\*])',
                self.regexFlags),
            'commentLine': re.compile(
                r'\s+\*.*?;', self.regexFlags),
            'putStatement': re.compile(
                r'%put.*?;',
                self.regexFlags),
            'macro': re.compile(
                r'(?:\/\*[^;]*\*\/\s*)?%macro.*?%mend',
                self.regexFlags),
            'libname': re.compile(
                r"libname .{1,8} ['\"\(][^'\"\(\)]*?['\"\)]\s*;",
                self.regexFlags),
            'sqllibname': re.compile(
                r'%sqllib\((.*?)\)',
                self.regexFlags),
            'include': re.compile(
                r"include ['\"].*?['\"]",
                self.regexFlags),
            'datastep': re.compile(
                r"(?:\s*|;\s*)([^A-Za-z0-9]data\s[^=].*?;.*?run;)",
                self.regexFlags),
            'dataObject': re.compile(
                r'\s*(.*?\(.*?[^(]*\))\s*;',
                self.regexFlags),
            'procedure': re.compile(
                r'proc .*?(?:run|quit);',
                self.regexFlags),
            'datastepHead': re.compile(
                r"(data .*?;)",
                self.regexFlags),
            'datastepBody': re.compile(
                r"data .*?;(.*?run;)",
                self.regexFlags)}

        self.SASKeywords = [
            'nway',
            'noprint',
            'nodup',
            'nodupkey',
            'replace',
            'ways',
            'noobs',
            'label',
            'missing',
            'outfile']

    def splitDataObjects(self, str):
        '''
        Splits a string into seperate data objects ignoring macro variables and brackets

        Parameters:
            str - String containing one more data objects

        Returns:
            list - Containing seperated data objects
        '''
        objects = []
        current = ''
        blev = 0
        mlev = 0
        for i, c in enumerate(str):
            if c == '(':
                blev += 1
                current += c
            elif c == ')':
                blev -= 1
                current += c
            elif c == '%':
                mlev += 1
            elif c == ';':
                mlev -= 1
            elif re.match(r'\s', c) is not None and blev == 0 and mlev == 0 and len(current) > 0 and re.match(r'\s*\(', str[i:]) is None:
                objects.append(current)
                current = ''
            elif c == ';':
                objects.append(current)
                current = ''
            else:
                current += c

        if len(current) > 0:
            objects.append(current)

        validObjects = [
            obj for obj in objects if self.validateSplitDataObjects(obj) is True]

        libSplitObjects = []

        for obj in validObjects:
            library = ''
            dataObject = ''
            macroLev = 0
            blev = 0
            current = ''
            for c in obj:
                if c == '&':
                    macroLev += 1
                    current += c
                elif c == '.' and macroLev > 0:
                    macroLev -= 1
                    current += c
                elif c == '(':
                    blev += 1
                    current += c
                elif c == ')':
                    blev -= 1
                    current += c
                elif c == '.' and macroLev == 0 and blev == 0:
                    library = current
                    current = ''
                else:
                    current += c
            dataObject = current
            dataObject = re.sub(';','',dataObject)
            libSplitObjects.append([library, dataObject])

        return libSplitObjects

    def validateSplitDataObjects(self, obj):
        '''
        Validates a data object against SASKeywords and commonsense

        Parameters:
            DataObject - Data object to be validated

        Returns:
            Bool - Data object is valid or not.
        '''
        if not len(re.sub(r'\s', '', obj)) > 0:
            return False
        if len(re.findall(r'^[^\(]*=[^\)]*$', obj, self.regexFlags)) > 0:
            return False
        if not re.match(
            r'^\s*end\s*[=]*$|^\s*out\s*[=]*$',
            obj,
                self.regexFlags) is None:
            return False
        for keyword in self.SASKeywords:
            if not re.match(r'\s*{}\s*'.format(keyword), obj,
                            self.regexFlags) is None:
                return False
        return True

    def parse(self, SASObject, str):
        '''
        Parses passed string for specified object from SASRegexDict

        Parameters:
            SASObjectName - Str name of SAS Object to be parsed key for SASRegexDict
            str - String of text to be parsed

        Returns:
            List - Returns list of parsed strings
        '''
        if SASObject in self.SASRegexDict.keys():
            return re.findall(self.SASRegexDict[SASObject], str)
        else:
            raise TypeError('SAS Object not found int SASRegexDict')

    def parseDataObjects(self, objectText):
        '''
        Parses Data Objects Strings into SASDataObjects grabbing library.

        Parameters:
            ObjectText - String defintion of data object.

        Returns:
            SASDataObject
        '''
        rawObjectList = self.splitDataObjects(objectText)

        objectList = []

        for dataObject in rawObjectList:

            library = dataObject[0]
            dataset = re.findall(
                r'([^(]+)[.]*', dataObject[1], self.regexFlags)[0]
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
                objectList.append(SASDataObject(library, dataset, condition))

        return objectList
