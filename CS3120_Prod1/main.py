#Bradley Isaacs
#Project 1: MAL Error Report
#CS 3210-001 

import os.path
import datetime

lineNum = 0
errors = 0
branch = []
opCode = []
immediate = []
branchCall = []
identifier = []
length = 0
found = False
# error type counters
illLabel = 0
invalidCode = 0
manyOp = 0
fewOp = 0
illID = 0
illLit = 0
# list to keep track of warnings
bCall = []
bLabel = []
# list that holds every line as an element
endStatement = []

def getFile():
    while True:
        file = input("Enter the file you wish to open:")
        if os.path.exists(file) == False: # file does not exist
            print("Sorry, file not found.")
            # better try again... Return to the start of the loop
            continue
        else: # file is found, leave the loop and return file
            return file
            break
def illLabelBranch(x): # x is the branch list
    str = x[0] # if branch list is not empty store first word in str
    noColon = str[:-1] # Removes the colon from the word
    if len(noColon) < 5 and noColon.isalpha(): # if less than 5 charaters and no numbers return true
        return True
    else:
        return False
def illLabelBranchCall(x): # x is the branchCall list
    bc = x[0] # if branch list is not empty store first word in bc
    if len(bc) < 5 and bc.isalpha(): # if less than 5 charaters and no numbers return true
        return True
    else:
        return False
def invalidopCode(x): # x is the operational code
    if x == "LOADI":
        return True
    elif x == 'LOAD':
        return True
    elif x == 'STORE':
        return True
    elif x == "ADD":
        return True
    elif x == 'INC':
        return True
    elif x == 'SUB':
        return True
    elif x == 'DEC':
        return True
    elif x == 'BEQ':
        return True
    elif x == "BLT":
        return True
    elif x == 'BGT':
        return True
    elif x == 'BR':
        return True
    elif x == 'NOOP':
        return True
    elif x == 'END':
        return True
    else:
        return False
def numberofOperands(x):
    if x == "LOADI":
        return 2
    elif x == 'LOAD':
        return 2
    elif x == 'STORE':
        return 2
    elif x == "ADD":
        return 3
    elif x == 'INC':
        return 1
    elif x == 'SUB':
        return 3
    elif x == 'DEC':
        return 1
    elif x == 'BEQ':
        return 3
    elif x == "BLT":
        return 3
    elif x == 'BGT':
        return 3
    elif x == 'BR':
        return 1
    elif x == 'NOOP':
        return 0
    elif x == 'END':
        return 0
    else:
        return False
def validId(x): #x is the identifier branch
    if len(x) <= 5 and x.isalpha(): # if less than 5 charaters and no numbers return true
        return True
    else:
        return False
def validImmediate(x):
    for i in x:
        if int(i) > 7:
            return False
def heading(x): # x is the location of the file provided by the user
    writeFile = open(x[:-4]+'.log', 'w')
    writeFile.write('\nError Report for: '+x[:-4]+'\n')
    writeFile.write(x + '\n')
    writeFile.write(x[:-4]+'.log\n')
    writeFile.write(str(datetime.datetime.now())+'\n')
    writeFile.write('Bradley Isaacs \n')
    writeFile.write('CS 3210\n')
    writeFile.write('\n--------------------------------------\n')
def section1(x, y, z): # x is the location of the file provided by the user, y file that is to be read, z is lineNum
    writeFile = open(x[:-4] + '.log', 'a') # a for append to exsisting file
    writeFile.write('\noriginal MAL Program listing\n\n')
    for line in y.splitlines():
        #inc z
        z+= 1
        writeFile.write(str(z)+'. '+line+'\n')
    writeFile.write('\n-------------------------------------------------\n\n')
def section2(x, y, z): # x is the location of the file provided by the user, y file that is to be read, z is lineNum
    writeFile = open(x[:-4] + '.log', 'a') # a for append to exsisting file
    writeFile.write('stripped MAL Program listing\n\n')
    for line in y.splitlines():
        #inc z
        z+= 1
        # if lines begins with a semi colon it must be a comment line so skip the line
        if line.startswith(";"):
            continue
        # skip blank lines
        if not line.strip():
            continue
        # if not blank or a comment line there might be an inline comment contiune to split by space
        code = line.split()
        # if there is a semi colon there this should be an inLine comment
        if ';' in code:
            # inLine comment found find the index at which the comments starts
            index = code.index(';')
            # keep removing the last word in code until the index containing the semi colon is reached
            while len(code) > index:
                del code[-1]
        stripedLine = ' '.join(code)
        # double check if any blank lines remain remove blank lines
        if not stripedLine.strip():
            continue
        code = stripedLine.split()
        stringCode = ' '.join(code)
        writeFile.write(str(z)+'. '+stringCode+'\n')
    writeFile.write('\n-------------------------------------------------\n\n')

# main program
location = getFile()
read = open(location, 'r').read()
heading(location)
section1(location, read, lineNum)
section2(location, read, lineNum)
# start of section 3
writeFile = open(location[:-4] + '.log', 'a') # a for append to exsisting file
writeFile.write('error report listing\n\n')
for line in read.splitlines():
    # imcriment lineNum
    lineNum += 1
    # if lines begins with a semi colon it must be a comment line so skip the line
    if line.startswith(";"):
        continue
    # remove blank lines
    if not line.strip():
        continue
    code = line.split()
    # if there is a semi colon there this should be an inLine comment
    if ';' in code:
        # inLine comment found find the index at which the comments starts
        index = code.index(';')
        # keep removing the last word in code until the index containing the semi colon is reached
        while len(code) > index:
            del code[-1]
    stripedLine = ' '.join(code)
    # append the stripedline read to endStatement lstrip remove all leading spaces
    endStatement.append(stripedLine.lstrip())
    # double check if any blank lines remain remove blank lines
    if not stripedLine.strip():
        continue
    code = stripedLine.split()
    # if the first word in code list ends with a colon it is a branch decloration
    # save in branch list and remove from code list
    if code[0].endswith(':'):
        branch.append(code[0])
        bLabel.append(code[0])
        code.remove(code[0])
    # if code is not empty (has a length) the opcode should be the first word
    # save in opCode list and remove from code list
    if len(code) > 0:
        opCode.append(code[0])
        code.remove(code[0])
    # if LOADI is the opcode and code still has a length the last word should be the immediate
    # save in immediate list and remove from code list
    if len(code) > 0:
        if opCode[0] == 'LOADI':
            immediate.append(code[-1])
            code.remove(code[-1])
    # if BR BGT BLT  is the opcode and code still has a length the last word should be the branch Call
    # save in branchCall list and remove from code list
    if len(code) > 0:
        if opCode[0] == 'BEQ' or opCode[0] == 'BLT' or opCode[0] == 'BGT' or opCode[0] == 'BR':
            branchCall.append(code[-1])
            bCall.append(code[-1]+':')
            code.remove(code[-1])
    # if STORE LOAD is the opcode and code still has a length the last word should be the identifier
    # save in identifier list and remove from code list
    if len(code) > 0:
        if opCode[0] == 'LOAD' or opCode[0] == 'STORE':
            identifier.append(code[-1])
            code.remove(code[-1])
    # remaining code list should only have registars
    # if bLabel and bCall are not empty if there's a match remove it from both lists
    if len(bLabel) > 0 and len(bCall) > 0:
        for x in bLabel: # x each word of bLabel
            for y in bCall: # y each word in bCall
                if x == y: # if x and y are equal each list has reference to same branch remove from both lists and break out of the loop
                    bLabel.remove(bLabel[bLabel.index(x)])
                    bCall.remove(bCall[bCall.index(y)])
                    break
    # create variable length which holds the length based on opcode
    if len(opCode) > 0:
        if opCode[0] == 'LOAD' or opCode[0] == 'STORE':
            length = len(code) + len(identifier)
        elif opCode[0] == 'LOADI':
            length = len(code) + len(immediate)
        elif opCode[0] == 'ADD' or opCode[0] == 'INC' or opCode[0] == 'SUB' or opCode[0] == 'DEC':
            length = len(code)
        elif opCode[0] == 'BEQ' or opCode[0] == 'BLT' or opCode[0] == 'BGT' or opCode[0] == 'BR':
            length = len(code) + len(branchCall)
        elif opCode[0] == 'END' or opCode[0] == 'NOOP':
            length = 0
    # check for errors
    # ill-formed labels: branches or branch calls should have max length five and have no numbers
    # Check for Branch label
    if len(branch) > 0 and illLabelBranch(branch) == False:
        found = True
        illLabel += 1
        errors += 1
        writeFile.write(str(lineNum)+'. '+stripedLine+'\n')
        writeFile.write('**error ill-formed branch label: '+branch[0]+'\n')
        # reset lists
        branch = []
        opCode = []
        immediate = []
        branchCall = []
        identifier = []
        length = 0
        found = False
        continue
    # if no branch then check for calls
    elif len(branchCall) > 0 and illLabelBranchCall(branchCall) == False:
        found = True
        illLabel += 1
        errors += 1
        writeFile.write(str(lineNum)+'. '+stripedLine+'\n')
        writeFile.write('**error ill-formed banch call: '+branchCall[0]+'\n')
        # reset lists
        branch = []
        opCode = []
        immediate = []
        branchCall = []
        identifier = []
        length = 0
        found = False
        continue
    # invalid opcode not one of MAL opcodes
    elif len(opCode) > 0 and invalidopCode(opCode[0]) == False:
        found = True
        invalidCode += 1
        errors += 1
        writeFile.write(str(lineNum) + '. ' + stripedLine+'\n')
        writeFile.write('**error invalid opCode: ' + opCode[0]+'\n')
        # reset lists
        branch = []
        opCode = []
        immediate = []
        branchCall = []
        identifier = []
        length = 0
        found = False
        continue
    # too many operands
    elif len(opCode) > 0 and numberofOperands(opCode[0]) < length:
        found = True
        errors += 1
        manyOp += 1
        writeFile.write(str(lineNum) + '. ' + stripedLine+'\n')
        writeFile.write('**error too many operands expected: ' + str(numberofOperands(opCode[0]))+ " Found: "+str(length)+'\n')
        # reset lists
        branch = []
        opCode = []
        immediate = []
        branchCall = []
        identifier = []
        length = 0
        found = False
        continue
    # too few operands
    elif len(opCode) > 0 and numberofOperands(opCode[0]) > length:
        found = True
        errors += 1
        fewOp += 1
        writeFile.write(str(lineNum) + '. ' + stripedLine+'\n')
        writeFile.write('**error too few operands expected: ' + str(numberofOperands(opCode[0]))+ " Found: "+str(length)+'\n')
        # reset lists
        branch = []
        opCode = []
        immediate = []
        branchCall = []
        identifier = []
        length = 0
        found = False
        continue
    # ill-formed identifier
    elif len(identifier) > 0 and validId(identifier[0]) == False:
        found = True
        errors += 1
        illID += 1
        writeFile.write(str(lineNum) + '. ' + stripedLine+'\n')
        writeFile.write('**error ill-formed identifier: ' + identifier[0]+'\n')
        # reset lists
        branch = []
        opCode = []
        immediate = []
        branchCall = []
        identifier = []
        length = 0
        found = False
        continue
    # ill-formed literal
    elif len(immediate) > 0 and validImmediate(immediate[0]) == False:
        found = True
        errors += 1
        illLit += 1
        writeFile.write(str(lineNum) + '. ' + stripedLine+'\n')
        writeFile.write('**error ill-formed literal: ' + immediate[0]+'\n')
        # reset lists
        branch = []
        opCode = []
        immediate = []
        branchCall = []
        identifier = []
        length = 0
        found = False
        continue
    # if no error found just print the line
    elif found == False:
        writeFile.write(str(lineNum) + '. ' + stripedLine+'\n')
    # reset lists
    branch = []
    opCode = []
    immediate = []
    branchCall = []
    identifier = []
    length = 0
    found = False
    # ended reading the document
writeFile.write('\n--------------------\n\n')
writeFile.write('Total errors found: '+str(errors)+'\n')
# if END is an element in the list
if 'END' in endStatement:
    # if the index of the endStatement list is not the last element: show error
    if endStatement.index('END') != len(endStatement)-1:
        errors += 1
        writeFile.write('--- MAL program does have an END statment, but not at the bottom of the program ---\n')
# elif 'END' is not in the list: show there is no END statement
elif not 'END' in endStatement:
    errors += 1
    writeFile.write('--- END Statement missing from program ---\n')
# give warnings if any
# if bCall is not empty print the labels that are called, but no branch present
if len(bCall) > 0:
    writeFile.write('**warning no branch found but calls for branch: ')
    for x in bCall:
        writeFile.write(x[:-1]+', ')
    writeFile.write('were made**\n')
# if bLabel is not empty print the branches that were made, but never called
if len(bLabel) > 0:
    writeFile.write('**warning there are no calls made to these branch(s): ')
    for x in bLabel:
        writeFile.write(x+', ')
    writeFile.write('**\n')
# evaluate error Types
if illLabel > 0:
    writeFile.write(str(illLabel)+' ill-formed Label\n')
if invalidCode > 0:
    writeFile.write(str(invalidCode) + ' invalid opcode\n')
if manyOp > 0:
    writeFile.write(str(manyOp) + ' too many operands\n')
if fewOp > 0:
    writeFile.write(str(fewOp) + ' too few operands\n')
if illID > 0:
    writeFile.write(str(illID) + ' ill-formed identifier\n')
if illLit > 0:
    writeFile.write(str(illLit) + ' ill-formed literal\n')
if errors > 0:
    writeFile.write('Processing complete -- MAL program not valid')
elif errors == 0:
    writeFile.write('Processing complete -- MAL program valid')
