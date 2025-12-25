import streamlit as st
import plotly.graph_objects as go

def render_connection_shield():
    st.title("Connection Shield (DSU Insurance)")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">GRID CONNECTION DELAY PROTECTION</h4>', unsafe_allow_html=True)

    # --- INPUTS ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Financial Exposure")
        monthly_debt = st.number_input("Monthly Debt Service (R)", value=1200000.0)
        monthly_opex = st.number_input("Fixed Monthly Opex (R)", value=300000.0)
        
        daily_burn_rate = (monthly_debt + monthly_opex) / 30
        st.metric("Daily Burn Rate (Financial Loss)", f"R {daily_burn_rate:,.0f} / day")

    with c2:
        st.subheader("Risk Probability (M-Data)")
        network_delay_prob = st.slider("Network Operator Delay Probability", 0.0, 1.0, 0.35)
        avg_delay_months = st.number_input("Avg Historical Delay (Months)", value=3.0)
        
        # Calc
        expected_payout = daily_burn_rate * (avg_delay_months * 30)
        premium_rate = 0.05 # 5% of limit
        premium = expected_payout * premium_rate
        
        st.metric("DSU Policy Limit", f"R {expected_payout:,.0f}", help="Coverage for the average delay period")
        st.metric("DSU Annual Premium", f"R {premium:,.0f}", delta="- Capex Addition")

    # --- VISUALIZATION ---
    st.markdown("---")
    st.subheader("Debt Service Exposure Meter")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = expected_payout,
        title = {'text': "Uncovered Exposure (3 Months)"},
        number = {'prefix': "R "},
        gauge = {
            'axis': {'range': [0, expected_payout * 2]},
            'bar': {'color': "#FF4500"}, # Red for risk
            'steps': [
                {'range': [0, premium], 'color': "#00BFFF"}, # Blue for cost
                {'range': [premium, expected_payout], 'color': "#333"}
            ],
        }
    ))
    
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Blue Segment represents the Premium Cost relative to the Red Risk Exposure.")
