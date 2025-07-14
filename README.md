# 📈 Yield Curve Analyzer – BAM Curve Dashboard

Ce projet est un **dashboard interactif** pour l'analyse et le calcul des **taux actuariels**, **taux zéro coupon**, et **taux forward** à partir des courbes de taux publiées par la **Banque Al-Maghrib (BAM)**. Il est conçu pour les analystes financiers, ingénieurs quantitatifs, chercheurs ou toute personne intéressée par la modélisation des courbes de taux.

## 🧰 Fonctionnalités principales

- 📥 Importation de courbes BAM au format CSV
- 📊 Visualisation interactive des courbes (Plotly)
- 🧮 Calcul des taux actuariels
- 🪙 Bootstrap des taux zéro coupon
- ⏩ Calcul des taux forwards pour différentes maturités
- 🧩 Interpolation personnalisée d’échéance
- 🧑‍💻 Interface web professionnelle (Flask)
- 🐳 Dockerisation pour déploiement simple

## 📂 Structure du projet

```bash
yield-curve-analyzer/
│
├── app.py                     # Point d'entrée principal (Flask ou Streamlit)
├── requirements.txt           # Dépendances Python
├── Dockerfile                 # Image Docker (si utilisé)
├── README.md                  # Fichier de documentation
├── static/                    # Fichiers CSS, JS, images
├── templates/                 # Layout HTML (Flask)
│
├── data/                      # Données d’entrée (CSV BAM)
├── output/                    # Résultats calculés/exportés
│
└── app/src/                       # Modules Python
       ├── io_bam.py              # Importation et nettoyage des données BAM
       ├── dates.py               # Gestion des échéances et maturités
       ├── bootstrap.py           # Calcul des taux actuariels et ZC
       ├── interpolation.py       # Interpolation spline/linéaire
       └── forward.py             # Calculs des taux forwards
```

## 📈 Exemple de visualisation :
Voici un aperçu du dashboard :

<img width="959" height="437" alt="image" src="https://github.com/user-attachments/assets/dfc1ab4c-178d-413e-b24e-6e251804a27c" />
<img width="954" height="353" alt="image" src="https://github.com/user-attachments/assets/4e2d3dd8-3087-4332-8c97-f28f357fdcef" />
<img width="959" height="437" alt="image" src="https://github.com/user-attachments/assets/3862a5ba-90cf-4e23-9639-9f1b212f5bbb" />
<img width="953" height="161" alt="image" src="https://github.com/user-attachments/assets/09c57783-2b94-445f-97e0-541e18f1f9cf" />



