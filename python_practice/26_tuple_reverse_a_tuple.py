'''Reverse a tuple.'''


input_tuple = tuple(input("Enter the elements separated with space: ").split())
reverse_tuple = input_tuple[::-1]

#for i in input_tuple:
 #   reverse_tuple.insert(0,i)

print("Here's the reverse tuple:", ' '.join(reverse_tuple))