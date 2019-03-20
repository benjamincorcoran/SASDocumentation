import re

class SASBaseObject(object):

    def __init__(self):

        self.regexFlags = re.DOTALL|re.IGNORECASE

        self.SASRegexDict = {
            'commentBlock':re.compile(r'\/\*.*?\*\/(?!\s*[\/\*])',self.regexFlags),
            'macro':re.compile(r'(?:\/\*[^;]*\*\/\s*)?%macro.*?%mend',self.regexFlags),
            'libname':re.compile(r"libname .{1,8} ['\"\(][^'\"\(\)]*?['\"\)]\s*;",self.regexFlags),
            'include':re.compile(r"include ['\"].*?['\"]",self.regexFlags),              
            'datastep':re.compile(r"\s*data [^=].*?;.*?run;",self.regexFlags),
            'dataObject':re.compile(r'\s*(.*?\(.*?[^(]*\))\s*;',self.regexFlags),
        
            'datastepHead':re.compile(r"(data .*?;)",self.regexFlags),
            'datastepBody':re.compile(r"data .*?;(.*?run;)",self.regexFlags)   
        }

    def splitDataObjects(self, str):
        objects = []
        current = ''
        blev = 0
        for i,c in enumerate(str):
            if c == '(':
                blev += 1
            elif c == ')':
                blev -= 1
            elif re.match('\s',c) is not None and blev == 0 and len(current)>0 and re.match('\s*\(',str[i:]) is None:
                objects.append(current)
                current=''
            elif c == ';':
                objects.append(current)
                current=''
            current += c
        return [obj for obj in objects if self.validateSplitDataObjects(obj) is True]
    
    def validateSplitDataObjects(self,obj):
        if len(re.sub('\s','',obj))>0:
            if re.match('end=',obj,self.regexFlags) is None:
                return True
            else:
                return False
        else:
            return False

    def parse(self,SASObject,str):
        if SASObject in self.SASRegexDict.keys():
            return re.findall(self.SASRegexDict[SASObject],str)
        else:
            raise TypeError('SAS Object not found int SASRegexDict')
    
    
                