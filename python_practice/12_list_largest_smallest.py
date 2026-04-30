'''Take a list and print the largest and smallest element.'''

num_list = input("Enter the numbers separated by space: ").split()
int_list = [float(i) for i in num_list]

print("The largest element is:", max(int_list))
print("The smallest element is:", min(int_list))