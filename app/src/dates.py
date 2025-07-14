from datetime import datetime, date
import pandas as pd
import numpy as np
from dateutil import parser

def parse_date_flexible(date_str):
    """
    Tente de parser une date dans un format souple, en considérant le jour en premier.
    Retourne un objet Timestamp ou pd.NaT si erreur.
    """
    try:
        return pd.to_datetime(parser.parse(str(date_str), dayfirst=True))
    except Exception:
        return pd.NaT


def get_base_date(df, col_name="Echeance") -> date:
    """
    Récupère la date de base (date de valorisation) en analysant la colonne des échéances.
    Utilise la date valide la plus ancienne trouvée. Si aucune date valide, retourne date.today().
    """
    dates_parsed = df[col_name].apply(parse_date_flexible).dropna()
    if not dates_parsed.empty:
        return dates_parsed.min().date()
    else:
        return date.today()


def calc_maturite(date_str: str, date_base: date) -> float:
    """
    Calcule la maturité en jours entre une date d’échéance et la date de base.
    Remplace les maturités nulles ou négatives par 1 jour (pour éviter les divisions par zéro).
    """
    try:
        d = parse_date_flexible(date_str)
        if pd.isna(d):
            return np.nan
        delta_days = (d.date() - date_base).days
        return max(delta_days, 1)  # 👈 correction ici : minimum 1 jour
    except Exception:
        return np.nan
