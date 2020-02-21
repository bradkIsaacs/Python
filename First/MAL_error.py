import re

reg = []
#Get MAL line
test = input("Enter a MAL commant ")
#Splits the MAL line into two words the operand (ADD, SUB, etc..) and another word of the registers/destionations (R0,R1,etc...)
opCode = test.split()
#Splits the registers/destionations word by a comma making two or three words and stores in reg list
#if opCode isn't atleast 2 in length (2 words long) reg will remain empty
if len(opCode) > 1:
    reg = re.split(',', opCode[1])
#Removes registers/destionations word from opCode list
#if opCode isn't atleast 2 in length (2 words long) don't remove the second word
print(reg)
if len(opCode) > 1:
    opCode.remove(opCode[1])

#Swicth funtion which returns the number of registers/destionations of the given operation
def operation_func(x):
    if x == "LOAD": return 2
    elif x == "LOADI" : return 2
    elif x == "STORE" : return 2
    elif x == "ADD" : return 3
    elif x == "INC" : return 1
    elif x == "SUB" : return 3
    elif x == "DEC" : return 1
    elif x == "BEQ" : return 3
    elif x == "BLT" : return 3
    elif x == "BGT" : return 3
    elif x == "BR" : return 1
#end of switch

#if return value from switch is greater than the length of reg somthing is missing
#else everything is fine
if operation_func(opCode[0]) > len(reg):
    print("Missing Registar or Destination decloration")
else :
    print("MAL line passed no errors")