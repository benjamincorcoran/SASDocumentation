import re

class SASArgument(object):
    '''
    SAS Argument Class
    
    Creates an object with the following properties

        Name: Name of the Argument given
        Type: Required or Optional
        DefaultValue: If type is optional then the default value
        DocString: Documentation String for the argument.
    '''

    def __init__(self,rawStr):

        reFlags = re.DOTALL|re.IGNORECASE
        self.name = re.sub('\s','',re.findall('(.*?)(?:[=\/\*]|$)',rawStr,reFlags)[0])
        
        if re.search('=',rawStr) is not None:
            self.type='Optional'
            defaultValue = re.findall('=([^\/]*)',rawStr,reFlags)

            if defaultValue is not None and len(defaultValue[0])>0:
                self.defaultValue=defaultValue[0]
            else:
                self.defaultValue='Not set'
        else:
            self.type='Required'
            self.defaultValue='Not set'

        if re.search('.*?\*(.*)\*',rawStr) is not None:
            self.docString = re.findall('.*?\*(.*)\*',rawStr,reFlags)[0]
        else:
            self.docString='No description provided'

    def __str__(self):
        _ = '{}\n - Type: {}\n - DefaultValue: {}\n - About: {}'.format(self.name,self.type,self.defaultValue,self.docString)
        return _
    
    def __repr__(self):
        return self.name
