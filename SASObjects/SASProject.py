import re 
import os 

from .SASProgram import SASProgram
from .SASFlowChart import SASFlowChart

class SASProject(object):

    def __init__(self, projectPath):

        self.projectPath = projectPath
        self.projectName = os.path.basename(projectPath)

        self.SASPrograms = []

        for root, dirs, files in os.walk(self.projectPath):
            for file in files:
                if os.path.splitext(file)[1] == '.sas':
                    self.SASPrograms.append(SASProgram(os.path.join(root,file)))
        
        self.projectFiles = []
        self.externalPrograms = []

        self.projectMacros = {}
        self.projectIncludes = {}

        for program in self.SASPrograms:
            self.projectFiles.append(program.filePath)
            for include in program.includes:
                self.projectIncludes[program.filePath]=include.path
            for macro in program.macros:
                self.projectMacros[program.filePath]=macro

        for projectFile, includePath in self.projectIncludes.items():
            if os.path.abspath(includePath) not in self.projectFiles:
                try:
                    self.externalPrograms.append(SASProgram(os.path.abspath(includePath)))
                except:
                    print('Could not find included file: {}'.format(includePath))

    def buildProject(self, outPath):

        self.outPath = os.path.join(outPath,'source','code')
        if not os.path.exists(self.outPath):
            os.makedirs(self.outPath)
        
        codeDocumentationFiles = self.writeProgramDocumentation(self.SASPrograms)
        externalDocumentationFiles = self.writeProgramDocumentation(self.externalPrograms)

        macroIndex = self.buildMacroIndex()
        MDWritePath = os.path.join(self.outPath,'_macroIndex.md')
        with open(MDWritePath,'w+') as out:
            out.write(macroIndex)
        
        with open(os.path.join(self.outPath,'_code.rst'),'w+') as codeRST:
            codeRST.write('Project Code\n============\n\n.. toctree::\n   :maxdepth: 2 \n\n')
            for docFile in codeDocumentationFiles:
                codeRST.write('   {}\n'.format(os.path.splitext(os.path.basename(docFile))[0]))
        
        if len(externalDocumentationFiles) > 0:
            with open(os.path.join(self.outPath,'_extcode.rst'),'w+') as codeRST:
                codeRST.write('External Code\n=============\n\n.. toctree::\n   :maxdepth: 2 \n\n')
                for docFile in externalDocumentationFiles:
                    codeRST.write('   {}\n'.format(os.path.splitext(os.path.basename(docFile))[0]))
            
        with open(os.path.join(self.outPath,'_mindex.rst'),'w+') as codeRST:
            codeRST.write('.. toctree::\n   :maxdepth: 3 \n\n   _macroIndex')

    
    def writeProgramDocumentation(self, programList):
        codeDocumentationFiles = []

        for SASProgram in programList:
            MDWritePath = os.path.join(self.outPath,re.sub('\s','',os.path.splitext(SASProgram.fileName)[0]+'.md'))
            PNGWritePath = os.path.join(self.outPath,re.sub('\s','',os.path.splitext(SASProgram.fileName)[0]+'.png'))

            FlowChart = SASFlowChart(SASProgram)
            if FlowChart.countNodes() > 0:
                FlowChart.saveFig(PNGWritePath)
            else:
                PNGWritePath = None
            
            documentation = self.buildProgramDocumentation(SASProgram,PNGWritePath)

            with open(MDWritePath,'w+') as out:
                out.write(documentation)

            codeDocumentationFiles.append(MDWritePath)
        return codeDocumentationFiles

    def buildProgramDocumentation(self, SASProgram, imagePath):

        markdownStr = ''
        markdownStr += '# {}\n\n'.format(SASProgram.name)
        if SASProgram.about is not None:
            markdownStr += '## About\n'
            markdownStr += '{}\n\n'.format(SASProgram.about)
        if imagePath is not None:
            markdownStr += '## Program Struture\n\n'
            markdownStr += '![Program Structure]({})\n\n'.format(os.path.basename(imagePath))
        if len(SASProgram.libnames['SAS'])+len(SASProgram.libnames['SQL'])> 0:
            markdownStr += '## Libraries\n\n'
            if len(SASProgram.libnames['SAS']) > 0:
                markdownStr += '### SAS Libraries\n\n'
                markdownStr += '| Name | Location |\n'
                markdownStr += '| --- | --- |\n'
                for libname in SASProgram.libnames['SAS']:
                    markdownStr += '| {} | [{}]({}) |\n'.format(libname.name,libname.path,libname.posixPath)
                markdownStr += '\n\n'
            if len(SASProgram.libnames['SQL']) > 0:
                markdownStr += '### SQL Libraries\n\n'
                markdownStr += '| Name | Database | Schema | Server |\n'
                markdownStr += '| --- | --- | --- | --- |\n'
                for libname in SASProgram.libnames['SQL']:
                    markdownStr += '| {} | {} | {} | {} |\n'.format(libname.name,libname.database,libname.schema,libname.server)
                markdownStr += '\n\n'
        if len(SASProgram.includes) > 0:
            markdownStr += '## Include\n\n'
            markdownStr += '| Path |\n'
            markdownStr += '| --- |\n'
            for include in SASProgram.includes:
                markdownStr += '| [{}]({}) |\n'.format(include.path,include.posixPath)
            markdownStr += '\n\n'
        if len(SASProgram.macros)> 0:
            markdownStr += '## Macro\n'
            for macro in SASProgram.macros:
                markdownStr += '### {}\n'.format(macro.name)
                markdownStr += '#### About\n'
                markdownStr += '{}\n\n'.format(macro.docString)
                if len(macro.help)>0:
                    markdownStr += '#### Help\n'
                    markdownStr += '{}\n\n'.format(macro.help)
                if len(macro.arguments)>0:
                    markdownStr += '#### Arguments\n\n'
                    markdownStr += '| Name | Type | Default Value | About |\n'
                    markdownStr += '| --- | --- | --- | --- |\n'
                    for arg in macro.arguments:
                        markdownStr += '| {} | {} | {} | {} |\n'.format(arg.name,arg.type,arg.defaultValue,arg.docString)
                markdownStr += '\n\n'
        if len(SASProgram.uniqueDataItems) > 0:
            markdownStr += '## Datasets\n\n'
            markdownStr += '| Library | Name |\n'
            markdownStr += '| --- | --- |\n'
            for dataItem in SASProgram.uniqueDataItems:
                markdownStr += '| {} | {} |\n'.format(dataItem[0],dataItem[1])
            markdownStr += '\n\n'
            
        markdownStr += '## Full code:\n\n<details><summary>Show/Hide</summary>\n\n'
        markdownStr += '~~~~sas\n\n'
        markdownStr += SASProgram.rawProgram
        markdownStr += '\n\n~~~~\n\n'
        markdownStr += '</details>\n\n'
        markdownStr += '## Properties\n\n'
        markdownStr += '| Meta | Property |\n| --- | --- |\n'
        markdownStr += '| **Author:** | |\n'
        markdownStr += '| **Path:** | *{}* |\n'.format(SASProgram.filePath)
        markdownStr += '| **Last updated:** | *{}* |\n'.format(SASProgram.LastUpdated)

        return markdownStr

    def buildMacroIndex(self):
        markdownStr = '# Macro index\n'
        for path,macro in self.projectMacros.items():
            markdownStr += '## {}\n'.format(macro.name)
            markdownStr += '*Found in: [{}]({})*\n'.format(os.path.splitext(os.path.basename(path))[0],re.sub('\s','',os.path.splitext(os.path.basename(path))[0]+'.md'))
            markdownStr += '### About\n'
            markdownStr += '{}\n\n'.format(macro.docString)
            if len(macro.help)>0:
                markdownStr += '### Help\n'
                markdownStr += '{}\n\n'.format(macro.help)
            if len(macro.arguments)>0:
                markdownStr += '### Arguments\n\n'
                markdownStr += '| Name | Type | Default Value | About |\n'
                markdownStr += '| --- | --- | --- | --- |\n'
                for arg in macro.arguments:
                    markdownStr += '| {} | {} | {} | {} |\n'.format(arg.name,arg.type,arg.defaultValue,arg.docString)
            markdownStr += '\n\n'
        return markdownStr
