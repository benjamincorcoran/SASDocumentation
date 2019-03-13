import re

class SASInclude(object):

    def __init__(self,rawStr):

        self.path= re.findall(r"include ['\"](.*?)['\"]",rawStr)[0]

    def __str__(self):
        return self.path
        
    def __repr__(self):
        return self.path