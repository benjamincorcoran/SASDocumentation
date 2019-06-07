
class SASBuildRule(object):

    def __init__(self, SASProject, loggers, ruleName='', mode='normal', adoLogging=False):

        self.loggers = loggers
        self.mode = mode
        self.isStrict = self.mode=='strict'
        self.adoLogging = adoLogging

        self.name=ruleName

        if self.isStrict:
            self.adoLevel = 'error'
        else:
            self.adoLevel = 'warning'

        self.log('\n\n'+ruleName+' test\n'+'-'*(len(ruleName)+5)+'\n')

        failures = dict()
        errors = 0

        for SASProgram in SASProject.SASPrograms:
            testResult = self.assess(SASProgram)
           
            if len(testResult)!=0:
                failures[SASProgram]=testResult
                errors += len(testResult)
                for fail in testResult:
                    if fail == "programFailure":
                        self.logError(SASProgram.name)
                    else:
                        self.logError(SASProgram.name,lineNumber=fail.startLine,dataObject=fail.id)


        self.logRuleResult(errors)
 
    def log(self,msg,ado=None):
        if self.adoLogging is False:
            self.loggers['log'].info(msg)
        else:
            if ado is None:
                self.loggers['log'].info(msg)
            else:
                self.loggers['ado'].info(msg,extra=dict(adotags=ado))

    def logError(self,path,lineNumber='',dataObject=''):
        adotags = 'task.logissue type={};sourcepath={};linenumber={}'.format(self.adoLevel,path,lineNumber)
        if lineNumber != '' and dataObject != '':
            self.log('Warning: {} requirement failed for "{}": \t{} [Line: {}]'.format(self.name,dataObject,path,lineNumber),ado=adotags)
        else:
            self.log('Warning: {} requirement failed for "{}"'.format(self.name,path),ado=adotags)

    def logRuleResult(self,errors):
        if self.isStrict and errors>0:
            result = 'Failed'
        elif errors>0:
            result = 'SucceededWithIssues'
        else:
            result = 'Succeeded'

        adotags = 'task.complete result={}'.format(result)
        self.log('SAS Build Rule "{}": {} - {} issues'.format(self.name,result,errors),ado=adotags)

