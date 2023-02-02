import pandas as pd
from DataRequest.y_finane_option_data import get_Option_Data_full , get_stock_price
import matplotlib.pyplot as plt

# the purpose of this script is to demonstrate de call/put parity
# C + Ke(-rT) = P + S0

ticker = 'TSLA'
options_df = get_Option_Data_full(ticker)

#Taking one maturity for observation
maturities = options_df['T_days'].unique()
maturity = maturities[3]

options_df = options_df[options_df['T_days'] == maturity]
options_df = options_df[['mid_price' , 'T_days' , 'strike','Type' , 'underlying_LastPrice']]

call = options_df[options_df['Type'] =='CALL']
put = options_df[options_df['Type'] =='PUT']

df = pd.merge(call, put, how='inner', on ='strike')
df = df.rename(columns={"mid_price_x": "calls_prices", "mid_price_y": "put_prices"})

#plot
df.plot(x='strike' , y =['calls_prices' , 'put_prices'])
plt.title(f'Observed market prices for call and put options for {ticker} , T = {maturity}d')
plt.show()


df['P + S -K'] = df.put_prices + df.underlying_LastPrice_y - df.strike

df.plot(x='strike' , y =['calls_prices' , 'P + S -K'])
plt.title(f'Market calls prices vs calculated (C/P Parity) {ticker} , T = {maturity}d')
plt.show()


df['C + K -S'] = df.calls_prices + df.strike - df.underlying_LastPrice_y
df.plot(x='strike' , y =['put_prices' , 'C + K -S'])
plt.title(f'Market calls prices vs calculated (C/P Parity) {ticker} , T = {maturity}d')
plt.show()
