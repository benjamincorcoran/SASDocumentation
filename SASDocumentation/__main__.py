import sys
import os
import re
import pkg_resources
import shutil
import m2r

import argparse

import sphinx.cmd.quickstart as quickstart
import sphinx.cmd.build as build

from .SASObjects.SASProject import SASProject
from .SASAnalysis.SASFlowChart import SASFlowChart

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path',default='.',help='Path to the SAS project directory')
    parser.add_argument('-o','--outdir',default='./docs',help='Path to the output directory. This is where the documenatation will be stored. Default: ./docs/')
    parser.add_argument('-a','--author',default='',help='Set documentation author')

    args = parser.parse_args()
    path = args.path
    out = args.outdir
    author = args.author

    sphinxResource = pkg_resources.resource_filename(
        'SASDocumentation', 'Sphinx')

    readmePath = os.path.join(path, 'README.md')
    if os.path.exists(readmePath):
        with open(readmePath) as r:
            projectREADME = r.read()
        try:
            projectTitle = re.findall('^#([^#\n]+)', projectREADME)[0]
        except BaseException:
            projectTitle = path
    else:
        projectREADME = ""
        projectTitle = path

    quickstart.main(['-q',
                        '--project={}'.format(projectTitle),
                        '--author={}'.format(author),
                        '--no-makefile',
                        '--sep',
                        '--template={}\sphinxTemplate'.format(
                            sphinxResource),
                        out])

    indexPath = os.path.join(out,'source','index.rst')
    _defaultIndex = os.path.join(out,'source','_defaultIndex.rst')
    
    batchPath = os.path.join(out,'make.bat')
    with open(batchPath,'w+') as batch:
        batch.write('python -m SASDocumentation "{}" "{}"'.format(os.path.abspath(path), os.path.abspath(out)))

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
            o.write(
                'Stick a README.md file in the project folder to add text here.\n\n\n')
            o.write(defaultIndex)

    shutil.rmtree(os.path.join(out, 'source', '_static'))
    shutil.copytree(
        os.path.join(
            sphinxResource, 'sphinxStatic'), os.path.join(
            out,'source', '_static'))

    project = SASProject(path)
    project.buildProject(out)

    build.main(['-M', 'html', os.path.join(out,'source'), os.path.join(out, 'build')])
