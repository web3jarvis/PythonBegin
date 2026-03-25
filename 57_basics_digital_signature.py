'''1. Write a Python program to:

Generate a public key and private key

Print both keys using ECDSA'''

# from Crypto.Hash import SHA256
# from Crypto.Signature import DSS
# from Crypto.PublicKey import ECC

# key = ECC.generate(curve='P-256')
# private_key = key
# public_key = key.public_key()

# print(private_key)
# print(public_key)

'''2. Write a program to: Take a text message. Create a digital signature using a private key'''

# from Crypto.Hash import SHA256
# from Crypto.Signature import DSS
# from Crypto.PublicKey import ECC

# key = ECC.generate(curve='P-256')
# private_key = key
# public_key = key.public_key()

# msg = input("Enter any message: ").encode()
# hobj = SHA256.new(msg)
# msg_hash = hobj.hexdigest()
# print(msg_hash)

# owner = DSS.new(private_key, 'fips-186-3')
# signature = owner.sign(hobj)
# print("Digital Signature: ", signature.hex())

'''3. Write a program to:
Verify the digital signature of a message using the public key. Print whether the signature is valid or not'''

# from Crypto.Hash import SHA256
# from Crypto.Signature import DSS
# from Crypto.PublicKey import ECC

# key = ECC.generate(curve='P-256')
# private_key = key
# public_key = key.public_key()

# msg = input("Enter any message: ").encode()
# hobj = SHA256.new(msg)
# msg_hash = hobj.hexdigest()

# owner = DSS.new(private_key, 'fips-186-3')
# signature = owner.sign(hobj)

# verifier = DSS.new(public_key, 'fips-186-3')
# try:
#     verifier.verify(hobj, signature)
#     print("Verified!")
# except ValueError:
#     print("Not Verified!")
    
'''4. Write a program to:
Sign a message. Change the message. Verify the old signature on the new message. Observe what happens.'''

# from Crypto.Signature import DSS
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import ECC

# key = ECC.generate(curve="P-256")
# private_key = key
# public_key = key.public_key()

# first_message = input("Enter the first message: ").encode()
# hash_first_message = SHA256.new(first_message)

# changed_message = input("Enter the changed message: ").encode()
# hash_changed_message = SHA256.new(changed_message)

# owner = DSS.new(private_key, 'fips-186-3')
# signature = owner.sign(hash_first_message)
# verifier = DSS.new(public_key, 'fips-186-3')

# try:
#     verifier.verify(hash_changed_message, signature)
#     print("Verified!")
# except ValueError:
#     print("Not Verified!")
    
'''5. Write a program to: Read a file. Create a digital signature for the file'''

# from Crypto.PublicKey import ECC
# from Crypto.Signature import DSS
# from Crypto.Hash import SHA256

# key = ECC.generate(curve="P-256")
# private_key = key
# public_key = key.public_key()

# fileobj = open("data.txt", "r")
# data = fileobj.read()
# datahash = SHA256.new(data.encode())

# signer = DSS.new(private_key, 'fips-186-3')
# signature = signer.sign(datahash)
# print("Digital Signature: ", signature.hex())


'''6. Write a function: def sign_message(message, private_key):
That returns the digital signature.'''

# from Crypto.PublicKey import ECC
# from Crypto.Hash import SHA256
# from Crypto.Signature import DSS

# def sign_message(message, private_key):
    
#     message_hash = SHA256.new(message)
    
#     signer = DSS.new(private_key, 'fips-186-3')
#     signature = signer.sign(message_hash)
    
#     print(signature.hex())

# key = ECC.generate(curve="P-256")
# private_key = key

# sign_message(input("Enter the message to be send: ").encode(), private_key)
    
    
'''7. Write a program that: Generates keys. Signs a message. Verifies the signature'''

# from Crypto.PublicKey import ECC
# from Crypto.Signature import DSS
# from Crypto.Hash import SHA256

# key = ECC.generate(curve='P-256')
# private_key = key
# public_key = key.public_key()

# message = input("Enter any message: ").encode()
# message_hash = SHA256.new(message)

# signer = DSS.new(private_key, 'fips-186-3')
# signature = signer.sign(message_hash)

# verifier = DSS.new(public_key, 'fips-186-3')
# verifier.verify(message_hash, signature)
    
    
    
    
    
    