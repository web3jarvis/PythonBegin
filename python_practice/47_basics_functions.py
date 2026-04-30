'''1. Write a function named hello() that prints: Hello, World!'''
# def hello():
#   print("Hello, World!")
# hello()

'''2. Write a function that takes two numbers as parameters and prints their sum.'''
# def num_sum(a, b):
#   print("Sum:", a+b)
# num_sum(int(input("Enter First: ")), int(input("Enter Second: ")))

'''3. Write a function that takes a number as input and returns its square.'''
# def square(a):
#   print("Its Square: ", a * a)
# square(int(input("Enter Number: ")))

'''4. Write a function that takes a number and prints whether it is even or odd.'''
# def evenodd(a): print("Even" if a % 2 == 0 else "Odd")
# evenodd(int(input("Enter Number: ")))

'''5. Write a function that takes two numbers and returns the larger number.'''
# def larger(a, b): print("Larger: ",a if a > b else b)
# larger(int(input("Enter First: ")), int(input("Enter Second: ")))

'''6. Write a function that takes a string and returns the number of vowels in it.'''
# def numofvowels(string):
#     c = 0
#     for i in string.lower():
#         if i in "aeiou": c += 1
#     print("The number of vowels are", c)

# numofvowels(input("Enter any word: "))
        
'''7. Write a function that takes a list of numbers and returns the sum of all elements.'''
# def sumofall(num_list):
#     int_list = [int(i) for i in num_list]
#     print(sum(int_list))
    
# sumofall(input("Enter numbers separated by space: ").split())

'''8. Write a function that takes a name as argument and prints: Hello, <name>
If no name is given, it should print: Hello, Guest'''
# def sayhello(name):
#     print("Hello, Guest" if name == "" else "Hello,", name)
# sayhello(input("Enter name: "))

'''9. Write a function that takes a number and returns True if it is prime, otherwise False.'''
# def checkprime(n):
#     if n <= 1:
#         return False
#     else:
#         for i in range(2, n):
#             if n % i == 0:
#                 return False
#         else:
#             return True

# print(checkprime(int(input("Enter any number: "))))