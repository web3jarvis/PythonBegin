

# numbers = [10, 20, 30, 40, 50]

# print(numbers[0])
# print(numbers[-1])
# print(len(numbers))

# fruits = ["apple", "banana", "mango"]

# fruits.append("orange")
# # fruits.pop(1)
# fruits.remove("banana")
# print(fruits)

# data = [1, 2, 3, 2, 4, 2]
# count=0
# for i in data:
#     if i == 2:
#         count+=1

# print("Number of twos: ", count)

# nums = [4, 7, 2, 9, 5]
# sort = sorted(nums)

# print("Largest:", sort[-1])

# nums = [8, 3, 12, 6, 1]

# smallest = nums[0]
# for i in nums:
#     if i < smallest:
#         smallest = i
# print("Smallest", smallest)

# numbers=[10, 20, 30, 40]
# sum=0
# for i in numbers:
#     sum+=i
# print("Sum", sum)

# nums=[1, 2, 3, 4, 5, 6, 8, 10]
# count=0
# for i in nums:
#     if i%2==0:
#         count+=1
# print("Evens:", count)

# data = [1, 2, 3, 4, 5]
# print("Reverse: ", data[::-1])

# nums=[1, 2, 2, 3, 4, 4, 5]
# new_nums=[]
# for i in nums:
#     if i not in new_nums:
#         new_nums.append(i)
# print("No Duplicates: ", new_nums)

# nums = [10, 5, 8, 20, 15]
# print("Second Largest: ", sorted(nums)[-2])

# nums=[1, 2, 3, 4, 5, 6]
# evens=[]
# odds=[]
# for i in nums:
#     if i%2==0:
#         evens.append(i)
#     else:
#         odds.append(i)
# print(evens)
# print(odds)

# list1 = [1, 2, 3, 4]
# list2 = [3, 4, 5, 6]
# common=[]
# for i in list1:
#     if i in list2:
#         common.append(i)
# print(common)

# names = ["Ram","Shyam","Mohan"]
# marks = [80, 90, 85]

# for n, m in zip(names, marks):
#     print(n, m)

# matrix = [[1,2],[3,4],[5,6]]

# flat = [num for row in matrix for num in row]
# print(flat)

# for i in range(1,21):
#     print("Fizz"*(i%3==0) + "Buzz"*(i%5==0) or i)
    

# words = ["I","love","Python"]
# print(" ".join(words))

# student = {"name": "Rahul", "age": 20, "course": "Python"}
# print(student['name'])
# print(student['age'])

# person = {"name": "Amit", "city": "Delhi"}
# person["age"] = 25
# print(person)

# product = {"name": "Laptop", "price": 50000}
# product["price"]=55000
# print(product)

# data={"a": 10, "b": 20, "c": 30}
# del data['b']
# print(data)

# info = {"name": "Neha", "age": 22}
# if "age" in info:
#     print("Yes")

# car = {"brand": "Toyota", "model": "Fortuner", "year": 2022}
# print(list(car.keys()))
# print(list(car.values()))

# marks = {"math": 80, "science": 75, "english": 90}
# for key, value in marks.items():
#     print(key, ":", value)

# expenses = {"food": 500, "travel": 300, "shopping": 700}
# te=sum(expenses.values())
# print(te)

# text = "banana"
# new_dict={}
# b=text.count('b')
# a=text.count('a')
# n=text.count('n')

# b, a, n = new_dict.keys()
# print(new_dict)

# from collections import Counter
# print(dict(Counter("banana")))

# nums = [3, 7, 2, 9, 5]
# smallest = nums[0]
# for i in nums:
#     if i<smallest:
#         smallest=i
# print(smallest)

# nums = [5, 10, 15, 20, 25]
# print([i for i in nums if i>=15])
# for i in nums:
#     if i>=15:
#         above_15.append(i)
# print(above_15)

# nums = [1, 2, 2, 3, 3, 4, 5]
# print(list(set(nums)))

# nums = [1, 2, 3, 4, 5, 6]
# print("Evens:", len([i for i in nums if i%2==0]))

# text = "python"
# print([i for i in text])

# from collections import Counter
# nums = [1, 2, 3, 4, 5]
# squares={i:i*i for i in nums}
# print(dict(Counter(squares)))

# nums = [1, 2, 3, 4, 5]
# squares = {}
# for i in nums:
#     squares[i] = i * i
# print(squares)

# nums = [1, 2, 3, 4, 5]
# print("Cube: ", {i:i*i*i for i in nums})

# nums = [1,2,3,4,5,6]
# print({i:i*i for i in nums if i%2==0})

# words = ["apple", "banana", "cherry"]
# print({i:len(i) for i in words})

# text = "abc"
# print({i:ord(i) for i in text})
        
# nums = [5, 12, 7, 18, 3]
# print({i:i*i for i in nums if i>10})
