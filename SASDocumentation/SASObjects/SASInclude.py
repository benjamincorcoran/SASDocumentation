import re
from pathlib import Path, PureWindowsPath, PurePosixPath

from .SASBaseObject import SASBaseObject

class SASInclude(SASBaseObject):
    '''
    SAS Include Object

    This object represents a SAS include statement. This path can be followed programmatically
    to find additionl extra-project code.

    Attributes:

        path: Path defined in the include statement
        posixPath: Web-friendly version of path

        StartLine (optional): The inital line in the parent code where this appears
        Endline (optional): The final line of the datastatement

    '''

    def __init__(self, rawStr, startLine):
        reFlags = re.DOTALL | re.IGNORECASE

        self.startLine = startLine
        self.endLine = rawStr.count('\n') + startLine

        self._path = re.findall(
            r"include ['\"](.*?)['\"]", rawStr, flags=reFlags)[0]
        self.path = str(PureWindowsPath(self._path))
        self.posixPath = re.sub(r'\s', '%20', str(PurePosixPath(self._path)))

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path
