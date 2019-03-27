import re

class SASBaseObject(object):

    def __init__(self):

        self.regexFlags = re.DOTALL|re.IGNORECASE

        self.SASRegexDict = {
            'commentBlock':re.compile(r'\/\*.*?\*\/(?!\s*[\/\*])|\*.*?;',self.regexFlags),
            'macro':re.compile(r'(?:\/\*[^;]*\*\/\s*)?%macro.*?%mend',self.regexFlags),
            'libname':re.compile(r"libname .{1,8} ['\"\(][^'\"\(\)]*?['\"\)]\s*;",self.regexFlags),
            'sqllibname':re.compile(r'%sqllib\((.*?)\)',self.regexFlags),
            'include':re.compile(r"include ['\"].*?['\"]",self.regexFlags),              
            'datastep':re.compile(r"\s*data [^=].*?;.*?run;",self.regexFlags),
            'dataObject':re.compile(r'\s*(.*?\(.*?[^(]*\))\s*;',self.regexFlags),
            'procedure':re.compile(r'proc .*?(?:run|quit);',self.regexFlags),
        
            'datastepHead':re.compile(r"(data .*?;)",self.regexFlags),
            'datastepBody':re.compile(r"data .*?;(.*?run;)",self.regexFlags)   
        }

        self.SASKeywords = ['nway','noprint','nodup','nodupkey','replace','ways','noobs','label','missing','outfile']


    def splitDataObjects(self, str):
        objects = []
        current = ''
        blev = 0
        mlev = 0
        for i,c in enumerate(str):
            if c == '(':
                blev += 1
                current += c
            elif c == ')':
                blev -= 1
                current += c
            elif c=='%':
                mlev += 1
            elif c==';':
                mlev -= 1
            elif re.match('\s',c) is not None and blev == 0 and mlev == 0 and len(current)>0 and re.match('\s*\(',str[i:]) is None:
                objects.append(current)
                current=''
            elif c == ';':
                objects.append(current)
                current=''
            else:
                current += c

        if len(current)>0:
            objects.append(current)
        
        validObjects =  [obj for obj in objects if self.validateSplitDataObjects(obj) is True]
        
        libSplitObjects = []

        for obj in validObjects:
            library = ''
            dataObject = ''
            macroLev = 0
            current=''
            for c in obj:
                if c == '&':
                    macroLev += 1
                    current += c
                elif c == '.' and macroLev > 0:
                    macroLev -= 1
                    current += c
                elif c == '.' and macroLev == 0:
                    library = current
                    current = ''
                else:
                    current += c
            dataObject = current
            libSplitObjects.append([library,dataObject])
        
        return libSplitObjects

    
    def validateSplitDataObjects(self,obj):
        if not len(re.sub('\s','',obj))>0:
            return False
        if len(re.findall('^[^\(]*=[^\)]*$',obj,self.regexFlags)) > 0:
            return False
        if not re.match('^\s*end\s*[=]*$|^\s*out\s*[=]*$',obj,self.regexFlags) is None:
            return False
        for keyword in self.SASKeywords:
            if not re.match('\s*{}\s*'.format(keyword),obj,self.regexFlags) is None:
                return False
        return True


    def parse(self,SASObject,str):
        if SASObject in self.SASRegexDict.keys():
            return re.findall(self.SASRegexDict[SASObject],str)
        else:
            raise TypeError('SAS Object not found int SASRegexDict')
    
    
    def parseDataObjects(self,objectText):
        rawObjectList = self.splitDataObjects(objectText)

        objectList = []
        
        for dataObject in rawObjectList:            
            
            library = dataObject[0]
            dataset = re.findall(r'([^(]+)[.]*',dataObject[1],self.regexFlags)[0]
            condition = re.findall(r'\((.*)\)',dataObject[1],self.regexFlags)
            
            
            if len(library) > 0:
                library = library
            else:
                library = None
            if len(condition) > 0:
                condition = condition[0]
            else:
                condition = None
            if len(dataset) > 0:
                objectList.append(SASDataObject(library,dataset,condition))

        return objectList