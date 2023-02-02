import pandas as pd
import yfinance as yf
import datetime


def get_option_data(symbol):
    tk = yf.Ticker(symbol)
    expirations = tk.options

    options = pd.DataFrame()

    for e in expirations:
        opt = tk.option_chain(e)
        opt = pd.concat([opt.calls,opt.puts])
        opt['expirationDate'] = e
        options = pd.concat([options, opt] ,ignore_index=True)

    options['expirationDate'] = pd.to_datetime(options['expirationDate'])
    options['T_days'] = (options['expirationDate'] - datetime.datetime.today()).dt.days
    options['T_days'] = options['T_days'].apply(lambda x: 0 if x < 0 else x)
    options['Type'] = options['contractSymbol'].str[4:].apply(lambda x: "CALL" if 'C' in x else "PUT" )
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)

    return options


def get_stock_price(ticker):
    data = yf.download(ticker)
    return pd.DataFrame(data)


def get_Option_Data_full(symbol) -> pd.DataFrame:
    print('getting options quotes..')
    option_df = get_option_data(symbol)
    print('getting stock price..')
    stockPrices_ = get_stock_price(symbol)

    last_price = stockPrices_.tail(1)['Adj Close'].values[0]
    option_df['underlying_LastPrice'] = last_price
    option_df['mid_price'] = (option_df['bid'] +  option_df['ask']) /2

    return option_df

