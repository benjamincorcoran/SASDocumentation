import re

class SASLibname(object):

    def __init__(self,rawStr):
        self.name = re.findall(r"libname (.*?) ['\"].*?['\"]",rawStr)[0]
        self.path = re.findall(r"libname .*? ['\"](.*?)['\"]",rawStr)[0]

    def __str__(self):
        return '{} - {}'.format(self.name,self.path)

    def __repr__(self):
        return self.name