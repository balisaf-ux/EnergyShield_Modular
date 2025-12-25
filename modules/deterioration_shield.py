import streamlit as st
import plotly.figure_factory as ff
import numpy as np
from assets.helpers import simulate_covenant_breach

def render_deterioration_shield():
    st.title("Deterioration Shield (Contingent Surety)")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">LIQUIDITY SHOCK & COVENANT PROTECTION</h4>', unsafe_allow_html=True)

    # --- INPUTS ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Covenant Parameters")
        current_ratio = st.number_input("Current Net Debt / EBITDA", value=2.5, step=0.1)
        threshold_ratio = st.number_input("Breach Threshold (Trigger)", value=4.0, step=0.1)
        volatility = st.slider("EBITDA Volatility (Simulated)", 0.1, 1.0, 0.4)
    
    with c2:
        st.subheader("Surety Bond Sizing")
        ppa_revenue_monthly = st.number_input("Monthly PPA Revenue (R)", value=2500000.0)
        coverage_months = st.selectbox("Coverage Duration", [3, 6, 9, 12], index=1)
        liability_cap = ppa_revenue_monthly * coverage_months
        
        # Run Simulation
        prob_breach, dist_data = simulate_covenant_breach(current_ratio, threshold_ratio, volatility)
        
        # Pricing Logic
        base_rate = 0.02 # 2% base
        risk_loading = (prob_breach / 100) * 0.15 # 15% loading based on prob
        final_rate = base_rate + risk_loading
        annual_premium = liability_cap * final_rate

    # --- METRICS ---
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Probability of Breach (12m)", f"{prob_breach:.1f}%", delta="Risk Factor")
    m2.metric("Max Liability Cap (LC Amount)", f"R {liability_cap:,.0f}")
    m3.metric("Annual Surety Premium", f"R {annual_premium:,.0f}", delta=f"Rate: {final_rate*100:.2f}%")

    # --- VISUALIZATION: PROBABILITY CURVE ---
    st.subheader("Probability of Covenant Breach")
    
    # Create Distplot
    fig = ff.create_distplot([dist_data], ['Projected EBITDA Ratio'], bin_size=0.1, show_hist=False, show_rug=False, colors=['#00BFFF'])
    
    # Add Threshold Line
    fig.add_vline(x=threshold_ratio, line_dash="dash", line_color="#FF4500", annotation_text="Breach Threshold")
    
    # Shade the Breach Area
    fig.update_layout(
        title="12-Month Covenant Forecast Distribution",
        xaxis_title="Net Debt / EBITDA Ratio",
        yaxis_title="Probability Density",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
