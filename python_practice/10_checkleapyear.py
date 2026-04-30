'''Take a year as input and check whether it is a leap year.'''

input_year = int(input("Enter the year:"))
if (input_year%4 == 0 and input_year%100 != 0) or input_year%400 == 0:
    print("Yes, the year is a leap year")
else:
    print("No, the year is not a leap year")