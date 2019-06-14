
import sys
import logging
import argparse
import re

from SASDocumentation.SASObjects.SASProject import SASProject

from .buildRules import *

def runRules(prj, loggers, mode='strict', adoLogging=False, export=False):
    args = (prj,loggers)
    kwargs = {'mode':mode,'adoLogging':adoLogging}

    testSuite = []

    testSuite.append(ruleCamelCase(*args,**kwargs))
    testSuite.append(ruleDescriptiveName(*args,**kwargs))

    testSuite.append(ruleNoProcMeans(*args,**kwargs))
    testSuite.append(ruleExplicitSortInput(*args,**kwargs))

    testSuite.append(ruleMacroRequiresHelp(*args,**kwargs))
    testSuite.append(ruleMacroRequiresDocString(*args,**kwargs))
    testSuite.append(ruleMacroArgRequiresDocString(*args,**kwargs))
    testSuite.append(ruleMacroLength(*args,**kwargs))
    testSuite.append(ruleNoMacroLibname(*args,**kwargs))
    testSuite.append(ruleUniqueMacroNames(*args,**kwargs))

    testSuite.append(ruleCommentProgramRatio(*args,**kwargs))
    return testSuite
            

def setupLogs():
    log = logging.getLogger('SASBuildRules')
    log.setLevel(logging.DEBUG)

    adolog = logging.getLogger('ADOLog')
    adolog.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    consoleFmt = logging.Formatter('%(message)s')
    console.setFormatter(consoleFmt)
    log.addHandler(console)

    ado = logging.StreamHandler()
    adoFmt = logging.Formatter('##vso[%(adotags)s]%(message)s')
    ado.setFormatter(adoFmt)  
    adolog.addHandler(ado)
  
    return {'log':log,'ado':adolog}  

def runBuildRules(prj,mode='normal',ado=False,export=False):
    loggers = setupLogs()
    testSuite = runRules(prj,loggers,mode=mode,adoLogging=ado)
    
    overall = 'Succeeded'
    for test in testSuite:
        if test.result=='Failed':
            overall = 'Failed'
            break
        if test.result=='SucceededWithIssues':
            overall = 'SucceededWithIssues'

    if export:
        md = "# SAS Build Tests\n"
        md += '| Rule | Result | Error(s) |\n'
        md += '| --- | --- | --- |'
        for i,test in enumerate(testSuite):
            md += '\n| [{}](#id{}) | {} | {} |'.format(test.ruleName,i+1,test.result,test.errors)
        md += '\n\n'

        for test in testSuite:
            md += '\n## {} \n *{} - {} error(s)*\n'.format(test.ruleName,test.result,test.errors)
            if test.errors>0:
                if test.scope=="object":
                    for program,fails in test.failures.items():
                        md+='\n**{}:**\n\n'.format(program.name)
                        for fail in fails:
                            md+='{} - {} - Line: {}\n\n'.format(program.name,fail.id,fail.startLine)
                elif test.scope=="program":
                    for fail in test.failures:
                        md+='{}\n'.format(fail)

        return (overall,md)
    else:
        return overall

if __name__ == "__main__":
    
    parser=argparse.ArgumentParser(description='Process switches')
    parser.add_argument('-s','--strict',default=False,action='store_true', help='Set global build rule mode as strict. Will fail build on any error.')
    parser.add_argument('-a','--ado',default=False,action='store_true',help='Turn on ADO output logging')
    parser.add_argument('-p','--path',default='.',type=str,help='Path to SAS project, defaults to current working directory')

    args = parser.parse_args()
    if args.strict:
        mode='strict'
    else:
        mode='normal'
    
    loggers = setupLogs()

    loggers['log'].info("Discovering SAS Code\n"+"="*20)
    prj = SASProject(args.path)

    loggers['log'].info("\nBegining SAS Build Tests\n"+"="*24)

    runRules(prj,loggers,mode=mode,adoLogging=args.ado)

