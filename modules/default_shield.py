import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from engine.rex_qf import REX_QF_Engine

# Initialize Engine Instance
rex_engine = REX_QF_Engine()

def render_default_shield():
    st.title("Risk Engine (Default Shield)")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">REX-QF CALCULATION ENGINE (API V1.0)</h4>', unsafe_allow_html=True)
    st.info("INSTRUCTION: Configure inputs below and run the calculation. Results will map to all other modules.")
    
    api_data = st.session_state.get('rex_qf_data')
    
    tab_inputs, tab_complexity, tab_results = st.tabs(["1. Financials & Reliability", "2. Complexity Factors", "3. REX-QF OUTPUT"])
    
    with tab_inputs:
        c1, c2 = st.columns(2)
        total_rev = c1.number_input("Total Annual Revenue (ZAR)", value=100000000.0)
        ael_total = c2.number_input("Agreed Exposure Limit (AEL Total)", value=50000000.0)
        tc_risk = st.slider("Technical Compliance Score (TCRisk %)", 0, 100, 85)
        st.subheader("Reliability (FL-Downtime Input)")
        fail_prob = st.slider("Backup Failure Prob (Derived from Lookup)", 0.0, 1.0, 0.15)
        fl_downtime = st.number_input("Financial Loss - Downtime (R/Year)", value=5000000.0)

    with tab_complexity:
        c1, c2 = st.columns(2)
        is_multi_site = c1.checkbox("Multi-site Operations", value=True)
        uptime_req = c2.selectbox("Required Uptime Tier", ["Standard", "High", "Critical"])
        comp_score = 0.4 
        if is_multi_site: comp_score += 0.3
        st.metric("Complexity Factor", f"{comp_score:.2f}")

    with tab_results:
        if st.button("RUN REX-QF API CALCULATION", use_container_width=True):
            rev_ratio = total_rev / ael_total if ael_total > 0 else 0
            score = rex_engine.calculate_score(rev_ratio, tc_risk, comp_score)
            ls_sigma = 0.45 
            dist, s_ael = rex_engine.run_monte_carlo(ls_sigma)
            
            # Save to Global Session State
            st.session_state['rex_qf_data'] = {
                'es_score': score,
                's_ael_tail': s_ael,
                'fl_downtime': fl_downtime,
                'sigma': ls_sigma,
                'tc_risk': tc_risk,
                'backup_reliability': fail_prob,
                'dist': dist
            }
            st.success("Calculation Complete. Data Mapped to System.")
            st.rerun()

        if api_data:
            col_gauge, col_radar = st.columns(2)
            with col_gauge:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number", value = api_data['es_score'], title = {'text': "ES Risk Score"},
                    gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#FFD700"}, 'steps': [{'range': [0, 50], 'color': "#333"}, {'range': [50, 75], 'color': "#555"}, {'range': [75, 100], 'color': "#00BFFF"}]}
                ))
                fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
                st.plotly_chart(fig, use_container_width=True)
            with col_radar:
                df_rad = pd.DataFrame(dict(r=[80, 60, 90, 70, 85], theta=['Revenue', 'Tech', 'Complexity', 'Credit', 'Market']))
                fig_rad = px.line_polar(df_rad, r='r', theta='theta', line_close=True)
                fig_rad.update_traces(fill='toself', line_color='#00BFFF', fillcolor='rgba(0, 191, 255, 0.3)')
                fig_rad.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
                st.plotly_chart(fig_rad, use_container_width=True)
