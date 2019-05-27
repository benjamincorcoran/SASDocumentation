# CamelCase build rule
# All SAS variable names should be camelCase

import re
import sys

class ruleCamelCase(object):

    def __init__(self, SASProject, logger, mode='normal'):

        self.logger = logger
        self.mode = mode
        self.isStrict = self.mode=='strict'

        if self.isStrict:
            self.adoLevel = 'error'
        else:
            self.adoLevel = 'warning'

        self.regex = r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*|^[a-z]+$'

        failures = dict()
        errors = 0
        for SASProgram in SASProject.SASPrograms:
            results = self.assess(SASProgram)
           
            if len(results)!=0:
                failures[SASProgram]=results
                errors += len(results)
                for dataObject in results:
                    self.logError(SASProgram.name,dataObject.startLine,dataObject=dataObject.id)

        self.logRuleResult(errors)
 
    def logError(self,path,lineNumber,dataObject=''):
        adotags = 'task.logissue type={};sourcepath={};linenumber={}'.format(self.adoLevel,path,lineNumber)
        additional = ': \t{} [Line: {}]'.format(path,lineNumber)
        info = dict(adotags=adotags,additional=additional)
        self.logger.warning('camelCase requirement failed for "{}"'.format(dataObject),extra=info)

    def logRuleResult(self,errors):
        if self.isStrict and errors>0:
            result = 'Failed'
        elif errors>0:
            result = 'SucceededWithIssues'
        else:
            result = 'Succeeded'

        adotags = 'task.complete result={}'.format(result)
        info = dict(adotags=adotags,additional='')
        self.logger.info('SAS Build Rule "camelCase": {} - {} issues'.format(result,errors),extra=info)



    def assess(self, SASProgram):
        failures = []
        for item in SASProgram.inputs+SASProgram.outputs:
            if re.match(self.regex,item.dataset) is None:
                failures.append(item)
        return failures

            

