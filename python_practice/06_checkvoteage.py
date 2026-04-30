'''Take age as input and check whether the person is eligible to vote (age >= 18).'''

user_age = int(input("Enter the voter age: "))
if user_age >= 18:
    print("The voter is eligible for voting.")
else:
    print("The voter is not eligible for voting.")