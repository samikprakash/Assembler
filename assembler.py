



file = open("sample_input.txt","r")


def label_exists(instruction):   #checks if instruction line contains symbol or not, instruction parameter is a string, to check if label exists
    temp = instruction.replace(" ","")
    if temp.find(":") == -1:
        return False
    return True

def make_symbol_table(symbol_table,instruction,ilc):  #takes symbol out of instruction line and adds it to symbol table, instruction parameter is a string
    temp = instruction.replace(" ","")
    if(label_exists(instruction)):
        symbol_table[instruction[:instruction.find(":")]] = ilc
    return
    
def add_variable(symbol_table,instruction,ilc,opcode_table): #adds variables to the variable table, here instruction parameter is a list
    
    if len(instruction) > 1:
        for x in instruction:
            if x not in opcode_table and x.isalpha():
                symbol_table[x] = "na"


def address_to_variable(symbol_table,ilc): #gives address to the variables in the variable table
    for x in symbol_table:
        if symbol_table[x] == "na":
            symbol_table[x] = ilc + 16 #word size is 16 bits 


# mapping instructions to the corresponding opcode :-
opcode_table = {"CLA":"0000","LAC":"0001","SAC":"0010","ADD":"0011","SUB":"0100",
"BRZ":"0101","BRN":"0110","BRP":"0111","INP":"1000","DSP":"1001","MUL":"1010","DIV":"1011","STP":"1100"} 


symbol_table = {} 

literal_table = {}
instruction_location_counter = 0

instructions = []
for i in file.readlines():
    # print(i)
    if i!='\n':
        temp_instruction = i.split()
        print(temp_instruction)
        instructions.append(i)
        make_symbol_table(symbol_table,i,instruction_location_counter)
        add_variable(symbol_table,temp_instruction,instruction_location_counter,opcode_table)
        instruction_location_counter+=12 

address_to_variable(symbol_table,instruction_location_counter)
file.close()

print(symbol_table)
