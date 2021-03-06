import re
import os
import json

from .SASProgram import SASProgram
from ..SASAnalysis.SASFlowChart import SASFlowChart


class SASProject(object):

    def __init__(self, projectPath):
        '''
        SAS Project Class
        This class represents a SAS Project, or several pieces of SAS Code that have
        been stored together. Given a root this class will search for all pieces of
        .sas code and generate a SASProgram object for each. Appending that object and
        its elements into this project class.

        This class also deals with the generation of SAS Program documentation into
        markdown text, as well as creating a macro index.

        Attributes:

            ProjectName: Name of the SAS Project
            ProjectPath: Path to the root of the Project
            SASPrograms: List of SASProgram objects found in the project

            ExternalPrograms: List of SASPrograms %included but not in the project
            ProjectMacros: Dict of all Macros discovered in the project
            ProjectIncludes: Dict of all includes discovered in the project


        '''

        self.projectPath = projectPath
        self.projectName = os.path.basename(projectPath)

        self.SASPrograms = []

        for root, dirs, files in os.walk(self.projectPath):
            for file in files:
                if os.path.splitext(file)[1] == '.sas':
                    self.SASPrograms.append(
                        SASProgram(os.path.join(root, file)))

        self.projectFiles = []
        self.externalPrograms = []

        self.projectMacros = {}
        self.projectIncludes = {}

        for program in self.SASPrograms:
            relPath = os.path.relpath(program.filePath,self.projectPath)
            self.projectFiles.append(program.filePath)
            for include in program.includes:
                self.projectIncludes[program.filePath] = include.path
            for macro in program.macros:
                self.projectMacros['{}:{}::{}'.format(relPath,macro.name,macro.startLine)] = macro
                

        for projectFile, includePath in self.projectIncludes.items():
            if os.path.abspath(includePath) not in self.projectFiles:
                try:
                    self.externalPrograms.append(
                        SASProgram(os.path.abspath(includePath)))
                except BaseException:
                    print('Could not find included file: {}'.format(includePath))

    def buildProject(self, outPath):
        '''
        Create a _code.rst, _extcode.rst, macroIndex.md and _mindex.rst files. These
        are structural files used by sphinx to generate documentation and list
        locations of program documentation generated by the writeProgramDocumentation
        function.

        This also calls the writeProgramDocumentation function which generates documentation
        for a list of SASPrograms

        Parameters:
            outPath: Root outpath for documentation, these files are written to
                     outpath/code
        '''

        self.outPath = os.path.join(outPath,'source', 'code')
        if not os.path.exists(self.outPath):
            os.makedirs(self.outPath)

        codeDocumentationFiles = self.writeProgramDocumentation(
            self.SASPrograms, '_code.rst')
        externalDocumentationFiles = self.writeProgramDocumentation(
            self.externalPrograms, '_extcode.rst')

        macroIndex = self.buildMacroIndex()
        MDWritePath = os.path.join(self.outPath, '_macroIndex.md')
        with open(MDWritePath, 'w+') as out:
            out.write(macroIndex)

        with open(os.path.join(self.outPath, '_mindex.rst'), 'w+') as codeRST:
            codeRST.write('.. toctree::\n   :maxdepth: 3 \n\n   _macroIndex')

    def writeProgramDocumentation(self, programList, rstFile):
        '''
        Loop over a list of SASProgram object and generate markdown documentation. This also
        generates the SASFlowChart object based on the program


        Parameters:
            programList: A List of SASProgram objects to generate documentation for
            rstFile: Specifies whether this is projectCode or externalCode and generates
                     an appropriate rstfile to return

        Returns:
            str: RST structured list of files processed for sphinx documenation to generate
                 tables of contents trees from.
        '''
        codeDocumentationFiles = dict()

        for SASProgram in programList:
            relPath = os.path.dirname(os.path.relpath(SASProgram.filePath,self.projectPath))

            if not os.path.exists(os.path.join(self.outPath,relPath)):
                os.makedirs(os.path.join(self.outPath,relPath))

            MDWritePath = os.path.join(self.outPath,relPath, re.sub(
                '\s', '', os.path.splitext(SASProgram.fileName)[0] + '.md'))
    
            FlowChart = SASFlowChart(SASProgram)

            documentation = self.buildProgramDocumentation(
                SASProgram, FlowChart)

            with open(MDWritePath, 'w+') as out:
                out.write(documentation)

            if relPath in codeDocumentationFiles:
                codeDocumentationFiles[relPath].append(MDWritePath)
            else:
                codeDocumentationFiles[relPath] = [MDWritePath]

        if len(codeDocumentationFiles) > 0:
            if rstFile == '_code.rst':
                title = 'Project Code'
            else:
                title = 'External Code'
            with open(os.path.join(self.outPath, rstFile), 'w+') as codeRST:
                codeRST.write('{}\n'.format(title) + '=' * len(title) + '\n\n')
                for relPath, docFileList in codeDocumentationFiles.items():
                    relPathTitle = "{}".format(relPath).replace("\\"," - ")
                    codeRST.write('{}\n'.format(relPathTitle)+'-'*len(relPathTitle)+'\n\n')
                    codeRST.write('.. toctree::\n   :maxdepth: 1  \n\n')
                    for docFile in docFileList:
                        codeRST.write('   {}\n'.format(
                            os.path.join(relPath,os.path.splitext(os.path.basename(docFile))[0])).replace("\\","//"))
                    codeRST.write('\n\n')

        return codeDocumentationFiles

    def buildProgramDocumentation(self, SASProgram, FlowChart):
        '''
        Generate a markdown string from a SASProgram object. A SASFlowChart is also
        generated if there are none null data objects present in the code.

        Parameters:
            SASProgram - A SAS Program Object
            FlowChart - The FlowChart object that corresponds to the SAS Program Object
        Returns:
            str: MD structured full documentation for the given SASProgram
        '''

        markdownStr = ''
        markdownStr += '# {}\n\n'.format(SASProgram.name)
        if SASProgram.about is not None:
            markdownStr += '## About\n'
            markdownStr += '{}\n\n'.format(SASProgram.about)
        if FlowChart.countNodes() > 0:
            markdownStr += '## Program Struture\n\n'
            markdownStr += "<script>window.flowChart=" + FlowChart.json + "</script>\n"
            markdownStr += '<div><svg id="flowChartViz"></svg></div>\n\n'
        if len(SASProgram.libnames['SAS']) + \
                len(SASProgram.libnames['SQL']) > 0:
            markdownStr += '## Libraries\n\n'
            if len(SASProgram.libnames['SAS']) > 0:
                markdownStr += '### SAS Libraries\n\n'
                markdownStr += '| Name | Location | Line |\n'
                markdownStr += '| --- | --- | --- |\n'
                for libname in SASProgram.libnames['SAS']:
                    markdownStr += '| {0} | [{1}]({2}) | {3} |\n'.format(
                        libname.name, libname.path, libname.posixPath, self.linkLines(
                            libname.startLine, libname.endLine))
                markdownStr += '\n\n'
            if len(SASProgram.libnames['SQL']) > 0:
                markdownStr += '### SQL Libraries\n\n'
                markdownStr += '| Name | Database | Schema | Server | Line |\n'
                markdownStr += '| --- | --- | --- | --- | --- |\n'
                for libname in SASProgram.libnames['SQL']:
                    markdownStr += '| {0} | {1} | {2} | {3} | {4} |\n'.format(
                        libname.name, libname.database, libname.schema, libname.server, self.linkLines(
                            libname.startLine, libname.endLine))
                markdownStr += '\n\n'
        if len(SASProgram.includes) > 0:
            markdownStr += '## Include\n\n'
            markdownStr += '| Path | Line |\n'
            markdownStr += '| --- | --- |\n'
            for include in SASProgram.includes:
                markdownStr += '| [{0}]({1}) | {2} |\n'.format(
                    include.path, include.posixPath, self.linkLines(
                        include.startLine, include.endLine))
            markdownStr += '\n\n'
        if len(SASProgram.macros) > 0:
            markdownStr += '## Macros\n'
            markdownStr += '---\n\n'
            for macro in SASProgram.macros:

                markdownStr += '### %{}\n'.format(macro.name)
                markdownStr += 'Lines: ' + \
                    self.linkLines(macro.startLine, macro.endLine)
                markdownStr += '\n\n{}\n\n'.format(macro.docString)

                if len(macro.help) > 0:
                    markdownStr += 'Help: \n\n'
                    markdownStr += '{}\n\n'.format(macro.help)
                if len(macro.arguments) > 0:
                    markdownStr += '**Arguments:**\n'
                    for arg in macro.arguments:
                        markdownStr += '* **{}** (*{}*) - {} \n'.format(
                            arg.name, arg.type, arg.docString)
                markdownStr += '---\n\n'
        if len(SASProgram.uniqueDataItems) > 0:
            markdownStr += '## Datasets\n\n'
            markdownStr += '| Library | Name | Lines |\n'
            markdownStr += '| --- | --- | --- |\n'
            for dataItem, lines in SASProgram.uniqueDataItems.items():
                markdownStr += '| {0} | {1} | '.format(
                    dataItem[0], dataItem[1])
                for line in lines:
                    markdownStr += self.linkLines(line[0], line[1]) + ", "
                markdownStr = markdownStr[:-2]
                markdownStr += ' |\n'
            markdownStr += '\n\n'

        markdownStr += '## Full code\n\n'

        markdownStr += '<script>window.rawCode=' + \
            json.dumps(SASProgram.rawProgram) + '</script>'
        markdownStr += '<textarea id="codeMirrorArea"></textarea>\n\n'

        markdownStr += '## Properties\n\n'
        markdownStr += '| Meta | Property |\n| --- | --- |\n'
        markdownStr += '| **Author:** | |\n'
        markdownStr += '| **Path:** | *{}* |\n'.format(SASProgram.filePath)
        markdownStr += '| **Last updated:** | *{}* |\n'.format(
            SASProgram.LastUpdated)

        return markdownStr

    def linkLines(self, startLine, endLine):
        '''
        Create a sphinx/html complient hyperlink that links line numbers to raw
        code posted in the HTML build. The class lineJump is picked up in javascript
        post build.

        Parameters:
            startLine - Startline in the code of the object
            endLine - Endline in the code of the object

        Returns:
            str: <a> tagged HTML markup of the startLine, endLine.
        '''
        if startLine == endLine:
            return '<a class="lineJump" startLine={0} endLine={1}>*{0}*</a>'.format(
                startLine, endLine)
        else:
            return '<a class="lineJump" startLine={0} endLine={1}>*{0}-{1}*</a>'.format(
                startLine, endLine)

    def buildMacroIndex(self):
        '''
        Create a markdown formatted string containing all macros found within the project. This is used to
        generate the macroIndex for sphinx.

        Returns:
            str: Markdown formatted string containing all macros and appropriate properties.
        '''

        markdownStr = '# Macro index\n\n *Index of all macros discovered in the project folder*\n\n---\n'
        for path, macro in self.projectMacros.items():
            markdownStr += '## %{}\n'.format(macro.name)
            markdownStr += '*Found in: [{}]({})*\n'.format(
                os.path.splitext(
                    os.path.basename(path))[0], re.sub(
                    '\s', '', os.path.splitext(
                        path)[0].replace("\\","//") + '.md'))
            markdownStr += '\n{}\n\n'.format(macro.docString)
            if len(macro.help) > 0:
                markdownStr += 'Help: \n\n'
                markdownStr += '{}\n\n'.format(macro.help)
            if len(macro.arguments) > 0:
                markdownStr += '**Arguments:**\n'
                for arg in macro.arguments:
                    markdownStr += '* **{}** (*{}*) - {} \n'.format(
                        arg.name, arg.type, arg.docString)
            markdownStr += '---\n\n'
        return markdownStr
