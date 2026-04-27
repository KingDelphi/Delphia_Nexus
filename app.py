import streamlit as st
import pandas as pd
import os
import hashlib

# 1. APEX STELLAR AESTHETICS (6 COLUMNS - BALANCED VIEW)
def apply_theme():
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] { 
            font-size: 11px !important; 
            background-color: #0c0e12; 
        }
        .stApp { background-color: #0c0e12; color: #d4af37; }
        
        /* High Contrast Terminal */
        section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #d4af37; }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] label {
            color: #ffffff !important; 
        }
        section[data-testid="stSidebar"] b, section[data-testid="stSidebar"] strong { color: #d4af37 !important; }

        /* Metrics */
        div[data-testid="stMetric"] { 
            background-color: #161b22; border: 1px solid #d4af37; 
            padding: 5px 10px !important; border-radius: 3px;
        }

        /* Squared Card Architecture */
        .asset-card { 
            background-color: #1c2128; border: 1px solid #30363d; 
            padding: 10px; border-radius: 4px; margin-bottom: 8px;
            text-align: center; min-height: 260px;
        }
        .asset-card:hover { border: 1px solid #d4af37; background-color: #21262d; }
        
        .asset-title {
            font-size: 9px !important; font-weight: bold; color: #ffffff !important;
            margin: 5px 0 !important; line-height: 1.2; height: 40px;
            display: flex; align-items: center; justify-content: center;
            text-transform: uppercase;
        }

        /* Precise 2x2 Buttons */
        .stButton>button { 
            width: 100%; font-size: 7.5px !important; height: 22px !important; 
            padding: 0px !important; background-color: #000000; color: #d4af37; 
            border: 1px solid #444; margin-bottom: 2px;
        }
        .stButton>button:hover { border-color: #d4af37; color: #fff; background-color: #d4af3722; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="NEXUS | APEX SYSTEM", page_icon="🏛️", layout="wide")
apply_theme()

# HELPER: Generate Security Hash
def generate_asset_hash(asset_id, sovereign):
    return hashlib.sha256(f"{asset_id}-{sovereign}-2026".encode()).hexdigest()[:16].upper()

# 2. CONFIGURATION
TIERS = {
    "Arquitecto": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Delphi": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Matriarca": {"LTV": 0.70, "Interest": 0.025, "Label": "TIER II - NOBLE"}
}
USERS = {"Arquitecto": "ROOT_777", "Delphi": "OMEGA_999", "Matriarca": "M_2026"}

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
    c_head[3].metric("CREDIT LINE AVAILABLE", f"{(user_assets['Value'].sum() * tier_data['LTV']):,.0f} DPX")
    if c_head[4].button("LOGOUT"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.divider()

    # 5. ASSET GRID (6 COLUMNS - MORE SQUARE)
    cols = st.columns(6)
    for i, (_, asset) in enumerate(user_assets.iterrows()):
        with cols[i % 6]:
            st.markdown('<div class="asset-card">', unsafe_allow_html=True)
            
            # --- ROBUST IMAGE ENGINE (v2.0) ---
            folder = asset['Soberano'].replace(" ", "_")
            asset_clean_name = str(asset['Asset']).split('.')[0] # Quitar extensión del nombre si existe
            base_dir = f"Boveda_Activos/{folder}/"
            img_to_show = None
            
            if os.path.exists(base_dir):
                files_in_folder = os.listdir(base_dir)
                for f in files_in_folder:
                    if f.startswith(asset_clean_name) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        img_to_show = base_dir + f
                        break
            
            if img_to_show:
                st.image(img_to_show, use_column_width=True)
            else:
                icon = "📄" if ".pdf" in str(asset['Asset']).lower() else "💎"
                st.markdown(f"<div style='height:80px; display:grid; place-items:center; font-size:30px;'>{icon}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='asset-title'>{asset['Asset']}</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#d4af37; font-weight:bold; font-size:12px;'>{asset['Value']:,.0f} DPX</p>", unsafe_allow_html=True)
            
            # 2x2 Logic
            b1, b2 = st.columns(2)
            if b1.button("TITLE", key=f"t_{asset['Asset_ID']}"):
                st.session_state['op'] = ('TITLE', asset)
            if b2.button("SPLIT", key=f"f_{asset['Asset_ID']}"):
                st.session_state['op'] = ('SPLIT', asset)
                
            b3, b4 = st.columns(2)
            if b3.button("LOAN", key=f"c_{asset['Asset_ID']}"):
                st.session_state['op'] = ('LOAN', asset)
            if b4.button("SELL", key=f"v_{asset['Asset_ID']}"):
                st.session_state['op'] = ('SELL', asset)
                
            st.markdown('</div>', unsafe_allow_html=True)

    # 6. TRANSACTION TERMINAL (SIDEBAR)
    if 'op' in st.session_state:
        mode, data = st.session_state['op']
        with st.sidebar:
            st.markdown(f"### ⚡ TERMINAL: {mode}")
            st.write(f"**Asset:** {data['Asset']}")
            st.write(f"**Global ID:** {data['Asset_ID']}")
            
            if mode == 'TITLE':
                a_hash = generate_asset_hash(data['Asset_ID'], user)
                st.markdown(f"""
                <div style='border:1px solid #d4af37; padding:10px; background:#111;'>
                    <p style='color:#d4af37; font-size:10px;'>OFFICIAL OWNERSHIP TITLE</p>
                    <p style='font-size:8px;'>VERIFICATION HASH:<br><b>{a_hash}</b></p>
                    <p style='font-size:8px;'>STATUS: SECURED</p>
                </div>
                """, unsafe_allow_html=True)
                st.button("DOWNLOAD PDF CERTIFICATE")

            elif mode == 'SELL':
                # El precio sugerido es el valor actual en el ledger
                price = st.number_input("Market Price (DPX)", value=float(data['Value']))
                st.write("This asset will be listed in the Global Market.")
                if st.button("CONFIRM LISTING"):
                    st.success("Order broadcasted to Market core.")
            
            elif mode == 'LOAN':
                max_borrow = data['Value'] * tier_data['LTV']
                st.write(f"---")
                st.write(f"**Tier:** {tier_data['Label']}")
                st.write(f"**Max Loan (LTV {tier_data['LTV']*100}%):**")
                st.markdown(f"## {max_borrow:,.2f} DPX")
                st.write(f"**Annual Interest Rate:** {tier_data['Interest']*100}%")
                st.write(f"**Status:** Unlocked")
                if st.button("EXECUTE INSTANT LOAN"):
                    st.warning("Asset will be LOCKED as collateral.")

            elif mode == 'SPLIT':
                st.write("Divide this asset into smaller sovereign units.")
                units = st.number_input("Total Units", min_value=2, value=100)
                st.write(f"New unit value: {data['Value']/units:,.2f} DPX")
                if st.button("EXECUTE RE-LEDGERING"):
                    st.info("Rewriting Truth Ledger...")

            if st.button("CLOSE TERMINAL"):
                del st.session_state['op']
                st.rerun()