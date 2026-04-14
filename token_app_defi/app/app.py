# -------------------------- Imports -------------------------
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from ape import networks, accounts
from db import Base, SessionLocal, engine
from models import AMM_Table, Token, User, Transaction, Wallet
from blockchain.ape_util import deploy_token, transfer_tokens, get_contract, swap_tokens
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# --------------------------- Utility Function to Sort Transactions -------------------------
def sort_by_timestamp(tx):
    return tx.timestamp

# ------------------------- Flask App Setup -------------------------
app = Flask(__name__)

# ------------------------- Secret Key Setup -------------------------
app.config['SECRET_KEY'] = 'qwertyisnotagoodsecretkey'

# ------------------------- Login Manager Setup -------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ------------------------- User Loader -------------------------
@login_manager.user_loader
def load_user(user_id):
    db_session = SessionLocal()
    user = db_session.get(User, int(user_id))
    db_session.close()
    return user

# ------------------------- Database Setup -------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------- Flask Routes ----------------------------------------------------
# --------------------------- Home Route -------------------------
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard", username=current_user.username))
    return render_template("index.html")

# --------------------------- Register Route -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db_session = SessionLocal()
        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            db_session.close()
            flash("Username already exists", "error")
            return redirect(url_for("register"))
        new_user = User(username=username, password=generate_password_hash(password))
        db_session.add(new_user)
        db_session.commit()
        db_session.close()

        return redirect(url_for("login"))
    return render_template("register.html")

# --------------------------- Login Route -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if not username or not password:
            flash("Username and password are required", "error")
            return redirect(url_for("login"))
        
        db_session = SessionLocal()
        user = db_session.query(User).filter_by(username=username).first()
        db_session.close()
        
        if not user:
            flash("User not found", "error")
            return redirect(url_for("login"))
        
        if not check_password_hash(user.password, password):
            flash("Incorrect password", "error")
            return redirect(url_for("login"))
        
        login_user(user)
        return redirect(url_for("dashboard", username=username))
    return render_template("login.html")

# --------------------------- Dashboard Route -------------------------
@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(username=username).first()
    if not user:
        db_session.close()
        return "User not found", 404
    
    wallets = db_session.query(Wallet).filter_by(user_wallet=user.id).first()
    created_tokens = db_session.query(Token).filter_by(owner_id=user.id).all()
    received_token_ids = [tx.token_id for tx in user.received_tx]
    received_tokens = db_session.query(Token).filter(Token.id.in_(received_token_ids)).all()
    all_tokens = created_tokens + received_tokens
    unique_ids = {}
    for token in all_tokens:
        unique_ids[token.id] = token
    all_tokens = list(unique_ids.values())
    
    token_balances = []
    if wallets:
        for token in all_tokens:
            try:
                balance = get_contract(token.contract_address).balanceOf(wallets.wallet_address)
                if int(balance) > 0:
                    token_balances.append({"token": token, "balance": int(balance)})
            except Exception as e:
                pass
            
    all_transactions = user.sent_tx + user.received_tx
    all_transactions.sort(key=sort_by_timestamp, reverse=True)
    
    return render_template('dashboard.html', 
                           user=user, 
                           wallet=wallets,
                           token_balances=token_balances, 
                           created_tokens=created_tokens,
                           transactions=all_transactions)

# --------------------------- Create Wallet Route -------------------------
@app.route('/create_wallet/<username>', methods=['GET', 'POST'])
@login_required
def create_wallet(username):
    username = username
    if current_user.username != username:
        return "Unauthorized", 403
        
    db_session = SessionLocal()
    existing_wallet = db_session.query(Wallet).filter_by(
                                        user_wallet=db_session.query(User).filter_by(
                                                                        username=username).first().id).first()
    if existing_wallet:
        db_session.close()
        return redirect(url_for('dashboard', username=username))
        
    account = accounts.test_accounts[len(db_session.query(Wallet).all())]
    new_user_wallet = Wallet(
                            wallet_address=account.address, 
                            public_key=account.public_key,
                            timestamp=datetime.now(),
                            user_wallet=db_session.query(User).filter_by(username=username).first().id)
    db_session.add(new_user_wallet)
    db_session.commit()
    db_session.close()

    return redirect(url_for('dashboard', username=username))
    
# --------------------------- Create Token Route -------------------------
@app.route('/create_token/<username>', methods=['GET', 'POST'])
@login_required
def create_token(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    if request.method == 'POST':
        token_name = request.form['token_name']
        token_symbol = request.form['token_symbol']
        initial_supply = int(request.form['initial_supply'])
        
        db_session = SessionLocal()
        token_owner = db_session.query(User).filter_by(username=username).first()
        
        if token_name == "" or token_symbol == "" or initial_supply <= 0:
            flash("Invalid token details.", "error")
            return redirect(url_for('create_token', username=username))
        
        if not token_owner:
            flash("Token owner not found.", "error")
            return redirect(url_for('dashboard', username=username))
        
        owner_wallet = db_session.query(Wallet).filter_by(user_wallet=token_owner.id).first()
        if not owner_wallet:
            flash("Please create a wallet first!", "error")
            return redirect(url_for('dashboard', username=username))
        
        success = False
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
            success = True
        except Exception as e:
            db_session.rollback()
        finally:
            db_session.close()
        if success:
            flash("Token created successfully!", "success")
            return render_template('token.html', 
                               user=current_user,
                               token_name=token_name, 
                               token_symbol=token_symbol, 
                               initial_supply=initial_supply)
        else:
            flash("Failed to create token.", "error")
            return redirect(url_for('create_token', username=username))
        
    return render_template('token.html', user=current_user)

# --------------------------- Transfer Route -------------------------
@app.route('/transfer/<username>', methods=['GET', 'POST'])
@login_required
def transfer(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    sender_username = username
    db_session = SessionLocal()
    user_wallet = db_session.query(Wallet).filter_by(user_wallet=current_user.id).first()
    all_tokens = db_session.query(Token).all()
    
    tokens_with_balance = {}
    if user_wallet:
        for token in all_tokens:
            try:
                balance = int(get_contract(token.contract_address).balanceOf(user_wallet.wallet_address))
                if balance > 0:
                    tokens_with_balance[token.token_name] = balance
            except Exception as e:
                pass

    transferable_tokens = [t for t in all_tokens if t.token_name in tokens_with_balance]
    
    if request.method == 'POST':
        recipient_username = request.form['recipient_username']
        token_name = request.form['token_name']
        amount = float(request.form['amount'])
        
        sender = db_session.query(User).filter_by(username=sender_username).first()
        recipient = db_session.query(User).filter_by(username=recipient_username).first()
        token = db_session.query(Token).filter_by(token_name=token_name).first()

        if not sender or not recipient or not token:
            flash("Sender, recipient, or token not found.", "error")
            return redirect(url_for('transfer', username=sender_username))
        
        if sender.id == recipient.id:
            flash("Cannot transfer to yourself!", "error")
            return redirect(url_for('transfer', username=sender_username))
        
        sender_wallet = db_session.query(Wallet).filter_by(user_wallet=sender.id).first()
        recipient_wallet = db_session.query(Wallet).filter_by(user_wallet=recipient.id).first()
        if not sender_wallet or not recipient_wallet:
            flash("Sender or recipient wallet not found.", "error")
            return redirect(url_for('transfer', username=sender_username))
        
        if amount <= 0 or get_contract(token.contract_address).balanceOf(sender_wallet.wallet_address) < amount:
            flash("Invalid amount or insufficient balance.", "error")
            return redirect(url_for('transfer', username=sender_username))
        
        try:
            tx_hash = transfer_tokens(sender.id - 1, recipient_wallet.wallet_address, amount, token.contract_address)
            new_tx = Transaction(sender_id=sender.id, 
                             recipient_id=recipient.id, 
                             amount=amount, 
                             tx_hash=str(tx_hash), 
                             token_id=token.id)
            db_session.add(new_tx)
            db_session.commit()
            flash("Transfer successful!", "success")
        except Exception as e:
            db_session.rollback()
            flash("Transfer failed: " + str(e), "error")
        finally:
            db_session.close()

        return redirect(url_for('transfer', username=sender_username))
    
    db_session.close()
    return render_template('transfer.html', 
                           user=current_user, 
                           user_tokens=transferable_tokens,
                           tokens_with_balance=tokens_with_balance)

# --------------------------- Logout Route -------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/swap/<username>", methods=['GET', 'POST'])
@login_required
def swap(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(username=username).first()
    user_wallet = db_session.query(Wallet).filter_by(user_wallet=current_user.id).first()
    amm = db_session.query(AMM_Table).first()
    
    if not user_wallet:
        flash("Please create a wallet first!", "error")
        return redirect(url_for('dashboard', username=username))
    
    if not amm:
        flash("No AMM found. Please ask the admin to deploy an AMM first!", "error")
        return redirect(url_for('dashboard', username=username))

    if request.method == 'POST':
        from_token = request.form['from_token']
        amount = float(request.form['amount'])
        
        if amount <= 0:
            flash("Invalid amount!", "error")
            return redirect(url_for('swap', username=username))
        
        try:
            tx_hash = swap_tokens(
                sender_id=user.id - 1, 
                amm_address=amm.amm_address, 
                from_token=from_token,
                amount=amount)
            flash("Swap successful! Transaction hash: " + str(tx_hash), "success")
        except Exception as e:
            flash("Swap failed: " + str(e), "error")
            print(f"[SWAP ERROR] {e}")
        finally:
            db_session.close()
        
        return redirect(url_for('swap', username=username))

    db_session.close()
    return render_template('swap.html', user=current_user, amm=amm, wallet=user_wallet)

# --------------------------- Main Entry Point -------------------------
if __name__ == "__main__":
    with networks.ethereum.local.use_provider("foundry"):
        app.run(debug=False, port=5000)