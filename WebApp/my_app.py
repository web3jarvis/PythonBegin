'''Design and implement a simplified blockchain web application using Flask, SQLite, and PyCryptodome that simulates the core architecture of a blockchain network. The application should allow users to generate a wallet using ECDSA (Elliptic Curve Digital Signature Algorithm), create and digitally sign transactions through a web form, and store these pending transactions in a database-based mempool. The system must verify digital signatures before processing transactions and implement a Proof of Work (PoW) mining mechanism with configurable difficulty to create new blocks. Each mined block should include verified transactions, contain a previous block hash to ensure chain linkage, and store its nonce and hash in the blockchain database. Upon successful mining, the mempool should be cleared, and the new block should be appended to the chain. The web interface should display the current mempool and full blockchain, demonstrating transaction flow, block formation, hashing, digital signatures, and consensus mechanics. The project should integrate concepts such as hashing (SHA-256), digital signatures (ECDSA), block structure, mempool management, proof of work, difficulty control, and backend database integration within a functioning Flask-based web application.'''

"""
    GOAL: To design a blockchain based web application
    
    Step 1: Wallet Creation using ECC
    
    Step 2: Create a digitally signed wallet; to create a DB named Mempool to store pending transactions.
    
    Step 3: Transactions verification will happen and creation of new blocks (DB creation)
    
    Step 4: Block creation with previous hash, nonce and current hash
    
    Step 5: Mempool clearing and appending new block
    
"""
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3, time, json
from db import DB_PATH

my_app = Flask(__name__)

def db_connections():
    connect = sqlite3.connect(DB_PATH)
    connect.row_factory = sqlite3.Row
    return connect
    
@my_app.route("/")
def home():
    return render_template("home.html")

@my_app.route("/wallet", methods=['POST'])
def wallet():
    name = request.form['name']
    key = ECC.generate(curve= "P-256")
    private_key = key.export_key(format="PEM")
    public_key = key.public_key().export_key(format="PEM")
    
    conn = db_connections()
    if conn.execute("""SELECT * FROM user WHERE name=?""", (name,)).fetchone():
        conn.close()
        return redirect(url_for('create_transactions', name=name))
    conn.execute(
        """INSERT INTO user (name, private_key, public_key) VALUES(?,?,?)""",
        (name, private_key, public_key)
    )
    conn.commit()
    conn.close()
    return render_template("home.html", name=name, private_key=private_key, public_key=public_key)

@my_app.route("/transactions")
@my_app.route("/transactions/<name>")
def render_transactions_page(name=None):
    return render_template("transactions.html", name=name)

@my_app.route("/create_transactions/<name>", methods=['GET', 'POST'])
def create_transactions(name):
    if request.method == "POST":
        sender = request.form["sender"]
        receiver = request.form["receiver"]
        amount = request.form["amount"] 
        timestamp = str(time.time())
        tx_data = f"{sender}:{receiver}:{amount}:{timestamp}"
        tx_hash = SHA256.new(tx_data.encode())
        
        conn = db_connections()
        
        user = conn.execute("""SELECT * FROM user WHERE name=?""", (sender,)).fetchone()
        sender = user['name']
        private_key = ECC.import_key(user['private_key'])
        public_key = user['public_key']
        owner = DSS.new(private_key, 'fips-186-3')
        signature = owner.sign(tx_hash).hex()
        
        tx = {
            "sender": name,
            "receiver": receiver,
            "amount": amount,
            "timestamp": timestamp,
            "signature": signature,
            "public_key": public_key
        }
        if verify_transactions(tx):
            conn.execute( 
            """INSERT INTO mempool (sender, receiver, amount, timestamp, signature, public_key) VALUES(?,?,?,?,?,?)""", 
            (tx["sender"], tx["receiver"], tx["amount"], tx["timestamp"], tx["signature"], tx["public_key"])
            )
            conn.commit()
            conn.close()
            
        return render_template("transactions.html", name=name)
    return render_template("transactions.html", name=name)

@my_app.route("/blocks")        
def blocks():
    conn = db_connections()
    tx = conn.execute("""SELECT * FROM mempool""").fetchall()
    
    if not tx:
        conn.close()
        return "No transactions to mine."
    
    verified_transactions = []
    for i in tx:
        verified_transactions.append(dict(i))
            
    last_block = conn.execute("""SELECT * FROM blockchain ORDER BY id DESC LIMIT 1""").fetchone()
    index = 1 if not last_block else last_block['index_number'] + 1
    timestamp = str(time.time())
    previous_hash = "0" if not last_block else last_block['block_hash']
    
    block_data = str(verified_transactions) + str(previous_hash)
    block_hash, nonce = proof_of_work(block_data, difficulty=3)
    
    conn.execute(
        """INSERT INTO blockchain 
        (index_number, timestamp, transactions, previous_hash, block_hash, nonce) VALUES(?,?,?,?,?,?)""",
        (index, timestamp, json.dumps(verified_transactions), previous_hash, block_hash, nonce)
    )
    conn.execute("""DELETE FROM mempool""")
    conn.commit()
    conn.close()
    return render_template("transactions.html", mempool=tx)

@my_app.route("/blockchain")        
def blockchain():
    conn = db_connections()
    all_blocks = conn.execute("""SELECT * FROM blockchain""").fetchall()
    conn.close()
    return render_template("blocks.html", blocks=all_blocks)

def verify_transactions(tx):
    tx_data = f"{tx['sender']}:{tx['receiver']}:{tx['amount']}:{tx['timestamp']}"
    tx_hash = SHA256.new(tx_data.encode())
    
    public_key = ECC.import_key(tx['public_key'])
    verifier = DSS.new(public_key, 'fips-186-3')
    
    try:
        verifier.verify(tx_hash, bytes.fromhex(tx['signature']))
        return True
    except:
        return False
    
def proof_of_work(block_data, difficulty):
    nonce = 0
    while True:
        full_block_data = block_data + str(nonce)
        block_hash = SHA256.new(full_block_data.encode()).hexdigest()
        
        if block_hash.startswith("0" * difficulty):
            return block_hash, nonce
        
        nonce+=1