import streamlit as st
import plotly.graph_objects as go
from assets.helpers import calculate_liability_forecast

def render_carbon_shield():
    st.title("Carbon Shield: Liability Forecast")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">TAX LIABILITY HEDGE & REVENUE STACKING</h4>', unsafe_allow_html=True)
    
    # --- INPUTS ---
    tab_inputs, tab_forecast, tab_monetization = st.tabs(["1. Calculation Inputs", "2. Liability Forecast", "3. Value Monetization"])
    
    # Default/Mapped values
    default_annual_mwh = 120000 
    default_ppa_mwh_avoided = 80000 
    
    with tab_inputs:
        st.subheader("Client & Grid Parameters")
        c1, c2, c3 = st.columns(3)
        # Mapped from REX-QF / CFD
        annual_mwh = c1.number_input("Client Annual Consumption (MWh/yr)", value=default_annual_mwh)
        ppa_mwh = c2.number_input("EnergyShield PPA Volume (MWh/yr)", value=default_ppa_mwh_avoided)
        term_years = c3.slider("Projection Term (Years)", 5, 25, 20)
        st.markdown("---")
        st.subheader("Tax & Emission Factors")
        c4, c5, c6 = st.columns(3)
        # Input 1: Grid Emission Factor (GEF)
        gef_start = c4.number_input("Grid Emission Factor (kg CO2/MWh)", value=1000.0, step=10.0, help="Eskom Grid Baseline")
        # Input 2: Tax Escalation Rate
        tax_escalation = c5.number_input("Tax Escalation Rate (%)", value=8.0, step=0.5, help="Annual Statutory Increase Rate")
        # Baseline Tax Rate (Mock value)
        tax_rate_start = c6.number_input("Current Carbon Tax Rate (R/t CO2e)", value=150.0, step=10.0)
        
        # RUN FORECAST (Using Helper)
        df_forecast = calculate_liability_forecast(annual_mwh, ppa_mwh, gef_start, tax_rate_start, tax_escalation, term_years)

    # --- FORECAST & WATERFALL ---
    with tab_forecast:
        st.subheader("20-Year Carbon Liability Projection")
        
        # Calculated Output: Total Avoided Liability (R)
        total_gross_liability = df_forecast['AnnualLiability'].sum() / (1 - (0.60)) # Reverse calculation to find true gross liability before allowance
        total_net_liability_after_ppa = df_forecast['AnnualLiability'].sum()
        total_avoided_liability = total_gross_liability - total_net_liability_after_ppa
        
        k1, k2 = st.columns(2)
        k1.metric("Total Avoided Liability (20Y)", f"R {total_avoided_liability:,.0f}", delta="Value of the Hedge")
        k2.metric("Final Net Liability (20Y)", f"R {total_net_liability_after_ppa:,.0f}")
        
        st.markdown("---")
        st.subheader("Liability Bridge Waterfall Chart")
        
        # --- LIABILITY BRIDGE WATERFALL ---
        
        # Calculations for Year 1 Waterfall
        gross_liability_start = (df_forecast['GrossEmissions'].iloc[0] * df_forecast['TaxRate'].iloc[0]) * 2.5 # Approximate true starting gross value
        allowance_reduction = gross_liability_start * 0.60
        ppa_avoidance = (df_forecast['AvoidedEmissions'].iloc[0] * df_forecast['TaxRate'].iloc[0]) 
        final_liability = gross_liability_start - allowance_reduction - ppa_avoidance

        fig_water = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["absolute", "relative", "relative", "total"],
            x = ["1. Gross Obligation", "2. Allowance", "3. PPA Avoidance", "4. Net Obligation"],
            textposition = "outside",
            y=[gross_liability_start, -allowance_reduction, -ppa_avoidance, final_liability],
            connector={"line":{"color":"rgb(63, 63, 63)"}}
        ))
        
        fig_water.update_layout(
            title="Year 1 Carbon Tax Liability Bridge", 
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            showlegend=False
        )
        st.plotly_chart(fig_water, use_container_width=True)

    # --- VALUE MONETIZATION ---
    with tab_monetization:
        st.subheader("Carbon Credit Monetization")
        
        # VSP Calculation: Surplus = PPA Avoidance - Client's Taxable Emissions
        client_emissions_after_allowance = df_forecast['GrossEmissions'].iloc[0] * (1 - 0.60)
        ppa_avoidance_tco2 = df_forecast['AvoidedEmissions'].iloc[0]
        
        surplus_credits_tco2 = max(0, ppa_avoidance_tco2 - client_emissions_after_allowance)
        
        # Value Stacking Potential (VSP)
        carbon_credit_price = st.number_input("Carbon Credit Market Price (R/t CO2e)", value=250.0)
        
        annual_credit_revenue = surplus_credits_tco2 * carbon_credit_price
        
        c1, c2 = st.columns(2)
        c1.metric("Surplus Credits Available (t CO2e)", f"{surplus_credits_tco2:,.0f}")
        # Output Metric: Annual Carbon Credit Revenue Potential (R)
        c2.metric("Annual Credit Revenue Potential", f"R {annual_credit_revenue:,.0f}", delta="+ Revenue Stream")
        
        if surplus_credits_tco2 > 0:
            st.success("✅ VSP Triggered: Surplus generation creates a revenue-generating asset.")
        else:
            st.info("No Surplus: Avoided emissions are currently used to offset internal liability only.")
