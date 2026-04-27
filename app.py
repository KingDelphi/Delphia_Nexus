import streamlit as st
import pandas as pd
import os

# 1. APEX STELLAR AESTHETICS (8-COLUMN HIGH DENSITY)
def apply_theme():
    st.markdown("""
        <style>
        /* General Zoom & Scale */
        html, body, [data-testid="stAppViewContainer"] { 
            font-size: 11px !important; 
            background-color: #0c0e12; 
        }
        .stApp { background-color: #0c0e12; color: #d4af37; }
        
        /* Sidebar/Terminal Styling */
        section[data-testid="stSidebar"] { 
            background-color: #000000 !important; 
            border-right: 1px solid #d4af37; 
        }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] h3 {
            color: #ffffff !important; /* White for high contrast */
        }
        section[data-testid="stSidebar"] b, section[data-testid="stSidebar"] strong {
            color: #d4af37 !important; /* Gold for emphasis */
        }

        /* Metrics Display */
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
            text-align: center; min-height: 220px;
        }
        .asset-card:hover { border: 1px solid #d4af37; background-color: #21262d; }
        
        /* Full Title Visibility */
        .asset-title {
            font-size: 10px !important; 
            font-weight: bold;
            color: #ffffff !important;
            margin: 5px 0 !important;
            line-height: 1.1;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: visible;
        }

        /* Asset Buttons 2x2 Layout */
        .stButton>button { 
            width: 100%; font-size: 8px !important; height: 18px !important; 
            padding: 0px !important; min-height: 18px !important;
            background-color: #000000; color: #d4af37; border: 1px solid #444;
        }
        .stButton>button:hover { border-color: #d4af37; color: #fff; background-color: #d4af3722; }
        
        h1, h2, h3 { font-family: 'Courier New', monospace; }
        .small-id { font-size: 8px; color: #8b949e; margin-bottom: 2px; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="NEXUS | APEX SYSTEM", page_icon="🏛️", layout="wide")
apply_theme()

# 2. FINANCIAL TIERS CONFIGURATION
TIERS = {
    "Arquitecto": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Delphi": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Matriarca": {"LTV": 0.70, "Interest": 0.025, "Label": "TIER II - NOBLE"},
    "Inversor_01": {"LTV": 0.50, "Interest": 0.050, "Label": "TIER III - ELITE"}
}

# 3. IDENTITY SYNCHRONIZATION
USERS = {"Arquitecto": "ROOT_777", "Delphi": "OMEGA_999", "Inversor_01": "INV_001"}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🏛️ NEXUS | SYSTEM ACCESS")
    u = st.selectbox("Identity Selection", list(USERS.keys()))
    p = st.text_input("Access Key", type="password")
    if st.button("SYNCHRONIZE"):
        if USERS[u] == p:
            st.session_state["authenticated"], st.session_state["user"] = True, u
            st.rerun()
else:
    # 4. DATA CORE LOAD
    ledger = pd.read_csv("Truth_Ledger_Master.csv").rename(columns={'Nombre': 'Asset'})
    accounts = pd.read_csv("Delphia_Bank_Accounts.csv")
    ledger['Value'] = pd.to_numeric(ledger['Valor'].astype(str).replace('[\$,]', '', regex=True), errors='coerce').fillna(0)
    
    user = st.session_state["user"]
    tier_data = TIERS.get(user, TIERS["Inversor_01"])
    
    # Filter Logic
    user_assets = ledger if user in ["Arquitecto", "Delphi"] else ledger[ledger['Soberano'].str.contains(user, na=False)]
    row_acc = accounts[accounts['Soberano'].str.contains(user, na=False)]
    balance = row_acc['Saldo_DPX'].values[0] if not row_acc.empty else 0.0

    # COMPACT GLOBAL HEADER
    c_head = st.columns([3, 1, 1, 1, 1])
    c_head[0].markdown(f"### 🏛️ {user} | {tier_data['Label']}")
    c_head[1].metric("BANK BALANCE", f"{balance:,.0f} DPX")
    c_head[2].metric("TOTAL ASSETS", f"{user_assets['Value'].sum():,.0f} DPX")
    c_head[3].metric("CREDIT LINE", f"{(user_assets['Value'].sum() * tier_data['Interest']):,.0f} DPX")
    if c_head[4].button("LOGOUT"):
        st.session_state["authenticated"] = False
        st.rerun()

    # 5. ASSET GRID (8 COLUMNS)
    st.subheader("💎 Master Ledger - High Density View")
    cols = st.columns(8)
    
    for i, (_, asset) in enumerate(user_assets.iterrows()):
        with cols[i % 8]:
            # Dynamic Image Path Finder
            folder = asset['Soberano'].replace(" ", "_")
            # Probar múltiples extensiones si el CSV no la tiene
            img_base = f"Boveda_Activos/{folder}/{asset['Asset']}"
            img_path = None
            for ext in ['', '.jpg', '.jpeg', '.png']:
                if os.path.exists(img_base + ext):
                    img_path = img_base + ext
                    break
            
            st.markdown('<div class="asset-card">', unsafe_allow_html=True)
            
            # Asset Visuals
            if img_path:
                st.image(img_path, use_column_width=True)
            else:
                icon = "📄" if ".pdf" in str(asset['Asset']).lower() else "💎"
                st.markdown(f"<div style='height:45px; display:grid; place-items:center; font-size:24px;'>{icon}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='asset-title'>{asset['Asset']}</div>", unsafe_allow_html=True)
            st.markdown(f"<p class='small-id'>{asset['Asset_ID']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#d4af37; font-weight:bold; margin:2px 0;'>{asset['Value']:,.0f} DPX</p>", unsafe_allow_html=True)
            
            # Action Buttons 2x2 Matrix
            b1, b2 = st.columns(2)
            if b1.button("TITLE", key=f"t_{asset['Asset_ID']}"):
                st.session_state['op'] = ('OWNERSHIP TITLE', asset['Asset'], asset['Asset_ID'])
            if b2.button("SPLIT", key=f"f_{asset['Asset_ID']}"):
                st.session_state['op'] = ('FRACTIONAL SPLIT', asset['Asset'], asset['Asset_ID'])
                
            b3, b4 = st.columns(2)
            if b3.button("LOAN", key=f"c_{asset['Asset_ID']}"):
                st.session_state['op'] = ('CREDIT LINE', asset['Asset'], asset['Asset_ID'])
            if b4.button("SELL", key=f"v_{asset['Asset_ID']}"):
                st.session_state['op'] = ('MARKET ORDER', asset['Asset'], asset['Asset_ID'])
                
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
                current_val = float(ledger[ledger['Asset_ID']==aid]['Value'].values[0])
                price = st.number_input("Listing Price (DPX)", value=current_val)
                if st.button("EXECUTE SELL ORDER"):
                    st.success(f"Order listed at {price:,.2f} DPX")
            
            elif op_type == 'FRACTIONAL SPLIT':
                parts = st.number_input("Units to generate", min_value=2, value=100)
                if st.button("EXECUTE FRACTIONING"):
                    st.success(f"Asset split into {parts} units.")
            
            elif op_type == 'CREDIT LINE':
                val = ledger[ledger['Asset_ID']==aid]['Value'].values[0]
                max_loan = val * tier_data['LTV']
                st.write(f"**Max Borrowing:** {max_loan:,.2f} DPX")
                st.write(f"**Annual Interest:** {tier_data['Interest']*100}%")
                if st.button("INJECT LIQUIDITY"):
                    st.success("DPX Credit wired to account.")

            if st.button("CLOSE TERMINAL"):
                del st.session_state['op']
                st.rerun()