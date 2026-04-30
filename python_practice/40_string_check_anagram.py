'''Check whether two strings are anagrams.'''

input_01 = input("Enter the first string: ") #pils
input_02 = input("Enter the second string: ") #slip
alphabets = 'abcdefghijklmnopqrstuvwxyz'
sorted_input_01 = ""
sorted_input_02 = ""

for i in alphabets:
    for j in input_01:
        if i == j:
            sorted_input_01 += i
            
for k in alphabets:
    for l in input_02:
        if k == l:
            sorted_input_02 += k
                 
if len(input_01) != len(input_02) or sorted_input_01 != sorted_input_02:
    print("These words are not anagram")
    
elif sorted_input_01 == sorted_input_02:
    print("These words are anagram")