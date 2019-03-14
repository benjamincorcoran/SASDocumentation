import sys
import os 
import re

from SASObjects.SASProgram import SASProgram

def writeMD(SASProgram):

	mdPath = re.sub('.sas$','.md',SASProgram.filePath,flags=re.IGNORECASE)
	with open(mdPath, 'w+') as out:
		out.write('# {}\n\n'.format(SASProgram.name))
		if SASProgram.about is not None:
			out.write('## About:\n')
			out.write('{}\n\n'.format(SASProgram.about))
		if len(SASProgram.libnames) > 0:
			out.write('## Libname(s):\n')
			out.write('| Name | Location |\n')
			out.write('| --- | --- |\n')
			for libname in SASProgram.libnames:
				out.write('| {} | [{}]({}) |\n'.format(libname.name,libname.path,libname.posixPath))
			out.write('\n\n')
		if len(SASProgram.includes) > 0:
			out.write('## Include(s):\n')
			out.write('| Path |\n')
			out.write('| --- |\n')
			for include in SASProgram.includes:
				out.write('| [{}]({}) |\n'.format(include.path,include.posixPath))
			out.write('\n\n')
		if len(SASProgram.macros)> 0:
			out.write('## Macro(s):\n')
			for macro in SASProgram.macros:
				out.write('### {}\n'.format(macro.name))
				out.write('#### About:\n')
				out.write('{}\n\n'.format(macro.docString))
				if len(macro.help)>0:
					out.write('#### Help:\n')
					out.write('{}'.format(macro.help))
				if len(macro.arguments)>0:
					out.write('#### Argument(s):\n\n')
					out.write('| Name | Type | Default Value | About |\n')
					out.write('| --- | --- | --- | --- |\n')
					for arg in macro.arguments:
						out.write('| {} | {} | {} | {} |\n'.format(arg.name,arg.type,arg.defaultValue,arg.docString))
				out.write('\n\n')
		out.write('## Full code:\n')
		out.write('~~~~.sas\n')
		out.write(SASProgram.rawProgram)
		out.write('\n~~~~\n')
		
		out.write('| Meta | Property |\n| --- | --- |\n')
		out.write('| **Author:** | |\n')
		out.write('| **Path:** | *{}* |\n'.format(SASProgram.filePath))
		out.write('| **Last updated:** | *{}* |\n'.format(SASProgram.LastUpdated))

		

		

if __name__ == "__main__":

	for root, dirs,files in os.walk('example/code'):
		for name in files:
			if len(re.findall('\.sas$',name,flags=re.IGNORECASE))>0:
				sp = SASProgram(os.path.join(root,name))
				writeMD(sp)
