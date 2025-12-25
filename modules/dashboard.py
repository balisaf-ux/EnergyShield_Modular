import streamlit as st
import plotly.graph_objects as go
from assets.helpers import mock_get_market_data, mock_get_grid_risk, mock_get_vix

def render_dashboard():
    st.title("SAWEM RISK TERMINAL")
    st.markdown(f'<h3 style="color: var(--color-alert-urgent)">MARKET STATUS: VOLATILE</h3>', unsafe_allow_html=True)
    
    # KPI Row
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.markdown(f'<div class="indicator-card"><p class="indicator-label">AVG SPOT PRICE</p><p class="indicator-value titan-gold">{mock_get_market_data()}</p></div>', unsafe_allow_html=True)
    with c2: 
        st.markdown(f'<div class="indicator-card grid-risk-card"><p class="indicator-label" style="color:red">GRID RISK</p><p class="indicator-value" style="color:red">{mock_get_grid_risk()}</p></div>', unsafe_allow_html=True)
    with c3: 
        st.markdown(f'<div class="indicator-card"><p class="indicator-label">VIX</p><p class="indicator-value titan-blue">{mock_get_vix()}</p></div>', unsafe_allow_html=True)
    
    # REX-QF Telemetry (If calculated)
    if st.session_state.get('rex_qf_data'):
        api_data = st.session_state['rex_qf_data']
        st.markdown("---")
        st.subheader("REX-QF Live Risk Telemetry")
        k1, k2, k3 = st.columns(3)
        k1.metric("Current ES Score", f"{api_data['es_score']:.1f} / 100")
        k2.metric("S-AEL (Tail Risk)", f"R {api_data['s_ael_tail']:,.0f}")
        k3.metric("FL-Downtime", f"R {api_data['fl_downtime']:,.0f}")
    else:
        st.markdown("---")
        st.info("System Standby: Run REX-QF Calculation in 'Default Shield' to populate telemetry.")
