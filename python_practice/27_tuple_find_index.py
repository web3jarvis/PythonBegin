'''Find the index of a given element in a tuple'''

input_tuple = tuple(input("Enter the tuple elements separated by space: ").split())
element_to_check_index = input("Enter the element to check: ")

for i in input_tuple:
    if i == element_to_check_index:
        print(input_tuple.index(element_to_check_index))
        
if element_to_check_index not in input_tuple:
    print("Not found.")