'''Design a Python application using cryptographic hashing to:

1. Securely hash user passwords

2. Verify password authenticity

3. Generate file integrity hashes

4. Compare SHA-256 and Keccak-256 outputs'''

from Crypto.Hash import SHA256, keccak

# 1. Securely hash user passwords
def HashingPassword(pwd):
    hashValue = SHA256.new()
    hashValue.update(pwd.encode())
    return hashValue.hexdigest()

# 2. Verify password authenticity
def VerifyPassword(stored_hash, reenter_pwd):
    new_hash = HashingPassword(reenter_pwd)
    return stored_hash == new_hash

# 3. Generate file integrity hashes
def hash_file_sha256(filename):
    hashValue = SHA256.new()
    try:
        with open(filename, "rb") as f:
            while chunk := f.read(4096):
                hashValue.update(chunk)
        return hashValue.hexdigest()
    except FileNotFoundError:
        return None

def hash_file_keccak(filename):
    hashValue = keccak.new(digest_bits=256)
    try:
        with open(filename, "rb") as f:
            while chunk := f.read(4096):
                hashValue.update(chunk)
        return hashValue.hexdigest()
    except FileNotFoundError:
        return None

# Creating a menu options for Call-To-Action   
def menu():
    print("\n====== Crypto Hashing Project ======")
    print("1. Hash a Password (SHA-256)")
    print("2. Verify Password")
    print("3. Hash a File (SHA-256)")
    print("4. Hash a File (Keccak-256)")
    print("5. Exit")

stored_password_hash = None
while True:
    menu()
    choice = input("Enter your choice: ")
    
    if choice == "1":
        stored_password_hash = HashingPassword(input("Enter password: "))
        print("Password Hash (SHA-256):", stored_password_hash)
    
    elif choice == "2":
        if stored_password_hash is None:
            print("No password stored yet. Please hash a password first.")
        else:
            reenter_pwd = input("Enter password to verify: ")
            if VerifyPassword(stored_password_hash, reenter_pwd):
                print("✅ Password Verified Successfully")
            else:
                print("❌ Incorrect Password")
    
    elif choice == "3":
        filename = input("Enter file name: ")
        file_hash = hash_file_sha256(filename)
        if file_hash:
            print("SHA-256 File Hash:", file_hash)
        else:
            print("File not found!")

    elif choice == "4":
        filename = input("Enter file name: ")
        file_hash = hash_file_keccak(filename)
        if file_hash:
            print("Keccak-256 File Hash:", file_hash)
        else:
            print("File not found!")
    
    elif choice == "5":
        print("Exiting program!")
        break
    
    else:
        print("Invalid choice, Try again!")
    