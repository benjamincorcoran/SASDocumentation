import sys
import os
import re
import pkg_resources
import shutil
import m2r

import argparse
from datetime import datetime

import sphinx.cmd.quickstart as quickstart
import sphinx.cmd.build as build

from .SASObjects.SASProject import SASProject
from .SASAnalysis.SASFlowChart import SASFlowChart

from .SASBuildRules.__main__ import runBuildRules

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path',default='.',help='Path to the SAS project directory')
    parser.add_argument('-o','--outdir',default='./docs',help='Path to the output directory. This is where the documenatation will be stored. Default: ./docs/')
    parser.add_argument('-a','--author',default='',help='Set documentation author')

    args = parser.parse_args()
    path = args.path
    out = args.outdir
    author = args.author

    date = datetime.today().strftime('%d_%m_%Y')

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

    project = SASProject(path)
    SASTestResult,SASTestMD = runBuildRules(project,export=True)

    buildBadgeColor = {"Succeeded":"brightgreen",
                       "SucceededWithIssues":"orange",
                       "Failed":"red"}

    badges = [
        '.. image:: https://img.shields.io/badge/SAS_Tests-{}-{}.svg'.format(SASTestResult,buildBadgeColor[SASTestResult]),
        '.. image:: https://img.shields.io/badge/Last_Built-{}-green.svg'.format(date),
        '.. image:: https://img.shields.io/badge/Author-{}-blue.svg'.format(author.replace(' ','_'))
        ]


    if projectREADME != '' and projectTitle != path: 
        _readMeTitle = re.findall('^(#[^#\n]+)', projectREADME)[0]
        _readMeText = re.findall('^#[^#\n]+(.*)',projectREADME,flags=re.DOTALL)[0]
        if _readMeText == '':
            _readMeText = 'Stick a README.md file in the project folder to add text here.\n\n\n'
        
    elif projectTitle == path and projectREADME != '':
        _readMeTitle = ''
        _readMeText = projectREADME 
    
    else:
        _readMeTitle = ''
        _readMeText = '\n\nStick a README.md file in the project folder to add text here.\n\n\n'
    
    projectREADME = m2r.convert('\n'.join([_readMeTitle,'\n'.join(badges),_readMeText]))


    with open(indexPath, 'w') as o:
        o.write(projectREADME)
        o.write(defaultIndex)

    shutil.rmtree(os.path.join(out, 'source', '_static'))
    shutil.copytree(
        os.path.join(
            sphinxResource, 'sphinxStatic'), os.path.join(
            out,'source', '_static'))

    
    project.buildProject(out)

    with open(os.path.join(out,'source','code','_sasTests.rst'),'w') as o:
        o.write(m2r.convert(SASTestMD))

    build.main(['-M', 'html', os.path.join(out,'source'), os.path.join(out, 'build')])
