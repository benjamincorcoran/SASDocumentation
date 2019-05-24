# CamelCase build rule
# All SAS variable names should be camelCase

import re
import sys

class ruleCamelCase(object):

    def __init__(self, SASProject, mode='normal'):

        self.regex = r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*|^[a-z]+$'
        self.strict = strict

        failures = dict()
        for SASProgram in SASProject.SASPrograms:
            results = self.assess(SASProgram)
           
            if len(results)!=0:
                failures[SASProgram]=results
                print("##vso[task.logissue type=warning]Warning: camelCase not followed for {} in {}".format(results,SASProgram.name))
        if len(failures) != 0 and mode='normal':
            print("##vso[task.complete result=SucceededWithIssues] SAS Build Rule: camelCase")
        elif len(failures) != and mode='strict':
            print("##vso[task.complete result=Failed] SAS Build Rule: camelCase")
 
    def assess(self, SASProgram):
        failures = []
        for item in SASProgram.inputs+SASProgram.outputs:
            if re.match(self.regex,item.dataset) is None:
                failures.append(item)
        return failures

            

