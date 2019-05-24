
import sys
from SASDocumentation.SASObjects.SASProject import SASProject
from .camelCase import ruleCamelCase

if __name__ == "__main__":
    path = '.'
    prj = SASProject(path)
    ruleCamelCase(prj, strict=True)