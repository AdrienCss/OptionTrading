from  BinomialModel.BinomialPricing  import  binom_EU1
from BlackAndScholes.BSPricing import priceBS
from DataRequest import y_finane_option_data , y_finane_stock_data
from Volatility.ImpliedVolatiliy import compute_theorical_IV
import matplotlib as plt
df = y_finane_option_data.get_option_data('TSLA')
stockPrices_ = y_finane_stock_data.get_stock_price('TSLA')

df['Underlying_Price'] = stockPrices_['Adj Close'].tail(1).values[0]

prices_Bi = []

for row in df.itertuples():
    price = binom_EU1(row.Underlying_Price, row.strike, row.T_days / 252, 0.01, 0.5, 200, row.Type)
    prices_Bi.append(price)

df['Binomial_Prices'] = prices_Bi

prices_BS = []
for row in df.itertuples():
    price = priceBS(row.Underlying_Price, row.strike, row.T_days / 252, 0.01 ,row.impliedVolatility , row.Type)
    prices_BS.append(price)


df['Black_And_Scholes_Prices'] = prices_BS
df['mid_Price'] = (df['bid'] + df['ask']) /2

IV = []
for row in df.itertuples():
    price = compute_theorical_IV(row.mid_Price , row.Underlying_Price ,row.strike, row.T_days / 252, 0.01 , row.Type)
    IV.append(price)
df['IV_Calculated'] = IV



# Chose Expiration
exp1 = df[(df.T_days == df.T_days.unique()[2]) & (df.Type=='CALL')]

import matplotlib.pyplot as plt
plt.plot(exp1.strike, exp1.mid_Price, label='Mid Price')
plt.plot(exp1.strike, exp1.Black_And_Scholes_Prices, label='B&S Prices')
plt.plot(exp1.strike, exp1.Binomial_Prices, label='Binomial Prices')

plt.xlabel('Strike')
plt.ylabel('Call Values')
plt.legend()
plt.show()

# plotIV
import matplotlib.pyplot as plt
plt.plot(exp1.strike, exp1.impliedVolatility, label='IV market')
plt.plot(exp1.strike, exp1.IV_Calculated, label='IV calculated')

plt.xlabel('Strike')
plt.ylabel('Implied Volatility Values')
plt.legend()
plt.show()
