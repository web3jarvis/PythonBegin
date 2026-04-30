'''5. Take three numbers as input and print the largest among them.'''

user_input_01 = float(input("Enter the 1st number:"))
user_input_02 = float(input("Enter the 2nd number:"))
user_input_03 = float(input("Enter the 3rd number:"))
if user_input_01 > user_input_02 and user_input_01 > user_input_03:
    print("The largest of the three numbers is: ", user_input_01)
elif user_input_02 > user_input_01 and user_input_02 > user_input_03:
    print("The largest of the three numbers is: ", user_input_02)
else:
    print("The largest of the three numbers is: ", user_input_03)