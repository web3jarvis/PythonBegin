'''Reverse a list without using the reverse() method'''

num_list = [int(i) for i in input("Enter the numbers separated by space: ").split()]
empty_list = []

for num in num_list:
    empty_list.insert(0, num)

print("The Reverse List: ", empty_list)

