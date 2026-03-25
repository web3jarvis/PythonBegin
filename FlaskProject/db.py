import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

connect = sqlite3.connect(DB_PATH)
cursor = connect.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS userdata
    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, mobile INTEGER NOT NULL)"""
)

connect.commit()
connect.close()