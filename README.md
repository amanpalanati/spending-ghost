# 💸 SpendingGhost

**Track your spending. See what it *could've* been.**  
SpendingGhost is a budgeting tool with a twist—it visualizes how your spending could have grown if you had invested instead of spent.

---

## 🚀 Live Demo
🌐 https://spending-ghost.onrender.com/login

---

## 📌 Inspiration
I wanted to make budgeting more insightful by directly showing consumers how their everyday purchases could have grown if they invested them instead. People often regret wasteful spending, so Spending Ghost turns that regret into a useful reflection.

---

## 🧠 What It Does
- Lets users enter past purchases and merchant names.
- Shows how many shares they could’ve bought at the time.
- Tracks the *current value* of those ghost shares.
- Displays overall portfolio gain/loss and per-merchant breakdowns.

---

## 🛠️ How It Works
- **Backend**: Python + Flask
- **Frontend**: HTML (basic for now)
- **Database**: SQLite (per-user transaction storage)
- **APIs**: Yahoo Finance via `yfinance` (for stock prices)
- **Hosting**: Render.com
