from scipy.stats import norm
from Enum.OptionType import OpionType
import numpy as np
import matplotlib.pyplot as plt

N = norm.cdf
N_prime = norm.pdf

def d1(S, K, T, r, sigma) -> float:
    return (np.log(S/K) + (r + sigma**2/2)*T) /\
                     sigma*np.sqrt(T)


def d2(S, K, T, r, sigma) -> float:
    return d1(S, K, T, r, sigma) - sigma* np.sqrt(T)

def Delta( S, K , T , r , sigma, type:OpionType) -> float:
    if type == OpionType.CALL:
        return N(d1(S, K, T, r, sigma))
    elif type == OpionType.PUT:
        return - N(-d1(S, K, T, r, sigma))

def Gamma(S, K, T, r, sigma) -> float:
    N_prime = norm.pdf
    return N_prime(d1(S,K, T, r, sigma))/(S*sigma*np.sqrt(T))

def Vega(S, K, T, r, sigma) -> float:
    return S*np.sqrt(T)*N_prime(d1(S,K,T,r,sigma))

def Theta(S, K, T, r, sigma ,  type:OpionType) -> float:
    if type == OpionType.CALL:
        p1 = - S*N_prime(d1(S, K, T, r, sigma))*sigma / (2 * np.sqrt(T))
        p2 = r*K*np.exp(-r*T)*N(d2(S, K, T, r, sigma))
        return p1 - p2
    elif type == OpionType.PUT:
        p1 = - S * N_prime(d1(S, K, T, r, sigma)) * sigma / (2 * np.sqrt(T))
        p2 = r * K * np.exp(-r * T) * N(-d2(S, K, T, r, sigma))
        return p1 + p2

def Rho(S, K, T, r, sigma , type:OpionType) -> float:
    if type == OpionType.CALL:
        return K * T * np.exp(-r * T) * N(d2(S, K, T, r, sigma))
    elif type == OpionType.PUT:
        return -K * T * np.exp(-r * T) * N(-d2(S, K, T, r, sigma))


S = 100
K = 100
T = 1
r = 0.00
sigma = 0.25

prices = np.arange(1, 250,1)

deltas_c = Delta(prices, K, T, r, sigma , OpionType.CALL)