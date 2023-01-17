import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from DataRequest import y_finane_option_data , y_finane_stock_data
from BlackAndScholes.BSPricing import BS_PUT , BS_CALL
from scipy.optimize import minimize_scalar



df_options = y_finane_option_data.get_option_data('GOOGL')
last_price = y_finane_stock_data.get_stock_price('GOOGL').tail(1)['Adj Close']
df_options['Underliying_LastPrice'] = last_price.values[0]

def compute_theorical_IV(opt_value, S, K, T, r, type_='CALL' ):
    def call_obj(sigma):
        return abs(BS_CALL(S, K, T, r, sigma) - opt_value)

    def put_obj(sigma):
        return abs(BS_PUT(S, K, T, r, sigma) - opt_value)

    if type_ == 'CALL':
        res = minimize_scalar(call_obj, bounds=(0.01, 15), method='bounded')
        return res.x
    elif type_ == 'PUT':
        res = minimize_scalar(put_obj, bounds=(0.01, 15),
                              method='bounded')
        return res.x
    else:
        raise ValueError("type_ must be 'put' or 'call'")


def plot_ImpliedVolatility(option_df : pd.DataFrame , type,minDay , maxDay):
    df_optionsCall = option_df[option_df['Type'] == type]
    df_optionsCall = df_optionsCall[(option_df['T_days'] > minDay) & (option_df['T_days'] < maxDay)]


    grouped_df = df_optionsCall.groupby('T_days')

    fig, ax = plt.subplots()

    for key, group in grouped_df:
        ax.plot(group['strike'], group['impliedVolatility'], label=key)

    ax.legend()
    ax.set_xlabel('Strike')
    ax.set_ylabel('ImpliedVolatility')
    plt.title(f'{type} Options Volatility skew at different maturities (days) ')
    plt.show()
