'''
Design a Python program that demonstrates how digital signatures work using the Elliptic Curve Digital Signature Algorithm (ECDSA).

The program should:
- Generate a public–private key pair using elliptic curve cryptography
- Take a message from the user
- Create a digital signature for the message using the private key
- Verify the signature using the public key
- Display whether the message is authentic or tampered
'''

from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256 

key = ECC.generate(curve='P-256')

private_key = key
public_key = key.public_key()

msg = input("Enter the message to be send: ").encode()
hash_msg = SHA256.new(msg)

sender = DSS.new(private_key, 'fips-186-3')
signature = sender.sign(hash_msg)

verifier = DSS.new(public_key, 'fips-186-3')

try:
    verifier.verify(hash_msg, signature)
    print("Authentic!")
except ValueError:
    print("Tampered!")
