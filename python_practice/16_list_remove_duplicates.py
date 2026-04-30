'''Remove duplicate elements from a list.'''


input_list = input("Enter the elements separated by space: ").split()
output_list = []

for i in input_list:
    if i not in output_list:
        output_list.append(i)
        print("New list without duplicates: ", output_list)