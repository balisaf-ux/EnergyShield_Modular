import streamlit as st

def apply_titan_theme():
    st.markdown("""
        <style>
            /* --- TITAN FINAL PALETTE (AAA CONTRAST) --- */
            :root {
                --color-bg-main: #1A1C24;       
                --color-bg-panel: #252833;      
                --color-bg-sidebar: #101216;    
                --color-text-primary: #FFFFFF;  
                --color-text-secondary: #E0E0E0; 
                --color-titan-gold: #FFD700;    
                --color-titan-blue: #00BFFF;    
                --color-accent-muted: #B8860B; 
                --color-alert-urgent: #FF4500;  
            }
            .stApp { background-color: var(--color-bg-main); color: var(--color-text-primary); }
            header { visibility: hidden; } 
            h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; }
            p, label, span, div { color: var(--color-text-secondary); }
            
            section[data-testid="stSidebar"] {
                background-color: var(--color-bg-sidebar);
                border-right: 1px solid #444;
            }
            .sidebar-user-info p { margin: 0; color: #FFFFFF !important; }
            .role-admin { color: var(--color-titan-gold); font-weight: 700; }
            .role-customer { color: var(--color-titan-blue); font-weight: 700; }
            
            /* Inputs & Widgets */
            div.stRadio > label { color: #FFFFFF !important; text-transform: uppercase; font-size: 0.9rem !important; font-weight: 500; }
            div.stRadio > label[data-baseweb="radio"][aria-checked="true"] { color: var(--color-titan-gold) !important; background-color: rgba(255, 215, 0, 0.1); }
            
            /* Metrics & Cards */
            .indicator-card { background-color: var(--color-bg-panel); padding: 20px; border-radius: 4px; border: 1px solid #555; text-align: center; }
            .grid-risk-card { background-color: #2A1A1A; border: 1px solid var(--color-alert-urgent); }
            .indicator-value { font-size: 2.2rem; font-weight: 700; margin-top: 5px; color: #FFFFFF !important; }
            .titan-gold { color: var(--color-titan-gold) !important; }
            .titan-blue { color: var(--color-titan-blue) !important; }
            div[data-testid="stMetricValue"] { color: var(--color-titan-gold) !important; font-family: 'Roboto Mono', monospace; font-weight: 700; }
            div[data-testid="stMetricLabel"] { color: #FFFFFF !important; text-transform: uppercase; font-size: 0.85rem; }
            
            /* Buttons */
            div.stButton > button {
                background-color: #FFFFFF !important; color: #000000 !important;
                border: 1px solid #FFFFFF; text-transform: uppercase; font-weight: 800; letter-spacing: 1px; transition: all 0.3s ease;
            }
            div.stButton > button:hover {
                background-color: var(--color-titan-gold) !important; border-color: var(--color-titan-gold) !important;
                color: #000000 !important; box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
            }
        </style>
    """, unsafe_allow_html=True)
