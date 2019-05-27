
class SASBuildRule(object):

    def __init__(self, SASProject, logger, ruleName='', mode='normal'):

        self.logger = logger
        self.mode = mode
        self.isStrict = self.mode=='strict'

        self.name=ruleName

        if self.isStrict:
            self.adoLevel = 'error'
        else:
            self.adoLevel = 'warning'

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
        self.logger.warning('{} requirement failed for "{}"'.format(self.name,dataObject),extra=info)

    def logRuleResult(self,errors):
        if self.isStrict and errors>0:
            result = 'Failed'
        elif errors>0:
            result = 'SucceededWithIssues'
        else:
            result = 'Succeeded'

        adotags = 'task.complete result={}'.format(result)
        info = dict(adotags=adotags,additional='')
        self.logger.info('SAS Build Rule "{}": {} - {} issues'.format(self.name,result,errors),extra=info)

