import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def render_price_spike_shield():
    st.title("Price Spike Shield: Hedge Structuring")
    st.markdown(f'<h4 style="color: var(--color-titan-blue)">DYNAMIC VALUATION & PAYOFF ANALYSIS</h4>', unsafe_allow_html=True)
    
    api_data = st.session_state.get('rex_qf_data')
    
    # --- INPUTS & PARAMETERS ---
    if api_data:
        annual_consumption_mwh = 120000 
        s_ael_val = float(api_data['s_ael_tail'])
        st.info(f"DATA MAPPED: Client Annual Consumption: {annual_consumption_mwh:,.0f} MWh/yr")
    else:
        st.warning("Run REX-QF in Default Shield to populate S-AEL data.")
        s_ael_val = 5000000.0
        annual_consumption_mwh = 100000
        
    col_inputs, col_metrics = st.columns([1, 2])

    with col_inputs:
        st.subheader("Hedge Parameters")
        prob_threshold = st.slider("Probability Threshold (Confidence %)", 90, 99, 95, 1)
        hedge_premium_rmwh = st.number_input("Hedge Premium (R/MWh)", min_value=0.0, value=65.0, step=5.0)
        strike = st.number_input("Trigger Price (Strike)", value=3000.0)
        
        # Default Cap based on S-AEL
        cap_per_mwh = s_ael_val / (annual_consumption_mwh / 10)
        cap = st.number_input("Payout Cap (R/MWh)", value=cap_per_mwh)
        
        duration_months = st.selectbox("Hedge Duration (Months)", options=[12, 24, 36, 60], index=1)
        
        current_sael = s_ael_val 

    # --- CFO LAYER CALCULATIONS ---
    aep = hedge_premium_rmwh * annual_consumption_mwh
    net_var_reduction = current_sael - aep 
    exceedance_prob = 100 - prob_threshold 

    with col_metrics:
        st.subheader("Financial Impact Analysis")
        m1, m2, m3 = st.columns(3)
        m1.metric("Unhedged Risk (S-AEL)", f"R {current_sael:,.0f}", help="Tail risk at 95% confidence.")
        m2.metric("Annual Est. Premium (AEP)", f"R {aep:,.0f}", delta="- Cost", delta_color="inverse")
        m3.metric("Net Capital Protected", f"R {net_var_reduction:,.0f}", delta="Value Proposition")
        
        st.markdown("---")
        st.markdown(f"**Implied Exceedance Probability (Uncovered Risk):** <span class='titan-blue'>{exceedance_prob:.1f}%</span>", unsafe_allow_html=True)
        
        # --- NET PAYOFF DIAGRAM ---
        st.subheader("Net Payoff Diagram (Cost Exposure)")
        
        mkt_prices = np.linspace(1000, 8000, 200)
        unhedged_cost = mkt_prices 
        shielded_cost = []
        
        max_payout_per_mwh = cap
        effective_cost_floor = strike + hedge_premium_rmwh
        re_exposure_threshold = strike + max_payout_per_mwh
        
        for p in mkt_prices:
            if p <= strike:
                cost = p + hedge_premium_rmwh
            elif p <= re_exposure_threshold:
                cost = effective_cost_floor
            else:
                cost = p - max_payout_per_mwh + hedge_premium_rmwh
            shielded_cost.append(cost)

        fig_pay = go.Figure()
        fig_pay.add_trace(go.Scatter(x=mkt_prices, y=unhedged_cost, name="Unhedged Exposure", line=dict(color='red', width=2, dash='dash')))
        fig_pay.add_trace(go.Scatter(x=mkt_prices, y=shielded_cost, name="Shielded Cost (Capped Risk)", line=dict(color='#00BFFF', width=4)))
        
        fig_pay.add_vline(x=re_exposure_threshold, line_dash="dot", line_color="#FFD700", annotation_text="Cap Exhausted")
        
        fig_pay.update_layout(
            title="Net Payoff Diagram: Effective Client Cost", 
            xaxis_title="Market Spot Price (R/MWh)", 
            yaxis_title="Effective Net Cost (R/MWh)", 
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#FFFFFF")
        )
        st.plotly_chart(fig_pay, use_container_width=True)

    if api_data:
        st.subheader("Objective 2.3: Probability Curve (S-AEL)")
        fig = px.histogram(api_data['dist'], nbins=50, title="Projected Loss Distribution (Tail Risk Analysis)",
                           labels={'value': 'Loss Magnitude', 'count': 'Frequency'}, color_discrete_sequence=['#00BFFF'])
        fig.add_vline(x=api_data['s_ael_tail'], line_dash="dash", line_color="#FFD700", annotation_text="S-AEL (95% VaR)")
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
