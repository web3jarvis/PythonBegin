'''Remove all spaces from a string'''

input_string = input("Enter any string: ") #good boy
no_space_string = ""

for i in input_string:
    if i == " ":
        no_space_string = input_string.replace(" ", "")
        
print("Without space string: ", no_space_string)
