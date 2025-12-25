import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_variance_swap():
    st.title("Variance Swap: Volatility Risk Pricing")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">MARKET VOLATILITY HEDGE ASSET</h4>', unsafe_allow_html=True)
    
    # --- INPUTS ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Contract Parameters")
        notional_vega = st.number_input("Notional Vega (ZAR/Vol Point)", value=50000.0, step=1000.0)
        tenor = st.slider("Contract Tenor (Years)", 1, 5, 3)
        
        st.markdown("---")
        st.subheader("Market Inputs (M-Data)")
        hist_vol = st.number_input("Historical Volatility (σ %)", value=18.5, step=0.1)
        risk_free_rate = st.number_input("Risk-Free Rate (JIBAR %)", value=8.25, step=0.05)
        
    with c2:
        st.subheader("Pricing & Outputs")
        # Logic: Fair Strike = Historic Vol + Volatility Risk Premium (VRP)
        vrp = 2.5 # Assumed Market VRP
        fair_strike_vol = hist_vol + vrp
        
        k1, k2 = st.columns(2)
        k1.metric("Fair Strike Volatility", f"{fair_strike_vol:.2f}%", delta=f"+{vrp}% VRP")
        k2.metric("Total Contract Value", f"R {(notional_vega * fair_strike_vol):,.0f}")
        
        st.info("Pricing Model: Replicating Portfolio (Log Contract) Proxy")

    st.markdown("---")
    st.subheader("Implied vs. Realized Volatility Spread")
    
    # --- VISUALIZATION LOGIC ---
    # Mock Data for Scatter Plot generation
    dates_scat = pd.date_range(start="2023-01-01", periods=24, freq='M')
    implied_v = np.random.normal(20, 2, 24)
    realized_v = implied_v + np.random.normal(0, 3, 24) # Realized matches implied with noise
    
    df_vol = pd.DataFrame({'Date': dates_scat, 'Implied Vol': implied_v, 'Realized Vol': realized_v})
    
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(x=df_vol['Date'], y=df_vol['Implied Vol'], mode='markers', name='Implied Vol (Market)', marker=dict(color='#00BFFF', size=10)))
    fig_vol.add_trace(go.Scatter(x=df_vol['Date'], y=df_vol['Realized Vol'], mode='markers', name='Realized Vol (Actual)', marker=dict(color='#FFD700', size=10, symbol='x')))
    
    # Add Strike Line
    fig_vol.add_hline(y=fair_strike_vol, line_dash="dash", line_color="white", annotation_text=f"Proposed Strike: {fair_strike_vol}%")
    
    fig_vol.update_layout(title="Volatility Regime Analysis", xaxis_title="Date", yaxis_title="Volatility (%)", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_vol, use_container_width=True)
