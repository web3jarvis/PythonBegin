'''Count how many times a given element appears in a tuple.'''

input_for_tuple = tuple(input("Enter the tuple elements separated by space: ").split())
element_to_check = input("Enter the element to count its appearance: ")


print("The number of times it appeared is: ", input_for_tuple.count(element_to_check))

#print('This element is not present in the tuple.')
        