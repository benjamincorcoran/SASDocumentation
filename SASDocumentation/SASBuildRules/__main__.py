
import sys
import logging

from SASDocumentation.SASObjects.SASProject import SASProject


from .buildRules import *

if __name__ == "__main__":
    
    mode = sys.argv[1]
    path = '.'

    log = logging.getLogger('SASBuildRules')
    log.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    consoleFmt = logging.Formatter('%(levelname)s - %(message)s %(additional)s')
    console.setFormatter(consoleFmt)
    log.addHandler(console)

    ado = logging.StreamHandler()
    adoFmt = logging.Formatter('##vso[%(adotags)s]%(message)s')
    ado.setFormatter(adoFmt)  
    log.addHandler(ado)

    prj = SASProject(path)

    ruleCamelCase(prj, log, mode=mode)
    ruleNoProcMeans(prj, log, mode=mode)
    ruleExplicitSortInput(prj, log, mode=mode)
    ruleMacroRequiresHelp(prj, log, mode=mode)
    ruleMacroRequiresDocString(prj, log, mode=mode)
    ruleMacroArgRequiresDocString(prj, log, mode=mode)