import re

lineNum = 0 #lineCounter to track lines
readFile = open('MAL_test','r').read()
original = [] # list that will store the original lines for section 1
striped = [] # list that will store the striped lines for section 2
error = [] # list that will store error lines for section 3

#Error methods
#ill-formed label
def illformedLabel (x):
    return
#Invalid opCode: opCode is not one of the MAL operations
def invalidOperation(x, z, q):
    if validOp(x) == False:
        error.append(str(z)+". "+q+" :"+x+" is not a valid operation")
#Too Many operands
def tooMany(x, y, z, q):
    if numberofOpts(x) < len(y):
        error.append(str(z) + ". " + q + " ;too many operands expected " + str(numberofOpts(x)) + " found " + str(len(y)))
#Too Few operands
def tooFew(x, y, z, q):
    if numberofOpts(x) > len(y):
        error.append(str(z)+". "+q+" ;too few operands expected "+str(numberofOpts(x))+" found "+str(len(y)))
#ill-formed Identifier: Name cannot have numbers or belonger than 5 chars
def illformedID(x):
    return
#ill-formed literal
def illformedLiteral(x):
    return
#Is the Opcode a valid selection
def validOp(x):
    if x == "LOAD":
        return True
    elif x == "LOADI":
        return True
    elif x == "STORE":
        return True
    elif x == "ADD":
        return True
    elif x == "INC":
        return True
    elif x == "SUB":
        return True
    elif x == "DEC":
        return True
    elif x == "BEQ":
        return True
    elif x == "BLT":
        return True
    elif x == "BGT":
        return True
    elif x == "BR":
        return True
    else:
        return False
#required number of operands
def numberofOpts(x):
    if x == "LOAD":
        return 2
    elif x == "LOADI":
        return 2
    elif x == "STORE":
        return 2
    elif x == "ADD":
        return 3
    elif x == "INC":
        return 1
    elif x == "SUB":
        return 3
    elif x == "DEC":
        return 1
    elif x == "BEQ":
        return 3
    elif x == "BLT":
        return 3
    elif x == "BGT":
        return 3
    elif x == "BR":
        return 1
    else:
        return 0
#runs each line through all checks and appends to list until fully read: x is the dummy for the operation code, y for the operands list, z for the lineNum, q is the uncommeted line
def makeList(x, y, z, q):
    invalidOperation(x, z, q)
    tooFew(x, y, z, q)
    tooMany(x, y, z, q)
    if len(error) < z:
        error.append(str(z) + ". " + q)
#method strips all whitespace and comments
def stripLines (x, y):
    # creatle list that slipts code and inline comments
    inLine = re.split(';', x)
    if len(inLine) > 1:
        del inLine[-1]
    # Combine back into string
    combine = ' '.join(inLine)
    striped.append(str(y)+'. '+x)
    print(striped)

for line in readFile.splitlines():
    # increment lineCounter
    lineNum += 1
    # append com to original list
    original.append(str(lineNum)+". "+line)
    # Splits the MAL line into two words the operand (ADD, SUB, etc..) and another word of the registers/destionations (R0,R1,etc...)
    opCode = line.split()
    # Splits the registers/destionations word by a comma making two or three words and stores in reg list
    # if opCode isn't atleast 2 in length (2 words long) reg will remain empty because there are no operands
    if len(opCode) > 1:
        operands = re.split(',', opCode[1])
    # Removes registers/destionations word from opCode list
    # if opCode isn't atleast 2 in length (2 words long) don't remove the second word
    if len(opCode) > 1:
        opCode.remove(opCode[1])
    #print(str(opCode)+""+str(operands))
    #opCode list holds the operation (ADD,SUB,etc...) operands list holds the operands (R1,etc... Lab)
    #makeList(opCode[0], operands, lineNum, com)
    stripLines(line, lineNum)
    #reset opCode and operands to be empty lists
    opCode = []
    operands = []