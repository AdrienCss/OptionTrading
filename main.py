from Volatility import ImpliedVolatiliy
from Option.OptionStrategies import OptionStrategies
from Option.Option import Option , Stock
from Enum.OptionType import OpionType
from Enum.BuySellSide import BuySellSide


#Underlying pricen quote
currentprice = 20
r=0.01
vol = 0.05
T =1

callOption = Option(price= 3 , K=15 , type= OpionType.CALL)
callOption2 = Option(price= 1 , K=25 , type= OpionType.CALL)
#stock = Stock(price = currentprice)

strategy = OptionStrategies(name = "Bear Spread" ,St = currentprice)

strategy.add_Option(option = callOption ,buySell = BuySellSide.BUY , option_number=1 )
strategy.add_Option(option = callOption2 ,buySell = BuySellSide.SELL , option_number=1 )

strategy.compute_greek_profile(T ,r , vol)

strategy.plot()
strategy.plotGreek(greekStr='gamma')
strategy.plotGreek(greekStr='theta')
strategy.plotGreek(greekStr='delta')
strategy.plotGreek(greekStr='vega')
