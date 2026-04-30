'''Design a Python program that simulates an Account-Based blockchain transaction system (similar to Ethereum).

The program should:
    -Maintain a list of accounts with balances
    -Allow users to:
    -View account balances
    -Send transactions between accounts
    -Deduct balance from sender
    -Add balance to receiver
    -Track nonce (transaction count) for each account
    -Deduct transaction fee (gas fee)
    -Prevent transactions if balance is insufficient
'''

# accounts= {
#     'add_1' :{'balance': 100,'nonce': 0},
#     'add_2' :{'balance': 200,'nonce': 0},
#     'add_3' :{'balance': 80,'nonce': 0},
# }

# gas_fee = 1

# def show_account():
    
#     for address, data in accounts.items():
#         print(f'{address} : Balance : {data['balance']} ETH | Nonce : {data['nonce']}')

# def create_transaction(sender, receiver):
    
#     send_amount = float(input("Enter the amount to be send: "))
#     total_cost = send_amount + gas_fee
    
#     if accounts[sender]['balance'] < total_cost:
#         print("Insufficient Balance.")
#         return
#     else:
#         accounts[sender]['balance'] -= total_cost
#         accounts[sender]['nonce'] += 1
        
#         accounts[receiver]['balance'] += send_amount

# print("Current Account Balances: ")
# show_account()

# create_transaction(input("Enter Sender Address: "), input("Enter Receiver Address: "))

# print("New Account Balances:")
# show_account()


'''You are given an accounts dictionary:

accounts = {
    "alice": 100,
    "bob": 50,
    "charlie": 75
}

👉 Take an account name as input and:

If account exists → print its balance

Else → print "Account not found"'''
        

# accounts = {
#     "alice": 100,
#     "bob": 50,
#     "charlie": 75
# }

# account_name = input("Enter the account name: ")

# if account_name in accounts.keys():
#     print(f"{account_name}'s balance is {accounts[account_name]}")     
# else:
#     print("Account not found")
        

'''Given:
accounts = {
    "alice": 100,
    "bob": 50
}

👉 Take input:
sender
receiver
amount

Rules:
Sender must exist
Receiver must exist
Sender balance ≥ amount

If valid:
Deduct amount from sender
Add amount to receiver
Print updated balances

Else print proper error message.

📌 This is basic ETH-style transfer logic.'''


# accounts = {
#     "alice": 100,
#     "bob": 50
# }

# print("Current Account Balances: ")
# for i, j in accounts.items():
#     print(f"{i} : {float(j)}")

# sender = input("Enter the sender name: ")
# if sender not in accounts:
#     print("Sender with that name doesn't exist.")
#     exit()
    
# receiver = input("Enter the receiver name: ")
# if receiver not in accounts:
#     print("Receiver with that name doesn't exist.")
#     exit()
    
# send_amount = float(input("Enter the amount to be send: "))
# if send_amount >= accounts[sender]:
#     print(f"Not enough balance in {sender}'s wallet")
#     exit()
# else:
#     accounts[sender] -= send_amount
#     accounts[receiver] += send_amount

# print("New Account Balances: ")
# print(f"{sender} : {accounts[sender]}")
# print(f"{receiver} : {accounts[receiver]}")


'''Same but dynamic program'''

accounts = {}
n = int(input("Kitne accounts create karne hain? "))
for i in range(n):
    name = input("Account name: ")
    balance = float(input("Initial balance: "))
    accounts[name] = balance
print("\nAccounts created:", accounts)

sender = input("\nSender name: ")
receiver = input("Receiver name: ")
send_amount = float(input("Amount to send: "))

if sender not in accounts:
    print("Sender account does not exist")

elif receiver not in accounts:
    print("Receiver account does not exist")

elif accounts[sender] < send_amount:
    print("Insufficient balance")

else:
    accounts[sender] -= send_amount
    accounts[receiver] += send_amount
    print("Transaction Successful")
    print("Updated balances:")
    print(f"{sender} : {accounts[sender]}")
    print(f"{receiver} : {accounts[receiver]}")
