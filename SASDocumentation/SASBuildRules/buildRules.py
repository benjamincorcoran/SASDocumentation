
import re
import sys

from .buildRuleObject import SASBuildRule

class ruleCamelCase(SASBuildRule):
    '''
    camelCase build rule
    All SAS variable names should be camelCase
    '''
    def __init__(self, SASProject, logger, mode='normal'):
        super().__init__(SASProject, logger, ruleName='camelCase', mode=mode)

    def assess(self, SASProgram):  
        camelCaseRegex = r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*|^[a-z]+$'
        failures = []
        for item in SASProgram.inputs+SASProgram.outputs:
            if re.match(camelCaseRegex,item.dataset) is None:
                failures.append(item)
        return failures

class ruleNoProcMeans(SASBuildRule):
    '''
    No Proc Means
    Proc Summary should be used in place of a proc mean
    '''
    def __init__(self, SASProject, logger, mode='normal'):
        super().__init__(SASProject, logger, ruleName='No proc means', mode=mode)

    def assess(self, SASProgram):
        failures = [x for x in SASProgram.procedures if re.match(r'mean',x.procedure,re.IGNORECASE) is not None]
        return failures
            

class ruleExplicitSortInput(SASBuildRule):
    '''
    Explicit Sort Input
    Proc sorts must have an explicit data=
    '''
    def __init__(self, SASProject, logger, mode='normal'):
        super().__init__(SASProject, logger, ruleName='Explicit sort input', mode=mode)

    def assess(self, SASProgram):
        sorts = [x for x in SASProgram.procedures if re.match(r'sort',x.procedure,re.IGNORECASE) is not None]
        failures = [x for x in sorts if len(x.inputs)==0]
        return failures

class ruleMacroRequiresHelp(SASBuildRule):
    '''
    Macro requires help statement
    Macros must have a help statement
    '''
    def __init__(self, SASProject, logger, mode='normal'):
        super().__init__(SASProject, logger, ruleName='Macro requires help statement', mode=mode)

    def assess(self, SASProgram):
        failures = [x for x in SASProgram.macros if x.help=='']
        return failures

class ruleMacroRequiresDocString(SASBuildRule):
    '''
    Macro Requires doc string
    Macros must have a doc string
    '''
    def __init__(self, SASProject, logger, mode='normal'):
        super().__init__(SASProject, logger, ruleName='Macro requires documentation', mode=mode)

    def assess(self, SASProgram):
        failures = [x for x in SASProgram.macros if x.docString=='No documentation']
        return failures                                            

class ruleMacroArgRequiresDocString(SASBuildRule):
    '''
    Macro arguments require a doc string
    Macros arguments must have a doc string
    '''
    def __init__(self, SASProject, logger, mode='normal'):
        super().__init__(SASProject, logger, ruleName='Macro arguement requires documentation', mode=mode)

    def assess(self, SASProgram):
        failures = []
        for macro in SASProgram.macros:
            for arg in macro.arguments:
                if arg.docString == 'No description provided':
                    arg.id = '{} in {}'.format(arg.name, macro.id)
                    arg.startLine=macro.startLine
                    failures.append(arg)
        return failures                                            