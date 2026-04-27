import streamlit as st
import pandas as pd
import os
from PIL import Image

# 1. APEX STELLAR AESTHETICS (HIGH DENSITY & HIGH CONTRAST)
def apply_theme():
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] { 
            font-size: 11px !important; 
            background-color: #0c0e12; 
        }
        .stApp { background-color: #0c0e12; color: #d4af37; }
        
        /* Sidebar/Terminal Styling */
        section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #d4af37; }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] h3 {
            color: #ffffff !important; 
        }
        section[data-testid="stSidebar"] b, section[data-testid="stSidebar"] strong { color: #d4af37 !important; }

        /* Metrics */
        div[data-testid="stMetric"] { 
            background-color: #161b22; border: 1px solid #d4af37; 
            padding: 5px 10px !important; border-radius: 3px;
        }
        div[data-testid="stMetricLabel"] > div { font-size: 10px !important; color: #8b949e !important; }
        div[data-testid="stMetricValue"] > div { font-size: 14px !important; color: #d4af37 !important; }

        /* Asset Card Architecture */
        .asset-card { 
            background-color: #1c2128; border: 1px solid #30363d; 
            padding: 8px; border-radius: 4px; margin-bottom: 5px;
            text-align: center; min-height: 240px;
        }
        .asset-card:hover { border: 1px solid #d4af37; background-color: #21262d; }
        
        .asset-title {
            font-size: 10px !important; font-weight: bold; color: #ffffff !important;
            margin: 5px 0 !important; line-height: 1.1; height: 35px;
            display: flex; align-items: center; justify-content: center;
        }

        /* Micro Buttons 2x2 */
        .stButton>button { 
            width: 100%; font-size: 8px !important; height: 20px !important; 
            padding: 0px !important; background-color: #000000; color: #d4af37; 
            border: 1px solid #444; margin-bottom: 2px;
        }
        .stButton>button:hover { border-color: #d4af37; color: #fff; }
        
        h1, h2, h3 { font-family: 'Courier New', monospace; }
        .small-id { font-size: 8px; color: #8b949e; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="NEXUS | APEX SYSTEM", page_icon="🏛️", layout="wide")
apply_theme()

# 2. CONFIGURATION
TIERS = {
    "Arquitecto": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Delphi": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Matriarca": {"LTV": 0.70, "Interest": 0.025, "Label": "TIER II - NOBLE"}
}
USERS = {"Arquitecto": "ROOT_777", "Delphi": "OMEGA_999"}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🏛️ NEXUS | SYSTEM ACCESS")
    u = st.selectbox("Select Identity", list(USERS.keys()))
    p = st.text_input("Access Key", type="password")
    if st.button("SYNCHRONIZE"):
        if USERS[u] == p:
            st.session_state["authenticated"], st.session_state["user"] = True, u
            st.rerun()
else:
    # 3. DATA LOAD
    ledger = pd.read_csv("Truth_Ledger_Master.csv").rename(columns={'Nombre': 'Asset'})
    accounts = pd.read_csv("Delphia_Bank_Accounts.csv")
    ledger['Value'] = pd.to_numeric(ledger['Valor'].astype(str).replace('[\$,]', '', regex=True), errors='coerce').fillna(0)
    
    user = st.session_state["user"]
    tier_data = TIERS.get(user, TIERS["Arquitecto"])
    user_assets = ledger if user in ["Arquitecto", "Delphi"] else ledger[ledger['Soberano'].str.contains(user, na=False)]
    
    # 4. COMPACT HEADER
    acc_row = accounts[accounts['Soberano'].str.contains(user, na=False)]
    balance = acc_row['Saldo_DPX'].values[0] if not acc_row.empty else 0.0

    c_head = st.columns([3, 1, 1, 1, 1])
    c_head[0].markdown(f"### 🏛️ {user} | {tier_data['Label']}")
    c_head[1].metric("BANK BALANCE", f"{balance:,.0f} DPX")
    c_head[2].metric("TOTAL ASSETS", f"{user_assets['Value'].sum():,.0f} DPX")
    c_head[3].metric("CREDIT LINE", f"{(user_assets['Value'].sum() * tier_data['LTV']):,.0f} DPX")
    if c_head[4].button("LOGOUT"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.divider()

    # 5. ASSET GRID (8 COLUMNS)
    cols = st.columns(8)
    for i, (_, asset) in enumerate(user_assets.iterrows()):
        with cols[i % 8]:
            st.markdown('<div class="asset-card">', unsafe_allow_html=True)
            
            # --- IMAGE LOGIC (SECURE) ---
            folder = asset['Soberano'].replace(" ", "_")
            asset_name = str(asset['Asset'])
            img_path = f"Boveda_Activos/{folder}/{asset_name}"
            
            # Solo permitir extensiones de imagen conocidas
            valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
            
            if img_path.lower().endswith(valid_extensions) and os.path.exists(img_path):
                try:
                    st.image(img_path, use_column_width=True)
                except Exception:
                    st.markdown("<div style='height:60px; font-size:24px;'>⚠️</div>", unsafe_allow_html=True)
            else:
                icon = "📄" if ".pdf" in asset_name.lower() else "💎"
                st.markdown(f"<div style='height:60px; display:grid; place-items:center; font-size:24px;'>{icon}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='asset-title'>{asset_name}</div>", unsafe_allow_html=True)
            st.markdown(f"<p class='small-id'>{asset['Asset_ID']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#d4af37; font-weight:bold;'>{asset['Value']:,.0f} DPX</p>", unsafe_allow_html=True)
            
            # Action Buttons 2x2
            b1, b2 = st.columns(2)
            if b1.button("TITLE", key=f"t_{asset['Asset_ID']}"):
                st.session_state['op'] = ('OWNERSHIP TITLE', asset_name, asset['Asset_ID'])
            if b2.button("SPLIT", key=f"f_{asset['Asset_ID']}"):
                st.session_state['op'] = ('FRACTIONAL SPLIT', asset_name, asset['Asset_ID'])
                
            b3, b4 = st.columns(2)
            if b3.button("LOAN", key=f"c_{asset['Asset_ID']}"):
                st.session_state['op'] = ('CREDIT LINE', asset_name, asset['Asset_ID'])
            if b4.button("SELL", key=f"v_{asset['Asset_ID']}"):
                st.session_state['op'] = ('MARKET ORDER', asset_name, asset['Asset_ID'])
                
            st.markdown('</div>', unsafe_allow_html=True)

    # 6. TRANSACTION TERMINAL (SIDEBAR)
    if 'op' in st.session_state:
        op_type, name, aid = st.session_state['op']
        with st.sidebar:
            st.markdown(f"### ⚡ TERMINAL: {op_type}")
            st.write(f"**Asset:** {name}")
            st.write(f"**ID:** {aid}")
            st.divider()
            
            if op_type == 'MARKET ORDER':
                price = st.number_input("Listing Price (DPX)", value=1000.0)
                if st.button("EXECUTE SELL ORDER"):
                    st.success("Order live in Open Market.")
            elif op_type == 'FRACTIONAL SPLIT':
                st.number_input("Units", min_value=2, value=100)
                st.button("EXECUTE SPLIT")
            elif op_type == 'CREDIT LINE':
                st.write(f"**Tier:** {tier_data['Label']}")
                st.button("INJECT LIQUIDITY")

            if st.button("CLOSE TERMINAL"):
                del st.session_state['op']
                st.rerun()