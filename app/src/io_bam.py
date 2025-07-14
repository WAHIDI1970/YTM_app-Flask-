import requests
import pandas as pd
from io import StringIO

def read_bam_csv_safely(csv_data: str) -> pd.DataFrame:
    """
    Lecture robuste d'un CSV de BAM en sautant les lignes d'en-tête et de pied de page,
    et en utilisant le point-virgule comme séparateur.
    """
    # Nettoyage des retours à la ligne pour plus de robustesse
    csv_data = csv_data.replace('\r\n', '\n').replace('\r', '\n').strip()

    # Lecture du CSV en sautant les 2 premières lignes et la dernière ligne (Total)
    # Le séparateur est probablement un point-virgule (';') lors de l'export depuis Excel (Fr)
    df = pd.read_csv(
        StringIO(csv_data),
        sep=";", 
        encoding="utf-8",
        skiprows=2,  # Correction: Saute les deux premières lignes
        skipfooter=1, # Correction: Saute la dernière ligne ('Total')
        engine='python', # Moteur nécessaire pour utiliser skipfooter
    )

    # Renommer les colonnes pour correspondre à ce que le script principal attend
    df.rename(columns={
        "Date d'échéance": "Echeance",
        "Taux moyen": "Taux moyen pondéré" # Le nom de colonne a changé dans le nouveau fichier
    }, inplace=True)

    # Vérification que les colonnes requises existent
    required_cols = ["Echeance", "Taux moyen pondéré"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Colonnes requises ('Echeance', 'Taux moyen pondéré') non trouvées. Colonnes : {df.columns.tolist()}")

    df = df.dropna(subset=required_cols)

    return df

def import_bam_curve(date_obj) -> pd.DataFrame:
    """
    Télécharge et nettoie la courbe des taux BAM pour une date donnée.
    """
    # Le format de date attendu par l'URL est souvent jj/mm/aaaa
    date_str = date_obj.strftime("%d/%m/%Y")
    encoded_date = date_str.replace("/", "%2F")
    url = (
        "https://www.bkam.ma/export/blockcsv/2340/"
        "c3367fcefc5f524397748201aee5dab8/"
        "e1d6b9bbf87f86f8ba53e8518e882982"
        f"?date={encoded_date}&block=e1d6b9bbf87f86f8ba53e8518e882982"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        csv_data = response.content.decode("utf-8")
        
        if not csv_data or "aucun" in csv_data.lower():
             raise ValueError(f"Aucune donnée disponible pour la date {date_str}.")

        return read_bam_csv_safely(csv_data)
    
    except requests.HTTPError as e:
        raise ValueError(f"Erreur réseau lors de l'import depuis BAM (code: {e.response.status_code}). Il n'y a peut-être pas de données pour cette date.")
    except Exception as e:
        raise ValueError(f"Une erreur est survenue lors du traitement des données BAM : {e}")