# -------------------------- Imports -------------------------
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from ape import networks, accounts
from db import Base, SessionLocal, engine
from models import Token, User, Transaction
from blockchain.ape_util import deploy_token, transfer_tokens, get_contract

# ------------------------- Flask App Setup -------------------------
app = Flask(__name__)

# ------------------------- Database Setup -------------------------
Base.metadata.create_all(bind=engine)

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

        db_session = SessionLocal()
        account = accounts.test_accounts[len(db_session.query(User).all())]
        new_user = User(username=username, 
                        wallet_address=account.address, 
                        public_key=account.public_key,
                        timestamp=datetime.utcnow())
        db_session.add(new_user)
        db_session.commit()
        db_session.close()

        return render_template('index.html', 
                               username=username, 
                               wallet_address=account.address, 
                               public_key=account.public_key
                    )
    return render_template('index.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(username=username).first()
    
    if not user:
        return "User not found", 404
    
    created_tokens = db_session.query(Token).filter_by(owner_id=user.id).all()
    
    received_token_ids = [tx.token_id for tx in user.received_tx]
    received_tokens = db_session.query(Token).filter(Token.id.in_(received_token_ids)).all()
    
    all_tokens = created_tokens + received_tokens
    unique_ids = {}
    for token in all_tokens:
        unique_ids[token.id] = token
        
    all_tokens = list(unique_ids.values())
    
    token_balances = []
    for token in all_tokens:
        balance = get_contract(token.contract_address).balanceOf(user.wallet_address)
        if int(balance) > 0:
            token_balances.append({"token": token, "balance": int(balance)})

    return render_template('dashboard.html', 
                           user=user, 
                           token_balances=token_balances, 
                           created_tokens=created_tokens,
                           transactions=user.sent_tx + user.received_tx)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        sender_username = request.form['sender_username']
        recipient_username = request.form['recipient_username']
        token_name = request.form['token_name']
        amount = float(request.form['amount'])
        
        db_session = SessionLocal()
        sender = db_session.query(User).filter_by(username=sender_username).first()
        recipient = db_session.query(User).filter_by(username=recipient_username).first()
        token = db_session.query(Token).filter_by(token_name=token_name).first()
        
        if not sender or not recipient or not token:
            return "Sender, recipient, or token not found", 404
        
        if amount <= 0 or get_contract(token.contract_address).balanceOf(sender.wallet_address) < amount:
            return "Invalid amount or insufficient balance", 400
        
        try:
            tx_hash = transfer_tokens(sender.id - 1, recipient.wallet_address, amount, token.contract_address)
            new_tx = Transaction(sender_id=sender.id, 
                             recipient_id=recipient.id, 
                             amount=amount, 
                             tx_hash=str(tx_hash), 
                             token_id=token.id)
            db_session.add(new_tx)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
        finally:
            db_session.close()

        return redirect(url_for('dashboard', username=sender_username))
    
    return render_template('transfer.html')

@app.route('/create_token', methods=['GET', 'POST'])
def create_token():
    if request.method == 'POST':
        token_name = request.form['token_name']
        token_symbol = request.form['token_symbol']
        initial_supply = int(request.form['initial_supply'])
        owner = request.form['token_owner']
        
        db_session = SessionLocal()
        token_owner = db_session.query(User).filter_by(username=owner).first()
        
        if token_name == "" or token_symbol == "" or initial_supply <= 0:
            return "Invalid token details", 400
        
        if not token_owner:
            return "Token owner not found", 404
        
        try:
            contract_address = deploy_token(token_owner.id - 1, token_name, token_symbol, initial_supply)
            
            new_token = Token(
                        token_name=token_name, 
                        token_symbol=token_symbol, 
                        initial_supply=initial_supply,
                        contract_address=contract_address,
                        owner_id=token_owner.id)
            db_session.add(new_token)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
        finally:
            db_session.close()
        return render_template('token.html', token_name=token_name, token_symbol=token_symbol, initial_supply=initial_supply)
    return render_template('token.html')

@app.route('/dashboard_redirect', methods=['GET'])
def dashboard_redirect():
    username = request.args.get('username')
    if not username:
        return "Username is required", 400
    return redirect(url_for('dashboard', username=username))

# --------------------------- Main Entry Point -------------------------
if __name__ == "__main__":
    with networks.ethereum.local.use_provider("foundry"):
        app.run(debug=False, port=5000)