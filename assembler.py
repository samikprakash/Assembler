
def decimalToBinary(n): 
    return bin(n).replace("0b","") 





def label_exists(instruction):   #checks if instruction line contains symbol or not, instruction parameter is a string, to check if label exists
    temp = instruction.replace(" ","")
    if temp.find(":") == -1:
        return False
    return True

def make_symbol_table(symbol_table,instruction,ilc):  #takes symbol out of instruction line and adds it to symbol table, instruction parameter is a string
    temp = instruction.replace(" ","")
    if(label_exists(instruction)):
        symbol_table[instruction[:instruction.find(":")+1]] = ilc
    return
    
def add_variable(symbol_table,instruction,ilc,opcode_table): #adds variables to the variable table, here instruction parameter is a list
    
    if len(instruction) > 1:
        for x in instruction:
            if x not in opcode_table and x.isalpha():
                symbol_table[x] = "na"
    return

def address_to_variable(symbol_table,ilc): #gives address to the variables in the variable table
    jump = 0
    for x in symbol_table:
        if symbol_table[x] == "na":
            symbol_table[x] = ilc + 16 #word size is 16 bits 
            ilc = ilc+16
            jump += 1
    return jump
 
def add_literal(literal_table,instruction):  #instruction parameter here is string
    temp = instruction.replace(" ","")
    index = temp.find("=")
    if index!=-1 and index != len(temp)-1:
        to_add = "'="
        i = index+1
        while(True):
            # print(temxp[i])
            if(temp[i].isdigit()):
                to_add += temp[i]
                i += 1
            else:
                break
        literal_table[to_add+"'"] = "na"
    return

def literal_to_address(literal_table,ilc):
    for x in literal_table:
        literal_table[x] = ilc + 12
        ilc += 12
    return






def first_pass(symbol_table,literal_table,instruction_location_counter,opcode_table):
    file = open("sample_input_new.txt","r")
    for i in file.readlines():
        # print(i)
        if i!='\n':
            # i=i.replace(":",'')
            temp_instruction = i.split()
            # print(temp_instruction)
            
            make_symbol_table(symbol_table,i,instruction_location_counter) #added labels

            add_variable(symbol_table,temp_instruction,instruction_location_counter,opcode_table) #added variables

            add_literal(literal_table,i)
            instruction_location_counter+=12 
    print(instruction_location_counter)   
    instruction_location_counter += 16*address_to_variable(symbol_table,instruction_location_counter)
    
    print(instruction_location_counter)
    literal_to_address(literal_table,instruction_location_counter)
    instruction_location_counter += 12*len(literal_table)
    file.close()
    return

def second_pass(symbol_table,literal_table,instruction_location_counter,opcode_table):
    file=open("sample_input_new.txt","r")
    output_file=open("output.txt","w")
    for i in file.readlines():
        if i!='\n':
            i=i.strip('\n')
            curr_instruction=i.split(" ")
            curr_instruction=(list(filter(lambda a: a != '', curr_instruction)))
            # print(curr_instruction)
            if curr_instruction[0]=="END" or curr_instruction[0]=="START":      #checking for end keyword
                continue
            if curr_instruction[0] not in symbol_table:     
                curr_opcode=curr_instruction[0]
                # print(curr_opcode)
                curr_opcode_binary=opcode_table[curr_opcode]
                if len(curr_instruction)!=1:                #for commands like CLA etc.

                    curr_symbol=curr_instruction[1]
                    if curr_symbol not in symbol_table:
                        curr_symbol=curr_symbol+":"
                    curr_symbol_binary=decimalToBinary(symbol_table[curr_symbol])
                    output_file.write(curr_opcode_binary+" "+curr_symbol_binary+" ")
                    output_file.write('\n')
                else:
                    output_file.write(curr_opcode_binary+" ")
                    output_file.write('\n')
            else:
                curr_instruction.pop(0)
                curr_opcode=curr_instruction[0]
                # print(curr_opcode)
                curr_opcode_binary=opcode_table[curr_opcode]
                if len(curr_instruction)!=1:                #for commands like CLA etc.

                    curr_symbol=curr_instruction[1]
                    if curr_symbol not in symbol_table:
                        curr_symbol=curr_symbol+":"
                    curr_symbol_binary=decimalToBinary(symbol_table[curr_symbol])
                    output_file.write(curr_opcode_binary+" "+curr_symbol_binary+" ")
                    output_file.write('\n')
                else:
                    output_file.write(curr_opcode_binary+" ")
                    output_file.write('\n')


    return



    


# mapping instructions to the corresponding opcode :-
opcode_table = {"CLA":"0000","LAC":"0001","SAC":"0010","ADD":"0011","SUB":"0100",
"BRZ":"0101","BRN":"0110","BRP":"0111","INP":"1000","DSP":"1001","MUL":"1010","DIV":"1011","STP":"1100"} 

symbol_table = {} 

literal_table = {}
instruction_location_counter = 0



first_pass(symbol_table,literal_table,instruction_location_counter,opcode_table)
print(literal_table)
print(symbol_table)
second_pass(symbol_table,literal_table,instruction_location_counter,opcode_table)


