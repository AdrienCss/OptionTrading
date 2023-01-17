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

