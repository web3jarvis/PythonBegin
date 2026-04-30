'''Convert all characters to uppercase without using upper().'''

input_string = input("Enter any string: ")
lower_case = ('abcdefghijklmnopqrstuvwxyz')
upper_case = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
output_string = []

for i in input_string:
    if i in lower_case:
        output_string.append(upper_case[lower_case.index(i)])
    else:
        output_string.append(i)
        
print(''.join(output_string))
        
        