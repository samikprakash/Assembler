file=open("sample_input.txt","r")
expanded_macros_file=open("expanded_macros.txt","w")

macro_table={}
macro_keyword="MACRO"
macro_end_keyword="ENDM"
macro_found=False
for i in file.readlines():
	if i!='\n':
		# print(i)
		currline=i.rstrip('\n')
		currline=currline.split(" ")
		currline=list(filter(lambda a: a != '', currline))
		print(currline)
		if macro_found:
			if macro_end_keyword not in currline:
				new_macro_def.append(currline)
			else:
				macro_table[macro_name]=new_macro_def
				macro_found=False
				continue
		elif macro_keyword in currline:
			new_macro_def=[]
			macro_found=True
			macro_name=currline[0]
		elif currline[0] in macro_table:
			found_macro_name=currline[0]
			for k in macro_table[found_macro_name]:
				for j in k:
					expanded_macros_file.write(j+" ")
				expanded_macros_file.write("\n")
		else:
			for j in currline:
				expanded_macros_file.write(j+" ")
			expanded_macros_file.write("\n")

print(macro_table)


