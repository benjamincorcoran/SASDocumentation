
import sys
from SASDocumentation.SASObjects.SASProject import SASProject
from .camelCase import ruleCamelCase

if __name__ == "__main__":
    
    mode = sys.argv[1]
    path = '.'

    prj = SASProject(path)

    ruleCamelCase(prj, mode=mode)