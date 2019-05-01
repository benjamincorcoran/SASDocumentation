import re
import os
import json

from .SASProgram import SASProgram
from ..SASAnalysis.SASFlowChart import SASFlowChart


class SASProject(object):

    def __init__(self, projectPath):

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
            self.projectFiles.append(program.filePath)
            for include in program.includes:
                self.projectIncludes[program.filePath] = include.path
            for macro in program.macros:
                self.projectMacros[program.filePath] = macro

        for projectFile, includePath in self.projectIncludes.items():
            if os.path.abspath(includePath) not in self.projectFiles:
                try:
                    self.externalPrograms.append(
                        SASProgram(os.path.abspath(includePath)))
                except BaseException:
                    print('Could not find included file: {}'.format(includePath))

    def buildProject(self, outPath):

        self.outPath = os.path.join(outPath, 'source', 'code')
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
        codeDocumentationFiles = []

        for SASProgram in programList:
            MDWritePath = os.path.join(self.outPath, re.sub(
                '\s', '', os.path.splitext(SASProgram.fileName)[0] + '.md'))
            
            FlowChart = SASFlowChart(SASProgram)

            documentation = self.buildProgramDocumentation(
                SASProgram, FlowChart)

            with open(MDWritePath, 'w+') as out:
                out.write(documentation)

            codeDocumentationFiles.append(MDWritePath)

        if len(codeDocumentationFiles) > 0:
            if rstFile == '_code.rst':
                title = 'Project Code'
            else:
                title = 'External Code'
            with open(os.path.join(self.outPath, rstFile), 'w+') as codeRST:
                codeRST.write('{}\n'.format(title) + '=' * len(title) + '\n\n')
                codeRST.write('.. toctree::\n   :maxdepth: 2 \n\n')
                for docFile in codeDocumentationFiles:
                    codeRST.write('   {}\n'.format(
                        os.path.splitext(os.path.basename(docFile))[0]))

        return codeDocumentationFiles

    def buildProgramDocumentation(self, SASProgram, FlowChart):

        markdownStr = ''
        markdownStr += '# {}\n\n'.format(SASProgram.name)
        if SASProgram.about is not None:
            markdownStr += '## About\n'
            markdownStr += '{}\n\n'.format(SASProgram.about)
        if FlowChart.countNodes() > 0:
            markdownStr += '## Program Struture\n\n'
            markdownStr += "<script>window.flowChart="+FlowChart.json+"</script>\n"
            markdownStr += '<div id="dataNetwork"></div>\n\n'
        if len(SASProgram.libnames['SAS']) + \
                len(SASProgram.libnames['SQL']) > 0:
            markdownStr += '## Libraries\n\n'
            if len(SASProgram.libnames['SAS']) > 0:
                markdownStr += '### SAS Libraries\n\n'
                markdownStr += '| Name | Location | Line |\n'
                markdownStr += '| --- | --- | --- |\n'
                for libname in SASProgram.libnames['SAS']:
                    markdownStr += '| {0} | [{1}]({2}) | {3} |\n'.format(
                        libname.name, libname.path, libname.posixPath, self.linkLines(libname.startLine, libname.endLine))
                markdownStr += '\n\n'
            if len(SASProgram.libnames['SQL']) > 0:
                markdownStr += '### SQL Libraries\n\n'
                markdownStr += '| Name | Database | Schema | Server | Line |\n'
                markdownStr += '| --- | --- | --- | --- | --- |\n'
                for libname in SASProgram.libnames['SQL']:
                    markdownStr += '| {0} | {1} | {2} | {3} | {4} |\n'.format(
                        libname.name, libname.database, libname.schema, libname.server, self.linkLines(libname.startLine, libname.endLine))
                markdownStr += '\n\n'
        if len(SASProgram.includes) > 0:
            markdownStr += '## Include\n\n'
            markdownStr += '| Path | Line |\n'
            markdownStr += '| --- | --- |\n'
            for include in SASProgram.includes:
                markdownStr += '| [{0}]({1}) | {2} |\n'.format(include.path,
                                                       include.posixPath, self.linkLines(include.startLine, include.endLine))
            markdownStr += '\n\n'
        if len(SASProgram.macros) > 0:
            markdownStr += '## Macro\n'
            markdownStr += '---\n\n'
            for macro in SASProgram.macros:

                markdownStr += '### %{}\n'.format(macro.name)
                markdownStr += 'Lines: '+self.linkLines(macro.startLine,macro.endLine)
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
                markdownStr += '| {0} | {1} | '.format(dataItem[0], dataItem[1])
                for line in lines:
                    markdownStr += self.linkLines(line[0], line[1])+", "
                markdownStr = markdownStr[:-2]
                markdownStr += ' |\n'
            markdownStr += '\n\n'

        markdownStr += '## Full code:\n\n'
        
        markdownStr += '<script>window.rawCode='+json.dumps(SASProgram.rawProgram)+'</script>'
        markdownStr += '<textarea id="code"></textarea>\n\n'
        
        markdownStr += '## Properties\n\n'
        markdownStr += '| Meta | Property |\n| --- | --- |\n'
        markdownStr += '| **Author:** | |\n'
        markdownStr += '| **Path:** | *{}* |\n'.format(SASProgram.filePath)
        markdownStr += '| **Last updated:** | *{}* |\n'.format(
            SASProgram.LastUpdated)

        return markdownStr

    def linkLines(self, startLine, endLine):
        if startLine==endLine:
            return '<a class="lineJump" startLine={0} endLine={1}>*{0}*</a>'.format(startLine, endLine)
        else:
            return '<a class="lineJump" startLine={0} endLine={1}>*{0}-{1}*</a>'.format(startLine, endLine)

    def buildMacroIndex(self):
        markdownStr = ' # Macro index\n *Index of all macros discovered in the project folder*\n\n---\n'
        for path, macro in self.projectMacros.items():
            markdownStr += '## %{}\n'.format(macro.name)
            markdownStr += '*Found in: [{}]({})*\n'.format(
                os.path.splitext(
                    os.path.basename(path))[0], re.sub(
                    '\s', '', os.path.splitext(
                        os.path.basename(path))[0] + '.md'))
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