'''Count how many even and odd numbers are present in a list.'''

num_list = [int(i) for i in input("Enter the numbers separated by space: ").split()]
even_count = sum(1 for num in num_list if num % 2 == 0)
odd_count = len(num_list) - even_count

print("Even Count: ", even_count)
print("Odd Count: ", odd_count)