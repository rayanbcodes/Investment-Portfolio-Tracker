# modules/data_fetch.py
import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="1y"):
    """
    Fetch historical stock data for the given ticker.
    Returns a DataFrame with Date and Close price.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        hist.reset_index(inplace=True)
        return hist[['Date', 'Close']]
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame(columns=['Date', 'Close'])

def fetch_current_price(ticker):
    """
    Fetch the current stock price.
    """
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[-1]
        return price
    except:
        return None
