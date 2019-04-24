import sys
import os
import re
import pkg_resources
import shutil
import m2r

import sphinx.cmd.quickstart as quickstart
import sphinx.cmd.build as build

from .SASObjects.SASProject import SASProject
from .SASAnalysis.SASFlowChart import SASFlowChart


class SASParser(object):

    def __init__(self, codepath, docpath):

        self.codepath = codepath
        self.docpath = docpath

        self.outDir = os.path.join(docpath, 'source', 'code')

        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)

        with open(os.path.join(self.outDir, 'code.rst'), 'w+') as codeRST:
            codeRST.write(
                'Code\n====\n\n.. toctree::\n   :maxdepth: 2\n   :glob:\n\n   *')


if __name__ == "__main__":
    if len(sys.argv) > 2:

        path = sys.argv[1]
        out = sys.argv[2]
        sphinxResource = pkg_resources.resource_filename(
            'SASDocumentation', 'Sphinx')

        readmePath = os.path.join(path, 'README.md')
        if os.path.exists(readmePath):
            with open(readmePath) as r:
                projectREADME = r.read()
            try:
                projectTitle = re.findall('^#([^#\n]+)', projectREADME)[0]
            except:
                projectTitle = path
        else:
            projectREADME = ""
            projectTitle = path

        quickstart.main(['-q',
                         '--project={}'.format(projectTitle),
                         '--author=corcobe',
                         '--batchfile',
                         '--template={}/sphinxTemplate'.format(
                             sphinxResource),
                         out])

        indexPath = os.path.join(out, 'index.rst')
        _defaultIndex = os.path.join(out, '_defaultIndex.rst')

        if not os.path.exists(_defaultIndex):
            with open(indexPath) as i:
                defaultIndex = i.read()
            with open(_defaultIndex, 'w') as di:
                di.write(defaultIndex)
        else:
            with open(_defaultIndex) as i:
                defaultIndex = i.read()

        os.remove(indexPath)

        with open(indexPath, 'w') as o:
            if projectREADME != '':
                projectREADME = m2r.convert(projectREADME)
                o.write(projectREADME)
                o.write(defaultIndex)
            else:
                o.write('Stick a README.md file in the project folder to add text here.\n\n\n')
                o.write(defaultIndex)

        shutil.rmtree(os.path.join(out, '_static'))
        shutil.copytree(
            os.path.join(
                sphinxResource, 'sphinxStatic'), os.path.join(
                out, '_static'))

        project = SASProject(path)
        project.buildProject(out)

        build.main(['-M', 'html', out, os.path.join(out, '_build')])
