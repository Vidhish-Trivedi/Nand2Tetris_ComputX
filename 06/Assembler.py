# Created by: Vidhish Trivedi (IMT2021055)
# Created for project - 6 of Nand2Tetris course.
# Part of project for ComputX group - IIITB

# assembly file.
import fileinput

# list of instructions and labels (if any) present in the assembly file.
list_ins_labels = []

# According to language specifications.
dict_comp = {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001", "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111", "D&A": "0000000", "D|A": "0010101", "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"}
dict_dest = {"null": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
dict_jump = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

with open('./a.txt', 'r') as f:
    txt = f.read().replace(' ', '')

with open('./g.txt', 'w') as f:
    f.write(txt)

assembly = fileinput.input("./g.txt")

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
    # print(_)
    if(_[0] != "("):
        ins_count += 1

label_count = len(list_ins_labels) - ins_count

# symbol table implemented using a symbol table.
symbol_table = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15, "SCREEN": 16384, "KBD": 24576}

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

# BINARY CONVERSION LOGIC.
# Convert to 15-bit binary.
def make_binary_15(n):
    n = int(n)
    b = "{0:b}".format(n)
    if len(b) < 15:
        b = "0"*(15 - len(b)) + b
    return(b)

# create a list for storing instructions converted to binary format.
list_ins_binary = []

j = 0  # to keep track of variable number (for handling variables)
for line in list_ins_labels:
    machine_code = ""
    machine_code1 = ""
    # handling labels, always used with A-type.
    if(str(line)[0] == "("):
        machine_code1 += "0"
        line1 = str(line)
        indx = line1.index(")")
        label1 = (line1[:indx])[1:]  # extracting label name.
        machine_code1 += make_binary_15(symbol_table[label1])
        
    
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

    # C-type instruction.
    # at any time, atleast one of ";" or "=" would be present.
    else:
        machine_code += "111"
        # if not a jump.
        if(";" not in str(line)):
            jump_final = "null"
            list_d = str(line).split("=")
            dest = list_d[0]
            comp = list_d[1]
            # handle in-line comments.
            comp_final = ""
            k = 0
            while(k < len(comp) and (comp[k] != " " and comp[k] != "/")):
                comp_final += comp[k]
                k += 1
            
        elif("=" not in str(line)):
            dest = "null"
            list_d = str(line).split(";")
            comp_final = list_d[0]
            jump = list_d[1]
            # handle in-line comments.
            jump_final = ""
            k = 0
            while(k < len(jump) and (jump[k] != " " and jump[k] != "/")):
                jump_final += jump[k]
                k += 1
        
        # generate comp bits.
        comp_bits = dict_comp[comp_final]

        # generate dest bits.
        dest_bits = dict_dest[dest]

        # generate jump bits.
        jump_bits = dict_jump[jump_final]

        machine_code += comp_bits
        machine_code += dest_bits
        machine_code += jump_bits
        
    if(machine_code != ""):
        list_ins_binary.append(machine_code)

# open file in write mode.
machineLang = open("./b.txt", "w")
# write to output file.
for line in list_ins_binary:
    # print(line)
    machineLang.write(line)
    machineLang.write("\n")
machineLang.close()
