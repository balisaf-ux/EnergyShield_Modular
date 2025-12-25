import streamlit as st
import numpy as np
import plotly.express as px

def render_price_floor_shield():
    st.title("Price Floor Shield (Revenue Put)")
    st.subheader("Minimum Revenue Guarantee Parameters")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        floor_price = st.slider("Floor Strike Price (ZAR/MWh)", 0, 1500, 650, step=10)
        volume = st.number_input("Contracted Volume (MWh/Year)", value=150000)
        revenue_protection = floor_price * volume
        st.metric("Total Revenue Protection Value", f"R {revenue_protection:,.0f}")
        
    with col2:
        st.info("Pricing Model: Asian Put Option (Average Rate)")
        st.text_input("Linked PPA Reference", "PPA-SA-2025-001")
        if st.button("Execute Floor Hedge"):
            st.success("Hedge Confirmation Sent to Trading Desk.")

    st.markdown("---")
    st.subheader("Payoff Structure Analysis")
    market_prices = np.linspace(200, 1200, 100)
    payouts = [max(floor_price - p, 0) for p in market_prices]
    fig = px.area(x=market_prices, y=payouts, labels={'x': 'Market Spot Price (ZAR)', 'y': 'Hedge Payout (ZAR/MWh)'}, title="Floor Option Payoff Profile")
    fig.update_traces(line_color='#FFD700', fillcolor='rgba(255, 215, 0, 0.2)') 
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
