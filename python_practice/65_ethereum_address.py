"""Generate an Ethereum Address from a public key"""

from Crypto.Hash import keccak
from Crypto.PublicKey import ECC, 


key = ECC.generate(curve="SECP256K1")
private_key = key
public_key = key.public_key()
public_key_xy = public_key.pointQ.x.to_bytes(32, 'big') + public_key.pointQ.y.to_bytes(32, 'big')

hash_object = keccak.new(digest_bits=256)
hash_object.update(public_key_xy)
key_hash = hash_object.hexdigest()

ETH_ADDRESS = "0x" + key_hash[-40:]


print("-"*50)
print(public_key)
print("-"*50)
print(public_key.export_key(format="DER"))
print("-"*50)
print("Key XY", public_key_xy)
print("-"*50)
print("Hash", key_hash)
print("-"*50)
print("Ether Address", ETH_ADDRESS)
print("-"*50)


