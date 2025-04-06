from transaction import Transaction
from datetime import datetime, timedelta

class Merchant:
    def __init__(self, name: str):
        self.name = name.title()  # e.g., "Starbucks"
        self.transactions: list[Transaction] = []
        self.total_spent = 0.0
        self.total_shares = 0.0
        self.current_value = 0.0
        self.net_gain = 0.0

    def add_transaction(self, txn: Transaction):
        txn.update_transaction()
        self.transactions.append(txn)
        self.update_merchant()

    def update_merchant(self):
        self.total_spent = 0.0
        self.total_shares = 0.0
        self.current_value = 0.0
        six_months_ago = datetime.now() - timedelta(days=182)
        valid_transactions = []
        
        for txn in self.transactions:
            txn.update_transaction()
            if txn.date > six_months_ago and txn.amount > 0:
                valid_transactions.append(txn)
                self.total_spent += txn.amount
                self.total_shares += txn.num_shares
                self.current_value += txn.current_value
        
        self.transactions = valid_transactions
        self.net_gain = round(self.current_value - self.total_spent, 2)