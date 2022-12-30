import pandas as pd
import yfinance as yf
import datetime

def get_option_data(symbol):
    tk = yf.Ticker(symbol)
    expirations = tk.options

    options = pd.DataFrame()

    for e in expirations:
        opt = tk.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt['expirationDate'] = e
        options = options.append(opt, ignore_index=True)

    options['expirationDate'] = pd.to_datetime(options['expirationDate']) + datetime.timedelta(days=1)
    options['dte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days / 365
    options['CALL'] = options['contractSymbol'].str[4:].apply(lambda x: "C" in x)
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mid'] = (options['bid'] + options['ask']) / 2

    return options
