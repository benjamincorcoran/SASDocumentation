import sys
import os 


from SASObjects.SASProgram import SASProgram

if __name__ == "__main__":

	pm1 = SASProgram('example/code/writexl.sas')
	print(pm1)
	print(pm1.macros)
	print(pm1.macros[0].help)
	print(pm1.macros[0])
