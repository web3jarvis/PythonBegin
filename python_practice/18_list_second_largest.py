'''Find the second largest element in a list.'''

input_list = [int(i) for i in input("Enter the elements separated by space: ").split()]

# largest = max(input_list)
# while largest in input_list:
#     input_list.remove(largest)
#     second_largest = max(input_list)

print("The Second Largest in the list: ", sorted(input_list)[-2])