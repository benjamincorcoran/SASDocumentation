
import sys
from SASDocumentation.SASObjects.SASProject import SASProject
from .camelCase import ruleCamelCase

if __name__ == "__main__":
    path = '.'
    print(path)
    prj = SASProject(path)
    print(prj)
    ruleCamelCase(prj, strict=True)