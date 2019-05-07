import re
from pathlib import Path, PureWindowsPath, PurePosixPath

from .SASBaseObject import SASBaseObject


class SASLibname(SASBaseObject):
    '''
    SAS Libname Object

    Creates an object with the following properties

        name: Defined name of the library
        path: Path defined in the libname statement
        posixPath: Web-friendly version of path

        StartLine (optional): The inital line in the parent code where this appears
        Endline (optional): The final line of the datastatement

    This object represents a SAS libname statement.
    '''

    def __init__(self, rawStr, startLine):
        SASBaseObject.__init__(self)

        self.startLine = startLine
        self.endLine = rawStr.count('\n') + startLine

        self.name = re.findall(
            r"libname (.{0,8}) ['\"\(][^'\"\(\)]*?['\"\)]\s*;",
            rawStr,
            flags=self.regexFlags)[0]
        self._path = re.findall(
            r"libname .{0,8} ['\"\(]([^'\"\(\)]*?)['\"\)]\s*;",
            rawStr,
            flags=self.regexFlags)[0]
        self.path = str(PureWindowsPath(Path(self._path)))
        self.posixPath = re.sub('\s', '%20', str(
            PurePosixPath(Path(self._path))))

    def __str__(self):
        return '{} - {}'.format(self.name, self.path)

    def __repr__(self):
        return self.name


class SASSQLLibname(SASBaseObject):
    '''
    SAS SQLLibname Object

    Creates an object with the following properties

        name: Defined name of the library
        server: Hosted SQL server for library
        database: Database on the SQL server for library
        schema: Defined schema for the library (default: dbo)


        StartLine (optional): The inital line in the parent code where this appears
        Endline (optional): The final line of the datastatement

    This object represents a SAS SQLlibname statement. This is pulled from the %SQLLIB macro only.
    '''

    def __init__(self, rawStr, startLine):
        SASBaseObject.__init__(self)

        self.startLine = startLine
        self.endLine = rawStr.count('\n') + startLine

        self.name = re.findall('(.*?)(?=,|$)', rawStr,
                               flags=self.regexFlags)[0]

        server = re.findall('server=(.*?)(?=,|$)',
                            rawStr, flags=self.regexFlags)
        database = re.findall('dbname=(.*?)(?=,|$)',
                              rawStr, flags=self.regexFlags)
        schema = re.findall('schema=(.*?)(?=,|$)',
                            rawStr, flags=self.regexFlags)

        if len(server) > 0:
            self.server = server[0]
        else:
            self.server = 'hefce-statdata'
        if len(database) > 0:
            self.database = database[0]
        else:
            self.database = self.name
        if len(schema) > 0:
            self.schema = schema[0]
        else:
            self.schema = 'dbo'

    def __str__(self):
        return '{}: {}.{} // {}'.format(self.name,
                                        self.database, self.schema, self.server)

    def __repr__(self):
        return '{}'.format(self.name)
