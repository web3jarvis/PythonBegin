'''Design a Python program using Object-Oriented Programming (OOP) concepts to manage student information.'''


class Student:
    # def __init__(self):
    #     self.name = ""
    #     self.roll_number = 0
    #     self.marks = 0.0
    def input_details(self):
        self.name = input("Enter the Student Name: ")
        self.roll_number = int(input("Enter the Student Roll Number: "))
        self.marks = float(input("Enter the Student Marks: "))
    def display_details(self):
        print("Student Name: ", self.name)
        print("Student Roll Number: ", self.roll_number)
        print("Student Marks: ", self.marks)
    def calculate_result(self):
        if self.marks >= 40:
            print("Pass")
        else:
            print("Fail")

objStudent = Student()
          
objStudent.input_details()
objStudent.display_details()
objStudent.calculate_result()
            