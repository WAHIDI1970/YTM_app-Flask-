import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import numpy as np
from .interpolation import interpolate_rate # Use relative import

def create_yield_curve_chart(df):
    """Generates the HTML for the interpolated yield curve chart."""
    if df is None or len(df) < 2:
        return None
        
    mats = pd.Series(np.linspace(df["maturite_annees"].min(), df["maturite_annees"].max(), 150))
    zc_interp = interpolate_rate(df["maturite_annees"], df["Taux_zero_coupon"], mats)
    act_interp = interpolate_rate(df["maturite_annees"], df["Taux_actuariel"], mats)
    
    fig = go.Figure()
    # ZC Curve
    fig.add_trace(go.Scatter(x=df["maturite_annees"], y=df["Taux_zero_coupon"] * 100, mode='markers', name='Taux ZC (Données)', marker=dict(size=8, color='#a78bfa')))
    fig.add_trace(go.Scatter(x=mats, y=zc_interp * 100, mode='lines', name='Courbe ZC Interpolée', line=dict(dash='solid', color='#6d28d9', width=3)))
    # Actuarial Curve
    fig.add_trace(go.Scatter(x=df["maturite_annees"], y=df["Taux_actuariel"] * 100, mode='markers', name='Taux Actuariel (Données)', marker=dict(size=8, symbol='diamond', color='#fca5a5')))
    fig.add_trace(go.Scatter(x=mats, y=act_interp * 100, mode='lines', name='Courbe Actuarielle Interpolée', line=dict(dash='dot', color='#dc2626', width=2)))
    
    fig.update_layout(
        title=dict(text="<b>Courbe des Taux Zéro-Coupon et Actuariels</b>", font=dict(size=20), x=0.5),
        xaxis_title="Maturité (années)",
        yaxis_title="Taux (%)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#4b5563")
    )
    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def create_forward_curve_chart(mats_end, forwards):
    """Generates the HTML for the forward curve chart."""
    if mats_end is None or forwards is None:
        return None

    fig = go.Figure(go.Scatter(
        x=mats_end, 
        y=forwards * 100, 
        mode='lines', 
        name='Taux Forward (%)', 
        line_shape='hv', 
        line=dict(color='#059669', width=3)
    ))
    fig.update_layout(
        title=dict(text="<b>Courbe des Taux Forwards</b>", font=dict(size=20), x=0.5),
        xaxis_title="Maturité (années)",
        yaxis_title="Taux Forward (%)",
        template="plotly_white",
        margin=dict(l=40, r=40, t=80, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#4b5563")
    )
    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
