'''Merge two lists entered by the user into a single list.'''

input_list_01 = list(input("Enter the elements for List-1 separated by space: ").split())
input_list_02 = list(input("Enter the elements for List-2 separated by space: ").split())

merge_list = input_list_01 + input_list_02
print(merge_list)


