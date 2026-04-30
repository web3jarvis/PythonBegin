'''
Replace all vowels in a string with '*'.

'''

input_string = input("Enter any string: ") #apple
vowels = 'aeiouAEIOU'
for j in vowels:
    input_string = input_string.replace(j, "*")
    
print("The new string is: ", input_string)
