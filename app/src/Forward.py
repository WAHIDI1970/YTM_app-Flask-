import numpy as np

def taux_forward(maturites, taux_zc):
    """
    Calcule les taux forwards implicites entre les maturités données.

    Parameters
    ----------
    maturites : array-like
        Tableau des maturités (en années), supposées triées en ordre croissant.
    taux_zc : array-like
        Tableau des taux zéro-coupon correspondants aux maturités.

    Returns
    -------
    mats_start : np.ndarray
        Tableau des maturités de début des intervalles forward.
    mats_end : np.ndarray
        Tableau des maturités de fin des intervalles forward.
    forwards : np.ndarray
        Taux forward implicites sur chaque intervalle.
    """
    maturites = np.asarray(maturites, dtype=float)
    taux_zc = np.asarray(taux_zc, dtype=float)

    # Calcul des différences de maturité pour éviter division par zéro
    diff = maturites[1:] - maturites[:-1]
    valid = diff > 1e-6  # Seuil pour éviter les doublons ou valeurs trop proches

    if not np.any(valid):
        return np.array([]), np.array([]), np.array([])

    mats_start = maturites[:-1][valid]
    mats_end = maturites[1:][valid]
    zc_start = taux_zc[:-1][valid]
    zc_end = taux_zc[1:][valid]

    forwards = (zc_end * mats_end - zc_start * mats_start) / (mats_end - mats_start)
    return mats_start, mats_end, forwards
