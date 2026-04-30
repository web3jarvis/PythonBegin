'''1. Create a tuple using tuple packing with 3 values: name, age, marks. Print the tuple.'''

# name, age, marks = input("Enter name, age, marks with spaces: ").split()
# my_tuple = name, int(age), float(marks)
# print(my_tuple)

'''2. Given a tuple: t = ("Rahul", 20, 85). Unpack the tuple into three variables and print them.'''

# t = ("Rahul", 20, 85)
# name, age, marks = t
# print(name)
# print(int(age))
# print(float(marks))

'''3. Create a tuple: t = (10, 20). Repeat the tuple 3 times using * operator.'''

# t = (10, 20)
# print(t * 3)

'''4. Create a tuple of numbers. Sort it and print the result.'''

# input_num = input("Enter the tuple of numbers: ").split()
# num_tuple = tuple(int(i) for i in input_num)
# t = tuple(sorted(num_tuple)); print(t)
# t = tuple(sorted(num_tuple, reverse=True)); print(t)

'''5. Create a tuple and delete it using the del keyword. Try printing it after deletion and observe the result.'''
# input_tuple = tuple(input("Enter the tuple elements: ").split())
# del input_tuple
# print(input_tuple)

'''6. Create a tuple of numbers. Change one element by: 
Converting tuple to list. Modifying the element. Converting back to tuple'''
# input_num = input("Enter the tuple of numbers: ").split()
# num_tuple = tuple(int(i) for i in input_num)
# num_list = list(num_tuple)

# print(num_tuple)
# print(num_list)
# num_list[0] = 10
# print(tuple(num_list))

'''7. Given a tuple: t = (1, 2, 3, 4, 5)
Unpack: First element into a. Last element into b. Remaining elements into c'''

# t = (1, 2, 3, 4, 5)
# a, *c, b = t
# print(a)
# print(b)
# print(c)

'''8. Create a tuple containing two tuples: ((1, 2), (3, 4)) 
Unpack both inner tuples into separate variables.'''

# t = ((1,2), (3,4))
# a, b = t; one, two = a; three, four = b
# print(a); print(b); print(one); print(two); print(three); print(four)

'''9. Create two tuples and: Concatenate them. Repeat the final tuple 2 times. Print the result.'''
# t1 = tuple(input("Enter tuple one: ").split())
# t2 = tuple(input("Enter tuple two: ").split())
# c = t1 + t2
# print(c*2)