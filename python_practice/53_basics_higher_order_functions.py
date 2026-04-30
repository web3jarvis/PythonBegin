'''Write a function apply_operation(func, a, b) that:
Takes another function as argument. Applies it to a and b. Example operations: add, multiply.'''

# def add(a,b):
#     return a + b
    
# def multiply(a,b):
#     return a * b

# def apply_operation(func,a,b):
#     return func(a,b)

# a = int(input("Enter valur of a: "))
# b = int(input("Enter valur of b: "))  
# print(apply_operation(add,a,b))
# print(apply_operation(multiply,a,b))

'''2. Write a function that returns another function which adds 10 to a number.'''

# def add_10(a):
#     return a + 10

# def hof(func, a):
#     return func(a)

# a = int(input("Enter any number: "))
# print("New Number: ", hof(add_10, a))

'''3. Create a generator function that yields numbers from 1 to 5 using yield.'''

# def mygen():
#     for i in range(1, 6):
#         yield i

# g = mygen()
# for j in g:
#     print(j)

'''4. Create a generator that yields even numbers from 1 to 20.'''

# def mygen():
#     for i in range(1, 21):
#         if i % 2 == 0:
#             yield i
            
# genobj = mygen()
# for j in genobj:
#     print(j)

'''5. Create a list and: Convert it into an iterator using iter(). Print elements using next()'''

# input_list = list(input("Enter the list element: ").split())
# print(input_list)
# itr = iter(input_list)

# for i in itr:
#     print(i)
    
'''6. Write a program that: Uses next() on an iterator. Handles the StopIteration exception'''
# try:
#     input_list = list(input("Enter the list elements: ").split())
#     itr = iter(input_list)

#     while True:
#         print(next(itr))
# except StopIteration:
#     print("XXXStop Iteration ErrorXXX")

'''7. Create a generator that yields square of numbers from 1 to 10.'''

# def mygen():
#     for i in range(1, 11):
#         yield i**2

# gobj = mygen()
# try:
#     while True:
#         print(next(gobj))
# except StopIteration:
#     pass

'''8. Write a decorator that:
Prints "Function started" before execution. Prints "Function ended" after execution. Apply it to a function.'''

# def mydecorator(func):
#     def wrapper():
#         print("Function Started")
#         func()
#         print("Function Ended")
#     return wrapper

# @mydecorator
# def func():
#     print("My Name is X")
    
# func()

'''9. Write a decorator that: Prints the function name. Then executes the function'''

# def mydecorator(myfunc):
#     def wrapper():
#         print("The name of the function is", myfunc.__name__)
#         myfunc()
#     return wrapper

# @mydecorator
# def newfunc():
#     print("And it do nothing.")
# try:
#     newfunc()
# except RecursionError:
#     pass

'''10. Write: A normal function that returns a list of numbers from 1 to 5.
A generator that yields numbers from 1 to 5. Print outputs of both.'''

# def numlist():
#     for i in range(1,6):
#         return i

# def mygenerator():
#     for j in range(1,6):
#         yield j

# print(numlist())        
# gobj = mygenerator()
# try:
#     while True:
#         print(next(gobj))
# except StopIteration:
#     pass
    
