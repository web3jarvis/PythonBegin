'''
Design a Python program that simulates how a blockchain processes transactions using:
    -Transactions
    -Mempool (pending transaction pool)
    -Blocks (confirmed transaction storage)

The program should:
    - Allow users to create transactions
    - Store pending transactions in a mempool
    - Allow miner to pick transactions from mempool
    - Create a block with selected transactions
    - Add block to blockchain
    - Clear processed transactions from mempool
'''
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256, keccak
import time

blockchain = []
mempool = []

def create_wallet(name):
    key = ECC.generate(curve = 'P-256')
    private_key = key
    public_key = key.public_key()
    
    public_key_xy = public_key.pointQ.x.to_bytes(32, "big") + public_key.pointQ.y.to_bytes(32, "big")
    hash_object = keccak.new(digest_bits=256)
    hash_object.update(public_key_xy)
    key_hash = hash_object.hexdigest()
    
    eth_address = "0x" + key_hash[-40:]
    
    return {
        "name" : name,
        "address" : eth_address,
        "private" : private_key,
        "public" : public_key
    }
    
def create_transaction(sender_wallet, receiver_name, amount):
    tx_data = f"{sender_wallet['name']} -> {receiver_name} : {amount} at {time.time()}"
    tx_hash = SHA256.new(tx_data.encode())
    
    owner = DSS.new(sender_wallet['private'], 'fips-186-3')
    signature = owner.sign(tx_hash)
    
    tx = { 
          "sender" : sender_wallet['name'],
          "address" : sender_wallet['address'],
          "receiver" : receiver_name,
          "amount" : amount,
          "data" : tx_data,
          "hash" : tx_hash,
          "signature" : signature, 
          "public_key" : sender_wallet['public']
    }
    mempool.append(tx)
    print("✅ Transaction created and added to mempool")
    
def verify_transaction(tx):
    hash_obj = SHA256.new(tx['data'].encode())
    verifier = DSS.new(tx['public_key'], 'fips-186-3')
    
    try: 
        verifier.verify(hash_obj, tx['signature'])
        return True
    except:
        return False
    
def calculate_hash(block):
    b_hash = SHA256.new(str(block).encode()) 
    return b_hash.hexdigest()

def create_block():
    if len(mempool) == 0:
        print("No transactions found")
        return
    
    verified_transaction = []
    for tx in mempool:
        if verify_transaction(tx):
            verified_transaction.append(tx)
            
    previous_hash = blockchain[-1]["hash"] if blockchain else "0"
    
    # if blockchain:
    #     p_h = blockchain[-1]["hash"]
    # else:
    #     p_h = '0'
    
    block = {
        "index" : len(blockchain) + 1,
        "time_stamp" : time.time(),
        "transactions": verified_transaction,
        "previous_hash" : previous_hash
    }
    block["hash"] = calculate_hash(block)
    blockchain.append(block)
    
    for tx in verified_transaction:
        mempool.remove(tx)
    print("✅ Block created ✅")
    
## --- INPUTS --- ##
sender_name = input("Enter the sender wallet name: ")
sender_wallet = create_wallet(sender_name)
receiver_name = input("Enter the receiver wallet name: ")
amount = float(input("Enter the amount to be send: "))
create_transaction(sender_wallet, receiver_name, amount)

####################

print("Number of transactions in mempool: ", len(mempool))
for tx in mempool:
    print(f"Sender: {tx['sender']} | Sender Address: {tx['address']} | Receiver: {tx['receiver']} | Amount: {tx['amount']}")
    
####################
    
create_block()
for block in blockchain:
    print(f"Block Number: {block['index']} \nTimestamp: {block['time_stamp']} \nBlock Hash: {block['hash']}")