from Volatility import ImpliedVolatiliy
from Option.OptionStrategies import OptionStrategies
from Option.Option import Option , Stock
from Enum.OptionType import OpionType
from Enum.BuySellSide import BuySellSide
from DataRequest import  y_finane_option_data , y_finane_stock_data
from Volatility.ImpliedVolatiliy import compute_theorical_IV, plot_ImpliedVolatility
import numpy as np


ticker = 'TSLA'

## Get Option/underlying stock Prices
option_df = y_finane_option_data.get_option_data(ticker)
stockPrices_ = y_finane_stock_data.get_stock_price(ticker)
last_price = stockPrices_.tail(1)['Adj Close'].values[0]

#chose options
currentprice = last_price
maturities =option_df['T_days'].unique()
random_maturity = np.random.choice(maturities)

options_df = option_df[option_df['T_days'] ==random_maturity]

call_df = options_df[options_df['Type'] =='CALL']
put_df = options_df[options_df['Type'] =='PUT']

call_OTM = call_df.iloc[(call_df['strike']-(currentprice + 15)).abs().argsort()[:1]]
call_ITM = call_df.iloc[(call_df['strike']-(currentprice - 15)).abs().argsort()[:1]]

put_OTM = put_df.iloc[(put_df['strike']-(currentprice - 15)).abs().argsort()[:1]]
put_ITM = put_df.iloc[(put_df['strike']-(currentprice + 15)).abs().argsort()[:1]]


## creating initial options objects
call_OTM = Option(price=call_OTM['lastPrice'].values[0], K=call_OTM['strike'].values[0] , type= OpionType.CALL)
call_ITM = Option(price=call_ITM['lastPrice'].values[0], K=call_ITM['strike'].values[0] , type= OpionType.CALL)

put_OTM = Option(price=put_OTM['lastPrice'].values[0], K=put_OTM['strike'].values[0] , type= OpionType.PUT)
put_ITM = Option(price=put_ITM['lastPrice'].values[0], K=put_ITM['strike'].values[0] , type= OpionType.PUT)

#stock = Stock(price = currentprice)


# Creating call spead
strategy = OptionStrategies(name = "Call spread (ITM / OTM)" ,St = currentprice)
strategy.add_Option(option= call_OTM ,buySell= BuySellSide.SELL , option_number=1 )
strategy.add_Option(option= call_ITM ,buySell= BuySellSide.BUY , option_number=1 )
strategy.plot()


strategy.compute_greek_profile(T ,r , vol)

strategy.plotGreek(greekStr='gamma')
strategy.plotGreek(greekStr='theta')
strategy.plotGreek(greekStr='delta')
strategy.plotGreek(greekStr='vega')


# Creating put spread
strategy = OptionStrategies(name = "PUT Spread (ITM / OTM)" ,St = currentprice)
strategy.add_Option(option= put_ITM ,buySell= BuySellSide.BUY , option_number=1 )
strategy.add_Option(option= put_OTM,buySell= BuySellSide.SELL , option_number=1 )
strategy.plot()


strategy.compute_greek_profile(T ,r , vol)

strategy.plot()




strategy.plotGreek(greekStr='gamma')
strategy.plotGreek(greekStr='theta')
strategy.plotGreek(greekStr='delta')
strategy.plotGreek(greekStr='vega')
