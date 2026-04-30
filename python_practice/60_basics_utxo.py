'''
Design a Python program that simulates a UTXO-based blockchain transaction system (similar to Bitcoin).
The program should:
Maintain a list of UTXOs (Unspent Transaction Outputs)
Allow users to:
    - View wallet balance (calculated from UTXOs)
    - Create a transaction
    - Spend existing UTXOs as inputs
    - Generate new UTXOs as outputs
    - Create a change output if required
    - Prevent double spending
    - Demonstrate how balances are derived from UTXOs (not stored directly)
'''

# utxo = {
#     'tra1' : 10, # 10 btc
# } #static utxo currently for testing purpose with only single key:value pair

# def get_balance(): # created function to fetch the initial balance
#     return sum(utxo.values()) # fetching all the values of dictionary, in this case its just '10', 
# #and applying the sum function and returning its value

# def display_utxo(): # created function to display all the UTXOs in the wallet
#     print(" Current UTXO")
#     for id, amt in utxo.items(): # tracing each item in the UTXO disctionary till the end of items there.
#         print(f'{id} -> {amt} BTC') # and printing each UTXO item
        
# def create_transaction(send_amt): # created function to initiate the transaction
#     global utxo # calling the global dictionary
    
#     print(" New Transaction ")
#     available_balance = get_balance() # assigning current balance to this new var using the function
    
#     if send_amt > available_balance: # verifying if amt to be send is sufficient as compare to wallet balance
#         print('insufficient amt')
#         return # if not return from the code block with the prompt message
    
#     # now if available balance is there, the function will process ahead
#     inputs = [] # creating a fresh list which will be a list of tuple of dictionary items, to check which UTXOs will be used
#     input_sum = 0 # increment counter to fetch total coins collected
    
#     for id, amt in utxo.items():
#         inputs.append((id, amt))
#         input_sum += amt
#         if input_sum >= send_amt: # if this condition fulfills it will stop tracing ahead and consider this much for deducting
#             break
        
#     for id, _ in inputs: # tracing each id of the new list ignoring the amt
#         utxo.pop(id) # destroy the old id
        
#     # new transaction id 
#     tran_id = 'tra' + str(len(utxo)+1) # creating a string for new UTXO key 
    
#     # making entry for the new transaction
#     utxo[tran_id]=send_amt # assigning the sent_amt to the specified key and creating a new entry for the UTXO
    
#     # new state 
#     change = input_sum - send_amt # determining the remaining balance
    
#     if change > 0:
#         utxo[f'{tran_id}change'] = change # if that is >0 creating another entry for the UTXO
        
#     print('transaction successful')
#     print(f' sent : {send_amt} and change : {change}')
    

# choice = input(' 1. bal , 2. utxo, 3. send transction : ')

# if choice == '1':
#     print(' balance : ', get_balance())
# elif choice == '2': 
#     display_utxo()
# elif choice =='3':
#     amt = int(input("Enter the amt : "))
#     create_transaction(amt)
# else : 
#     print(' invalid choice')
    
    
'''You are given a list of UTXOs (unspent outputs): utxos = [2.5, 1.0, 0.75, 3.25]
Write a program to calculate and print the total wallet balance.'''

# utxos = [2.5, 1.0, 0.75, 3.25]

# def getbalance():
#     return sum(utxos)

# print("Total Wallet Balance", getbalance())

'''Given: List of UTXOs
Transaction amount to send
utxos = [1.2, 0.8, 2.0]
send_amount = 3.0

👉 Check if total UTXOs ≥ send_amount
If yes → "Transaction Possible"
Else → "Insufficient Balance"'''


# utxos = [1.2, 0.8, 2.0]
# send_amount = 3.0

# getbalance = sum(utxos)

# if getbalance >= send_amount:
#     print("Transaction Possible")
# else:
#     print("Insufficient Balance")


'''Given: utxos = [0.5, 1.5, 2.0, 0.8]
send_amount = 2.3
👉 Select UTXOs in order until their sum is ≥ send_amount.
Print: Selected UTXOs
Total selected amount'''

# utxos = [0.5, 1.5, 2.0, 0.8]
# sorted_utxos = sorted(utxos)

# send_amount = 2.8

# getbalance = sum(sorted_utxos)

# if send_amount > getbalance:
#     print("Insufficient Balance")
# else:
#     selected_utxos = []
#     selected_sum = 0

#     for i in sorted_utxos:
#         selected_utxos.append(i)
#         selected_sum += i
#         if selected_sum >= send_amount:
#             break

# print("Selected UTXOs: ", selected_utxos)

# change = selected_sum - send_amount
# new_balance = getbalance - send_amount
# if change > 0:
#     print("Old Balance: ", getbalance)
#     print("Sent Amount: ", send_amount)
#     print("Change Left from UTXOs: ", change)
#     print("New Balance", new_balance)
# else:
#     print("No change left")
    
    
'''UTXO with Dictionaries:
Wallet Balance from UTXO Objects

You are given a wallet UTXO list:

utxos = [
    {"txid": "a1", "index": 0, "amount": 1.5},
    {"txid": "b2", "index": 1, "amount": 0.8},
    {"txid": "c3", "index": 0, "amount": 2.0}
]


👉 Total wallet balance calculate using "amount" '''


utxos = [
    {"txid": "a1", "index": 0, "amount": 1.5},
    {"txid": "b2", "index": 1, "amount": 0.8},
    {"txid": "c3", "index": 0, "amount": 2.0}
]

utxo_balance = 0
for element in utxos:
    utxo_balance += element['amount']
    
print("Total wallet balance: ", utxo_balance)

send_amount = float(input("Enter the amount to be send: "))

if send_amount > utxo_balance:
    print("Not Enough Balance!")
    

