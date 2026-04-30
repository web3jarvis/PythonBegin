'''1. You are given a list of transaction amounts:

transactions = [120, 45, 200, 75, 60, 30, 90]


👉 Tasks:

Create a new list that contains only even amounts

Calculate and print:

Filtered list

Total of filtered transactions'''

# transactions = [120, 45, 200, 75, 60, 30, 90]
# even = []

# for i in transactions:
#     if i % 2 == 0:
#         even.append(i)

# print("New List: ", even)
# print("Total of filtered transactions: ", sum(even))

'''2. You are given a list of user IDs:

user_ids = ["u1", "u2", "u1", "u3", "u2", "u4"]


👉 Tasks:

Remove duplicates while maintaining order

Print the cleaned list

📌 Constraint: ❌ Do NOT use set()'''

# user_ids = ["u1", "u2", "u1", "u3", "u2", "u4"]
# cleaned_list = []

# for i in user_ids:
#     if i not in cleaned_list:
#         cleaned_list.append(i)
        
# print(cleaned_list)

'''3. You are given a list of integers and a target sum:

numbers = [2, 7, 11, 15, 3, 6]
target = 9


👉 Tasks:

Find all unique pairs (a, b) such that:

a + b == target


Do NOT reuse the same index twice

Print pairs as tuples'''

# numbers = [2, 7, 11, 15, 3, 6]
# target = 9
# pairs = []

# for a in range(len(numbers)):
#     for b in range(a+1, len(numbers)):
#         if numbers[a] + numbers[b] == target:
#             pairs.append((numbers[a], numbers[b]))

# print(pairs)

'''4. You are given a tuple of numbers:

nums = (10, 20, 30, 40, 50)

Tasks:

Print the first element

Print the last element

Print the length of the tuple'''

# nums = (10, 20, 30, 40, 50)

# print(nums[0])
# print(nums[-1])
# print(len(nums))


'''5. Given:

data = (1, 2, 3, 2, 4, 2)

👉 Count how many times 2 appears in the tuple.'''

# data = (1, 2, 3, 2, 4, 2)
# count = 0
# for i in data:
#     if i == 2:
#         count += 1

# print(count)

'''6. Given:

employee = ("Amit", 30, "HR", 45000)

Tasks:

Unpack the tuple into variables'''

# employee = ("Amit", 30, "HR", 45000)

# name, age, department, salary = employee

# print(name)
# print(age)
# print(department)
# print(salary)

'''7. Reverse a String

Given:

word = "blockchain"

Tasks:

Reverse the string using a loop

Reverse the string using slicing'''


# word = "blockchain"

# reverse = ""
# for i in word:
#     reverse = i + reverse
# print(reverse)

# slice_reverse = word[::-1]
# print(slice_reverse)

'''nums = [10, 20, 30, 40]
👉 Find the sum of all elements using a loop.'''

# nums = [10, 20, 30, 40]
# sum = 0

# for i in nums:
#     sum += i

# print(sum)

'''items = ["apple", "banana", "cherry"]
👉 Remove "banana" from the list.'''

# items = ["apple", "banana", "cherry"]

# items.remove('banana')

# print(items)

'''s = "madam"
👉 Check whether the string is a palindrome.'''

# s = "madam"
# reverse = s[::-1]

# if s == reverse:
#     print("It is palindrome")
# else:
#     print("Not Palindrome")

