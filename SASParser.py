import sys
import os 
import re

from SASObjects.SASProgram import SASProgram

class SASParser(object):

	def __init__(self, codepath, docpath):

		self.codepath = codepath
		self.docpath = docpath 

		self.SASPrograms = []

		for root, dirs, files in os.walk(self.codepath):
			for name in files:
				if len(re.findall('\.sas$',name,flags=re.IGNORECASE))>0:
					SASfile = os.path.join(root,name)
					self.SASPrograms.append(SASProgram(SASfile))
		
		self.outDir = os.path.join(docpath,'source','code')
		
		if not os.path.exists(self.outDir):
			os.makedirs(self.outDir)
		for program in self.SASPrograms:
			self.writeMD(program,self.outDir)


	def writeMD(self,SASProgram,outpath):

		mdPath = os.path.join(outpath,re.sub('.sas$','.md',SASProgram.fileName,flags=re.IGNORECASE))
		with open(mdPath, 'w+') as out:
			out.write('# {}\n\n'.format(SASProgram.name))
			if SASProgram.about is not None:
				out.write('## About\n')
				out.write('{}\n\n'.format(SASProgram.about))
			if len(SASProgram.libnames) > 0:
				out.write('## Libname(s)\n\n')
				out.write('| Name | Location |\n')
				out.write('| --- | --- |\n')
				for libname in SASProgram.libnames:
					out.write('| {} | [{}]({}) |\n'.format(libname.name,libname.path,libname.posixPath))
				out.write('\n\n')
			if len(SASProgram.includes) > 0:
				out.write('## Include(s)\n\n')
				out.write('| Path |\n')
				out.write('| --- |\n')
				for include in SASProgram.includes:
					out.write('| [{}]({}) |\n'.format(include.path,include.posixPath))
				out.write('\n\n')
			if len(SASProgram.macros)> 0:
				out.write('## Macro(s)\n')
				for macro in SASProgram.macros:
					out.write('### {}\n'.format(macro.name))
					out.write('#### About\n')
					out.write('{}\n\n'.format(macro.docString))
					if len(macro.help)>0:
						out.write('#### Help\n')
						out.write('{}'.format(macro.help))
					if len(macro.arguments)>0:
						out.write('#### Argument(s)\n\n')
						out.write('| Name | Type | Default Value | About |\n')
						out.write('| --- | --- | --- | --- |\n')
						for arg in macro.arguments:
							out.write('| {} | {} | {} | {} |\n'.format(arg.name,arg.type,arg.defaultValue,arg.docString))
					out.write('\n\n')
			if len(SASProgram.datasets) > 0:
				out.write('## Datasets(s)\n\n')
				out.write('| Library | Name |\n')
				out.write('| --- | --- |\n')
				for dataset in SASProgram.datasets:
					out.write('| {} | {} |\n'.format(dataset.library,dataset.name))
				out.write('\n\n')

			out.write('## Full code:\n\n<details><summary>Show/Hide</summary>\n\n')
			out.write('~~~~sas\n\n')
			out.write(SASProgram.rawProgram)
			out.write('\n\n~~~~\n\n')
			out.write('</details>\n\n')
			out.write('## Properties\n\n')
			out.write('| Meta | Property |\n| --- | --- |\n')
			out.write('| **Author:** | |\n')
			out.write('| **Path:** | *{}* |\n'.format(SASProgram.filePath))
			out.write('| **Last updated:** | *{}* |\n'.format(SASProgram.LastUpdated))

		
if __name__ == "__main__":
	
	parser = SASParser('example','example/docs')

