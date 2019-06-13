
import sys
import logging
import argparse

from SASDocumentation.SASObjects.SASProject import SASProject


from .buildRules import *


def runRules(prj, loggers, mode='strict', adoLogging=False):
    args = (prj,loggers)
    kwargs = {'mode':mode,'adoLogging':adoLogging}

    ruleCamelCase(*args,**kwargs)
    ruleDescriptiveName(*args,**kwargs)

    ruleNoProcMeans(*args,**kwargs)
    ruleExplicitSortInput(*args,**kwargs)

    ruleMacroRequiresHelp(*args,**kwargs)
    ruleMacroRequiresDocString(*args,**kwargs)
    ruleMacroArgRequiresDocString(*args,**kwargs)
    ruleMacroLength(*args,**kwargs)
    ruleNoMacroLibname(*args,**kwargs)
    ruleUniqueMacroNames(*args,**kwargs)

    ruleCommentProgramRatio(*args,**kwargs)


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
  
    loggers = {'log':log,'ado':adolog}  

    log.info("Discovering SAS Code\n"+"="*20)

    prj = SASProject(args.path)

    log.info("\nBegining SAS Build Tests\n"+"="*24)

    runRules(prj,loggers,mode=mode,adoLogging=args.ado)

