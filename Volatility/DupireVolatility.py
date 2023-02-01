from BlackAndScholes import BSPricing
import numpy as np


from scipy.stats import norm

N_prime = norm.pdf


def ComputeDupireVolatility(S , K , r , T , sigma , type , increment = 1.5):

    BSp = BSPricing.priceBS

    delta_T_finite = (BSp(S=S , K=K , r=r, T=(T + increment), type=type, sigma=sigma)  - BSp(S=S, K=K , r=r, T=T, type=type, sigma=sigma)) / (increment)

    delta_K_finite = (BSp(S=S , K=K  + increment, r=r, T=T, type=type, sigma=sigma) - BSp(S=S, K=K , r=r, T=T, type=type, sigma=sigma)) / (increment)

    delta_2K_finite = (BSp(S=S , K=K  + increment, r=r, T=T, type=type, sigma=sigma) - 2 * BSp(S=S, K=K , r=r, T=T, type=type, sigma=sigma)
                   + BSp(S=S , K= K  - increment, r=r, T=T, type=type, sigma=sigma)) / (increment)

    local_volatility = np.sqrt( (delta_T_finite + r * K  * delta_K_finite) / (0.5 * K  * K  * delta_2K_finite))

    return local_volatility



##Check

S=770.05
K = 850
sigma = 0.194722
T =0.07
increment = 1.5

r = 0.0066

localIV = ComputeDupireVolatility(S, K,r,T,sigma , 'CALL',increment)