'''Check whether a string is a palindrome'''

input_string = input("Enter any string: ")
reverse_string = input_string[::-1]

if input_string == reverse_string:
    print("The string is a palindrome.")
else:
    print("The string is NOT a palindrome.")