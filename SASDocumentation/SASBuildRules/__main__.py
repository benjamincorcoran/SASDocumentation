
import sys
import logging

from SASDocumentation.SASObjects.SASProject import SASProject


from .buildRules import *


def runRuleTests(prj, loggers, mode='strict', adoLogging=False):
    #ruleCamelCase(prj, loggers, ruleName='camelCase',  mode=mode, adoLogging=adoLogging)
    ruleNoProcMeans(prj, loggers, ruleName='PROC MEAN disallowed',mode=mode, adoLogging=adoLogging)
    ruleExplicitSortInput(prj, loggers, ruleName='Explicit sort input', mode=mode, adoLogging=adoLogging)
    # ruleMacroRequiresHelp(prj, loggers, ruleName='Macro help', mode=mode, adoLogging=adoLogging)
    # ruleMacroRequiresDocString(prj, loggers, ruleName='Macro documentation', mode=mode, adoLogging=adoLogging)
    # ruleMacroArgRequiresDocString(prj, loggers, ruleName='Macro arguement documentation', mode=mode, adoLogging=adoLogging)


if __name__ == "__main__":
    
    mode = sys.argv[1]
    path = r'.'

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

    prj = SASProject(path)

    log.info("\nBegining SAS Build Tests\n"+"="*24)
    runRuleTests(prj,loggers,mode='strict',adoLogging=True)

