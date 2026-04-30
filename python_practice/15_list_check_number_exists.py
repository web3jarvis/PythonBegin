'''Check whether a given element exists in the list or not.'''

input_list = list(input("Enter any list of characters or numbers separated by space: ").split())
element_to_check = input("Enter any element to check: ")

if element_to_check in input_list:
    print("Given Element is present.")   
else:
    print("Given Element is not present.")
