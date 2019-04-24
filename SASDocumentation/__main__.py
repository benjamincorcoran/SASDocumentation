import sys
import os 
import re
import pkg_resources
import shutil

import sphinx.cmd.quickstart as quickstart
import sphinx.cmd.build as build

from .SASObjects.SASProject import SASProject
from .SASAnalysis.SASFlowChart import SASFlowChart

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
		sphinxResource = pkg_resources.resource_filename('SASDocumentation', 'Sphinx')

		quickstart.main(['-q',
						 '--project={}'.format(path),
						 '--author=corcobe',
						 '--batchfile',
						 '--template={}/sphinxTemplate'.format(sphinxResource),
						 out])

		shutil.rmtree(os.path.join(out,'_static'))
		shutil.copytree(os.path.join(sphinxResource,'sphinxStatic'),os.path.join(out,'_static'))

		project = SASProject(path)
		project.buildProject(out)

		build.main(['-M','html',out,os.path.join(out,'_build')])




