'''Find the maximum and minimum element in a tuple.'''

input_for_tuple = input("Enter the elements for tuple separated by space: ").split()
integer_tuple = tuple(int(i) for i in input_for_tuple)

print("The maximum element is: ", max(integer_tuple))
print("The minimum element is: ", min(integer_tuple))