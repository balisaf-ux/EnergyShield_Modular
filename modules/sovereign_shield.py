import streamlit as st
import plotly.graph_objects as go

def render_sovereign_shield():
    st.title("Sovereign Shield (PRI Wrapper)")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">POLITICAL FORCE MAJEURE PROTECTION</h4>', unsafe_allow_html=True)

    # --- INPUTS ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Policy Scope")
        country_risk = st.select_slider("Country Risk Rating (M-Data)", options=["1 (Low)", "2", "3 (Med)", "4", "5 (High)"], value="3 (Med)")
        termination_val = st.number_input("Project Termination Value (R)", value=150000000.0, help="Debt + Equity Breakage Costs")
        
        st.markdown("**Covered Events:**")
        st.checkbox("Expropriation / Nationalization", value=True, disabled=True)
        st.checkbox("Currency Inconvertibility", value=True, disabled=True)
        st.checkbox("Breach of Contract (Change in Law)", value=True)

    with c2:
        st.subheader("Premium Calculation")
        # Simple Rating Logic
        rating_map = {"1 (Low)": 0.005, "2": 0.008, "3 (Med)": 0.012, "4": 0.018, "5 (High)": 0.025}
        base_rate = rating_map[country_risk]
        
        annual_premium = termination_val * base_rate
        
        st.metric("Applicable PRI Rate", f"{base_rate*100:.2f}%")
        st.metric("Annual PRI Premium", f"R {annual_premium:,.0f}", delta="- Opex Impact")
        st.metric("Guaranteed Payout (Termination)", f"R {termination_val:,.0f}", delta="Bankable Security")

    # --- VISUALIZATION ---
    st.markdown("---")
    st.subheader("Cost-Benefit Analysis: Premium vs. Exposure")
    
    total_20y_premium = annual_premium * 20
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Total 20Y Cost', 'Potential Payout'], y=[total_20y_premium, termination_val], 
                         marker_color=['#FFD700', '#00BFFF'], text=[f"R {total_20y_premium:,.0f}", f"R {termination_val:,.0f}"], textposition='auto'))
    
    fig.update_layout(title="Hedge Efficiency", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', yaxis_title="ZAR Value")
    st.plotly_chart(fig, use_container_width=True)
