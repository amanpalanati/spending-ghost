import sqlite3
from transaction import Transaction
from datetime import datetime


DATABASE = "transactions.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            merchant TEXT NOT NULL,
            amount REAL NOT NULL,
            stock_price REAL NOT NULL,
            num_shares REAL NOT NULL,
            current_value REAL NOT NULL,
            user_id TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_transaction(date_time, merchant, amount, stock_price, num_shares, current_value, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO transactions (
            date_time, merchant, amount, stock_price, num_shares, current_value, user_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        date_time.isoformat(),  # Storing as ISO formatted string
        merchant,
        amount,
        stock_price,
        num_shares,
        current_value,
        user_id
    ))
    conn.commit()
    conn.close()

def load_transactions(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT date_time, merchant, amount, stock_price, num_shares, current_value
        FROM transactions
        WHERE user_id = ?
    ''', (user_id,))
    rows = cur.fetchall()
    conn.close()
    
    transactions = []
    for row in rows:
        txn = Transaction.from_db_row(dict(row))
        transactions.append(txn)
    return transactions