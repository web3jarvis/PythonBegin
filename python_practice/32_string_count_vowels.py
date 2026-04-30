'''Count the number of vowels in a string'''

input_string = input("Enter any string: ")
vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
vowel_count = 0

for i in input_string:
    if i in vowels:
        vowel_count += 1
        
print("The number of vowels: ", vowel_count)