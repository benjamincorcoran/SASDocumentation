import re

class SASBaseObject():

    def __init__(self):

        self.regexFlags = re.DOTALL|re.IGNORECASE
        self.SASRegexDict =
            {
                'commentBlock':re.compile(r'\/\*.*?\*\/(?!\s*[\/\*])',self.regexFlags),
                'macro':re.compile(r'(?:\/\*[^;]*\*\/\s*)?%macro.*?%mend',self.regexFlags),
                'libname':re.compile(r"libname .{0,8} ['\"\(][^'\"\(\)]*?['\"\)]\s*;')",self.regexFlags),
                'include':re.compile(r"include ['\"](.*?)['\"]",self.regexFlags),              
                'datastep':re.compile(r"data [^=]*?run;",self.regexFlags)
            }

    def parseSASObject(SASObject,str):
        if SASobject in self.SASRegexDict.keys():
            return re.findall(self.SASRegexDict[SASObject],str,self.regexFlags)
        else:
            raise TypeError('SAS Object not found int SASRegexDict')

                