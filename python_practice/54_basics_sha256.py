'''1. Write a Python program to: Take a string as input. Generate and print its SHA-256 hash'''

#Option 1
# import hashlib as myhash
# mystring = input("Enter your name: ")

# new_hash = myhash.sha256(mystring.encode()).hexdigest()
# print(new_hash)

#################################

#Option 2

# from Crypto.Hash import SHA256
# mystring = input("Enter your name: ")

# hobj = SHA256.new()
# hobj.update(mystring.encode())
# print(hobj.hexdigest())

'''2. Write a program to: Take a password as input. Convert it to SHA-256 hash. Print the hashed password'''

# from Crypto.Hash import SHA256
# mypwd = input("Enter the password: ")

# hobj = SHA256.new()
# hobj.update(mypwd.encode())
# print(hobj.hexdigest())

'''3. Write a program to: Hash the same string twice. Check whether both hashes are equal'''

# from Crypto.Hash import SHA256
# import os
# mypwd = input("Enter the password: ")

# h1 = SHA256.new()
# h1.update(mypwd.encode())
# fh1 = h1.hexdigest()

# salt = os.urandom(16)
# h2 = SHA256.new()
# h2.update(mypwd.encode() + salt)
# print(mypwd.encode() + salt)
# fh2 = h2.hexdigest()

# print("Same Hash Values." if fh1 == fh2 else "Not Same")

'''4. Write a program to: Hash two different strings. Print both hashes. Check whether they are same or different'''

# from Crypto.Hash import SHA256

# apwd = input("Enter the password: ")
# h1 = SHA256.new()
# h1.update(apwd.encode())
# fh1 = h1.hexdigest()
# print(fh1)

# bpwd = input("Enter another password: ")
# h2 = SHA256.new()
# h2.update(bpwd.encode())
# fh2 = h2.hexdigest()
# print(fh2)

# print("Same!" if fh1 == fh2 else "Different!")

'''5. Write a program to:
Store a SHA-256 hash of a password. Take user input password. Hash it and verify whether it matches the stored hash'''

# from Crypto.Hash import SHA256

# storedhash = SHA256.new("qwerty".encode()).hexdigest()
# print(storedhash)

# user_pwd = input("Enter your password: ")
# user_hash = SHA256.new(user_pwd.encode()).hexdigest()
# print(user_hash)

# print("Matched!" if storedhash == user_hash else "Not matched!")

'''6. Write a program to: Read a text file. Generate and print its SHA-256 hash'''

# from Crypto.Hash import SHA256

# fobject = open('data.txt', 'r')
# data = fobject.read()
# fobject.close()
# print(data)

# datahash = SHA256.new(data.encode()).hexdigest()
# print(datahash)

'''7. Write a program to:
Hash a file. Modify the file content. Hash it again. Compare both hashes and print whether file was changed'''

# from Crypto.Hash import SHA256

# f = open('data.txt', 'r')
# fdata = f.read() 
# filehash = SHA256.new(fdata.encode()).hexdigest()
# print(filehash)

# f = open('data.txt', 'a')
# f.write("\nnew line")

# f = open('data.txt', 'r')
# new_fdata = f.read()
# new_filehash = SHA256.new(new_fdata.encode()).hexdigest()
# print(new_filehash)

# if filehash == new_filehash:
#     print("Hash Matching!")
# else:
#     print("Unmatched!")

'''8. Write a program to:
Take a string .Encode it using UTF-8. Generate its SHA-256 hash (Understand why encoding is needed)'''

# from Crypto.Hash import SHA256

# def generate_hash(data):
#     string_hash = SHA256.new(data.encode("utf-8")).hexdigest()
#     print(string_hash)
#     print(len(string_hash))

# generate_hash(input("Enter any string: "))