read = open('test.txt','r').read()
for line in read:
    if line[0] == " " :
        print("found an end of line")
read.close()