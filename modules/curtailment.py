import streamlit as st
import plotly.graph_objects as go
from assets.helpers import generate_clipping_data

def render_curtailment_shield():
    st.title("Curtailment Shield")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">GRID CONGESTION & REVENUE PROTECTION</h4>', unsafe_allow_html=True)
    
    tab_grid, tab_finance, tab_hedge = st.tabs(["1. Grid Congestion Analysis", "2. Financial Impact", "3. Hedge Structure"])
    
    # Init vars to prevent scope errors
    curtailed_mwh_daily = 0
    df_clip = None
    
    with tab_grid:
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Grid Node / Zone", ["Northern Cape (Upington)", "Eastern Cape (Cookhouse)", "Western Cape (Touwsrivier)"])
            plant_capacity = st.number_input("Plant Capacity (MW)", value=100.0)
            grid_limit = st.number_input("Grid Export Limit (MW)", value=80.0)
        with c2:
            df_clip = generate_clipping_data(plant_capacity, grid_limit)
            fig_clip = go.Figure()
            fig_clip.add_trace(go.Scatter(x=df_clip['Hour'], y=df_clip['Potential Generation'], fill='tozeroy', name='Potential Gen', line=dict(color='#00BFFF')))
            fig_clip.add_trace(go.Scatter(x=df_clip['Hour'], y=df_clip['Grid Limit'], name='Grid Limit', line=dict(color='#FF4500', width=3, dash='dash')))
            fig_clip.update_layout(template="plotly_dark", title="Generation Profile vs Grid Limit (Clipping)", paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_clip, use_container_width=True)
            curtailed_mwh_daily = df_clip['Curtailed Energy'].sum()
            st.error(f"Daily Curtailed Energy: {curtailed_mwh_daily:.2f} MWh")

    with tab_finance:
        c1, c2 = st.columns(2)
        ppa_rate = c1.number_input("PPA Rate (R/MWh)", value=1200.0)
        daily_loss = curtailed_mwh_daily * ppa_rate
        st.metric("Daily Revenue Loss", f"R {daily_loss:,.0f}")
        
        # Ensure df_clip exists before calc
        potential_rev = df_clip['Potential Generation'].sum() * ppa_rate
        net_rev = potential_rev - daily_loss
        
        fig_water = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["Potential Revenue", "Grid Curtailment Loss", "Net Realized Revenue"],
            textposition = "outside",
            text = [f"R {potential_rev:,.0f}", f"-R {daily_loss:,.0f}", f"R {net_rev:,.0f}"],
            y = [potential_rev, -daily_loss, 0],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
        fig_water.update_layout(title = "Daily Revenue Waterfall", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_water, use_container_width=True)

    with tab_hedge:
        st.subheader("Deemed Energy Hedge Configuration")
        c1, c2 = st.columns(2)
        deductible = c1.slider("Curtailment Deductible (%)", 0, 10, 2)
        coverage_ratio = c2.slider("Coverage Ratio (%)", 50, 100, 90)
        
        total_gen = df_clip['Potential Generation'].sum()
        payout_trigger = (curtailed_mwh_daily / total_gen) * 100 if total_gen > 0 else 0
        
        st.metric("Current Curtailment %", f"{payout_trigger:.1f}%")
        if payout_trigger > deductible:
            claimable = (payout_trigger - deductible) * coverage_ratio
            st.success(f"HEDGE ACTIVE: Payout Triggered. Recoverable: {claimable:.1f}% of Loss")
        else:
            st.info("No Payout: Curtailment below Deductible threshold.")
