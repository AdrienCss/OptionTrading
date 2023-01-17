import pandas as pd
import yfinance as yf



def get_stock_price(ticker):
    data = yf.download(ticker)
    return pd.DataFrame(data)
