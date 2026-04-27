import streamlit as st
import pandas as pd
import os
import hashlib
import io

# Intentamos importar fpdf con un manejo de error para que la app no muera si falta
try:
    from fpdf import FPDF
except ImportError:
    st.error("⚠️ Falta la librería 'fpdf'. Por favor, añade 'fpdf' a tu archivo requirements.txt")

# 1. APEX STELLAR AESTHETICS (GRID SYSTEM & HIGH CONTRAST)
def apply_theme():
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] { 
            font-size: 11px !important; 
            background-color: #0c0e12; 
        }
        .stApp { background-color: #0c0e12; color: #d4af37; }
        
        /* Metrics Header Contrast Fix */
        [data-testid="stMetricLabel"] p { color: #d4af37 !important; font-weight: bold !important; font-size: 10px !important; }
        [data-testid="stMetricValue"] div { color: #ffffff !important; font-size: 16px !important; }
        div[data-testid="stMetric"] { 
            background-color: #161b22; border: 1px solid #d4af37; 
            padding: 5px 10px !important; border-radius: 3px; 
        }

        /* Unified Asset Card Architecture */
        .asset-card { 
            background-color: #1c2128; border: 1px solid #30363d; 
            padding: 10px; border-radius: 4px; 
            height: 350px; /* Altura fija para uniformidad */
            display: flex; flex-direction: column; justify-content: space-between;
            text-align: center; margin-bottom: 15px;
        }
        .asset-card:hover { border: 1px solid #d4af37; background-color: #21262d; }
        
        /* Standardized Image Container */
        .img-slot {
            width: 100%; height: 160px; 
            overflow: hidden; border-radius: 2px;
            background-color: #000; display: flex; align-items: center; justify-content: center;
            margin-bottom: 5px;
        }
        .img-slot img { width: 100%; height: 100%; object-fit: cover; }

        .asset-title {
            font-size: 8.5px !important; font-weight: bold; color: #ffffff !important;
            margin: 5px 0 !important; line-height: 1.2; height: 35px;
            display: flex; align-items: center; justify-content: center;
            text-transform: uppercase;
        }

        /* Micro Buttons - Texto más pequeño para evitar desborde */
        .stButton>button { 
            width: 100%; font-size: 6.5px !important; height: 18px !important; 
            padding: 0px !important; background-color: #000000; color: #d4af37; 
            border: 1px solid #444; margin-bottom: 2px; text-transform: uppercase;
        }
        .stButton>button:hover { border-color: #d4af37; color: #fff; background-color: #d4af3722; }
        
        /* Sidebar Styles */
        section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #d4af37; }
        
        /* Eliminar espacios vacíos de st.image nativo */
        [data-testid="stImage"] { margin-bottom: 0px !important; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="NEXUS | APEX SYSTEM", page_icon="🏛️", layout="wide")
apply_theme()

# --- HELPERS ---
def generate_asset_hash(asset_id, sovereign):
    return hashlib.sha256(f"{asset_id}-{sovereign}-2026-DELPHIA".encode()).hexdigest()[:24].upper()

def create_pdf_certificate(asset_name, asset_id, sovereign, value, a_hash):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(12, 14, 18)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(212, 175, 55)
    pdf.set_font("Courier", "B", 24)
    pdf.cell(190, 40, "DELPHIA NEXUS SYSTEM", 0, 1, "C")
    pdf.ln(20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "", 12)
    pdf.cell(190, 10, f"ASSET: {asset_name}", 0, 1, "L")
    pdf.cell(190, 10, f"ID: {asset_id}", 0, 1, "L")
    pdf.cell(190, 10, f"VALUE: {value} DPX", 0, 1, "L")
    pdf.ln(20)
    pdf.set_text_color(212, 175, 55)
    pdf.multi_cell(190, 10, f"HASH: {a_hash}", 0, "C")
    return pdf.output(dest='S').encode('latin-1')

# 2. CONFIGURATION & DATA
TIERS = {
    "Arquitecto": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Delphi": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Matriarca": {"LTV": 0.70, "Interest": 0.025, "Label": "TIER II - NOBLE"}
}
USERS = {"Arquitecto": "ROOT_777", "Delphi": "OMEGA_999", "Matriarca": "M_2026"}

if "authenticated" not in st.session_state: st.session_state["authenticated"] = False

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
    
    # 4. HEADER
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

    # 5. ASSET GRID (6 COLUMNS)
    cols = st.columns(6)
    for i, (_, asset) in enumerate(user_assets.iterrows()):
        with cols[i % 6]:
            folder = asset['Soberano'].replace(" ", "_")
            asset_clean_name = str(asset['Asset']).split('.')[0]
            base_dir = f"Boveda_Activos/{folder}/"
            img_to_show = None
            if os.path.exists(base_dir):
                files = os.listdir(base_dir)
                for f in files:
                    if f.startswith(asset_clean_name) and f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        img_to_show = base_dir + f
                        break

            # Card Architecture
            st.markdown('<div class="asset-card">', unsafe_allow_html=True)
            
            # Slot de imagen/icono único para evitar duplicados
            if img_to_show:
                st.image(img_to_show, use_column_width=True)
            else:
                icon = "📄" if ".pdf" in str(asset['Asset']).lower() else "💎"
                st.markdown(f"<div class='img-slot'><span style='font-size:40px;'>{icon}</span></div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='asset-title'>{asset['Asset']}</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#d4af37; font-weight:bold; font-size:11px; margin:0;'>{asset['Value']:,.0f} DPX</p>", unsafe_allow_html=True)
            
            # Botones compactos
            b_top = st.columns(2)
            if b_top[0].button("TITLE", key=f"t_{asset['Asset_ID']}"): st.session_state['op'] = ('TITLE', asset)
            if b_top[1].button("SPLIT", key=f"f_{asset['Asset_ID']}"): st.session_state['op'] = ('SPLIT', asset)
            b_bot = st.columns(2)
            if b_bot[0].button("LOAN", key=f"c_{asset['Asset_ID']}"): st.session_state['op'] = ('LOAN', asset)
            if b_bot[1].button("SELL", key=f"v_{asset['Asset_ID']}"): st.session_state['op'] = ('SELL', asset)
            st.markdown('</div>', unsafe_allow_html=True)

    # 6. TRANSACTION TERMINAL
    if 'op' in st.session_state:
        mode, data = st.session_state['op']
        with st.sidebar:
            st.markdown(f"### ⚡ TERMINAL: {mode}")
            st.divider()
            
            if mode == 'TITLE':
                a_hash = generate_asset_hash(data['Asset_ID'], user)
                st.markdown(f"<div style='border:1px solid #d4af37; padding:10px; background:#111; font-family:monospace; font-size:9px;'>HASH: {a_hash}<br>STATUS: SECURED</div>", unsafe_allow_html=True)
                if 'FPDF' in globals():
                    pdf_data = create_pdf_certificate(data['Asset'], data['Asset_ID'], user, data['Value'], a_hash)
                    st.download_button("DOWNLOAD CERTIFICATE", data=pdf_data, file_name=f"CERT_{data['Asset_ID']}.pdf", mime="application/pdf")
            elif mode == 'LOAN':
                max_l = data['Value'] * tier_data['LTV']
                st.metric("LOAN POTENTIAL", f"{max_l:,.0f} DPX")
                if st.button("EXECUTE"): st.success("LIQUIDITY SENT")
            elif mode == 'SPLIT':
                st.number_input("Units", min_value=2, value=100)
                if st.button("PROCESS"): st.info("Splitting Asset...")
            elif mode == 'SELL':
                st.number_input("Price", value=float(data['Value']))
                if st.button("LIST"): st.success("Listed on Market")

            if st.button("CLOSE"):
                del st.session_state['op']
                st.rerun()