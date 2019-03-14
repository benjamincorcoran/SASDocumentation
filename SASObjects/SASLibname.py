import re
from pathlib import Path, PureWindowsPath, PurePosixPath

class SASLibname(object):
    
    def __init__(self,rawStr):
        reFlags = re.DOTALL|re.IGNORECASE
        self.name = re.findall(r"libname (.*?) ['\"].*?['\"]",rawStr,flags=reFlags)[0]
        self._path = Path(re.findall(r"libname .*? ['\"](.*?)['\"]",rawStr,flags=reFlags)[0])
        self.path = str(PureWindowsPath(self._path))
        self.posixPath = re.sub('\s','%20',str(PurePosixPath(self._path)))
    

    def __str__(self):
        return '{} - {}'.format(self.name,self.path)

    def __repr__(self):
        return self.name