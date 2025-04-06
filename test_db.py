"""
NOTICE: Running this test will create a new SQLite database file named 'transactions.db' in the current directory.
Make sure to remove this file if you don't want to keep it.
"""

from datetime import datetime, timedelta
from database import init_db, save_transaction, load_transactions

init_db()

date = datetime.now()
merchant = "Starbucks"
amount = 6.64
stock_price = 85.55
num_shares = 0.08
current_value = 6.64
user_id = "test user aman"

save_transaction(date, merchant, amount, stock_price, num_shares, current_value, user_id)


date = datetime.now() - timedelta(days=5, hours=4, minutes=3, seconds=2)
merchant = "another merchant"
amount = 642.99
stock_price = 24.83
num_shares = 25.92
current_value = 6423.99
user_id = "another tester"

save_transaction(date, merchant, amount, stock_price, num_shares, current_value, user_id)


date = datetime.now() - timedelta(days=2, hours=3, minutes=4, seconds=5)
merchant = "other merchant"
amount = 10.20
stock_price = 102.29
num_shares = 0.10
current_value = 5.20
user_id = "test user aman"

save_transaction(date, merchant, amount, stock_price, num_shares, current_value, user_id)


rows = load_transactions("test user aman")
print("Rows for user 'test user aman':")
for row in rows:
    print(dict(row))

rows = load_transactions("another tester")
print("Rows for user 'another tester':")
for row in rows:
    print(dict(row))



