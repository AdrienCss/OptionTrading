import numpy as np
from scipy.stats import norm
import Option.Option as Option
N = norm.cdf


def BS_CALL(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * N(d1) - K * np.exp(-r*T)* N(d2)


def BS_PUT(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma* np.sqrt(T)
    return K* np.exp(-r*T) * N(-d2) - S*N(-d1)


def priceBS(S, K, T, r, sigma ,type='CALL'):
    if type == 'CALL':
        return BS_CALL(S, K, T, r, sigma)
    if type == 'PUT':
        return BS_PUT(S, K, T, r, sigma)
    else:
        raise ValueError('Unrecognized type')
