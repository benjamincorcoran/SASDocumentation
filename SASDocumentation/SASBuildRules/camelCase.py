# CamelCase build rule
# All SAS variable names should be camelCase

import re
import sys
import logging

class ruleCamelCase(object):

    def __init__(self, SASProject, strict=False):

        self.regex = r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*|^[a-z]+$'
        self.strict = strict

        self.logger = logging.getLogger('Logger')
        self.logger.setLevel(logging.DEBUG)

        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.logger.addHandler(self.ch)

        failures = dict()
        for SASProgram in SASProject.SASPrograms:
            results = self.assess(SASProgram)
           
            if len(results)!=0:
                failures[SASProgram]=results
                self.logger.warning("##vso[task.logissue type=warning]Warning: camelCase not followed for {} in {}".format(results,SASProgram.name))
        if len(failures) != 0:
            self.logger.warning("##vso[task.complete result=SucceededWithIssues] SAS Build Rule: camelCase")

    def assess(self, SASProgram):
        failures = []
        for item in SASProgram.inputs+SASProgram.outputs:
            if re.match(self.regex,item.dataset) is None:
                failures.append(item)
        return failures

            

