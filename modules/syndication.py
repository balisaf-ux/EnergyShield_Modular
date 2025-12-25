import streamlit as st
import pandas as pd
import plotly.express as px

def render_syndication_placement():
    st.title("Syndication & Placement")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">PROJECT FINANCING & RISK TRANSFER</h4>', unsafe_allow_html=True)
    
    tab_struct, tab_risk_radar, tab_place = st.tabs(["1. Deal Structuring", "2. Risk Profile Radar", "3. Placement Feasibility"])
    
    with tab_struct:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Capital Stack")
            debt_ratio = st.slider("Debt Tranche (%)", 0, 100, 70)
            equity_ratio = 100 - debt_ratio
            st.progress(debt_ratio)
            st.caption(f"Debt: {debt_ratio}% | Equity: {equity_ratio}%")
            
        with c2:
            st.subheader("Financial Covenants")
            dscr = st.number_input("Project DSCR (Debt Service Coverage Ratio)", value=1.35, step=0.05)
            irr = st.number_input("Equity IRR (%)", value=18.5, step=0.5)
            
    with tab_risk_radar:
        st.subheader("Syndication Risk Factor Radar Chart")
        
        # Mock Data for Radar - In production, this pulls from Session State modules
        risk_data = pd.DataFrame(dict(
            r=[80, 75, 90, 65, 85],
            theta=['Counterparty Risk', 'Technical Risk', 'Market Price Risk', 'Regulatory Risk', 'Env/Social Risk']
        ))
        
        fig_radar = px.line_polar(risk_data, r='r', theta='theta', line_close=True)
        fig_radar.update_traces(fill='toself', line_color='#FFD700', fillcolor='rgba(255, 215, 0, 0.3)')
        fig_radar.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
                bgcolor='#1A1C24'
            ),
            title="Project Risk Profile (Higher = Lower Risk)"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with tab_place:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("Risk Mitigation Checklist")
            # Automated checks
            st.checkbox("Grid Uptime Shield (Volume Risk)", value=True, disabled=True)
            st.checkbox("Price Spike Shield (Cost Risk)", value=True, disabled=True)
            st.checkbox("Carbon Shield (Tax Risk)", value=True, disabled=True)
            st.checkbox("Curtailment Shield (Revenue Risk)", value=False, disabled=True)
            
        with c2:
            st.subheader("Placement Feasibility")
            # Logic: Score based on DSCR and Risk Checks
            feasibility_score = 0
            if dscr >= 1.25: feasibility_score += 40
            if dscr >= 1.4: feasibility_score += 20
            if debt_ratio <= 75: feasibility_score += 20
            feasibility_score += 10 # Base
            
            score_color = "red"
            if feasibility_score > 50: score_color = "yellow"
            if feasibility_score > 75: score_color = "#00BFFF" # Titan Blue
            
            st.markdown(f"<h1 style='color: {score_color}; text-align: center; font-size: 80px;'>{feasibility_score}/100</h1>", unsafe_allow_html=True)
            if feasibility_score > 75:
                st.success("✅ HIGH BANKABILITY: Ready for Tier 1 Syndication.")
            else:
                st.warning("⚠️ OPTIMIZATION REQUIRED: Improve DSCR or lower Debt Ratio.")
