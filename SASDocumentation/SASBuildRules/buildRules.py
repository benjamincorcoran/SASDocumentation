
import re
import sys

from .buildRuleObject import SASBuildRule

class ruleCamelCase(SASBuildRule):
    '''
    camelCase build rule
    All SAS variable names should be camelCase
    '''
    def define(self):
        self.ruleName = 'camelCase'
        self.scope = 'object'

    def assess(self, SASProgram):  
        camelCaseRegex = r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*|^[a-z]+$'
        failures = []
        for item in SASProgram.inputs+SASProgram.outputs:
            if re.match(camelCaseRegex,item.dataset) is None:
                failures.append(item)
        return failures

class ruleDescriptiveName(SASBuildRule):
    '''
    Descriptive Name build rule
    All SAS Variable names should be descriptive
    '''
    def define(self):
        self.ruleName = 'Descriptive naming'
        self.scope = 'object'

    def assess(self, SASProgram):
        descriptiveRegex = '[a-zA-Z]{4}'
        failures = []
        for item in SASProgram.inputs+SASProgram.outputs:
            if re.match(descriptiveRegex,item.dataset) is None:
                failures.append(item)
        return failures

class ruleNoProcMeans(SASBuildRule):
    '''
    No Proc Means
    Proc Summary should be used in place of a proc mean
    '''
    def define(self):
        self.ruleName = 'PROC MEAN disallowed'
        self.scope = 'object'

    def assess(self, SASProgram):
        failures = [x for x in SASProgram.procedures if re.match(r'mean',x.procedure,re.IGNORECASE) is not None]
        return failures
            

class ruleExplicitSortInput(SASBuildRule):
    '''
    Explicit Sort Input
    Proc sorts must have an explicit data=
    '''
    def define(self):
        self.ruleName = 'Explicit sort input'
        self.scope = 'object'

    def assess(self, SASProgram):
        sorts = [x for x in SASProgram.procedures if re.match(r'sort',x.procedure,re.IGNORECASE) is not None]
        failures = [x for x in sorts if len(x.inputs)==0]
        return failures

class ruleMacroRequiresHelp(SASBuildRule):
    '''
    Macro requires help statement
    Macros must have a help statement
    '''
    def define(self):
        self.ruleName = 'Macro help'
        self.scope = 'object'

    def assess(self, SASProgram):
        failures = [x for x in SASProgram.macros if x.help=='']
        return failures

class ruleMacroRequiresDocString(SASBuildRule):
    '''
    Macro Requires doc string
    Macros must have a doc string
    '''
    def define(self):
        self.ruleName = 'Macro documentation'
        self.scope = 'object'

    def assess(self, SASProgram):
        failures = [x for x in SASProgram.macros if x.docString=='No documentation']
        return failures                                            

class ruleMacroArgRequiresDocString(SASBuildRule):
    '''
    Macro arguments require a doc string
    Macros arguments must have a doc string
    '''
    def define(self):
        self.ruleName = 'Macro arguement documentation'
        self.scope = 'object'

    def assess(self, SASProgram):
        failures = []
        for macro in SASProgram.macros:
            for arg in macro.arguments:
                if arg.docString == 'No description provided':
                    arg.id = '{} in {}'.format(arg.name, macro.id)
                    arg.startLine=macro.startLine
                    failures.append(arg)
        return failures

class ruleMacroLength(SASBuildRule):
    '''
    Macros should not exceed 200 lines
    '''
    def define(self):
        self.ruleName = 'Macro length limit'
        self.scope = 'object'
        
    def assess(self, SASProgram):
        failures = []
        for macro in SASProgram.macros:
            if macro.endLine - macro.startLine > 200:
                failures.append(macro)
        return failures

class ruleNoMacroLibname(SASBuildRule):
    '''
    Macros should not contain libname statement
    '''
    def define(self):
        self.ruleName = 'Macros should not contrain libnames'
        self.scope = 'object'
        
    def assess(self, SASProgram):
        failures = []
        for macro in SASProgram.macros:
            if SASProgram.parse('libname',macro.rawStr) is not None:
                failures.append(macro)
        return failures

class ruleCommentProgramRatio(SASBuildRule):
    '''
    Code should be well documented
    '''
    def define(self):
        self.ruleName = 'Comment/Program ratio > 0.25'
        self.scope = 'program'
        
    def assess(self, SASProgram):
        if len(''.join(SASProgram.rawComments))/len(SASProgram.unCommentedProgram) < 0.2:
            return 'Fail'
        else:
            return 'Pass'