import re
import datetime

reg = []
branch = []
identifier = []
#lineCounter to track lines
lineNum = 0
#counter to track errors
error = 0
location = input("Enter the path to the file you want to open: ")
read = open(location,'r').read()
writeFile = open(location[:-4]+'.log','w')
#create Heading
writeFile.write("\nMAL error report\n"+location+"\n"+str(datetime.datetime.now())+"\nBradley Isaacs\nCS 3210\n")
#create section
writeFile.write("\n-------------\n")
writeFile.write("\noriginal MAL program listing:\n\n")
for line in read.splitlines():
    #increment lineCounter
    lineNum += 1
    writeFile.write(str(lineNum)+". "+line+"\n")
#end first section


#section strip/remove comments and whitespace
writeFile = open(location[:-4]+'.log','a') #'a' append to end of txt rather than overwrite
writeFile.write("\n-------------\n")
writeFile.write("\nstripped MAL program listing:\n\n")
#reset lineNum
lineNum = 0
for line in read.splitlines():
    #creatle list that slipts code and inline comments
    inLine = re.split(';',line)
    if len(inLine) > 1:
        del inLine[-1]
    #Combine back into string
    com = ' '.join(inLine)
    #increment lineCounter
    lineNum += 1
    # if not line.strip (if blank line) replace with no line
    # else if ; is first it is a comment replace with no line
    # else print with line number
    if not line.strip():
        writeFile.write("")
    elif line[0] == ";":
        writeFile.write("")
    else:
        writeFile.write(str(lineNum)+". "+com+"\n")
#end of not striped report section

#error methods
# Swicth funtion which returns the number of registers/destionations of the given operation
def operands(x, y):
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
            return y
# Swicth funtion which returns true if a valid MAL operation
def validOperation(x):
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
# check if valid octal literal: Any digit can not be more than 7
def validLiteral(x, y):
    if x == "LOADI":
        for digit in y:
            print(digit)
            if int(digit) > 7:
                return False
    return True
# check if valid label: must not exceed langth 5 or have any numbers
def validLabel(y):
    y = y[:-1]
    if len(y) < 6:
        return y.isalpha()
    elif len(y) > 5:
        return False
def validBranchCall(y):
    if len(y) < 6:
        return y.isalpha()
    elif len(y) > 5:
        return False
def validID(x):
    if len(x) < 6:
        return x.isalpha()
    elif len(x) > 5:
        return False


#append last section where we display errors
#reset lineNum for next section
lineNum = 0;
writeFile = open(location[:-4]+'.log','a')
writeFile.write("\n-------------\n")
writeFile.write("\nerror report listing:\n\n")

for line in read.splitlines():
    # creatle list that slipts code and inline comments
    inLine = re.split(';', line)
    if len(inLine) > 1:
        del inLine[-1]
    # Combine back into string
    com = ' '.join(inLine)
    #increment lineCounter
    lineNum += 1
    # Splits the MAL line into two words the operand (ADD, SUB, etc..) and another word of the registers/destionations (R0,R1,etc...)
    opCode = line.split()
    # if there is a branch decloration first strip into branch and remove from opCode
    if len(opCode) > 1:
        if opCode[0].endswith(':'):
            branch.append(opCode[0])
            opCode.remove(opCode[0])
    if len(opCode) > 2:
        if opCode[0]=='LOAD' or opCode[0]=='STORE':
            identifier.append(opCode[2])
            opCode.remove(opCode[2])
    # strip opCode till 2 words remain the opcode and the regs/labels/identifier
    if len(opCode) > 2:
        while True:
            opCode.remove(opCode[-1])
            if len(opCode) == 2:
                break
    # create a new list that holds regs/labels/identifier and remove word two from opCode
    if len(opCode) > 1:
        reg = re.split(",",opCode[-1])
        opCode.remove(opCode[-1])
    # if not line.strip (if blank line) skip it
    # else if ; is first char in the line, it is a comment skip it
    if not line.strip():
        # reset opCode, branch, indetifier and reg to be empty lists
        opCode = []
        reg = []
        branch = []
        identifier = []
        continue  # skip line if blank
    if line[0] == ";":
        # reset opCode, branch, indetifier and reg to be empty lists
        opCode = []
        reg = []
        branch = []
        identifier = []
        # if the line is now black skip it
        if not line.strip():
            # reset opCode, branch, indetifier and reg to be empty lists
            opCode = []
            reg = []
            branch = []
            identifier = []
            continue  # skip line if blank
        continue  # skip line if comment
    # checking for errors
    # ill-formed label
    if len(branch) > 0 and len(reg) > 0:
        if validLabel(branch[0]) == False:
            error += 1
            writeFile.write(str(lineNum) + ". " + com + "\n")
            # error detected
            if len(branch) > 0:
                writeFile.write("**error: invalid label " + branch[0] + "\n")
                # reset opCode, branch, indetifier and reg to be empty lists
                opCode = []
                reg = []
                branch = []
                identifier = []
                continue  # move to next line
            else:
                writeFile.write("**error: invalid label " + reg[-1] + "\n")
                # reset opCode, branch, indetifier and reg to be empty lists
                opCode = []
                reg = []
                branch = []
                identifier = []
                continue  # move to next line
        '''else: # if true is retured
            writeFile.write(str(lineNum) + ". " + com + "\n")
            # reset opCode, branch and reg to be empty lists
            opCode = []
            reg = []
            branch = []
            continue  # move to next line'''
    # Invalid Branch Call
    if opCode[0]=='BEQ' or opCode[0]=='BLT' or opCode[0]=='BGT' or opCode[0]=='BR':
        if len(reg) > 0:
            if validBranchCall(reg[-1]) == False:
                error += 1
                writeFile.write(str(lineNum) + ". " + com + "\n")
                writeFile.write("**error: invalid label call "+str(reg[-1])+"\n")
                # reset opCode, branch, indetifier and reg to be empty lists
                opCode = []
                reg = []
                branch = []
                identifier = []
                continue  # move to next line if error was found
    # invalid opcode
    if len(reg) > 0:
        if validOperation(opCode[0]) == False:
            error += 1
            writeFile.write(str(lineNum) + ". " + com + "\n")
            # error detected
            writeFile.write("**error: invalid opcode " + opCode[0] + "\n")
            # reset opCode, branch, indetifier and reg to be empty lists
            opCode = []
            reg = []
            branch = []
            identifier = []
            continue  # move to next line if error was found
    # too many operands
    if operands(opCode[0],len(reg)) < len(reg):
        error += 1
        writeFile.write(str(lineNum) + ". " + com + "\n")
        # create error message
        writeFile.write("**error: too many operands expected " + str(operands(opCode[0],len(reg))) + " found "+str(len(reg))+"\n")
        # reset opCode, branch, indetifier and reg to be empty lists
        opCode = []
        reg = []
        branch = []
        identifier = []
        continue # move to next line if error was found
    # too few operands
    if operands(opCode[0],len(reg)) > len(reg):
        error += 1
        writeFile.write(str(lineNum) + ". " + com + "\n")
        # create error message
        writeFile.write("**error: too few operands expected " + str(operands(opCode[0],len(reg))) + " found "+str(len(reg))+"\n")
        # reset opCode, branch, indetifier and reg to be empty lists
        opCode = []
        reg = []
        branch = []
        identifier = []
        continue  # move to next line if error was found
    # ill-formed identifier
    if opCode[0] == 'LOAD' or opCode[0] == 'STORE':
        if validID(identifier[0]) == False:
            error += 1
            writeFile.write(str(lineNum) + ". " + com + "\n")
            # create error message
            writeFile.write("**error: invalid identifier "+identifier[0]+" \n")
            # reset opCode, branch, indetifier and reg to be empty lists
            opCode = []
            reg = []
            branch = []
            identifier = []
            continue  # # move to next line if error was found
    # ill-formed literal
    if len(reg) > 0 and validLiteral(opCode[0], reg[-1]) == False:
        error += 1
        writeFile.write(str(lineNum) + ". " + com + "\n")
        # error detected
        writeFile.write("**error: ill-formed literal " + reg[-1] + " number is invalid for octal\n")
        # reset opCode, branch, indetifier and reg to be empty lists
        opCode = []
        reg = []
        branch = []
        identifier = []
        continue  # # move to next line if error was found
    # if no error is found just print the line with the line number
    else:
        writeFile.write(str(lineNum) + ". " + com + "\n")
        # reset opCode, branch, indetifier and reg to be empty lists
        opCode = []
        reg = []
        branch = []
        identifier = []

#write error total at end
writeFile.write('\n-----------------\n')
writeFile.write('\nTotal Errors = '+ str(error) +'\n')