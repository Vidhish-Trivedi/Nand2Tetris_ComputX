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
    print(_)
    if(_[0] != "("):
        ins_count += 1

label_count = len(list_ins_labels) - ins_count

# print(ins_count)
# print(label_count)

########################################################


# BINARY CONVERSION LOGIC.


########################################################


# # open file in write mode.
# machineLang = open("./machine.txt", "w")
# # write to output file.
# for line in list_ins_labels:
#     machineLang.write(line)
#     machineLang.write("\n")
# machineLang.close()
