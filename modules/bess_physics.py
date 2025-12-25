import streamlit as st
import numpy as np
import plotly.express as px
from assets.helpers import generate_bess_revenue

def render_bess_physics_engine():
    st.title("BESS Physics Engine")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">MULTI-OBJECTIVE OPTIMIZATION ENGINE</h4>', unsafe_allow_html=True)
    
    tab_design, tab_econ, tab_risk = st.tabs(["1. System Design", "2. Revenue Optimization", "3. Risk Stress Test"])
    
    with tab_design:
        col1, col2 = st.columns(2)
        with col1:
            ep_ratio = st.slider("Energy-to-Power Ratio (E/P)", 1.0, 6.0, 4.0, step=0.5)
            target_life = st.number_input("Required Operational Life (Years)", 5, 25, 20)
        with col2:
            amb_temp = st.slider("Avg Ambient Temp (°C)", 10, 45, 25)
            grid_mode = st.radio("Grid Connection Mode", ["Grid-Tied", "Off-Grid / Island"])
        
        base_deg_rate = 0.02
        temp_factor = 1.0 + max(0, (amb_temp - 25) * 0.05)
        mode_factor = 1.5 if grid_mode == "Off-Grid / Island" else 1.0
        effective_deg_rate = base_deg_rate * temp_factor * mode_factor
        
        capacity_at_eol = (1 - effective_deg_rate) ** target_life
        required_oversizing = 0.8 / capacity_at_eol 
        
        st.markdown("---")
        k1, k2, k3 = st.columns(3)
        k1.metric("Effective Degradation Rate", f"{effective_deg_rate*100:.2f}% / yr")
        k2.metric("Capacity at Year 20", f"{capacity_at_eol*100:.1f}%")
        k3.metric("Required Oversizing (CapEx)", f"{required_oversizing:.2f}x", "To meet 80% EoL")
        
        years = np.arange(0, target_life + 1)
        soh = [(1 - effective_deg_rate)**y * 100 for y in years]
        fig_deg = px.line(x=years, y=soh, title="BESS State of Health (SoH) Forecast", labels={'x':'Year', 'y':'SoH (%)'})
        fig_deg.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Contractual EoL (80%)")
        fig_deg.update_traces(line_color='#00BFFF', line_width=3)
        fig_deg.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_deg, use_container_width=True)

    with tab_econ:
        col_opt1, col_opt2 = st.columns([1, 2])
        with col_opt1:
            st.info(f"Optimization Strategy: {'Arbitrage Focus' if ep_ratio > 2 else 'Ancillary Focus'}")
            deg_cost = st.number_input("Cost of Degradation (R/Cycle)", value=150.0)
        
        with col_opt2:
            df_rev = generate_bess_revenue(ep_ratio, deg_cost)
            fig_stack = px.area(df_rev, x='Month', y=['Arbitrage', 'Ancillary', 'Capacity'], 
                                 title="Revenue Stacking (Gross)", color_discrete_sequence=['#FFD700', '#00BFFF', '#CD7F32'])
            fig_stack.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_stack, use_container_width=True)

    with tab_risk:
        st.warning("Impact: Stage 4 Load Shedding reduces asset life by 1.5 Years")
