

def decimalToBinary(n):
	output=bin(n).replace("0b","")
	if len(output)<8:
		missingzeroes=8-len(output)
		output="0"*missingzeroes+output

	return output


#errors are defined below
def argument_errors(instruction,line_number): #instruction is a list
	opcodes_onearg = ["LAC","SAC","ADD","SUB",
	"BRZ","BRN","BRP","INP","DSP","MUL","DIV"]
	opcodes_noarg = ["CLA","STP"]
	if instruction[0].find(":")==-1 and  instruction[0] != "START" and  instruction[0] != "END":
		if instruction[0] in opcodes_onearg and len(instruction)>2:
			print("Error. Too many argruments for "+ instruction[0]+ " on line "+str(line_number))
			exit()
		if instruction[0] in opcodes_onearg and len(instruction)<2:
			print("Error. Argrument required for "+ instruction[0]+ " on line "+str(line_number))
			exit()
		if instruction[0] in opcodes_noarg and len(instruction)>1:
			print("Error. No argruments required for "+ instruction[0]+ " on line "+str(line_number))
			exit()
	if instruction[0].find(":")!=-1 and  instruction[1] != "START" and  instruction[1] != "END":
		if instruction[1] in opcodes_onearg and len(instruction)>3:
			print("Error. Too many argruments for "+ instruction[1]+ " on line "+str(line_number))
			exit()
		if instruction[1] in opcodes_onearg and len(instruction)<3:
			print("Error. Argrument required for "+ instruction[1]+ " on line "+str(line_number))
			exit()
		if instruction[1] in opcodes_noarg and len(instruction)>2:
			print("Error. No argruments required for "+ instruction[1]+ " on line "+str(line_number))

			exit()

	return
def invalid_opcode(opcode,opcode_table,line_number):
	if(opcode not in opcode_table):
		print("Error on line " + str(line_number)+ ". Invalid opcode " + opcode+ ". Please enter a valid opcode. ")
		exit()
	return

def branching_errors(instruction,line_number,symbol_table): #instruction is a list
	branch_opcodes = ["BRZ","BRP","BRN"]
	if instruction[0].find(":") != -1 and instruction[1] in branch_opcodes:
		if instruction[2] + ":" not in symbol_table:
			print("Error on line " + str(line_number)+  ". Please define an identifier(label) with branching opcodes.")
			exit()

	elif instruction[0].find(":") == -1 and instruction[0] in branch_opcodes:
		if instruction[1] + ":" not in symbol_table:
			print("Error on line "+str(line_number) + ". Please define an identifier(label) with branching opcodes.")
			exit()


def label_exists(instruction):   #checks if instruction line contains symbol or not, instruction parameter is a string, to check if label exists
	temp = instruction.replace(" ","")
	if temp.find(":") == -1:
		return False
	return True

def make_symbol_table(symbol_table,instruction,ilc,line_number):  #takes symbol out of instruction line and adds it to symbol table, instruction parameter is a string
	temp = instruction.replace(" ","")
	if(label_exists(instruction)):
		if instruction[:instruction.find(":")+1] in symbol_table:
			print("Error on "+ str(line_number)+ ": label already defined. Please use a unique label")
			exit()
		
		symbol_table[instruction[:instruction.find(":")+1]] = ilc
	return

def add_variable(symbol_table,instruction,ilc,opcode_table,variable_table): #adds variables to the variable table, here instruction parameter is a list

	if len(instruction) > 1:
		for x in instruction:
			if x not in opcode_table and x.isalpha() and x != "START" and x != "END":
				symbol_table[x] = "na"
				variable_table.add(x)
	return



def address_to_variable(symbol_table,ilc): #gives address to the variables in the variable table
	jump = 0
	for x in symbol_table:
		if symbol_table[x] == "na":
			symbol_table[x] = ilc + 1 #word size is 1 bits
			ilc = ilc+1
			jump += 1
	return jump

def add_literal(literal_table,instruction,line_number,literal_line_table):  #instruction parameter here is list
	temp = instruction

	index = temp[-1].find("=")
	if index!=-1:
		literal_table[temp[-1]] = "na"
		literal_line_table[temp[-1]] = line_number

	
	
	return

def literal_to_address(literal_table,ilc):
	for x in literal_table:
		literal_table[x] = ilc + 1
		ilc += 1
	return
def literal_errors(literal_table,literal_line_table):
	list_keys=literal_table.keys()
	for i in list_keys:
		for j in i:
			if j.isalpha():
				print("Error on line "+ str(literal_line_table[i])+ ": Literal should consist of integers only")
				exit()
			if j.isalnum()==False and j!="=" and j!="'":
				print("Error on line "+ str(literal_line_table[i])+ ": Literal should consist of integers only")
				exit()






def first_pass(symbol_table,literal_table,instruction_location_counter,opcode_table,literal_line_table):
	variables = set() #to see which are variables
	file = open("sample_input_new.txt","r")
	# print((file.read()))
	#errors related to start and end statements :-
	file1 = open("sample_input_new.txt","r")
	a = file1.read()
	# print(a.find("END"))
	if a.find("END") == -1:
		print("END statement is missing. Please add end statement.")
		exit()
	# print(file1.read().find("END"))
	if a.find("START") == -1:
		print("START statement is missing. Please add end statement.")
		exit()
	if a.count("END") >1:
		print("More than 1 END statements .There should only be one occurence of END statement. Please remove additional END statements")
		exit()
	if a.find("START") != 0:
		print("Illegal START statement in the middle of the program. Please remove.")
		exit()

	if a.count("START") >1:
		print("More than 1 START statements .There should only be one occurence of START statement. Please remove additional START statements")
		exit()

	file1.close()


	line_number = 0
	for i in file.readlines():
		# print(i)
		line_number += 1
		if i.find("#") != -1:        #for handling comments
			continue
		if i!='\n':
			# i=i.replace(":",'')
			temp_instruction = i.split()
			argument_errors(temp_instruction,line_number)
			# print(temp_instruction)
			
			# print(line_number)
			if len(temp_instruction) >2 :
				if(temp_instruction[0].find(":") != -1):
					# print(temp_instruction[0])
					invalid_opcode(temp_instruction[1],opcode_table,line_number)

			if len(temp_instruction) == 2 and temp_instruction[0] != "START" and temp_instruction[0].find(":") == -1:
				invalid_opcode(temp_instruction[0],opcode_table,line_number)


			make_symbol_table(symbol_table,i,instruction_location_counter,line_number) #added labels

			add_variable(symbol_table,temp_instruction,instruction_location_counter,opcode_table,variables) #added variables

			add_literal(literal_table,temp_instruction,line_number,literal_line_table)
			instruction_location_counter+=1
	# print(instruction_location_counter)
	instruction_location_counter += 1*address_to_variable(symbol_table,instruction_location_counter)
	# print(variables)
	# print(instruction_location_counter)
	literal_to_address(literal_table,instruction_location_counter)
	instruction_location_counter += 1*len(literal_table)
	file.close()
	return

def second_pass(symbol_table,literal_table,instruction_location_counter,opcode_table,literal_line_table):
	literal_errors(literal_table,literal_line_table)
	file=open("sample_input_new.txt","r")
	output_file=open("output.txt","w")
	line_number = 0
	for i in file.readlines():
		line_number += 1

		if i!='\n':
			# line_number += 1
			# print(i.fin)
			if i.find("#") != -1:        #for handling comments
				continue
			i = i.strip('\n')
			curr_instruction=i.split()
			branching_errors(curr_instruction,line_number,symbol_table)
			# print(curr_instruction)
			if curr_instruction[0]=="END" or curr_instruction[0]=="START":      #checking for end keyword
				continue
			if curr_instruction[0] not in symbol_table:
				curr_opcode=curr_instruction[0]
				# print(curr_opcode)
				# invalid_opcode(curr_opcode,opcode_table,line_number )
				curr_opcode_binary=opcode_table[curr_opcode]
				#check for valid opcode

				if len(curr_instruction)!=1:                #for commands like CLA etc.
					if curr_instruction[-1].isdigit():
						# print(curr_instruction[-1])
						curr_symbol_binary=decimalToBinary(int(curr_instruction[-1]))
						# print(curr_symbol_binary)
						output_file.write(curr_opcode_binary+" "+curr_symbol_binary+" ")
						output_file.write('\n')
					
						continue





					
					curr_symbol=curr_instruction[1]
					if curr_symbol not in symbol_table:
						if curr_symbol in literal_table:
							curr_symbol_binary=decimalToBinary(literal_table[curr_symbol])
							output_file.write(curr_opcode_binary+" "+curr_symbol_binary+" ")

						else:
							curr_symbol=curr_symbol+":"
							curr_symbol_binary=decimalToBinary(symbol_table[curr_symbol])
							output_file.write(curr_opcode_binary+" "+curr_symbol_binary+" ")
						output_file.write('\n')
					else:
						curr_symbol_binary=decimalToBinary(symbol_table[curr_symbol])
						output_file.write(curr_opcode_binary+" "+curr_symbol_binary+" ")
						output_file.write('\n')

				else:
					output_file.write(curr_opcode_binary+" ")
					output_file.write('\n')
			else:
				curr_instruction.pop(0)
				curr_opcode=curr_instruction[0]
				if curr_instruction[-1].isdigit():
						print(curr_instruction[-1])
						curr_symbol_binary=decimalToBinary(int(curr_instruction[-1]))
						print(curr_symbol_binary)
						output_file.write(curr_opcode_binary+" "+curr_symbol_binary+" ")
						output_file.write('\n')
					
						continue


				# print(curr_opcode)
				curr_opcode_binary=opcode_table[curr_opcode]
				if len(curr_instruction)!=1:                #for commands like CLA etc.

					curr_symbol=curr_instruction[1]
					if curr_symbol not in symbol_table:
						if curr_symbol in literal_table:
							curr_symbol_binary=decimalToBinary(literal_table[curr_symbol])
							output_file.write(curr_opcode_binary+" "+curr_symbol_binary+" ")
						else:
							curr_symbol=curr_symbol+":"
							curr_symbol_binary=decimalToBinary(symbol_table[curr_symbol])
							output_file.write(curr_opcode_binary+" "+curr_symbol_binary+" ")
						output_file.write('\n')
					else:
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
literal_line_table = {}



first_pass(symbol_table,literal_table,instruction_location_counter,opcode_table,literal_line_table)
print(literal_table)
# print(literal_line_table)
print(symbol_table)
second_pass(symbol_table,literal_table,instruction_location_counter,opcode_table,literal_line_table)
