'''Design a Python program using inheritance to manage employee details in a company.'''

class Employee:
    # def __init__(self):
    #     self.name = ""
    #     self.employee_id = 0
    #     self.salary = 0
    def input_details(self):
        self.name = input("Enter the Employee Name: ")
        self.employee_id = int(input("Enter the Employee ID: "))
        self.salary = int(input("Enter the Employee Salary: "))
    def display_details(self):
        print("Employee Name: ",self.name)
        print("Employee ID: ", self.employee_id)
        print("Employee Salary: ", self.salary)

class Manager(Employee):
    def additional(self):
        self.department = input("Enter the Manager Department: ")
    def display_manager_details(self):
        print(f'{self.name} works in {self.department}')
    
objManager = Manager()

objManager.input_details()
objManager.additional()
objManager.display_details()
objManager.display_manager_details()
