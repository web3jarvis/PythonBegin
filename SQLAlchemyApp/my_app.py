'''Design and implement a simplified blockchain web application using Flask, SQLite, and PyCryptodome that simulates the core architecture of a blockchain network. The application should allow users to generate a wallet using ECDSA (Elliptic Curve Digital Signature Algorithm), create and digitally sign transactions through a web form, and store these pending transactions in a database-based mempool. The system must verify digital signatures before processing transactions and implement a Proof of Work (PoW) mining mechanism with configurable difficulty to create new blocks. Each mined block should include verified transactions, contain a previous block hash to ensure chain linkage, and store its nonce and hash in the blockchain database. Upon successful mining, the mempool should be cleared, and the new block should be appended to the chain. The web interface should display the current mempool and full blockchain, demonstrating transaction flow, block formation, hashing, digital signatures, and consensus mechanics. The project should integrate concepts such as hashing (SHA-256), digital signatures (ECDSA), block structure, mempool management, proof of work, difficulty control, and backend database integration within a functioning Flask-based web application.'''

from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import time, json

my_app = Flask(__name__)
my_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(my_app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    private_key = db.Column(db.Text)
    public_key = db.Column(db.Text)
    
class Mempool(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.Text)
    signature = db.Column(db.Text)
    public_key = db.Column(db.Text)

class Blockchain(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    index_number = db.Column(db.Integer)
    timestamp = db.Column(db.Text)
    transactions = db.Column(db.Text)
    previous_hash = db.Column(db.Text)
    block_hash = db.Column(db.Text)
    nonce = db.Column(db.Integer)

with my_app.app_context():
    db.create_all()

@my_app.route("/")
def home():
    return render_template("home.html")

@my_app.route("/wallet", methods=['POST'])
def wallet():
    name = request.form['name']
    
    if User.query.filter_by(name=name).first():
        return redirect(url_for('create_transactions', name=name))
    
    key = ECC.generate(curve= "P-256")
    private_key = key.export_key(format="PEM")
    public_key = key.public_key().export_key(format="PEM")
    
    new_user = User(name=name, private_key=private_key, public_key=public_key)
    db.session.add(new_user)
    db.session.commit()
    
    return render_template("home.html", name=name, private_key=new_user.private_key, public_key=new_user.public_key)

@my_app.route("/transactions")
@my_app.route("/transactions/<name>")
def render_transactions_page(name=None):
    return render_template("transactions.html", name=name)

@my_app.route("/create_transactions/<name>", methods=['GET', 'POST'])
def create_transactions(name):
    
    if request.method == "POST":
        
        sender = request.form["sender"]
        receiver = request.form["receiver"]
        amount = int(request.form["amount"])
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        tx_data = f"{sender}:{receiver}:{amount}:{timestamp}"
        tx_hash = SHA256.new(tx_data.encode())
        
        user = User.query.filter_by(name=sender).first()
        
        private_key = ECC.import_key(user.private_key)
        public_key = user.public_key
        owner = DSS.new(private_key, 'fips-186-3')
        signature = owner.sign(tx_hash).hex()
        
        tx = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": timestamp,
            "signature": signature,
            "public_key": public_key
        }
        if verify_transactions(tx):          
            new_transaction = Mempool(**tx)
            db.session.add(new_transaction)
            db.session.commit()
        
    return render_template("transactions.html", name=name)

@my_app.route("/blocks")        
def blocks():
    
    tx = Mempool.query.all()
    if not tx:
        return "No transactions to mine."
    
    verified_transactions = []
    for i in tx:
        if verify_transactions(i.__dict__):
            verified_transactions.append({
                "sender": i.sender,
                "receiver": i.receiver,
                "amount": i.amount,
                "timestamp": i.timestamp,
                "signature": i.signature,
                "public_key": i.public_key
            })
            
    last_block = Blockchain.query.order_by(Blockchain.id.desc()).first()
    index = 1 if not last_block else last_block.index_number + 1
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    previous_hash = "0" if not last_block else last_block.block_hash
    
    block_data = json.dumps(verified_transactions, sort_keys=True) + previous_hash
    block_hash, nonce = proof_of_work(block_data, difficulty=3)
    
    block = Blockchain(
        index_number = index,
        timestamp = timestamp,
        transactions = json.dumps(verified_transactions),
        previous_hash = previous_hash,
        block_hash = block_hash,
        nonce = nonce
    )
    db.session.add(block)
    Mempool.query.delete()
    db.session.commit()
    
    return render_template("transactions.html", mempool=tx)

@my_app.route("/blockchain")        
def blockchain():
    all_blocks = Blockchain.query.all()
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
        
        nonce += 1
        
if __name__ == "__main__":
    my_app.run(debug=True)