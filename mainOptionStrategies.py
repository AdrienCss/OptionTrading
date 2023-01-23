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



call_OTM_df = call_df.iloc[(call_df['strike']-(currentprice + 15)).abs().argsort()[:1]]
call_ITM_df = call_df.iloc[(call_df['strike']-(currentprice - 15)).abs().argsort()[:1]]

put_OTM_df = put_df.iloc[(put_df['strike']-(currentprice - 15)).abs().argsort()[:1]]
put_ITM_df = put_df.iloc[(put_df['strike']-(currentprice + 15)).abs().argsort()[:1]]


## creating initial options objects
call_OTM = Option(price=call_OTM_df['lastPrice'].values[0], K=call_OTM_df['strike'].values[0] , type= OpionType.CALL)
call_ITM = Option(price=call_ITM_df['lastPrice'].values[0], K=call_ITM_df['strike'].values[0] , type= OpionType.CALL)

put_OTM = Option(price=put_OTM_df['lastPrice'].values[0], K=put_OTM_df['strike'].values[0] , type= OpionType.PUT)
put_ITM = Option(price=put_ITM_df['lastPrice'].values[0], K=put_ITM_df['strike'].values[0] , type= OpionType.PUT)

#stock = Stock(price = currentprice)

T = 6
r = 0.015
vol =  0.20#(call_OTM_df['impliedVolatility'].values[0] + call_ITM_df['impliedVolatility'].values[0] )/ 2

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
strategy.plotGreek(greekStr='gamma')
strategy.plotGreek(greekStr='theta')
strategy.plotGreek(greekStr='delta')
strategy.plotGreek(greekStr='vega')



# Creating Straddle => Same Strike
#Check that CALL = PUT strike

call_dfs= call_df.iloc[(call_df['strike']-(currentprice - 15)).abs().argsort()[:1]]
put_dfs = put_df[(put_df['strike'] == call_df['strike'].values[0])]

put = Option(price=put_dfs['lastPrice'].values[0], K=put_dfs['strike'].values[0] , type= OpionType.PUT)
call = Option(price=call_dfs['lastPrice'].values[0], K=call_dfs['strike'].values[0] , type= OpionType.CALL)


strategy = OptionStrategies(name = "Straddle" ,St = currentprice)
strategy.add_Option(option= put ,buySell= BuySellSide.BUY , option_number=1 )
strategy.add_Option(option= call,buySell= BuySellSide.BUY , option_number=1 )
strategy.plot()

strategy.compute_greek_profile(T ,r , vol)
strategy.plotGreek(greekStr='gamma')
strategy.plotGreek(greekStr='theta')
strategy.plotGreek(greekStr='delta')
strategy.plotGreek(greekStr='vega')


# Creating Strangle
#Check that CALL strike  >  PUT strike

call_df= call_df.iloc[(call_df['strike']-(currentprice - 15)).abs().argsort()[:1]]
put_df= put_df.iloc[(put_df['strike']-(currentprice - 70)).abs().argsort()[:1]]


put = Option(price=put_df['lastPrice'].values[0], K=put_df['strike'].values[0] , type= OpionType.PUT)
call = Option(price=call_df['lastPrice'].values[0], K=call_df['strike'].values[0] , type= OpionType.CALL)


strategy = OptionStrategies(name = "Strangle" ,St = currentprice)
strategy.add_Option(option= call ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_Option(option= put ,buySell= BuySellSide.BUY, option_number=1 )
strategy.plot()

strategy.compute_greek_profile(T ,r , vol)
strategy.plotGreek(greekStr='gamma')
strategy.plotGreek(greekStr='theta')
strategy.plotGreek(greekStr='delta')
strategy.plotGreek(greekStr='vega')


#synthetic call

put_df1 = put_df.iloc[(put_df['strike']-(currentprice - 15)).abs().argsort()[:1]]

put = Option(price=put_df1['lastPrice'].values[0], K=put_df1['strike'].values[0] , type= OpionType.PUT)
stock = Stock(price = last_price)

strategy = OptionStrategies(name = "Synthetic call" ,St = currentprice)
strategy.add_Option(option= put ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_deltaOne(stock=stock,buySell= BuySellSide.BUY )
strategy.plot()



#synthetic PUT

call_df1 = call_df.iloc[(call_df['strike']-(currentprice - 15)).abs().argsort()[:1]]

call = Option(price=call_df1['lastPrice'].values[0], K=call_df1['strike'].values[0] , type= OpionType.CALL)
stock = Stock(price = currentprice)

strategy = OptionStrategies(name = "Synthetic PUT", St = currentprice)
strategy.add_Option(option= call ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_deltaOne(stock=stock,buySell= BuySellSide.SELL )

strategy.plot()

#Butterfly

call1 = Option(price=put_df1['lastPrice'].values[0], K=put_df1['strike'].values[0] , type= OpionType.PUT)
call2 = Option(price=put_df1['lastPrice'].values[0], K=put_df1['strike'].values[0] , type= OpionType.PUT)
call2 = Option(price=put_df1['lastPrice'].values[0], K=put_df1['strike'].values[0] , type= OpionType.PUT)



stock = Stock(price = last_price)

obj = OptionStrategies('Butterfly Spread', St = currentprice)
strategy.add_Option(option= call ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_Option(option= call ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_Option(option= call ,buySell= BuySellSide.BUY, option_number=1 )

obj.plot(color='black', linewidth=2)
obj.describe()