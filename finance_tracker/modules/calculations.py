# modules/calculations.py
import pandas as pd
import numpy as np

def calculate_portfolio(df):
    """
    Calculate current value, gain/loss, and daily % change.
    """
    df['Current Value'] = df['Shares'] * df['Current Price']
    df['Gain/Loss'] = df['Current Value'] - df['Shares'] * df['Purchase Price']
    df['Daily Change %'] = ((df['Current Price'] - df['Previous Close']) / df['Previous Close']) * 100
    return df

def portfolio_volatility(df, historical_prices):
    """
    Calculate annualized volatility of the portfolio using historical returns.
    historical_prices: dict of ticker -> DataFrame with 'Date' and 'Close'
    """
    returns_list = []
    for ticker, hist_df in historical_prices.items():
        hist_df['Return'] = hist_df['Close'].pct_change()
        returns_list.append(hist_df['Return'].fillna(0))

    # Combine returns into a DataFrame
    returns_df = pd.concat(returns_list, axis=1)
    returns_df.columns = df['Stock']
    # Portfolio weights
    weights = df['Current Value'] / df['Current Value'].sum()
    # Portfolio daily returns
    port_returns = returns_df.dot(weights)
    # Annualized volatility
    vol = np.std(port_returns) * np.sqrt(252)
    return vol
