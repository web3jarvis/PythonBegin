'''Create a tuple from user input and print its length.'''


input_for_tuple = input("Enter data separated by space: ").split()

final_tuple = tuple(input_for_tuple)

print("The length of this tuple is: ", len(final_tuple))