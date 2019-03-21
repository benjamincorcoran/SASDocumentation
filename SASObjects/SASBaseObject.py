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
            'procedure':re.compile(r'proc .*?(?:run|quit);',self.regexFlags),
        
            'datastepHead':re.compile(r"(data .*?;)",self.regexFlags),
            'datastepBody':re.compile(r"data .*?;(.*?run;)",self.regexFlags)   
        }

        self.SASKeywords = ['nway','noprint','nodup','nodupkey']


    def splitDataObjects(self, str):
        objects = []
        current = ''
        blev = 0
        for i,c in enumerate(str):
            if c == '(':
                blev += 1
                current += c
            elif c == ')':
                blev -= 1
                current += c
            elif re.match('\s',c) is not None and blev == 0 and len(current)>0 and re.match('\s*\(',str[i:]) is None:
                objects.append(current)
                current=''
            elif c == ';':
                objects.append(current)
                current=''
            else:
                current += c

        if len(current)>0:
            objects.append(current)
        return [obj for obj in objects if self.validateSplitDataObjects(obj) is True]
    
    def validateSplitDataObjects(self,obj):
        if not len(re.sub('\s','',obj))>0:
            return False
        
        if not re.match('end=|out=',obj,self.regexFlags) is None:
            return False
        for keyword in self.SASKeywords:
            if not re.match('^{}$'.format(keyword),obj,self.regexFlags) is None:
                return False
        return True


    def parse(self,SASObject,str):
        if SASObject in self.SASRegexDict.keys():
            return re.findall(self.SASRegexDict[SASObject],str)
        else:
            raise TypeError('SAS Object not found int SASRegexDict')
    
    
                