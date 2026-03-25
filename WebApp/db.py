import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
connect = sqlite3.connect(DB_PATH)
cursor = connect.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS user
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    private_key TEXT,
    public_key TEXT)"""
)
cursor.execute(
    
    """CREATE TABLE IF NOT EXISTS mempool
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    sender TEXT, 
    receiver TEXT, 
    amount INTEGER,
    timestamp REAL,
    signature TEXT,
    public_key TEXT)"""
)
cursor.execute(
    
    """CREATE TABLE IF NOT EXISTS blockchain
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    index_number INTEGER, 
    timestamp REAL, 
    transactions TEXT, 
    previous_hash TEXT, 
    block_hash TEXT, 
    nonce INTEGER)"""
)
connect.commit()
connect.close()