import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def render_grid_uptime_shield():
    st.title("Grid Uptime Shield (Parametric)")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">AUTOMATED PAYOUT ENGINE</h4>', unsafe_allow_html=True)
    
    # Check for REX-QF Data
    api_data = st.session_state.get('rex_qf_data')
    
    # Default / Init Variables
    default_bi_hr = 5000.0
    default_backup = 0.15
    bi_val_hr_input = default_bi_hr
    aep = 0.0
    payout_event = 0.0
    
    if api_data:
        derived_hr = float(api_data['fl_downtime']) / 2000.0 
        default_bi_hr = derived_hr
        bi_val_hr_input = derived_hr
        default_backup = float(api_data.get('backup_reliability', 0.15))
        st.success(f"REX-QF MAPPED: FL-Downtime Base: R {api_data['fl_downtime']:,.0f}/yr")

    tab_profile, tab_config, tab_visuals = st.tabs(["1. Client Technical Profile", "2. Financial Triggers", "3. Coverage Visualization"])

    with tab_profile:
        st.subheader("1. Client Energy Profile")
        col_tech1, col_tech2, col_tech3 = st.columns(3)
        peak_demand = col_tech1.number_input("Contracted Peak Demand (MVA)", min_value=0.1, value=2.5, step=0.1)
        consumption_at_risk = col_tech2.number_input("Consumption @ Risk (kWh/hr)", min_value=1.0, value=1500.0, step=100.0)
        col_tech3.metric("System Load Classification", "Medium (1-10 MW)")
        
        st.markdown("---")
        st.subheader("2. Financial Validation (Implied Loss)")
        # Allow overwrite
        bi_val_hr_input = st.number_input("Business Interruption Value (R/Hr) - To Validate", value=default_bi_hr, format="%.2f")
        
        implied_loss_kwh = bi_val_hr_input / consumption_at_risk if consumption_at_risk > 0 else 0
        
        col_val1, col_val2 = st.columns(2)
        col_val1.metric("Implied Loss per kWh", f"R {implied_loss_kwh:.2f} / kWh")
        if implied_loss_kwh > 500: col_val2.error("⚠️ ALERT: IMPLAUSIBLE VALUE.")
        else: col_val2.success("✅ VALID: Loss value aligns with energy profile.")

    with tab_config:
        c1, c2 = st.columns(2)
        with c1:
            trigger_stage = st.selectbox("Trigger Stage (M2 Forecast)", ["Stage 4", "Stage 6", "Stage 8"])
            min_duration = st.number_input("Payout Duration Multiplier (Hours)", min_value=1.0, value=2.5, step=0.5)
            deductible = st.number_input("Deductible Time (Minutes)", min_value=0, value=30, step=15)
        with c2:
            # Use updated input
            bi_val_hr = bi_val_hr_input
            backup_rel = st.slider("Existing Backup Reliability (%)", 0.0, 1.0, default_backup, disabled=True)
            net_exposure_factor = 1.0 - backup_rel
            
            billable_hours = max(0, min_duration - (deductible/60))
            payout_event = bi_val_hr * net_exposure_factor * billable_hours
            mpl = bi_val_hr * net_exposure_factor * 500 # Max Payout Limit assumption
            freq = 50 # Assumed annual frequency
            aep = payout_event * freq * 0.15 # Premium calculation
            
            st.markdown("---")
            c_payout, c_mpl, c_prem = st.columns(3)
            c_payout.metric("PAYOUT / EVENT", f"R {payout_event:,.2f}")
            c_mpl.metric("MAX PAYOUT LIMIT", f"R {mpl:,.0f}")
            c_prem.metric("ANNUAL EST. PREMIUM", f"R {aep:,.0f}")

    with tab_visuals:
        v1, v2 = st.columns(2)
        with v1:
            st.subheader("Risk Coverage Heatmap")
            # Mock Heatmap Data
            hm_data = np.random.choice([0, 2, 4, 6], size=(24, 30), p=[0.6, 0.2, 0.15, 0.05])
            fig_hm = px.imshow(hm_data, labels=dict(x="Day", y="Hour", color="Stage"),
                                 color_continuous_scale='RdYlGn_r', title="Forecast Trigger Frequency (M2)")
            fig_hm.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_hm, use_container_width=True)
        with v2:
            st.subheader("Payout Scenario Chart")
            stages = ['Stage 2', 'Stage 4', 'Stage 6', 'Stage 8']
            # Safe access to calculated vars
            payouts = [0, payout_event, payout_event*1.5, payout_event*2.5]
            premiums = [0, aep, aep*0.8, aep*0.6] 
            df_scen = pd.DataFrame({'Stage': stages, 'Payout': payouts, 'Premium Cost': premiums})
            fig_area = px.area(df_scen, x='Stage', y=['Payout', 'Premium Cost'], 
                                 title="Hedge Value: Payout vs Cost", color_discrete_sequence=['#00BFFF', '#FFD700'])
            fig_area.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_area, use_container_width=True)
