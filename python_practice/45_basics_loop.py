'''1. Use a for loop to print numbers from 1 to 10.'''
# for i in range(1, 11):
#     print(i)

'''2. Use a loop to print all even numbers from 1 to 20.'''
# for i in range(2,21,2):
#     print(i)

'''3. Take a number n as input and use a loop to find the sum of numbers from 1 to n.'''
# n = int(input("Enter the range of number 'n': "))
# sum_n = 0
# for i in range(1, n+1):
#     sum_n += i

# print(sum_n)

'''4. Take a number as input and print its multiplication table up to 10.'''
# n = int(input("Enter the number: "))
# for i in range(1, 11):
#     print(f'{n} x {i} = ', n*i)

'''5. Take a number as input and use a while loop to count how many digits it has.'''
# n = input("Enter the number: ")
# length = len(n)
# count = 1
# while (count<length):
#     count += 1
#     if '-' in n:
#         length = len(n)-1
        
# print(count)

'''6. Take a number as input and reverse it using a loop.'''
# n = input("Enter the number: ")
# reverse_n = ""
# for i in n:
#     reverse_n = i + reverse_n
    
# print(reverse_n)
    
'''7. Use nested loops to print:'''
# char = input("Enter any character: ")

#option 1
# for i in range(1, 6):
#     for j in range(i):
#         print(char, end="")
#     print()

#option 2
# for i in range(1, 6):
#     print(char*i)
    
# for i in range(5,0,-1):
#     print(char*i)

'''8. Take a number as input and check whether it is prime or not using a loop.'''
# n = int(input("Enter the number: "))
# while n > 0:
#     if n%1 == 0 or n%n == 0:
#         print("Prime")
#         break
#     elif n%1 != 0 and n%n != 0:
#         print("Not Prime")
#         break

'''9. Use a loop to print numbers from 1 to 10, but stop the loop when number is 6.'''

# for i in range(1, 11):
#     print(i, end=" ")
#     if i == 6:
#         break