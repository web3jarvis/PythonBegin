'''Take a number as input and check whether it is divisible by both 5 and 11.'''

number = int(input("Enter a whole number: "))
if number%5 == 0 and number%11 == 0:
    print("The number is divisible by both 5 and 11.")
elif number%5 == 0 and number%11 != 0:
    print("The number is divisible by 5 but not by 11")
elif number%5 != 0 and number%11 == 0:
    print("The number is divisible by 11 but not by 5")
else:
    print("The number is not divisible by both 5 and 11")
