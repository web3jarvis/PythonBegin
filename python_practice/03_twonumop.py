'''Take two numbers and one operator (+, -, *, /) as input and perform the calculation.'''

user_input_01 = int(input("Enter the 1st number: "))
user_input_02 = int(input("Enter the 2nd number: "))
operator = input("Enter the operator: ")
if operator == "+":
    print("The sum is: ", user_input_01 + user_input_02)
elif operator == "-":
    print("The difference is: ", user_input_01 - user_input_02)
elif operator == "*":
    print("The product is: ", user_input_01 * user_input_02)
elif operator == "/":
    print("The division is: ", user_input_01 / user_input_02)
    