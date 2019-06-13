
class SASBuildRule(object):

    def __init__(self, SASProject, loggers, mode='normal', adoLogging=False):

        self.SASProject = SASProject
        self.loggers = loggers
        self.mode = mode

        self.isStrict = self.mode=='strict'
        self.adoLogging = adoLogging

        if self.isStrict:
            self.adoLevel = 'error'
        else:
            self.adoLevel = 'warning'

        self.define()
        self.run()
        
 
    def define(self):
        self.ruleName = 'Base Rule Object'
        self.scope = 'object'


    def log(self,msg,ado=None):
        if self.adoLogging is False:
            self.loggers['log'].info(msg)
        else:
            if ado is None:
                self.loggers['log'].info(msg)
            else:
                self.loggers['ado'].info(msg,extra=dict(adotags=ado))

    def run(self):

        self.log('\n\n'+self.ruleName+' test\n'+'-'*(len(self.ruleName)+5)+'\n')

        failures = dict()
        errors = 0

        if self.scope=='object':
            for SASProgram in self.SASProject.SASPrograms:
                testResult = self.assess(SASProgram)
            
                if len(testResult)!=0:
                    failures[SASProgram]=testResult
                    errors += len(testResult)
                    for fail in testResult:
                        self.logError(SASProgram.name,lineNumber=fail.startLine,dataObject=fail.id)

        elif self.scope=='program':
            for SASProgram in self.SASProject.SASPrograms:
                testResult = self.assess(SASProgram)
                if testResult == 'Fail':
                    errors += 1
                    self.logError(SASProgram.name)


        # elif self.scope=='project':
            
            # Do something


        self.logRuleResult(errors)

    
    def logError(self,path,lineNumber='',dataObject=''):
        adotags = 'task.logissue type={};sourcepath={};linenumber={}'.format(self.adoLevel,path,lineNumber)
        if lineNumber != '' and dataObject != '':
            self.log('Warning: {} requirement failed for "{}": \t{} [Line: {}]'.format(self.ruleName,dataObject,path,lineNumber),ado=adotags)
        else:
            self.log('Warning: {} requirement failed for "{}"'.format(self.ruleName,path),ado=adotags)

    
    def logRuleResult(self,errors):
        if self.isStrict and errors>0:
            result = 'Failed'
        elif errors>0:
            result = 'SucceededWithIssues'
        else:
            result = 'Succeeded'

        adotags = 'task.complete result={}'.format(result)
        self.log('SAS Build Rule "{}": {} - {} issues'.format(self.ruleName,result,errors),ado=adotags)

