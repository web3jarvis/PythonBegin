'''Find how many times a given character appears in a string.'''


input_string = input("Enter any string: ")
char_to_check = input("Enter the character to be checked: ")
char_count = 0

for i in input_string:
    if i == char_to_check:
        char_count += 1
        
print("Character count: ", char_count)
        