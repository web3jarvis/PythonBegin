'''
    Take text input from the user
    Encode the input using:
    Hex encoding
    Base64 encoding
    Base58 encoding
    Decode the encoded values back to the original text
    Display all encoded and decoded outputs
'''
    
text = input("Enter any text: ").encode()

hex_encode = text.hex()
hex_decode = bytes.fromhex(hex_encode).decode()
print(hex_encode)
print(hex_decode)

import base64
b64_encode = base64.b64encode(text).decode()
print(b64_encode)
b64_decode = base64.b64decode(b64_encode).decode()
print(b64_decode)

import base58
b58_encode = base58.b58encode(text).decode()
print(b58_encode)
b58_decode = base58.b58decode(b58_encode).decode()
print(b58_decode)



