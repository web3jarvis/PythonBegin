'''1. Create an empty list. Take a number as input and add it to the list using append(). Print the list.'''

# input_num = input("Enter numbers: ")
# empty_list = []

# print(input_num)

# for i in input_num:
#     empty_list.append(input_num)
    
# print(empty_list)

'''2. Create a list: x = [10, 20]. Use append([30, 40]). Print the list
Then use extend([30, 40]). Print the list again'''

# x = [10, 20]
# x.append([30, 40])
# print(x)

# x = [10, 20]
# x.extend([30, 40])
# print(x)

'''3. Create a list of numbers. Insert a new number at index 0 using insert().'''

# num_list = input("Enter the numbers: ").split()
# new_num = input("Enter the new number to add: ")

# num_list.insert(0, new_num)
# print(num_list)

'''4. Create a list: x = [10, 20, 40, 50]. Insert 30 at the correct position using insert().'''

# x = [10, 20, 40, 50]
# x.insert(2, 30)
# print(x)

'''5. Create a list: x = [5, 10, 15, 20]. Replace 15 with 99 using index replacement.'''

# x = [5, 10, 15, 20]
# i = x.index(15)
# x[i] = 99
# print(x)

'''6. Create a list of numbers. Replace: First element with 100. Last element with 500'''

# num_list = list(map(int, input("Enter the numbers: ").split()))
# num_list[0] = 100
# num_list[-1] = 500
# print(num_list)

'''7. Create a list: x = [1, 2, 3, 4, 5]. 
Take: index from user. new value from user. Replace the element at that index.'''

# x = [1, 2, 3, 4, 5]
# user_index = int(input("Which index to modify? "))
# if user_index < 0 or user_index >= len(x):
#     print("Not Possible!")
# else:
#     new_value = int(input("Enter the new value to enter: "))
#     x[user_index] = new_value
#     print(x)


'''8. Create an empty list and perform the following:
Append 10. Append 20. Insert 15 at index 1. Extend the list with [25, 30]
Replace 20 with 99. Print the final list.'''

# el = []; print(el) #[]
# el.append(10); print(el) #10
# el.append(20); print(el) #10, 20
# el.insert(1, 15); print(el) #10, 15, 20
# el.extend([25, 30]); print(el) #10, 15, 20, 25, 30
# el[2] = 99; print(el)

'''9. Create a list of numbers. Remove a given number from the list using remove().'''

# nl = list(map(int, input("Enter the numbers: ").split()))
# tr = int(input("Enter the number to remove: "))

# if tr in nl:
#     nl.remove(tr)
#     print(nl)
# else:
#     print("Number not in list.")
    
'''10. Create a list and remove the last element using pop(). Print both: Removed element. Updated list'''

# nl = list(map(int, input("Enter the numbers: ").split()))
# print(nl.pop())
# print(nl)

'''11. Create a list of numbers. Remove an element at a given index using pop(index).'''

# nl = list(map(int, input("Enter the numbers: ").split()))
# index_tr = int(input("Enter the index number to remove: "))

# print(nl.pop(index_tr))
# print(nl)

'''12. Create a list of numbers. Delete the element at index 2 using del.'''

# n_list = list(map(int, input("Enter the numbers: ").split())) #11 22 33 44 55

# del n_list[2]
# print(n_list)

'''13. Create a list of numbers. Delete elements from index 1 to 3 using del.'''

# n_list = list(map(int, input("Enter the numbers: ").split())) #11 22 33 44 55 66

# del n_list[1:4]
# print(n_list)

'''14. Create a list of numbers and reverse it using reverse().'''

# n_list = list(map(int, input("Enter the numbers: ").split())) #11 22 33 44 55 66
# n_list.reverse()
# print(n_list)

'''15. Create a list: x = [1, 2, 3]. Repeat the list 3 times using * operator and print the result.'''

# x = [1, 2, 3]
# y = x * 3
# print(y)

'''16. Create a list of numbers and sort it in ascending and descending order using sort().'''

l = list(map(int, input("Enter the numbers: ").split())) #11 22 66 33 44 55 01

l.sort(); print(l)
l.sort(reverse=True); print(l)

