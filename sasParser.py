import sys
import os 


from SASObjects.SASProgram import SASProgram

if __name__ == "__main__":

	pm1 = SASProgram('example/code/macro.sas')
	print(pm1)
	print(pm1.libnames)
	print(pm1.macros)
	print(pm1.macros[0].help)
	print(pm1.macros[0])
