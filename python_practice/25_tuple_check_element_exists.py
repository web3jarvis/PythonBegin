'''Check whether an element exists in a tuple.'''

input_tuple = tuple(input("Enter a set of numbers or chars separated by space: ").split())
element_to_check = input("Enter an element to check: ")

if element_to_check in input_tuple:
    print("<<<Yes the entered element exists in the tuple.>>>")
else:
    print("<<<Does not exist.>>>")
        
