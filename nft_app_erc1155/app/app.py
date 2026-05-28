from flask import Flask, request, render_template, redirect, url_for, flash
from ape import accounts, networks
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from db import SessionLocal, Base, engine
from models import NFTCollection, User, Wallet, Transaction
from blockchain.ape_util import deploy_and_mint_nft, set_owner_royalty, transfer_nft_owner
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
    user = db_session.get(User, int(user_id)) 
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
            
    transaction_history = list(set(user.sent_tx + user.received_tx)) # Deduplicate
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

# ---------------------------- NFT Mint Route ----------------------------
@app.route('/mint_nft/<username>', methods=['GET', 'POST'])
@login_required
def mint_nft(username):
    if current_user.username != username:
        return "Unauthorized", 403
    
    if not current_user.is_admin:
        flash("Access denied! Only admin can mint NFTs.", "error")
        return redirect(url_for('dashboard', username=username))
    
    db_session = SessionLocal()
    user_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if not user_wallet:
        flash("Please create a wallet first!", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=current_user.username))
    
    if request.method == 'POST':
        nft_name = request.form['nft_name']
        nft_description = request.form['nft_description']
        file = request.files['file']
        nft_supply = int(request.form['nft_supply'])
        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            

            try:
                new_nft = NFTCollection(
                                    owner_id=current_user.id, 
                                    name=nft_name, 
                                    description=nft_description, 
                                    image_cid=filename, 
                                    metadata_uri=f"http://127.0.0.1:5000/static/uploads/{filename}", 
                                    nft_supply=nft_supply,
                                    timestamp=datetime.now()
                                    )
                db_session.add(new_nft)
                db_session.commit()
                nft_id = new_nft.id
                admin_nft_mint(nft_id)
                flash(f"Upload successful! NFT named \"{nft_name}\" minted successfully into the marketplace!", "success")
            except Exception as e:
                print(f"Exception occurred: {e}")
                db_session.rollback()
                flash("Failed to mint NFT.", "error")
            finally:
                db_session.close()
        else:
            flash("No file uploaded.", "error")
    return render_template('mint.html', 
                           username=username, 
                           user=current_user,
                           wallet=user_wallet)

# ---------------------------- Admin NFT Minting Route ----------------------------
def admin_nft_mint(id):
    
    db_session = SessionLocal()
    user_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if not user_wallet:
        flash("Please create a wallet first!", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=current_user.username))
    
    nft_item = db_session.query(NFTCollection).filter_by(id=id).first()
    if not nft_item:
        flash("NFT not found.", "error")
        db_session.close()
        return redirect(url_for('nft_gallery', username=current_user.username))
    
    metadata_uri = nft_item.metadata_uri
    
    if request.method == 'POST':
        nft_name_by_admin = nft_item.name
        
        success = False
        try:
            admin_nft_txn_hash = deploy_and_mint_nft(current_user.id - 1, nft_item.id, metadata_uri, nft_item.nft_supply)
            
            admin_nft_tx = Transaction(
                                    sender_id=current_user.id, 
                                    receiver_id=current_user.id, 
                                    amount=1, 
                                    tx_type='admin_nft_mint', 
                                    nft_id=nft_item.id, 
                                    tx_hash=str(admin_nft_txn_hash), 
                                    timestamp=datetime.now())
            db_session.add(admin_nft_tx)
            db_session.commit()
            success = True
        except Exception as e:
            print(f"Exception, if any: {e}")
            db_session.rollback()
        finally:
            db_session.close()

        if success:
            flash(f"Successfully minted \"{nft_name_by_admin}\" NFT!", "success")
        else:
            flash("Failed to mint NFT.", "error")
        
        return redirect(url_for('nft_gallery', username=current_user.username))

# ---------------------------- View NFT Gallery ----------------------------
@app.route('/nft_gallery/<username>', methods=['GET'])
@login_required
def nft_gallery(username):
    db_session = SessionLocal()
    user_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
    if not user_wallet:
        flash("Please create a wallet first!", "error")
        db_session.close()
        return redirect(url_for('dashboard', username=username))
    try:
        all_nfts = db_session.query(NFTCollection).all()
        
        transfer_nft_txs = db_session.query(Transaction).filter_by(
            receiver_id=current_user.id, 
            tx_type='transfer_nft'
        ).all()
        
        nft_owner_ids = [tx.nft_id for tx in transfer_nft_txs]

        for nft in all_nfts:
            nft_owner_count = db_session.query(Transaction).filter_by(
                nft_id=nft.id, 
                tx_type='transfer_nft'
            ).count()
            nft.owner_count = nft_owner_count
            nft.already_owned = nft.id in nft_owner_ids
            nft.owner_name = nft.owner.username
        
            latest_tx = db_session.query(Transaction).filter_by(
                nft_id=nft.id, 
                tx_type='transfer_nft'
            ).order_by(Transaction.timestamp.desc()).first()
            if latest_tx:
                nft.current_owner_name = db_session.query(User).filter_by(id=latest_tx.receiver_id).first().username
            else:
                nft.current_owner_name = nft.owner_name
        
    except Exception as e:
        print(f"Error: {e}")
        all_nfts = []
    finally:
        db_session.close()
    
    return render_template('gallery.html', username=username, wallet=user_wallet, nfts=all_nfts)

# --------------------------- Transfer NFT ---------------------------
@app.route('/transfer_nft/<username>/<int:id>', methods=['GET', 'POST'])
@login_required
def transfer_nft(username, id):
    if current_user.username != username:
        return "Unauthorized", 403
    
    db_session = SessionLocal()
    success = False
    
    try:
        nft = db_session.query(NFTCollection).filter_by(id=id).first()
        if not nft:
            flash("NFT not found.", "error")
            return redirect(url_for('nft_gallery', username=username))
        
        user_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=current_user.id).first()
        if not user_wallet:
            flash("Please create a wallet first!", "error")
            return redirect(url_for('nft_gallery', username=username))
        
        if nft.owner_id == current_user.id:
            flash("You yourself is the owner of this NFT!", "error")
            return redirect(url_for('nft_gallery', username=username))
        
        current_owner_count = db_session.query(Transaction).filter_by(
            nft_id=nft.id, 
            tx_type='transfer_nft'
        ).count()
        if current_owner_count >= nft.nft_supply:
            flash("All NFTs of this collection have been transferred. Please buy from secondary market!", "error")
            return redirect(url_for('nft_gallery', username=username))
        
        transfer_nft_txn_hash = transfer_nft_owner(nft.owner_id - 1, user_wallet.wallet_address, nft.id, 1)
            
        transfer_nft_tx = Transaction(
                                    sender_id=nft.owner_id, 
                                    receiver_id=current_user.id, 
                                    amount=1, 
                                    tx_type='transfer_nft', 
                                    nft_id=nft.id, 
                                    tx_hash=str(transfer_nft_txn_hash), 
                                    timestamp=datetime.now())
        db_session.add(transfer_nft_tx)
        
        nft_owner_wallet = db_session.query(Wallet).filter_by(wallet_ownerid=nft.owner_id).first()
        royalty_receipt_hash = set_owner_royalty(nft.owner_id - 1, nft_owner_wallet.wallet_address, 1000)
        royalty_receipt_tx = Transaction(
                                    sender_id=current_user.id, 
                                    receiver_id=nft.owner_id, 
                                    amount=0.01, 
                                    tx_type='royalty_payment', 
                                    nft_id=nft.id, 
                                    tx_hash=str(royalty_receipt_hash), 
                                    timestamp=datetime.now())
        db_session.add(royalty_receipt_tx)
        
        db_session.commit()
        success = True
    except Exception as e:
        print(f"Exception, if any: {e}")
        db_session.rollback()
    finally:
        db_session.close()
        
    if success == True:
        flash(f"Successfully got NFT with ID {id}!", "success")
    else:
        flash("Failed to transfer NFT.", "error")
        
    return redirect(url_for('dashboard', username=username))
            
            
# --------------------------- Main Function -------------------------
if __name__ == "__main__":
    with networks.ethereum.local.use_provider("foundry"):
        app.run(debug=False, port=5000, threaded=False)