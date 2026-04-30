'''Merge two tuples into one tuple.'''

input_tuple_01 = tuple(input("Enter the tuple elements separated by space: ").split())
input_tuple_02 = tuple(input("Enter the tuple elements separated by space: ").split())

merge_tuple = input_tuple_01 + input_tuple_02

print(merge_tuple)