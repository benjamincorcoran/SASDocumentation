import sys
import os 
import re

from SASObjects.SASProject import SASProject

class SASParser(object):

	def __init__(self, codepath, docpath):

		self.codepath = codepath
		self.docpath = docpath 

		self.outDir = os.path.join(docpath,'source','code')

		if not os.path.exists(self.outDir):
			os.makedirs(self.outDir)

		with open(os.path.join(self.outDir,'code.rst'),'w+') as codeRST:
			codeRST.write('Code\n====\n\n.. toctree::\n   :maxdepth: 2\n   :glob:\n\n   *')

		
if __name__ == "__main__":
	if len(sys.argv)>2:
		path = sys.argv[1]
		out = sys.argv[2]
		project = SASProject(path)
		project.buildProject(out)


