from transaction import Transaction
from merchant import Merchant

class Portfolio:
    def __init__(self):
        self.merchants: list[Merchant] = []
        self.total_spent = 0.0
        self.current_value = 0.0
        self.net_gain = 0.0

    def add_transaction(self, txn: Transaction):
        txn.update_transaction()
        added = False
        for m in self.merchants:
            if m.name == txn.merchant:
                m.add_transaction(txn)
                added = True
                break
        if not added:
            m = Merchant(txn.merchant)
            m.add_transaction(txn)
            self.merchants.append(m)
        self.update_portfolio()
            
    def update_portfolio(self):
        self.total_spent = 0.0
        self.current_value = 0.0
        valid_merchants = []

        for m in self.merchants:
            m.update_merchant()
            if m.total_spent > 0:
                valid_merchants.append(m)
                self.total_spent += m.total_spent
                self.current_value += m.current_value

        self.merchants = valid_merchants
        self.total_spent = round(self.total_spent, 2)
        self.current_value = round(self.current_value, 2)
        self.net_gain = round(self.current_value - self.total_spent, 2)
