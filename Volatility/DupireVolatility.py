import numpy as np
from pyblackscholes import black_scholes
import pyblp

def dupire_matrix(option_prices, spot, rf, div, expiries, strikes):
    """
    Calcule la matrice de volatilité implicite avec la méthode de Dupire
    à partir des prix des options.

    option_prices : numpy array
        un tableau numpy contenant les prix des options
    spot : float
        le prix actuel de l'actif sous-jacent
    rf : float
        le taux d'intérêt sans risque
    div : float
        le taux de dividende
    expiries : numpy array
        un tableau numpy contenant les échéances des options
    strikes : numpy array
        un tableau numpy contenant les strikes des options
    """
    n_strikes = len(strikes)
    n_expiries = len(expiries)
    impl_vols = np.zeros((n_expiries, n_strikes))
    for i in range(n_expiries):
        for j in range(n_strikes):
            t = expiries[i]
            k = strikes[j]
            # Calculer la volatilité implicite pour chaque option
            price = option_prices[i, j]
            call = 1
            try:
                impl_vol = black_scholes.implied_volatility(price, spot, k, t, rf, div, call)
                impl_vols[i, j] = impl_vol
            except Exception as e:
                pass
    # Construire la matrice de volatilité implicite
    mat_dupire = np.zeros((n_expiries, n_strikes))
    for i in range(n_expiries):
        for j in range(n_strikes):
            t = expiries[i]
            k = strikes[j]
            mat_dupire[i, j] = (2 * rf) / (k ** 2 * t) * impl_vols[i, j]
    return mat_dupire