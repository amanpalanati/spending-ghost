from datetime import datetime, timedelta
import yfinance as yf
import pytz
import requests
import pandas_market_calendars as cal
import tzlocal

class Transaction:
    def __init__(self, date: str, time: str, merchant: str, amount: float):
        try:
            self.date = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.date = datetime.now()
        self.merchant = merchant.title()  # e.g., "Starbucks"
        self.amount = amount
        self.stock_price = self.get_stock_price()
        self.num_shares = round(float(self.amount) / self.stock_price if self.stock_price != 0.0 else 0.0, 2)
        self.current_value = round((round(float(yf.Ticker(self.get_ticker(self.merchant)).info.get("regularMarketPrice")), 2) - self.stock_price) * self.num_shares + self.amount, 2)
    
    def get_ticker(self, company_name):
        try:
            yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            params = {"q": company_name, "quotes_count": 1, "country": "United States"}

            res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
            data = res.json()

            company_code = data['quotes'][0]['symbol']
            return company_code
        except Exception as e:
            return "SPY"  # Default to S&P 500 ETF if error occurs
        
    def get_stock_price(self):
        try:
            utc_dt = self.date.replace(tzinfo=tzlocal.get_localzone()).astimezone(pytz.utc).replace(second=0, microsecond=0)
            ticker = yf.Ticker(self.get_ticker(self.merchant))
            hist = ticker.history(start=utc_dt, end=(utc_dt + timedelta(minutes=1)), interval="1m")
            if not hist.empty:
                return round(float(hist['Open'].iloc[0]), 2) # get the price as a float and round it to 2 decimal places
            else:
                next_market_open = self.next_market_open(self.date, market='NYSE').replace(second=0, microsecond=0)
                if next_market_open <= datetime.now(tzlocal.get_localzone()):
                    hist = ticker.history(start=next_market_open, end=(next_market_open + timedelta(minutes=1)), interval="1m")
                    return round(float(hist['Open'].iloc[0]), 2)
                else:
                    return round(float(ticker.info.get("regularMarketPrice")), 2)
        except Exception as e:
            return 0.0

    def next_market_open(self, specified_datetime: datetime, market='NYSE'):
        eastern_dt = specified_datetime.replace(tzinfo=tzlocal.get_localzone()).astimezone(pytz.timezone("America/New_York"))
        nyse = cal.get_calendar(market)
        schedule = nyse.schedule(start_date=eastern_dt, end_date=eastern_dt + timedelta(days=10))
        for market_date, row in schedule.iterrows():
            market_open = row['market_open']
            market_open = market_open.astimezone(pytz.timezone("America/New_York"))
            if market_open > eastern_dt:
                return market_open.astimezone(tzlocal.get_localzone())
    
    def update_transaction(self):
        self.current_value = round((round(float(yf.Ticker(self.get_ticker(self.merchant)).info.get("regularMarketPrice")), 2) - self.stock_price) * self.num_shares + self.amount, 2)