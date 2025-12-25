import streamlit as st
import sys
import os

# --- 1. SYSTEM PATH SETUP ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- 2. ASSET IMPORTS ---
try:
    from assets.theme import apply_titan_theme
except ImportError:
    st.error("CRITICAL: Assets not found. Ensure 'assets/theme.py' exists.")
    st.stop()

# --- 3. MODULE IMPORTS ---
from modules.dashboard import render_dashboard
from modules.default_shield import render_default_shield
from modules.price_spike import render_price_spike_shield
from modules.cfd_valuation import render_cfd_valuation
from modules.variance_swap import render_variance_swap
from modules.grid_uptime import render_grid_uptime_shield
from modules.geospatial import render_geospatial_engine
from modules.carbon_shield import render_carbon_shield
from modules.bess_physics import render_bess_physics_engine
from modules.syndication import render_syndication_placement
from modules.curtailment import render_curtailment_shield
from modules.price_floor import render_price_floor_shield
# v8.1 New Modules
from modules.deterioration_shield import render_deterioration_shield
from modules.sovereign_shield import render_sovereign_shield
from modules.merchant_tail import render_merchant_tail_shield
from modules.connection_shield import render_connection_shield

# --- 4. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EnergyShield FOS v8.1",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_titan_theme()

# --- 5. SESSION STATE INITIALIZATION ---
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

if 'rex_qf_data' not in st.session_state:
    st.session_state['rex_qf_data'] = None

# --- 6. NAVIGATION CONTROLLERS ---

def render_admin_layout():
    # ORDERED MODULE MAP
    MODULE_MAP = {
        "TERMINAL HOME": render_dashboard,
        "DEFAULT SHIELD (REX-QF)": render_default_shield,
        "--- CORE SHIELDS ---": None, # Separator
        "PRICE SPIKE SHIELD": render_price_spike_shield,
        "GRID UPTIME SHIELD": render_grid_uptime_shield,
        "PRICE FLOOR SHIELD": render_price_floor_shield,
        "CURTAILMENT SHIELD": render_curtailment_shield,
        "CARBON SHIELD": render_carbon_shield,
        "--- NEXT-GEN SHIELDS ---": None, # Separator
        "DETERIORATION SHIELD": render_deterioration_shield,
        "SOVEREIGN SHIELD": render_sovereign_shield,
        "MERCHANT TAIL SHIELD": render_merchant_tail_shield,
        "CONNECTION SHIELD": render_connection_shield,
        "--- ENGINES ---": None, # Separator
        "CFD VALUATION": render_cfd_valuation,
        "VARIANCE SWAP": render_variance_swap,
        "BESS PHYSICS ENGINE": render_bess_physics_engine,
        "GEOSPATIAL ENGINE": render_geospatial_engine,
        "SYNDICATION PLACEMENT": render_syndication_placement
    }

    with st.sidebar:
        st.markdown("## ⚡ ENERGYSHIELD")
        st.markdown(f"<div class='sidebar-user-info'><p>User: Sovereign Builder</p><p>Role: <span class='role-admin'>Admin</span></p></div>", unsafe_allow_html=True)
        
        if st.button("LOGOUT"):
            st.session_state['user_role'] = None
            st.rerun()
            
        st.markdown("---")
        
        # Custom Radio Loop to handle separators
        clean_keys = [k for k in MODULE_MAP.keys() if "---" not in k]
        selection = st.radio("Select Module", clean_keys, label_visibility="collapsed")
        
        if st.session_state.get('rex_qf_data'):
            st.markdown("---")
            st.success("✅ REX-QF: LINKED")
        
        st.markdown("---")
        st.caption("v8.1 Next-Gen Architect")

    # Routing Logic
    renderer = MODULE_MAP.get(selection)
    
    if renderer:
        try:
            renderer()
        except Exception as e:
            st.error(f"Module Error: {e}")
    else:
        st.error("Navigation Error")

def render_customer_layout():
    with st.sidebar:
        st.markdown("## ⚡ ENERGYSHIELD")
        st.caption("Client View")
        if st.button("LOGOUT"):
            st.session_state['user_role'] = None
            st.rerun()
    
    st.title("My Portfolio")
    st.info("Customer portal is under maintenance during v8.1 refactor.")

# --- 7. MAIN ENTRY POINT ---
def main():
    if st.session_state['user_role'] is None:
        st.markdown('<div style="text-align: center; padding-top: 150px;"><h1>⚡ ENERGYSHIELD TERMINAL</h1></div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c2: 
            if st.button("LOGIN AS ADMIN", use_container_width=True):
                st.session_state['user_role'] = 'Admin'
                st.rerun()
        with c3:
            if st.button("LOGIN AS CUSTOMER", use_container_width=True):
                st.session_state['user_role'] = 'Customer'
                st.rerun()
                
    elif st.session_state['user_role'] == 'Admin':
        render_admin_layout()
    elif st.session_state['user_role'] == 'Customer':
        render_customer_layout()

if __name__ == "__main__":
    main()
