from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import os
import io
from datetime import date

from app.src.dates import get_base_date, calc_maturite
from app.src.io_bam import import_bam_curve
from app.src.bootstrap import taux_actuariel, bootstrap_zc
from app.src.Forward import taux_forward
from app.src.interpolation import interpolate_rate

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "une-cle-secrete-pour-le-developpement")

PICKLE_FILE = 'tmp_df.pkl'

@app.route('/', methods=['GET', 'POST'])
def index():
    df, df_fw = None, None
    error = None
    interpolated_rate = None
    interpolated_target = None
    interpolated_maturity = None
    kpi_stats = {}
    chart_data = {}

    def perform_calculations(df_input):
        df_input.rename(columns={
            "Date échéance": "Echeance", "Date d'échéance": "Echeance",
            "Taux moyen": "Taux moyen pondéré"
        }, inplace=True, errors='ignore')

        if "Echeance" not in df_input.columns or "Taux moyen pondéré" not in df_input.columns:
            raise ValueError("Colonnes 'Echeance' et/ou 'Taux moyen pondéré' introuvables.")

        date_base = get_base_date(df_input, col_name="Echeance")
        df_input["maturite_jours"] = df_input["Echeance"].apply(lambda s: calc_maturite(s, date_base))
        df_input.dropna(subset=["maturite_jours"], inplace=True)
        df_input["maturite_annees"] = df_input["maturite_jours"].astype(float) / 365.25
        df_input["Taux_decimal"] = df_input["Taux moyen pondéré"].astype(str).str.replace('%', '').str.replace(',', '.').astype(float) / 100
        df_input.sort_values(by="maturite_annees", inplace=True)
        df_input["Taux_actuariel"] = df_input.apply(lambda r: taux_actuariel(r["maturite_annees"], r["Taux_decimal"]), axis=1)
        df_input["Taux_zero_coupon"] = bootstrap_zc(df_input)
        return df_input

    if request.method == 'GET' and not session.get('has_data'):
        try:
            today_str = date.today().isoformat()
            df = import_bam_curve(date.today())
            df = perform_calculations(df)
            df.to_pickle(PICKLE_FILE)
            session['has_data'] = True
            session['last_mode'] = 'bam'
            session['last_date'] = today_str
        except Exception as e:
            error = f"Erreur lors du chargement automatique des données BAM : {e}"
            session.clear()

    if session.get('has_data') and os.path.exists(PICKLE_FILE):
        try:
            df = pd.read_pickle(PICKLE_FILE)
        except (FileNotFoundError, EOFError):
            session.clear()
            error = "Erreur de chargement des données de session. Veuillez recharger les données."

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'reset':
            session.clear()
            if os.path.exists(PICKLE_FILE):
                os.remove(PICKLE_FILE)
            return redirect(url_for('index'))

        elif action == 'calculate_curves':
            mode = request.form.get('mode')
            raw_df = None
            try:
                if mode == "bam":
                    date_str = request.form.get("date_bam")
                    date_pub = pd.to_datetime(date_str).date() if date_str else date.today()
                    raw_df = import_bam_curve(date_pub)
                    session['last_mode'] = 'bam'
                    session['last_date'] = date_str
                elif mode == "upload":
                    file = request.files.get('csv')
                    if file and file.filename:
                        csv_data = io.StringIO(file.stream.read().decode("UTF-8"))
                        raw_df = pd.read_csv(csv_data, sep=';', skiprows=2, skipfooter=1, engine='python', dtype=str)
                        session['last_mode'] = 'upload'
                        session['last_filename'] = file.filename
                    else:
                        error = "Aucun fichier CSV sélectionné."

                if raw_df is not None:
                    df = perform_calculations(raw_df)
                    df.to_pickle(PICKLE_FILE)
                    session['has_data'] = True
                elif not error:
                    error = "Aucune donnée n'a été importée."
            except Exception as e:
                error = f"Erreur lors du calcul des taux : {e}"
                session.clear()

        elif action == 'calculate_forwards':
            if df is not None and 'Taux_zero_coupon' in df.columns:
                if len(df) > 1:
                    mats = df["maturite_annees"].to_numpy()
                    zc = df["Taux_zero_coupon"].to_numpy()
                    mats_start, mats_end, forwards = taux_forward(mats, zc)
                    df_fw = pd.DataFrame({
                        "De (années)": [f"{x:.2f}" for x in mats_start],
                        "À (années)": [f"{x:.2f}" for x in mats_end],
                        "Taux Forward (%)": [f"{x*100:.2f}" for x in forwards]
                    })
                else:
                    error = "Données insuffisantes pour calculer les taux forwards."
            else:
                error = "Veuillez d'abord importer et calculer les courbes de base."

        elif action == 'interpolate_date':
            date_str = request.form.get("target_date")
            if df is not None and 'Taux_zero_coupon' in df.columns and date_str:
                try:
                    date_cible = pd.to_datetime(date_str).date()
                    base_date = get_base_date(df)
                    jours = calc_maturite(date_cible.isoformat(), base_date)
                    maturity = jours / 365.25
                    mats = df["maturite_annees"].to_numpy()
                    zc = df["Taux_zero_coupon"].to_numpy()
                    interpolated = interpolate_rate(mats, zc, maturity)
                    interpolated_rate = f"{interpolated * 100:.4f}"
                    interpolated_target = date_cible.strftime("%d/%m/%Y")
                    interpolated_maturity = f"{maturity:.2f}"
                except Exception as e:
                    error = f"Erreur lors de l'interpolation : {e}"
            else:
                error = "Date invalide ou données manquantes pour l’interpolation."

    df_display = None
    if df is not None:
        df_display = df.copy()
        for col in ['Taux_decimal', 'Taux_actuariel', 'Taux_zero_coupon']:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"{x*100:.4f}%")
        if 'maturite_annees' in df_display.columns:
            df_display['maturite_annees'] = df_display['maturite_annees'].apply(lambda x: f"{x:.2f}")

        if not df.empty:
            kpi_stats = {
                'nb_echeances': len(df),
                'taux_zc_max': f"{df['Taux_zero_coupon'].max()*100:.2f}%",
                'maturite_max': f"{df['maturite_annees'].max():.2f} ans"
            }

            chart_data["yield_curve"] = {
                "labels": df["maturite_annees"].round(2).tolist(),
                "actuarial_rates": (df["Taux_actuariel"] * 100).round(2).tolist(),
                "zc_rates": (df["Taux_zero_coupon"] * 100).round(2).tolist()
            }

    if df_fw is not None and not df_fw.empty:
        chart_data["forward_curve"] = {
            "labels": df_fw["À (années)"].tolist(),
            "rates": [float(val.replace(",", ".")) for val in df_fw["Taux Forward (%)"]]
        }

    return render_template(
        "dashboard.html",
        df_table=df_display.to_html(classes='table', index=False) if df_display is not None else None,
        df_fw_table=df_fw.to_html(classes='table', index=False) if df_fw is not None else None,
        error=error,
        has_data=session.get('has_data', False),
        last_date=session.get('last_date', date.today().isoformat()),
        interpolated_rate=interpolated_rate,
        interpolated_target=interpolated_target,
        interpolated_maturity=interpolated_maturity,
        kpi_stats=kpi_stats,
        chart_data=chart_data
    )
if __name__ == '__main__':
    app.run(debug=True)