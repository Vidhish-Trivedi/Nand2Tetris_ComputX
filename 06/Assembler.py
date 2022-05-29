# Created by: Vidhish Trivedi (IMT2021055)
# Created for project - 6 of Nand2Tetris course.
# Part of project for ComputX group - IIITB

# assembly file.
import fileinput

# list of instructions and labels (if any) present in the assembly file.
list_ins_labels = []

# instructions in assembly file should be written without spaces,
# That is: D=A+D is accepted, D = A + D is not accepted.
# There should be an empty line at the end of the assembly file.
assembly = fileinput.input("./assembly.txt")

for line in assembly:
    # remove blank lines (white spaces).
    if(line == "\n"):
        pass
    # remove comments (in-line comments will be handled seperately).
    elif(line[0] != "/"):
        # print(line, end="")
        list_ins_labels.append(line[:len(line) - 1])

# count number of instructions.
ins_count = 0
for _ in list_ins_labels:
    print(_)############################
    if(_[0] != "("):
        ins_count += 1

label_count = len(list_ins_labels) - ins_count

# print()
# print(ins_count)
# print(label_count)

# symbol table implemented using a symbol table.
symbol_table = {}

# First Pass, to add labels,
# (this would not add variables, which do not have a corresponding (XYZ) line for an @XYZ line).
i = 0
for line in list_ins_labels:
    if(line[0] == "("):
        label1 = ""
        for _ in line:
            if(_ != "(" and _ != ")"):
                label1 = label1 + _
        symbol_table[label1] = i
    else:
        i += 1

# print()
# print(i)
print("---------------")
print(symbol_table)
print("---------------")


# BINARY CONVERSION LOGIC.
# Convert to 15-bit binary.
def make_binary_15(n):
    n = int(n)
    b = "{0:b}".format(n)
    if len(b) < 15:
        b = "0"*(15 - len(b)) + b
    return(b)

# Convert a binary string to decimal.
def make_decimal(n):
    n = int(n, 2)
    return(str(n))

# create a list for storing instructions converted to binary format.
list_ins_binary = []

j = 0  # to keep track of variable number (for handling variables)
for line in list_ins_labels:
    machine_code = ""
    # handling labels, always used with A-type.
    if("(" in line or ")" in line):
        machine_code += "0"
        line1 = str(line)
        indx = line1.index(")")
        label1 = (line1[:indx])[1:]  # extracting label name.
        # print(label1)
        machine_code += make_binary_15(symbol_table[label1])
        
    
    # A-type instruction, continued.
    elif(str(line[0]) == "@"):
        machine_code += "0"
        list_a = str(line).split()  # split at spaces, this will let us handle in-line comments.
        # when non-negative decimal constant is used.
        if(list_a[0][1:].isdigit()):
            machine_code += make_binary_15(list_a[0][1:])

        # for handling variables.
        else:
            variable1 = list_a[0][1:]
            if(variable1 in symbol_table):
                pass
            else:
                symbol_table[variable1] = j + 16  # add address of variable (in decimal) to the symbol_table. 
                j += 1
            machine_code += make_binary_15(symbol_table[variable1])
        
    list_ins_binary.append(machine_code)
    

# print("---------------")
# print(symbol_table)
# print("---------------")
# print(list_ins_binary)
# print("---------------")


# # open file in write mode.
# machineLang = open("./machine.txt", "w")
# # write to output file.
# for line in list_ins_labels:
#     machineLang.write(line)
#     machineLang.write("\n")
# machineLang.close()
