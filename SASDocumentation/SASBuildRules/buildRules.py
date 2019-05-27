
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
        super().__init__(SASProject, logger, ruleName='No Proc Means', mode=mode)

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