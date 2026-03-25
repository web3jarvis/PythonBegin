# -------------------------- Imports -------------------------
from datetime import datetime

from flask import Flask, render_template, request, redirect, session, url_for
from ape import networks, accounts
from db import Base, SessionLocal, engine
from models import User, Transaction
from blockchain.ape_util import transfer_tokens, get_contract

# ------------------------- Flask App Setup -------------------------
app = Flask(__name__)

# ------------------------- Database Setup -------------------------
Base.metadata.create_all(bind=engine)

# --------------------------- Ape Framework Setup -------------------------
# provider = networks.ethereum.local.use_provider("foundry")
# provider.connect()

# # -------------------------- Smart Contract Setup -------------------------
# CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
# contract=provider.contract(CONTRACT_ADDRESS)
# test_account = accounts.test_accounts[0]

# --------------------------- Flask Routes -------------------------

# --------------------------- Home Route -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# --------------------------- Create Wallet Route -------------------------
@app.route('/create_wallet', methods=['GET', 'POST'])
def create_wallet():
    if request.method == 'POST':
        username = request.form['username']

        session = SessionLocal()
        account = accounts.test_accounts[len(session.query(User).all())]
        new_user = User(username=username, 
                        wallet_address=account.address, 
                        public_key=account.public_key,
                        timestamp=datetime.utcnow())
        session.add(new_user)
        session.commit()
        session.close()

        return render_template('index.html', 
                               username=username, 
                               wallet_address=account.address, 
                               public_key=account.public_key
                    )
    return render_template('index.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    balance = get_contract().balanceOf(user.wallet_address)
    balance = int(balance)
    return render_template('dashboard.html', 
                           user=user, 
                           balance=balance, 
                           transactions=user.sent_tx + user.received_tx)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        sender_username = request.form['sender_username']
        recipient_username = request.form['recipient_username']
        amount = float(request.form['amount'])
        
        session = SessionLocal()
        sender = session.query(User).filter_by(username=sender_username).first()
        recipient = session.query(User).filter_by(username=recipient_username).first()
        
        if not sender or not recipient:
            return "Sender or recipient not found", 404
        
        try:
            tx_hash = transfer_tokens(sender.wallet_address, recipient.wallet_address, amount)
            # contract.transfer(recipient.wallet_address, int(amount), sender=sender.wallet_address)
            new_tx = Transaction(sender_id=sender.id, 
                             recipient_id=recipient.id, 
                             amount=amount, 
                             tx_hash=tx_hash, 
                             token_id=1)
            session.add(new_tx)
            session.commit()
        except Exception as e:
            session.rollback()
        finally:
            session.close()

        return redirect(url_for('dashboard', username=sender_username))
    
    return render_template('transfer.html')

# --------------------------- Main Entry Point -------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)