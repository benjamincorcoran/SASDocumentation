import sys
import os 

from SASObjects.SASProgram import SASProgram

def writeMD(SASProgram):

	mdPath = SASProgram.filePath.replace('.sas','.md')
	with open(mdPath, 'w+') as out:
		out.write('# {}\n\n'.format(SASProgram.name))
		if len(SASProgram.libnames) > 0:
			out.write('## Libname(s):\n')
			out.write('| Name | Location |\n')
			out.write('| --- | --- |\n')
			for libname in SASProgram.libnames:
				out.write('| {} | {} |\n'.format(libname.name,libname.path))
			out.write('\n\n')
		if len(SASProgram.includes) > 0:
			out.write('## Include(s):\n')
			out.write('| Path |\n')
			out.write('| --- |\n')
			for include in SASProgram.includes:
				out.write('| {} |\n'.format(include.path))
			out.write('\n\n')
		if len(SASProgram.macros)> 0:
			out.write('## Macros(s):\n')
			for macro in SASProgram.macros:
				out.write('### {}\n'.format(macro.name))
				out.write('*{}*\n\n'.format(macro.docString))
				out.write('#### Argument(s):\n\n')
				out.write('| Name | Type | Default Value | About |\n')
				out.write('| --- | --- | --- | --- |\n')
				for arg in macro.arguments:
					out.write('| {} | {} | {} | {} |\n'.format(arg.name,arg.type,arg.defaultValue,arg.docString))
				out.write('\n\n')
		out.write('## Full code:\n')
		out.write('~~~~\n')
		out.write(SASProgram.rawProgram)
		out.write('\n~~~~')

		

if __name__ == "__main__":

	pm1 = SASProgram('example/code/whatmacro.sas')

	writeMD(pm1)
