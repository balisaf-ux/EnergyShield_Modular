import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_cfd_valuation():
    st.title("CFD Valuation & Structuring")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">ZERO-NPV PRICING ENGINE</h4>', unsafe_allow_html=True)
    
    # Check for REX-QF Data to map Volatility
    api_data = st.session_state.get('rex_qf_data')
    default_vol = 15.5
    mapped_vol = default_vol
    
    if api_data:
        # Map Sigma from REX Engine to Volatility %
        mapped_vol = float(api_data['sigma'] * 100)
        st.info(f"DATA MAPPED: Volatility derived from REX-QF Sigma ({mapped_vol:.1f}%)")
        
    tab_config, tab_heatmap, tab_payout = st.tabs(["1. Deal & Risk Configuration", "2. Sensitivity Heatmap", "3. Payout Profile"])
    
    # --- SHARED CALCULATION LOGIC ---
    # We define inputs first to use them across tabs
    with tab_config:
        c1, c2, c3 = st.columns(3)
        with c1:
            contract_type = st.selectbox("Contract Type", ["Financial CFD (Swap)", "Physical PPA"])
            term_years = st.slider("Project Term (Years)", 5, 25, 20)
            capacity = st.number_input("Capacity (MW)", value=100)
        with c2:
            wacc = st.number_input("WACC (Discount Rate %)", 5.0, 20.0, 11.5, step=0.1)
            cpi = st.number_input("CPI Forecast (%)", 3.0, 8.0, 5.2)
            volatility = st.number_input("Spot Price Volatility (σ %)", value=mapped_vol)
        with c3:
            risk_premium = 150.0 
            st.metric("Credit Risk Premium", f"+ {risk_premium:.0f} bps")

        # Logic: NERSA Curve DCF
        years = np.arange(1, term_years + 1)
        growth = [0.1274, 0.0536, 0.0619] # M1 Tariff Assumption
        while len(growth) < term_years: growth.append(cpi/100)
        
        base_price = 1200
        market_prices_proj = []
        curr = base_price
        for g in growth:
            curr = curr * (1 + g)
            market_prices_proj.append(curr)
        
        discount_factors = [(1 + wacc/100)**-t for t in years]
        npv_market = sum([p * d for p, d in zip(market_prices_proj, discount_factors)])
        sum_df = sum(discount_factors)
        
        # The Core Zero-NPV Formula
        zero_npv_strike = (npv_market / sum_df) + (risk_premium/100 * 100) 
        
        market_benchmark = 1350.0
        alpha = market_benchmark - zero_npv_strike
        var_hedge = (volatility/100) * (capacity * 24 * 365) * zero_npv_strike * 0.1
        
        st.markdown("---")
        k1, k2, k3 = st.columns(3)
        k1.metric("ZERO-NPV STRIKE PRICE", f"R {zero_npv_strike:,.2f} / MWh", "Fair Value")
        k2.metric("IMPLIED MARKET PREMIUM (ALPHA)", f"R {alpha:,.2f} / MWh", " Competitive Advantage" if alpha > 0 else "Premium")
        k3.metric("VaR HEDGE VALUE", f"R {var_hedge/1000000:,.1f} M", "Risk Capital Reduction")

    with tab_heatmap:
        st.subheader("Strike Price Sensitivity Analysis")
        wacc_range = [9.0, 10.0, 11.0, 11.5, 12.0, 13.0]
        term_range = [10, 15, 20, 25]
        heatmap_data = []
        
        # Sensitivity Logic
        for w in wacc_range:
            row = []
            for t in term_range:
                yrs = np.arange(1, t+1)
                dfs = [(1 + w/100)**-y for y in yrs]
                # Adjust market price projection length to match term 't'
                mp = market_prices_proj[:t] if t <= len(market_prices_proj) else market_prices_proj + [market_prices_proj[-1]]*(t-len(market_prices_proj))
                npv = sum([p * d for p, d in zip(mp, dfs)])
                strike = npv / sum(dfs)
                row.append(round(strike, 0))
            heatmap_data.append(row)
            
        fig_heat = px.imshow(heatmap_data, 
                                 labels=dict(x="Project Term (Years)", y="WACC (%)", color="Strike Price"),
                                 x=term_range, y=wacc_range,
                                 text_auto=True, color_continuous_scale='Viridis')
        fig_heat.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', title="Zero-NPV Strike Price Matrix (ZAR/MWh)")
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab_payout:
        st.subheader("CFD Payout Mechanics")
        grid_prices = np.linspace(800, 2500, 100)
        diffs = grid_prices - zero_npv_strike
        client_cf = diffs 
        
        fig_pay = go.Figure()
        fig_pay.add_trace(go.Scatter(x=grid_prices, y=client_cf, mode='lines', name='Hedge Cashflow', line=dict(color='#00BFFF', width=3)))
        fig_pay.add_hline(y=0, line_dash="dash", line_color="white", annotation_text="Break-Even")
        fig_pay.add_vline(x=zero_npv_strike, line_dash="dot", line_color="#FFD700", annotation_text=f"Strike: {zero_npv_strike:.0f}")
        
        fig_pay.update_layout(title="Hedge Cashflow vs Grid Price", xaxis_title="Actual Grid Price (ZAR/MWh)", yaxis_title="Payout to Client (ZAR/MWh)", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pay, use_container_width=True)
