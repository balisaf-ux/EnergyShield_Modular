import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

def render_geospatial_engine():
    st.title("Geospatial Risk Engine")
    st.markdown(f'<h4 style="color: var(--color-titan-gold)">PREDICTIVE GIS INTELLIGENCE (7-LAYER)</h4>', unsafe_allow_html=True)
    
    tab_map, tab_shading, tab_intel = st.tabs(["1. Predictive Risk Layers", "2. Shading & Elevation Analysis", "3. Competitive Project Vicinity"])
    
    # --- TAB 1: 7-LAYER MAP ---
    with tab_map:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.subheader("Layer Selection")
            active_layer = st.radio("Select Intelligence Layer", 
                            [
                                "1. Regulatory Zones (TC-Risk)",
                                "2. Financial Risk Hotspot (FL-Downtime)",
                                "3. Transmission Capacity (Curtailment Risk)",
                                "4. Solar Irradiance (GHI/TPI)",
                                "5. Wind Resource (Hybrid Feasibility)",
                                "6. Grid Infrastructure Boundaries"
                            ])
            risk_year = st.slider("Risk Horizon", 2025, 2045, 2025)
            st.info(f"Visualizing Risk Context for: {risk_year}")

        with c2:
            lat_base, lon_base = -29.1, 26.2
            fig_map = go.Figure()
            
            # Base Client Site Marker
            fig_map.add_trace(go.Scattermapbox(
                lat=[lat_base], lon=[lon_base], mode='markers+text', 
                marker=go.scattermapbox.Marker(size=25, color='gold', symbol='star'),
                text=["Client Site (Project Alpha)"], textposition="bottom center", name="Client Site"
            ))

            # --- LAYER 1: REGULATORY ZONES (RED/YELLOW/GREEN) ---
            if active_layer == "1. Regulatory Zones (TC-Risk)":
                # Red Zone (Restricted)
                fig_map.add_trace(go.Scattermapbox(lat=[lat_base+0.05], lon=[lon_base+0.05], mode='markers', 
                                                   marker=dict(size=60, color='red', opacity=0.4), name="Red Zone (Restricted)"))
                # Yellow Zone (Permitted with Restrictions)
                fig_map.add_trace(go.Scattermapbox(lat=[lat_base-0.03], lon=[lon_base+0.02], mode='markers', 
                                                   marker=dict(size=50, color='yellow', opacity=0.4), name="Yellow Zone (Permitted)"))
                # Green Zone (Pre-Approved)
                fig_map.add_trace(go.Scattermapbox(lat=[lat_base+0.02], lon=[lon_base-0.02], mode='markers', 
                                                   marker=dict(size=40, color='green', opacity=0.4), name="Green Zone (Pre-Approved)"))
            
            # --- LAYER 2: FINANCIAL RISK HOTSPOT (FL-DOWNTIME) ---
            elif active_layer == "2. Financial Risk Hotspot (FL-Downtime)":
                lats = lat_base + np.random.uniform(-0.1, 0.1, 50)
                lons = lon_base + np.random.uniform(-0.1, 0.1, 50)
                vals = np.random.uniform(50, 100, 50)
                fig_map.add_trace(go.Densitymapbox(lat=lats, lon=lons, z=vals, radius=20, colorscale='Hot', name="Shedding Intensity"))

            # --- LAYER 3: TRANSMISSION & CURTAILMENT ---
            elif active_layer == "3. Transmission Capacity (Curtailment Risk)":
                # Feeder A (High Congestion - Red)
                fig_map.add_trace(go.Scattermapbox(mode="lines", lat=[lat_base, lat_base+0.1], lon=[lon_base, lon_base+0.1], 
                                                   line=dict(width=4, color="red"), name="Feeder A (98% Cap)"))
                # Feeder B (Available Capacity - Green)
                fig_map.add_trace(go.Scattermapbox(mode="lines", lat=[lat_base, lat_base-0.1], lon=[lon_base, lon_base-0.05], 
                                                   line=dict(width=4, color="green"), name="Feeder B (40% Cap)"))

            # --- LAYER 4: SOLAR IRRADIANCE (TPI) ---
            elif active_layer == "4. Solar Irradiance (GHI/TPI)":
                lats = lat_base + np.random.uniform(-0.1, 0.1, 100)
                lons = lon_base + np.random.uniform(-0.1, 0.1, 100)
                ghi = np.random.uniform(1800, 2400, 100)
                fig_map.add_trace(go.Densitymapbox(lat=lats, lon=lons, z=ghi, radius=15, colorscale='Solar', name="GHI (kWh/m2)"))

            # --- LAYER 5: WIND RESOURCE (NEW) ---
            elif active_layer == "5. Wind Resource (Hybrid Feasibility)":
                # Simulating Wind Contour
                lats = lat_base + np.random.uniform(-0.1, 0.1, 80)
                lons = lon_base + np.random.uniform(-0.1, 0.1, 80)
                speeds = np.random.uniform(4.0, 9.0, 80)
                fig_map.add_trace(go.Densitymapbox(lat=lats, lon=lons, z=speeds, radius=25, colorscale='Viridis', name="Wind Speed (m/s)"))

            # --- LAYER 6: INFRASTRUCTURE ---
            elif active_layer == "6. Grid Infrastructure Boundaries":
                 fig_map.add_trace(go.Scattermapbox(lat=[lat_base+0.04], lon=[lon_base-0.04], mode='markers', 
                                                   marker=dict(size=15, color='white', symbol='square'), name="Substation Alpha"))

            fig_map.update_layout(mapbox_style="carto-darkmatter", mapbox=dict(center=dict(lat=lat_base, lon=lon_base), zoom=10.5), margin={"r":0,"t":0,"l":0,"b":0}, height=550, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_map, use_container_width=True)

    # --- TAB 2: SHADING TOOL (Enhancement 4) ---
    with tab_shading:
        st.subheader("Shading and Elevation Analysis Tool")
        sc1, sc2 = st.columns([1, 2])
        with sc1:
            date_sim = st.date_input("Simulation Date", value=datetime(2025, 6, 21)) # Default to Winter Solstice
            time_day = st.slider("Time of Day", 6, 18, 10)
            st.caption("Using DEM (Digital Elevation Model) for Latitude -29.1")
        with sc2:
            # Mock Logic for Visual
            shadow_len = abs(12 - time_day) * 15 # Simple proxy logic
            shadow_direction = "West" if time_day < 12 else "East"
            st.metric(f"Projected Shadow Length ({shadow_direction})", f"{shadow_len} meters")
            
            if time_day < 8 or time_day > 16:
                st.warning("⚠️ High Shading Risk: Low sun angle detected.")
            else:
                st.success("✅ Optimal Generation Window")

    # --- TAB 3: COMPETITIVE INTELLIGENCE (Enhancement 7) ---
    with tab_intel:
        st.subheader("Large Renewable Energy Project Vicinity Layer")
        st.caption("Grid Impact & Market Saturation Analysis (Radius: 50km)")
        
        # Map for Competitive Projects
        comp_lats = [-29.05, -29.15, -29.12]
        comp_lons = [26.15, 26.25, 26.18]
        comp_names = ["De Aar Solar 1", "Longyuan Mulilo Wind", "Titan PV Gamma"]
        comp_caps = ["50 MW", "140 MW", "75 MW"]
        comp_tech = ["Solar PV", "Onshore Wind", "Solar PV"]
        
        fig_comp = go.Figure()
        # Client Site
        fig_comp.add_trace(go.Scattermapbox(
                lat=[-29.1], lon=[26.2], mode='markers', 
                marker=go.scattermapbox.Marker(size=20, color='gold'), name="CLIENT SITE"
            ))
        
        # Competitors
        fig_comp.add_trace(go.Scattermapbox(
            lat=comp_lats, lon=comp_lons, mode='markers',
            marker=go.scattermapbox.Marker(size=15, color='#00BFFF'),
            text=[f"{n} ({c} - {t})" for n,c,t in zip(comp_names, comp_caps, comp_tech)],
            hoverinfo='text',
            name="Competitor IPP"
        ))
        
        fig_comp.update_layout(mapbox_style="carto-darkmatter", mapbox=dict(center=dict(lat=-29.1, lon=26.2), zoom=9), margin={"r":0,"t":0,"l":0,"b":0}, height=400, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_comp, use_container_width=True)
        
        st.table(pd.DataFrame({
            'Project Name': comp_names, 
            'Technology': comp_tech,
            'Capacity': comp_caps, 
            'Grid Status': ['Operational', 'Operational', 'Under Construction']
        }))
