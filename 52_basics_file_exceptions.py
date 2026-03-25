'''1. Write a Python program to:
Create a file named data.txt. Write the text "Hello Python" into it. Close the file'''

# fileobject = open('data.py', 'w')
# fileobject.write("Hello Python")
# fileobject.close()

'''2. Write a program to: Open data.txt. Read and print its contents'''

# fileobject = open('data.txt', 'r')
# content = fileobject.read()
# print(content)

'''3. Write a program to:
Open data.txt in append mode. Add the line "File handling is easy". Close the file'''

# fileobject = open('data.txt', 'a')
# fileobject.write("\nFile handling is easy")
# fileobject.close()

'''4. Write a program to read data.txt line by line and print each line.'''

# fileobject = open('data.txt', 'r')
# for i in fileobject:
#     print(i, end='\n')

'''5. Write a program to: Try opening a file that does not exist. Handle the error using try and except'''
# try:
#     fobj = open('mydata.txt', 'r')
#     d = fobj.read()
#     print(d)
#     fobj.close()
# except FileNotFoundError:
#     print("Nothing found!")

'''6. Write a program to: Open a file inside try. Close the file inside finally. Print a message "File closed"'''
# try:
#     fobj = open("mydata.txt", "r")
#     d = fobj.read()
#     print(d)
# except FileNotFoundError:
#     print("File not found")
# finally:
#     try:
#         fobj.close()
#         print("File Closed")
#     except:
#         pass

'''7. Write a program to: Create a binary file data.bin. Write some bytes into it'''

# fobj = open("data.bin", "wb")
# d = fobj.write(b"First Binary File")
# fobj.close()

'''8. Write a program to: Read and print the contents of data.bin'''

# fobj = open("data.bin", 'rb')
# d = fobj.read()
# nb = d.decode()
# print(nb)

'''9. Write a program to: Take a number as input. Raise an exception if the number is negative'''

# try:
#     num = int(input("Enter any number: "))
#     if num < 0:
#         raise ValueError("Don't enter negative number!")
#     print(num*2)
# except ValueError as e:
#     print(e)

'''10. Write a program to: Divide two numbers. Handle ZeroDivisionError. Print "Cannot divide by zero"'''

# try:
#     a = int(input("Enter first number: "))
#     b = int(input("Enter second number: "))
#     if b == 0:
#         raise ZeroDivisionError("Cannot divide by zero")
#     else:
#         print(float(a/b))
# except ZeroDivisionError as z:
#     print(z)

'''11. Write a program to: Open a text file data.txt. Count and print the total number of words in it'''

# fobj = open("data.txt", "r")
# d = fobj.read()
# print(len(d.split()))
# fobj.close()

'''12. Write a program to: Open a text file. Count and print the total number of lines'''

# fobj = open("data.txt", "r")
# d = fobj.readlines()
# print(len(d))
# fobj.close()

'''13. Write a program to: Open source.txt and destination.txt. Copy all contents from source to destination'''

# fsource = open("source.txt", "w+")
# s = fsource.write("New Source Content2")

# fsource.seek(0)
# sc = fsource.read()

# fdest = open("destination.txt", "w")
# d = fdest.write(sc)

'''14. Write a program to:
Take two numbers as input. Divide them and print the result. 
Handle ValueError if input is not a number. Handle ZeroDivisionError if denominator is 0'''

# try:
#     a = int(input("Enter first number: "))
#     b = int(input("Enter second number: "))
#     print("Division Ouput: ", a/b)
    
# except ValueError:
#     print("Entered value should be a number!")
    
# except ZeroDivisionError:
#     print("Denominator cannot be 0.")
    
'''15. Write a program to:
Take age as input. Raise an exception if age < 18. Print custom message: "Age must be 18 or older!"'''

# try:
#     age = int(input("Enter the age: "))
#     if age < 18:
#         raise ValueError("Age must be 18 or older!")
#     else:
#         print("You can vote or drive!")
# except ValueError as v:
#     print(v)
    
        

