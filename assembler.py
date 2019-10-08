# mapping instructions to the corresponding opcode :-

opcode_table = {"CLA":"0000","LAC":"0001","SAC":"0010","ADD":"0011","SUB":"0100",
"BRZ":"0101","BRN":"0110","BRP":"0111","INP":"1000","DSP":"1001","MUL":"1010","DIV":"1011","STP":"1100"} 

file = open("sample_input.txt","r")


def symbol_exists(instruction):   #checks if instruction line contains symbol or not
    temp = instruction.replace(" ","")
    if temp.find(":") == -1:
        return False
    return True

def make_symbol_table(symbol_table,instruction,ilc):  #takes symbol out of instruction line and adds it to symbol table
    temp = instruction.replace(" ","")
    if(symbol_exists(instruction)):
        symbol_table[instruction[:instruction.find(":")]] = ilc
    return
    
    
symbol_table = {}

instruction_location_counter = 0

instructions = []
for i in file.readlines():
    # print(i)
    if i!='\n':
        instructions.append(i)
        make_symbol_table(symbol_table,i,instruction_location_counter)
        instruction_location_counter+=12 
    
file.close()

print(symbol_table)