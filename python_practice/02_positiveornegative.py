'''Take a number as input and print whether it is Positive, Negative, or Zero.'''

user_input = int(input("Enter any number to check if its positive or negative: "))  
if user_input > 0:
    print("The input number is Positive")
elif user_input < 0:
    print("The input number is Negative")
else:
    print("The input number is zero")