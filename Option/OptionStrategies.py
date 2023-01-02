import numpy as np
from Option.Option import  Option ,Stock
import matplotlib.pyplot as plt
from Enum.BuySellSide import BuySellSide
from Enum.OptionType import OpionType
from BlackAndScholes import Greeks
from typing import Union

class OptionStrategies:
    """
        the purpose of this class is to implement option trading strategies on one and the same underlying
    """
    def __init__(self, name, St):
        self.name = name
        self.St = St
        self.STs = np.arange(1, St * 2, 1)
        self.payoffs = np.zeros_like(self.STs)
        self.instruments = []
        self.side = []

        self.gamma=np.zeros_like(self.STs)
        self.delta=np.zeros_like(self.STs)
        self.theta=np.zeros_like(self.STs)
        self.vega=np.zeros_like(self.STs)


    def add_Option(self ,  option : Option , buySell:BuySellSide ,  option_number = 1) -> None:

        for nb in range(1 , option_number+1):
            self.instruments.append(option)
            self.side.append(buySell.value)

        self.payoffs = self.payoffs  + self._payoff(option,buySell,option_number)

        print(f"{str(option_number)} option(s) added ")

    def add_deltaOne(self, stock:Stock, buySell:BuySellSide, stock_number=1) -> None:

        for nb in range(1 , stock_number+1):
            self.instruments.append(stock) ## add later stockPrice

        self.payoffs = self.payoffs  + self._payoff(stock,buySell,stock_number)

        print(f"{str(stock_number)} option(s) added ")

    def _payoff(self , instr :Union[Option , Stock]  , side:BuySellSide , number):

        payoff= None
        if(type(instr) == Option):
            option = instr
            K = option.K
            if side == BuySellSide.BUY:
                if option.type ==OpionType.CALL:
                    payoff = np.array([max(S - K, 0) - option.price for S in self.STs]) * number
                elif option.type == OpionType.PUT:
                    payoff = np.array([max(K - S, 0) - option.price for S in self.STs]) * number

            elif side == BuySellSide.SELL:
                if option.type == OpionType.CALL:
                    payoff = np.array([- (max(S - K, 0) - option.price )for S in self.STs]) * number
                elif option.type == OpionType.PUT:
                    payoff = np.array([-(max(K - S, 0) - option.price )for S in self.STs]) * number

        elif (type(instr) == Stock):
            stock = instr
            if side == BuySellSide.BUY:
                payoff = np.array([S - stock.price for S in self.STs]) * number
            elif side == BuySellSide.SELL:
                payoff = np.array([ stock.price -S for S in self.STs]) * number
        return payoff

    def plot(self, **params):
        plt.plot(self.STs, self.payoffs, **params)
        plt.title(f"Payoff Diagram for {self.name}")
        plt.fill_between(self.STs, self.payoffs,where=(self.payoffs > 0), facecolor='g', alpha=0.4)
        plt.fill_between(self.STs, self.payoffs,where=(self.payoffs < 0), facecolor='r', alpha=0.4)

        plt.xlabel(r'$S_T$')
        plt.ylabel('Profit in $')
        plt.show()

    def describe(self):
        max_profit = self.payoffs.max()
        max_loss = self.payoffs.min()
        print(f"Max Profit: ${round(max_profit, 3)}")
        print(f"Max loss: ${round(max_loss, 3)}")
        c = 0
        for o in self.instruments:
            print(o)
            if o.type == 'call' and o.side == 1:
                c += o.price
            elif o.type == 'call' and o.side == -1:
                c -= o.price
            elif o.type == 'put' and o.side == 1:
                c += o.price
            elif o.type == 'put' and o.side == -1:
                c - + o.price

        print(f"Cost of entering position ${c}")

    def compute_greek_profile(self , T, r, sigma ):

        instr_side =list(zip(self.side,self.instruments))

        for side , instr in instr_side:
            self.delta =self.delta + side * Greeks.Delta(self.STs ,instr.K ,T , r , sigma ,  instr.type)
            self.gamma = self.gamma + side * Greeks.Gamma(self.STs ,instr.K ,T , r , sigma)
            self.vega = self.vega + side * Greeks.Vega(self.STs ,instr.K ,T , r , sigma )
            self.theta = self.theta + side * Greeks.Theta(self.STs ,instr.K ,T , r , sigma ,  instr.type)

    def plotGreek(self,greekStr,  **params):
        greek= getattr(self, greekStr)
        plt.plot(self.STs, greek, **params)
        plt.title(f"{greekStr} Profile")
        plt.xlabel(r'$S_T$')
        plt.show()