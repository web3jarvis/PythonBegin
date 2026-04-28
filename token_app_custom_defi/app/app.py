from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from ape import accounts, project, networks
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import SessionLocal, Base, engine
from models import User, Wallet, Token, Transaction, AMM
from blockchain.ape_util import add_liquidity, deploy_staking, deploy_token, execute_stake, execute_unstake, get_contract, get_staking_contract, transfer_tokens, deploy_pool, swap_tokens
from datetime import datetime

# ---------------------------- Helper Functions -------------------------
def sort_by_timestamp(tx):
    return tx.timestamp

# ---------------------------- Initialize Flask App -------------------------
app = Flask(__name__)

# ---------------------------- Configure Flask App -------------------------
app.config['SECRET_KEY'] = 'your_secret_key_here'

# ---------------------------- Initialize Flask-Login -------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ---------------------------- Create Database Tables -------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------- User Loader for Flask-Login -------------------------
@login_manager.user_loader
def load_user(user_id):
    db_session = SessionLocal()
    user = db_session.query(User).get(int(user_id))
    db_session.close()
    return user    

# ---------------------------- Home Route -------------------------
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', username=current_user.username))
    return render_template('index.html')

# ---------------------------- Register Route -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password']
        
        db_session = SessionLocal()
        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.", "error")
            db_session.close()
            return redirect(url_for('register'))
        
        usercount = db_session.query(User).count()
        if usercount == 0:
            is_first_user = True
        else:
            is_first_user = False
        
        new_user = User(username=username, 
                        password=generate_password_hash(password), 
                        is_admin=is_first_user)
        
        db_session.add(new_user)
        db_session.commit()
        db_session.close()
        flash("Registration successful! Please log in.", "success")
        
        return redirect(url_for('login'))
    return render_template('register.html')
        
# ------------------------- Login Route -------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash("Username and Password are required", 'error')
            return redirect(url_for('login'))
        
        db_session = SessionLocal()
        user = db_session.query(User).filter_by(username=username).first()
        db_session.close()
        
        if not user:
            flash("User does not exists.", 'error')
            return redirect(url_for('login'))
        
        if not check_password_hash(user.password, password):
            flash("Incorrect password.", 'error')
            return redirect(url_for('login'))
        
        login_user(user)
        flash("Login successful!", "success")
        
        return redirect(url_for('dashboard', username=username))
    return render_template('login.html')

# ------------------------- Logout Route -------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('home'))

# ---------------------------- Dashboard Route -------------------------
@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(username=username).first()
    if not user:
        db_session.close()
        return "User not found.", 404
    
    wallet = db_session.query(Wallet).filter_by(wallet_ownerid=user.id).first()
    created_tokens = db_session.query(Token).filter_by(token_ownerid=user.id).all()
    
    all_tokens = db_session.query(Token).all()
    token_balances = []
    if wallet:
        for token in all_tokens:
            try:
                raw_balance = int(get_contract(token.contract_address).balanceOf(wallet.wallet_address))
                actual_balance = raw_balance / (10**18)
                if actual_balance > 0:
                    token_balances.append({"token": token, "balance": int(actual_balance)})
            except Exception as e:
                pass
            
    all_transactions = list(set(user.sent_tx + user.received_tx)) # Deduplicate
    created_pools = db_session.query(AMM).filter_by(amm_ownerid=user.id).all()
    transaction_history = all_transactions + created_pools
    transaction_history.sort(key=sort_by_timestamp, reverse=True)
    
    active_staking_tokens = db_session.query(Token).filter_by(is_stake_active=True).all()   
    render_data = render_template('dashboard.html', 
                                   user=user, 
                                   username=username, 
                                   wallet=wallet,
                                   token_balances=token_balances, 
                                   created_tokens=created_tokens,
                                   created_pools=created_pools, 
                                   transactions=transaction_history,
                                   active_staking_tokens=active_staking_tokens)
    db_session.close()
    return render_data

# ---------------------------- Create Wallet ----------------------------
@app.route('/create_wallet/<username>', methods=['GET', 'POST'])
@login_required
def create_wallet(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    existing_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if existing_wallet:
        db_session.close()
        return redirect(url_for('dashboard', username=username))
    
    account = accounts.test_accounts[len(db_session.query(Wallet).all())]
    new_user_wallet = Wallet(
                            wallet_address=account.address, 
                            public_key=account.public_key,
                            wallet_ownerid=current_user.id,
                            timestamp=datetime.now())
    db_session.add(new_user_wallet)
    db_session.commit()
    db_session.close()
    
    return redirect(url_for('dashboard', username=username))

# ---------------------------- Create Token ----------------------------
@app.route('/create_token/<username>', methods=['GET', 'POST'])
@login_required
def create_token(username):
    if current_user.username!=username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    user_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if not user_wallet:
        flash("Please create a wallet first!", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=username))
    
    active_staking_tokens = db_session.query(Token).filter_by(is_stake_active=True).all()
    
    if request.method == 'POST':
        token_name = request.form['token_name']
        token_symbol = request.form['token_symbol']
        initial_supply = int(request.form['initial_supply'])
        
        if token_name == "" or token_symbol == "" or initial_supply <= 0:
            flash("Invalid token details.", "error")
            db_session.close()
            return redirect(url_for('create_token', username=username))
        
        success=False
        try:
            contract_address, token_txn_hash = deploy_token(
                                                current_user.id - 1, 
                                                token_name, 
                                                token_symbol, 
                                                initial_supply)
            
            new_token = Token(
                            token_name=token_name,
                            token_symbol=token_symbol,
                            initial_supply=initial_supply,
                            contract_address=contract_address,
                            token_ownerid=current_user.id,
                            timestamp=datetime.now())
            db_session.add(new_token)
            db_session.flush()  # Flush to get new_token.id for the transaction record
            new_token_tx = Transaction(
                                    sender_id=current_user.id, 
                                    receiver_id=current_user.id, 
                                    amount=initial_supply, 
                                    tx_type='mint', 
                                    tx_hash=str(token_txn_hash), 
                                    token_id=new_token.id, 
                                    timestamp=datetime.now())
            db_session.add(new_token_tx)
            db_session.commit()
            success = True
        except Exception as e:
            print(f"Exception, if any: {e}")
            db_session.rollback()
        finally:
            db_session.close()
        if success:
            flash("Token created successfully!", "success")
            return render_template('token.html',
                                   user=current_user, 
                                   username=username,
                                   success=success,
                                   token_name=token_name, 
                                   token_symbol=token_symbol, 
                                   initial_supply=initial_supply)
        else:
            flash("Failed to create token.", "error")
            return redirect(url_for('create_token', username=username))
        
    db_session.close()
    return render_template('token.html', 
                           username=username, 
                           user=current_user,
                           active_staking_tokens=active_staking_tokens)

# --------------------------- Transfer Token ---------------------------
@app.route('/transfer/<username>', methods=['GET', 'POST'])
@login_required
def transfer(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    sender_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if not sender_wallet:
        flash("Please create a wallet first!", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=username))
    
    all_tokens = db_session.query(Token).all()
    tokens_with_balance = {}
    if sender_wallet:
        for i in all_tokens:
            try:
                raw_balance = int(get_contract(i.contract_address).balanceOf(sender_wallet.wallet_address))
                actual_balance = raw_balance / (10**18)
                if actual_balance > 0:
                    tokens_with_balance[i.token_name] = int(actual_balance)
            except Exception as e:
                pass
    
    transferable_tokens = [t for t in all_tokens if t.token_name in tokens_with_balance]
    active_staking_tokens = db_session.query(Token).filter_by(is_stake_active=True).all()
    
    if request.method == 'POST':
        receiver_username = request.form['receiver_username']
        token_name = request.form['token_name']
        amount = int(request.form['amount'])
        
        sender = current_user
        receiver = db_session.query(User).filter_by(username=receiver_username).first()
        token = db_session.query(Token).filter_by(token_name=token_name).first()
        
        if not sender or not receiver or not token:
            flash("Sender, receiver, or token not found.", "error")
            db_session.close()
            return redirect(url_for('transfer', username=username))
        
        if sender.id == receiver.id or sender.username == receiver.username:
            flash("Cannot transfer to yourself!", "error")
            db_session.close()
            return redirect(url_for('transfer', username=username))
            
        receiver_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=receiver.id).first()
        if not receiver_wallet:
            flash("Receiver wallet not found.", "error")
            db_session.close()
            return redirect(url_for('transfer', username=username))
        
        if amount <=0 or int(get_contract(token.contract_address).balanceOf(sender_wallet.wallet_address)) < amount* (10**18):
            flash("Invalid amount or insufficient balance.", "error")
            db_session.close()
            return redirect(url_for('transfer', username=username))
        
        try:
            txn_hash = transfer_tokens(
                                    sender_id=sender.id - 1, 
                                    receiver_address=receiver_wallet.wallet_address, 
                                    amount=amount,
                                    contract_address=token.contract_address)
            new_tx = Transaction(
                                sender_id=sender.id, 
                                receiver_id=receiver.id, 
                                amount=amount, 
                                tx_type='transfer', 
                                tx_hash=str(txn_hash), 
                                token_id=token.id, 
                                timestamp=datetime.now())
            db_session.add(new_tx)
            db_session.commit()
            flash("Transfer successful!", "success")
        except Exception as e:
            db_session.rollback()
            flash("Transfer failed: " + str(e), "error")
        finally:
            db_session.close()
        
        return redirect(url_for('transfer', username=current_user.username))
    
    db_session.close()
    return render_template('transfer.html', 
                           user=current_user, 
                           transferable_tokens=transferable_tokens, 
                           tokens_with_balance=tokens_with_balance, 
                           username=username,
                           active_staking_tokens=active_staking_tokens)

# --------------------------- Create Pool ---------------------------
@app.route('/create_pool/<username>', methods=['GET', 'POST'])
@login_required
def create_pool(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    
    wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if not wallet:
        flash("Please create a wallet first!", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=username))

    session_user = db_session.query(User).get(current_user.id)
    created_tokens = db_session.query(Token).filter_by(token_ownerid=session_user.id).all()
    received_token_ids = [tx.token_id for tx in session_user.received_tx]
    received_tokens = db_session.query(Token).filter(Token.id.in_(received_token_ids)).all()
    
    all_tokens = {t.id: t for t in (created_tokens + received_tokens)}.values() # Deduplicate
    active_staking_tokens = db_session.query(Token).filter_by(is_stake_active=True).all()
    
    if request.method == 'POST':
        token_A_name = request.form['token_A_name']
        token_B_name = request.form['token_B_name']
        reserve_A = int(request.form['reserve_A']) # DB value
        reserve_B = int(request.form['reserve_B']) # DB value
        
        if token_A_name == token_B_name:
            flash("Cannot pair the same token.", "error")
            db_session.close()
            return redirect(url_for('create_pool', username=username))
        
        if reserve_A <= 0 or reserve_B <= 0:
            flash("Invalid amount on the pool reserves.", "error")
            db_session.close()
            return redirect(url_for('create_pool', username=username))
        
        token_A = db_session.query(Token).filter_by(token_name=token_A_name).first()
        token_B = db_session.query(Token).filter_by(token_name=token_B_name).first()
        if not token_A or not token_B:
            flash("Selected tokens not found.", "error")
            db_session.close()
            return redirect(url_for('create_pool', username=username))
        
        existing_pool = db_session.query(AMM).filter(
            ((AMM.token_A_address == token_A.contract_address) & (AMM.token_B_address == token_B.contract_address)) |
            ((AMM.token_A_address == token_B.contract_address) & (AMM.token_B_address == token_A.contract_address))
        ).first()
        if existing_pool:
            flash("Pool with these pairs already exists.", "error")
            db_session.close()
            return redirect(url_for('create_pool', username=username))
        
        try:
            token_A_address = token_A.contract_address # DB value
            token_B_address = token_B.contract_address # DB value
            amm_address = deploy_pool(current_user.id - 1, token_A_address, token_B_address) # DB value
            add_liquidity_txn_hash = add_liquidity(current_user.id - 1, amm_address, reserve_A, reserve_B) # DB value
            new_amm = AMM(
                        amm_address=amm_address, 
                        token_A_address=token_A_address, 
                        token_B_address=token_B_address, 
                        reserve_A=reserve_A, 
                        reserve_B=reserve_B, 
                        initial_reserve_A=reserve_A, 
                        initial_reserve_B=reserve_B,
                        amm_txn_hash=str(add_liquidity_txn_hash), 
                        amm_ownerid=current_user.id, 
                        timestamp=datetime.now())
            db_session.add(new_amm)
            db_session.commit()
            flash("Pool created successfully!", "success")
        except Exception as e:
            db_session.rollback()
            flash("Failed to create pool: " + str(e), "error")
            return redirect(url_for('create_pool', username=username))
        finally:
            db_session.close()
        
        return redirect(url_for('dashboard', username=username))
    
    db_session.close()
    return render_template('amm_pool.html', 
                           username=username, 
                           user=current_user, 
                           wallet=wallet,
                           user_tokens=list(all_tokens),
                           active_staking_tokens=active_staking_tokens)

# --------------------------- Swap Token ---------------------------
@app.route('/swap/<username>', methods=['GET', 'POST'])
@login_required
def swap(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if not wallet:
        flash("Please create a wallet first!", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=username))
    
    pools = db_session.query(AMM).all()
    active_tokens = {}
    for pool in pools:
        _ = pool.token_A
        _ = pool.token_B
        active_tokens[pool.token_A.token_name] = pool.token_A
        active_tokens[pool.token_B.token_name] = pool.token_B
    active_tokens = list(active_tokens.values())
    
    active_staking_tokens = db_session.query(Token).filter_by(is_stake_active=True).all()
    
    if request.method == 'POST':
        from_token_name = request.form['from_token']
        to_token_name = request.form['to_token']
        from_amount = float(request.form['from_amount'])
        
        if from_token_name == to_token_name:
            flash("Cannot swap the same token.", "error")
            db_session.close()
            return redirect(url_for('swap', username=username))
        
        if from_amount <= 0:
            flash("Invalid swap amount.", "error")
            db_session.close()
            return redirect(url_for('swap', username=username))
        
        from_token = db_session.query(Token).filter_by(contract_address=from_token_name).first()
        to_token = db_session.query(Token).filter_by(contract_address=to_token_name).first()
        
        if not from_token or not to_token:
            flash("Selected tokens not found.", "error")
            db_session.close()
            return redirect(url_for('swap', username=username))
        
        selected_pool = db_session.query(AMM).filter(
            ((AMM.token_A_address == from_token.contract_address) & (AMM.token_B_address == to_token.contract_address)) |
            ((AMM.token_A_address == to_token.contract_address) & (AMM.token_B_address == from_token.contract_address))
        ).first()
        
        if not selected_pool:
            flash("No liquidity pool found for the selected token pair.", "error")
            db_session.close()
            return redirect(url_for('swap', username=username))
        
        from_token_type = 'A' if selected_pool.token_A_address == from_token.contract_address else 'B'
        if from_token_type == 'A':
            reserve_in = selected_pool.reserve_A
            reserve_out = selected_pool.reserve_B
        else:
            reserve_in = selected_pool.reserve_B
            reserve_out = selected_pool.reserve_A
        
        calculated_out = (from_amount * reserve_out) / (reserve_in + from_amount)
        
        try:
            swap_txn_hash = swap_tokens(
                                    sender_id=current_user.id - 1, 
                                    amm_pool_address=selected_pool.amm_address, 
                                    from_token=from_token_type, 
                                    amount=from_amount)
            if from_token_type == 'A':
                selected_pool.reserve_A += from_amount
                selected_pool.reserve_B -= calculated_out
            else:
                selected_pool.reserve_B += from_amount
                selected_pool.reserve_A -= calculated_out
                
            new_tx = Transaction(
                                sender_id=current_user.id, 
                                receiver_id=current_user.id, 
                                amount=from_amount, 
                                tx_type='swap', 
                                tx_hash=str(swap_txn_hash), 
                                token_id=from_token.id, 
                                received_amount=calculated_out, 
                                received_token_id=to_token.id, 
                                timestamp=datetime.now())
            db_session.add(new_tx)
            db_session.commit()
            flash("Swap executed successfully!", "success")
        except Exception as e:
            flash("Swap failed: " + str(e), "error")
        finally:
            db_session.close()
        
        return redirect(url_for('dashboard', username=username))
    
    db_session.close()
    return render_template('swap.html', 
                           username=username, 
                           user=current_user, 
                           active_tokens=active_tokens, 
                           wallet=wallet, 
                           pools=pools,
                           active_staking_tokens=active_staking_tokens)

# --------------------------- Manage Staking Route - Only for admin ---------------------------
@app.route('/manage_staking/<username>', methods=['GET', 'POST'])
@login_required
def manage_staking(username):
    if current_user.username != username or not current_user.is_admin:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    if request.method == 'POST':
        token_id = int(request.form['token_id'])
        token = db_session.query(Token).filter_by(id=token_id).first()
        if token:
            try:
                staking_address = deploy_staking(token_address=token.contract_address)
                transfer_txn_hash = transfer_tokens(
                    sender_id=current_user.id - 1,
                    receiver_address=staking_address,
                    amount=int(token.initial_supply * 0.05),  # Initial stake amount for the staking contract
                    contract_address=token.contract_address
                )
                new_tx = Transaction(
                    sender_id=current_user.id,
                    receiver_id=current_user.id,
                    amount=int(token.initial_supply * 0.05),
                    tx_type='pool_fund',
                    tx_hash=str(transfer_txn_hash),
                    token_id=token.id,
                    timestamp=datetime.now()
                )
                db_session.add(new_tx)
                token.is_stake_active = True
                token.staking_address = staking_address
                db_session.commit()
                flash(f"Staking activated and funded for {token.token_name}.", "success")
            except Exception as e:
                db_session.rollback()
                flash(f"Failed to activate staking: {str(e)}", "error")

        db_session.close()
        return redirect(url_for('manage_staking', username=username))
    
    inactive_staking_tokens = db_session.query(Token).filter_by(is_stake_active=False).all()
    active_staking_tokens = db_session.query(Token).filter_by(is_stake_active=True).all()
    
    db_session.close()
    return render_template('staking_admin.html', 
                            username=username, 
                            user=current_user,
                            inactive_staking_tokens=inactive_staking_tokens, 
                            active_staking_tokens=active_staking_tokens)
    
# --------------------------- Staking Route ---------------------------
@app.route('/staking/<username>', methods=['GET', 'POST'])
@login_required
def staking(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    user_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if not user_wallet:
        flash("Please create a wallet first!", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=username))
    
    if request.method == 'POST':
        action = request.form.get('action')
        amount = float(request.form.get('amount'))
        final_amount = int(amount * (10**18))
        token_id = int(request.form.get('token_id'))
        token = db_session.query(Token).filter_by(id=token_id).first()

        try:
            if action == 'stake':
                stake_txn_hash = execute_stake(
                                        sender_id=current_user.id - 1, 
                                        token_address=token.contract_address, 
                                        staking_address=token.staking_address, 
                                        amount=final_amount)
                flash("Stake executed successfully!", "success")
                new_tx = Transaction(
                                sender_id=current_user.id, 
                                receiver_id=current_user.id, 
                                amount=amount, 
                                tx_type='stake', 
                                tx_hash=str(stake_txn_hash), 
                                token_id=token.id, 
                                received_amount=amount, 
                                received_token_id=token.id,
                                timestamp=datetime.now())
                db_session.add(new_tx)
                
            elif action == 'unstake':
                staking_balance = int(get_staking_contract(token.staking_address).stakingBalance(user_wallet.wallet_address))
                if final_amount <= 0 or final_amount > staking_balance:
                    flash(f"You have only {staking_balance / (10**18)} {token.token_symbol} staked. You cannot unstake more than that.", "error")
                    db_session.close()
                    return redirect(url_for('staking', username=username))
                unstake_txn_hash = execute_unstake(
                                        sender_id=current_user.id - 1, 
                                        token_address=token.contract_address, 
                                        staking_address=token.staking_address, 
                                        amount=final_amount)
                flash("Unstake executed successfully!", "success")
                new_tx = Transaction(
                                sender_id=current_user.id, 
                                receiver_id=current_user.id, 
                                amount=amount, 
                                tx_type='unstake', 
                                tx_hash=str(unstake_txn_hash), 
                                token_id=token.id, 
                                received_amount=amount * 1.1, 
                                received_token_id=token.id,
                                timestamp=datetime.now())
                db_session.add(new_tx)
                
            db_session.commit()
        except Exception as e:
            flash("Staking action failed: " + str(e), "error")
            db_session.rollback()
    
    active_staking_tokens = db_session.query(Token).filter_by(is_stake_active=True).all()
    if not active_staking_tokens:
        flash("No active staking tokens found.", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=username))
    
    staking_balances = {}
    for token in active_staking_tokens:
        balance = int(get_staking_contract(token.staking_address).stakingBalance(user_wallet.wallet_address))
        staking_balances[token.id] = balance / (10**18)
    
    db_session.close()
    return render_template('staking_user.html', 
                           username=username, 
                           user=current_user, 
                           active_staking_tokens=active_staking_tokens,
                           staking_balances=staking_balances)
    
# --------------------------- Main Function -------------------------
if __name__ == "__main__":
    with networks.ethereum.local.use_provider("foundry"):
        app.run(debug=False, port=5000, threaded=False)