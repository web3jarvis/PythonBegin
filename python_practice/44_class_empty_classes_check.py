'''Write a Python program to create two empty classes, Student and Marks. 
Now create some instances and check whether they are instances of the said classes or not. 
Also, check whether the said classes are subclasses of the built-in object class or not.
'''

class Student:
        pass
class Marks:
        pass

objStudent = Student()
objMarks = Marks()

print(isinstance(objStudent, Student))
print(isinstance(objMarks, Marks))
print(issubclass(Student, object))
print(issubclass(Marks, object)) 