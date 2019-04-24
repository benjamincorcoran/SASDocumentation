import re
from pathlib import Path, PureWindowsPath, PurePosixPath


class SASInclude(object):

    def __init__(self, rawStr):
        reFlags = re.DOTALL | re.IGNORECASE
        self._path = re.findall(
            r"include ['\"](.*?)['\"]", rawStr, flags=reFlags)[0]
        self.path = str(PureWindowsPath(self._path))
        self.posixPath = re.sub(r'\s', '%20', str(PurePosixPath(self._path)))

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path
