'''
Write a simple Python class named Student and display its type.
Also, display the __dict__ attribute keys and 
the value of the __module__ attribute of the Student class.
'''
class Student:
    def __init__(self):
        self.firstname = input("Enter the first name: ")
        self.lastname = input("Enter the last name: ")
        self.rollno = int(input("Enter the roll number: "))
    def display(self):
        print("Student First Name: ", self.firstname)
        print("Student Last Name: ", self.lastname)
        print("Student Roll Number: ", self.rollno)

objStudent = Student()
objStudent.display()
print(type(Student))
print(objStudent.__dict__.values())
print(objStudent.__module__)
