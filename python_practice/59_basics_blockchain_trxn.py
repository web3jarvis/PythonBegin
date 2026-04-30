'''Design a Python program that simulates a basic blockchain transaction system.

The program should:

Generate a wallet using ECDSA. Encode wallet keys using Hex & Base58. Take a transaction message from the user.

Hash the transaction using:

SHA-256, Keccak-256

Digitally sign the transaction using ECDSA

Verify the signature using the public key

Display all outputs clearly to show how blockchain security works'''

from Crypto.Hash import SHA256, keccak
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import base58

###################################

key = ECC.generate(curve = 'P-256')
private_key = key #d
public_key = key.public_key() #Q = x + y

###################################

hex_private_key = hex(private_key.d)
hex_public_key = hex(public_key.pointQ.x + public_key.pointQ.y)

# print(private_key.d)

b58_private_key = base58.b58encode(private_key.d).decode()
b58_public_key = base58.b58encode(public_key).decode()

###################################

t_message = input("Enter the transaction message: ").encode()

sha256_message = SHA256.new(t_message)

keccak_message = keccak.new(digest_bits=256)
keccak_message.update(t_message)

###################################

owner = DSS.new(private_key, 'fips-186-3')
signature = owner.sign(sha256_message)
verifier = DSS.new(public_key, 'fips-186-3')
try:
    verifier.verify(sha256_message, signature)
    print("Verified!")
except ValueError:
    print("Not Verified!")

###################################
# print(sha256_message)
# print(keccak_message)

# print(private_key)
# print(hex_private_key)
# print(b58_private_key)

# print(public_key.pointQ)
# print(hex_public_key)
# print(b58_public_key)

