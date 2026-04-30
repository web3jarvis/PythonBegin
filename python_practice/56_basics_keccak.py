'''1. Write a Python program to: Take a string as input. Generate and print its Keccak (SHA3-256) hash'''

from Crypto.Hash import keccak

input_string = input("Enter any string: ")

hobj = keccak.new(digest_bits=256)
hobj.update(input_string.encode("utf-8"))

print(hobj.hexdigest())

'''2. Write a program to: Hash the same string two times using Keccak. Check whether both hashes are equal'''

from Crypto.Hash import keccak

string = input("Enter String: ")
hobj1 = keccak.new(digest_bits=256)
hobj1.update(string.encode("utf-8"))
h1 = hobj1.hexdigest()
print(h1)

hobj2 = keccak.new(digest_bits=256)
hobj2.update(string.encode("utf-8"))
h2 = hobj2.hexdigest()
print(h2)

print("Both hashes are same!" if h1 == h2 else "Hashes are different!")


'''3. Write a program to: Read a text file. Generate its Keccak hash'''

# from Crypto.Hash import keccak

# fobj = open('data.txt', 'r')
# fdata = fobj.read()

# k_hash = keccak.new(digest_bits=256)
# k_hash.update(fdata.encode("utf-8"))

# print(k_hash.hexdigest())

'''4. Ethereum-style address generation'''

# import hashlib

# public_key = "my_public_key"

# keccak_hash = hashlib.sha3_256(public_key.encode()).hexdigest()

# eth_address = "0x" + keccak_hash[-40:]

# print(eth_address)

#########################################

# from Crypto.Hash import keccak

# public_key = "my_public_key"

# keccak_obj = keccak.new(digest_bits=256)
# keccak_obj.update(public_key.encode())
# keccak_hash = keccak_obj.hexdigest()

# eth_address = "0x" + keccak_hash[-40:]

# print(eth_address)