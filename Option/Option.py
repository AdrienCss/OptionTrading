from Enum import OptionType

class Option:
    def __init__(self, type : OptionType, K, price):
        self.type = type
        self.K = K
        self.price = price

class Stock:
    def __init__(self , price ):
        self.price= price