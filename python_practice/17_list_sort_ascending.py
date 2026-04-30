'''Sort a list in ascending order without using sort().'''

input_list = [int(i) for i in input("Enter the elements separated by space: ").split()] #11 22 55 33 77 99 44
output_list = []

while len(input_list) > 0:
    smallest_one = min(input_list)
    output_list.append(smallest_one)
    input_list.remove(smallest_one)
    
print("Ascending Order: ", output_list)