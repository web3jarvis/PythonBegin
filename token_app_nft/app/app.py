from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from ape import accounts, networks
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from db import SessionLocal, Base, engine
from models import NFTCollection, User, Wallet, Transaction
from blockchain.ape_util import deploy_and_mint_nft
from datetime import datetime
import os

# ---------------------------- Helper Functions -------------------------
def sort_by_timestamp(tx):
    return tx.timestamp

# ---------------------------- Initialize Flask App -------------------------
app = Flask(__name__)

# ---------------------------- Configure Flask App -------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
            
    all_transactions = list(set(user.sent_tx + user.received_tx)) # Deduplicate
    transaction_history = all_transactions
    transaction_history.sort(key=sort_by_timestamp, reverse=True)
    
    render_data = render_template('dashboard.html', 
                                   user=user, 
                                   username=username, 
                                   wallet=wallet,
                                   transactions=transaction_history)
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

# ---------------------------- Mint NFT ----------------------------
@app.route('/mint_nft/<username>', methods=['GET', 'POST'])
@login_required
def mint_nft(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    user_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if not user_wallet:
        flash("Please create a wallet first!", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=username))
    
    image_url = "https://ipfs.io/ipfs/bafybeiht5whhdlmk2acdano6yw7flk6lnzj6gmorieturrxw3lxjadaod4"
    metadata_uri = "ipfs://bafkreidq3mfl5s3w6n465nyq57kguoo62fm7hjodqf3ubml7odpktnxj2q"

    if request.method == 'POST':
        fixed_nft_name = "My Custom NFT Pass"
        
        success = False
        try:
            txn_hash = deploy_and_mint_nft(current_user.id - 1, metadata_uri, fixed_nft_name)
            
            new_nft_tx = Transaction(
                                    sender_id=current_user.id, 
                                    receiver_id=current_user.id, 
                                    amount=1, 
                                    tx_type='mint_nft', 
                                    tx_hash=str(txn_hash), 
                                    timestamp=datetime.now())
            db_session.add(new_nft_tx)
            db_session.commit()
            success = True
        except Exception as e:
            print(f"Exception, if any: {e}")
            db_session.rollback()
        finally:
            db_session.close()

        if success:
            flash("NFT minted successfully!", "success")
            return render_template('mint.html',
                                   user=current_user, 
                                   username=username,
                                   success=success,
                                   nft_name=fixed_nft_name, 
                                   image_url=image_url,
                                   txn_hash=txn_hash)
        else:
            flash("Failed to mint NFT.", "error")
            return redirect(url_for('mint_nft', username=username))
        
    db_session.close()
    return render_template('mint.html', 
                           username=username, 
                           user=current_user,
                           image_url=image_url)

# ---------------------------- NFT Upload Route ----------------------------
@app.route('/upload_nft/<username>', methods=['GET', 'POST'])
@login_required
def upload_nft(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    if not current_user.is_admin:
        flash("Access denied! Only admin can upload NFTs.", "error")
        return redirect(url_for('dashboard', username=username))
    
    if request.method == 'POST':
        nft_name = request.form['nft_name']
        nft_description = request.form['nft_description']
        file = request.files['file']
        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            db_session = SessionLocal()
            try:
                new_nft = NFTCollection(
                                    owner_id=current_user.id, 
                                    name=nft_name, 
                                    description=nft_description, 
                                    image_cid=filename, 
                                    metadata_uri=f"http://127.0.0.1:5000/static/uploads/{filename}", 
                                    timestamp=datetime.now()
                                    )
                db_session.add(new_nft)
                db_session.commit()
                flash(f"NFT, {nft_name}, uploaded successfully!", "success")
            except Exception as e:
                print(f"Exception occurred: {e}")
                db_session.rollback()
                flash("Failed to upload NFT.", "error")
            finally:
                db_session.close()
        else:
            flash("No file uploaded.", "error")
    return render_template('upload.html', 
                           username=username, 
                           user=current_user)
    

# --------------------------- Main Function -------------------------
if __name__ == "__main__":
    with networks.ethereum.local.use_provider("foundry"):
        app.run(debug=False, port=5000, threaded=False)