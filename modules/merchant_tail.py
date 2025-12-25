import streamlit as st
import plotly.express as px
from assets.helpers import calculate_black_scholes_put, generate_merchant_tail_scenario

def render_merchant_tail_shield():
    st.title("Merchant Tail Shield (Floor Option)")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">POST-PPA REVENUE GUARANTEE</h4>', unsafe_allow_html=True)

    # --- INPUTS ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Option Parameters")
        merchant_term = st.slider("Merchant Term (Years)", 1, 10, 5)
        annual_yield_kwh = st.number_input("Annual Yield (kWh)", value=2500000.0)
        strike_price = st.number_input("Floor Strike Price (R/kWh)", value=0.45, step=0.01)
        
    with c2:
        st.subheader("Market Volatility (SAWEM)")
        spot_price = st.number_input("Current Forward Spot (R/kWh)", value=0.85)
        volatility = st.slider("Implied Volatility (%)", 10, 100, 35) / 100
        risk_free = 0.09
        
        # Calc Premium
        # Approximating 'Time' as average duration of the tail (half the term)
        T = merchant_term / 2 
        option_prem_per_kwh = calculate_black_scholes_put(spot_price, strike_price, T, risk_free, volatility)
        
        total_premium = option_prem_per_kwh * annual_yield_kwh * merchant_term
        
        st.metric("Option Premium (per kWh)", f"R {option_prem_per_kwh:.3f}", delta="Cost of Floor")
        st.metric("Total Hedge Cost (Upfront)", f"R {total_premium:,.0f}")

    # --- VISUALIZATION ---
    st.markdown("---")
    st.subheader("Merchant Tail Revenue Security Plot")
    
    df_scen = generate_merchant_tail_scenario(strike_price, volatility, merchant_term)
    
    fig = px.line(df_scen, x='Month', y=['Spot Price', 'Floor Price'], color_discrete_sequence=['#00BFFF', '#FFD700'])
    fig.add_ribbon(x=df_scen['Month'], ymin=df_scen['Floor Price'], ymax=df_scen['Spot Price'], fillcolor='rgba(0,191,255,0.1)', name="Upside Potential")
    
    fig.update_layout(title="Forecasted Spot vs. Guaranteed Floor", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
