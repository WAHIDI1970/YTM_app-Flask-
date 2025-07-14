import numpy as np
import pandas as pd

def taux_actuariel(T: float, t: float) -> float:
    """
    Calcule le taux actuariel à partir du taux moyen pondéré et de la maturité T (en années).
    Pour T < 1 an, utilise la capitalisation composée adaptée.
    """
    if T <= 0:
        raise ValueError("La maturité T doit être strictement positive.")
    if T < 1.0:
        n = 1 / T
        return (1 + t / n) ** n - 1
    return t


def bootstrap_zc(df: pd.DataFrame) -> pd.Series:
    """
    Calcule les taux zéro-coupon par bootstrap à partir d'un DataFrame contenant :
      - 'maturite_en_ans' : maturité en années (doit être > 0)
      - 'Taux_decimal' : taux moyen pondéré en décimal (ex : 0.025 pour 2.5%)
    
    Retourne une Series de taux zéro-coupon.
    """
    zc_dict = {}
    zc_list = []

    for idx, row in df.iterrows():
        T = row["maturite_annees"]
        if T <= 0:
            raise ValueError(f"Maturité non valide (≤ 0) détectée à l'index {idx} : {T}")
        
        r = taux_actuariel(T, row["Taux_decimal"])
        C = r  # coupon annuel supposé égal au taux actuariel
        
        if T <= 1:
            # Cas échéance courte, taux ZC égal taux actuariel
            zc = r
        else:
            # Somme actualisée des coupons précédents
            s = 0.0
            for k in range(1, int(np.floor(T)) + 1):
                prev_zc = zc_dict.get(k)
                if prev_zc is None:
                    # Si pas encore calculé, fallback au taux actuariel
                    prev_zc = r
                s += C / (1 + prev_zc) ** k

            denom = 1 - s
            if denom <= 0:
                # Protection contre division par zéro ou négative
                zc = r
            else:
                zc = ((1 + C) / denom) ** (1 / T) - 1

        zc_dict[int(round(T))] = zc
        zc_list.append(zc)

    return pd.Series(zc_list, index=df.index)
