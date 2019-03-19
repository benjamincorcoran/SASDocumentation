import re

class SASBaseObject(object):

    def __init__(self):

        self.regexFlags = re.DOTALL|re.IGNORECASE

        self.SASRegexDict = {
            'commentBlock':re.compile(r'\/\*.*?\*\/(?!\s*[\/\*])',self.regexFlags),
            'macro':re.compile(r'(?:\/\*[^;]*\*\/\s*)?%macro.*?%mend',self.regexFlags),
            'libname':re.compile(r"libname .{0,8} ['\"\(][^'\"\(\)]*?['\"\)]\s*;",self.regexFlags),
            'include':re.compile(r"include ['\"].*?['\"]",self.regexFlags),              
            'datastep':re.compile(r"\s*data [A-Za-z0-9\_\-\. \&]*?;.*?run;",self.regexFlags)
        }

    def parseSASObject(self,SASObject,str):
        if SASObject in self.SASRegexDict.keys():
            return re.findall(self.SASRegexDict[SASObject],str)
        else:
            raise TypeError('SAS Object not found int SASRegexDict')
    
    
                