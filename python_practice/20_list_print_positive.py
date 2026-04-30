'''Print only the positive numbers from a list.'''

input_list = [int(i) for i in input("Enter the elements separated by space: ").split()]  #1 2 -3 4 -5
positive_only_list = []

for i in input_list:
    if i > 0:
        positive_only_list.append(i)
        
print(positive_only_list)
    

