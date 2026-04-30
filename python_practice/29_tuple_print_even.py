'''Print only the even numbers from a tuple.'''

input_tuple = tuple(input("Enter the elements separated with space: ").split())
even_tuple = []

for i in input_tuple:
    if int(i) % 2 == 0:
        even_tuple.append(i)

print("Tuple of Evens:", tuple(even_tuple))

