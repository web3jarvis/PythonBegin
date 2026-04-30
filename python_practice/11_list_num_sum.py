'''Take a list of numbers from the user and print the sum of all elements.'''

num_list = input("Enter the numbers separated by space:").split()
int_list = [int(i) for i in num_list]

print("The sum of the numbers is:", sum(int_list))

