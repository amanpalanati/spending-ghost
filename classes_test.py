import unittest
from transaction import Transaction
from merchant import Merchant
from portfolio import Portfolio
from datetime import datetime

class TestClasses(unittest.TestCase):
    def setUp(self):
        self.week_old = Transaction("2025-03-31", "20:30:43", "best buy", 799.99)
        self.friday = Transaction("2025-04-04", "12:36:12", "sbux", 6.64)
        self.bad_transaction = Transaction("wrong date", "not a real time", "goofy ahh merchant", 0)

        self.best_buy = Merchant("best buy")
        self.starbucks = Merchant("starbucks")
        self.bad_merchant = Merchant("Goofy Ahh merchant")

        self.portfolio = Portfolio()

    def test_transaction_initialization(self):
        # Test initialization of a week old transaction
        self.assertEqual(self.week_old.date, datetime.strptime("2025-03-31 20:30:43", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(self.week_old.merchant, "Best Buy")
        self.assertEqual(self.week_old.amount, 799.99)
        self.assertEqual(self.week_old.stock_price, 73.66) # BBY stock price on 2025-04-01 6:30:00 Pacific Time
        self.assertEqual(self.week_old.num_shares, 10.86)
        self.assertEqual(self.week_old.current_value, 656.42) # Current value of the transaction

        # Test initialization of a transaction that happened on friday
        self.assertEqual(self.friday.date, datetime.strptime("2025-04-04 12:36:12", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(self.friday.merchant, "Sbux")
        self.assertEqual(self.friday.amount, 6.64)
        self.assertEqual(self.friday.stock_price, 82.76) # SBUX stock price on 2025-04-04 12:36:00 Pacific Time
        self.assertEqual(self.friday.num_shares, 0.08)
        self.assertEqual(self.friday.current_value, 6.59) # Current value of the transaction

        # Test initialization of a transaction with a bad merchant
        self.assertEqual(self.bad_transaction.merchant, "Goofy Ahh Merchant")
        self.assertEqual(self.bad_transaction.amount, 0)
        self.assertEqual(self.bad_transaction.stock_price, 505.28) # SBUX stock price on 2025-04-04 12:36:00 Pacific Time
        self.assertEqual(self.bad_transaction.num_shares, 0)
        self.assertEqual(self.bad_transaction.current_value, 0) # Current value of the transaction

    def test_update_transaction(self):
        self.week_old.update_transaction()
        self.assertEqual(self.week_old.date, datetime.strptime("2025-03-31 20:30:43", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(self.week_old.merchant, "Best Buy")
        self.assertEqual(self.week_old.amount, 799.99)
        self.assertEqual(self.week_old.stock_price, 73.66) # BBY stock price on 2025-04-01 6:30:00 Pacific Time
        self.assertEqual(self.week_old.num_shares, 10.86)
        self.assertEqual(self.week_old.current_value, 656.42) # Current value of the transaction

    def test_merchant_add_transaction_and_update_merchant(self):
        # Test Best Buy merchant
        self.best_buy.add_transaction(self.week_old)
        self.assertEqual(self.best_buy.transactions, [self.week_old])
        self.assertEqual(self.best_buy.total_spent, 799.99)
        self.assertEqual(self.best_buy.total_shares, 10.86)
        self.assertEqual(self.best_buy.current_value, 656.42)
        self.assertEqual(self.best_buy.net_gain, -143.57)
        
        # Test Starbucks merchant
        self.starbucks.add_transaction(self.friday)
        self.assertEqual(self.starbucks.transactions, [self.friday])
        self.assertEqual(self.starbucks.total_spent, 6.64)
        self.assertEqual(self.starbucks.total_shares, 0.08)
        self.assertEqual(self.starbucks.current_value, 6.59)
        self.assertEqual(self.starbucks.net_gain, -0.05)

        # Test bad merchant
        self.bad_merchant.add_transaction(self.bad_transaction)
        self.assertEqual(self.bad_merchant.transactions, [])
        self.assertEqual(self.bad_merchant.total_spent, 0)
        self.assertEqual(self.bad_merchant.total_shares, 0)
        self.assertEqual(self.bad_merchant.current_value, 0)
        self.assertEqual(self.bad_merchant.net_gain, 0)

    def test_portfolio_add_transaction_and_update_portfolio(self):
        # self.merchants: list[Merchant] = []
        # self.total_spent = 0.0
        # self.current_value = 0.0
        # self.net_gain = 0.0

        self.portfolio.add_transaction(self.week_old)
        self.portfolio.add_transaction(self.friday)
        self.portfolio.add_transaction(self.bad_transaction)

        self.assertEqual(len(self.portfolio.merchants), 2)  # Only valid merchants should be in the portfolio
        self.assertEqual(self.portfolio.total_spent, 799.99 + 6.64)
        self.assertEqual(self.portfolio.current_value, 656.42 + 6.59)
        self.assertEqual(self.portfolio.net_gain, (656.42 + 6.59) - (799.99 + 6.64))

    if __name__ == '__main__':
        unittest.main()