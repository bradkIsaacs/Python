import re

test = input("Enter a MAL commant ")
print(test)
opCode = test.split()
print(opCode)
reg = re.split(',', opCode[1])
opCode.remove(opCode[1])
print(reg)
print(opCode)