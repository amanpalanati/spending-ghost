from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import init_db, load_transactions, save_transaction
from datetime import datetime
from transaction import Transaction
from merchant import Merchant
from portfolio import Portfolio

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for sessions and flash messages

# Initialize the database (creates tables if they don't exist)
init_db()

@app.route("/")
def index():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    
    rows = load_transactions(user_id)
    transactions = rows
    
    portfolio = Portfolio()
    for txn in transactions:
        portfolio.add_transaction(txn)
    
    return render_template("index.html", portfolio=portfolio)

@app.route("/merchant/<merchant_name>")
def merchant_detail(merchant_name):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    
    # Load all transactions for the user (they're already Transaction objects)
    transactions = load_transactions(user_id)
    merchant_transactions = []
    for txn in transactions:
        # Use dot notation to access the merchant attribute
        if txn.merchant.lower() == merchant_name.lower():
            merchant_transactions.append(txn)
    
    return render_template("merchant.html", merchant_name=merchant_name, transactions=merchant_transactions)

@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # Ensure the user is logged in
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        date_str = request.form.get("date")   # e.g., "2025-04-04"
        time_str = request.form.get("time")     # e.g., "14:30:00"
        merchant = request.form.get("merchant")
        amount = float(request.form.get("amount"))
        
        try:
            # Create a Transaction object using your logic in transaction.py.
            txn = Transaction(date=date_str, time=time_str, merchant=merchant, amount=amount)
        except Exception as e:
            flash("Invalid transaction data!")
            return redirect(url_for("add_transaction"))
        
        # Now, use the computed values from the Transaction object.
        # For instance, ensure num_shares is rounded to two decimal places.
        computed_num_shares = round(txn.num_shares, 2)
        
        save_transaction(
            txn.date,               # datetime object
            txn.merchant,
            txn.amount,
            txn.stock_price,
            computed_num_shares,
            txn.current_value,
            user_id
        )
        flash("Transaction added successfully!")
        return redirect(url_for("index"))
    
    return render_template("add.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        if user_id:
            session["user_id"] = user_id
            flash(f"Logged in as {user_id}")
            return redirect(url_for("index"))
        else:
            flash("Please enter a user ID.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)