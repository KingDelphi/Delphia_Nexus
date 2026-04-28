import streamlit as st
import pandas as pd
import os
import hashlib
from fpdf import FPDF
import io
import base64

# =============================================
# 1. CONFIGURACIÓN INICIAL Y TEMA VISUAL (APEX STELLAR AESTHETICS)
# =============================================
def apply_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            font-size: 11px !important;
            background-color: #0c0e12;
        }
        .stApp { 
            background-color: #0c0e12; 
            color: #d4af37; 
        }

        /* FIX HEADER METRICS: BLANCO Y DORADO */
        [data-testid="stMetricValue"] {
            color: #d4af37 !important;
            font-family: 'Cinzel', serif !important;
            font-size: 1.8rem !important;
        }
        [data-testid="stMetricLabel"] p {
            color: #ffffff !important;
            font-family: 'Rajdhani', sans-serif !important;
            letter-spacing: 1.5px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
        }

        /* =============================================
           FIX PRINCIPAL: ELIMINAR CAJAS VACÍAS (FRAMES)
           ============================================= */
        /* Eliminamos el espacio entre elementos de Streamlit dentro de las columnas */
        [data-testid="stVerticalBlock"] > div {
            gap: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .element-container {
            margin-bottom: 0 !important;
        }

        /* Ocultar contenedores de markdown vacíos que generan las cajas fantasma */
        .element-container:has(div:empty) {
            display: none !important;
        }

        /* Asset Card Architecture */
        .asset-card {
            background-color: #1c2128; 
            border: 1px solid #30363d;
            padding: 8px; 
            border-radius: 4px;
            height: 385px;
            display: flex; 
            flex-direction: column; 
            justify-content: space-between;
            text-align: center; 
            margin-bottom: 15px;
            overflow: hidden;
            position: relative;
            z-index: 1;
        }
        .asset-card:hover { 
            border: 1px solid #d4af37; 
            background-color: #21262d; 
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
        }

        .img-container {
            width: 100%; 
            height: 180px;
            overflow: hidden; 
            border-radius: 2px;
            background-color: #111; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            margin-bottom: 8px;
        }
        
        [data-testid="stImage"] img {
            height: 180px !important;
            width: 100% !important;
            object-fit: cover !important;
            border-radius: 2px;
            display: block !important;
            margin-top: 0 !important;
        }

        .asset-title {
            font-size: 9px !important; 
            font-weight: bold; 
            color: #ffffff !important;
            margin: 8px 0 !important; 
            line-height: 1.2; 
            height: 30px;
            display: flex; 
            align-items: center; 
            justify-content: center;
            text-transform: uppercase; 
            overflow: hidden;
            font-family: 'Rajdhani', sans-serif; 
            letter-spacing: 1px;
        }

        /* Buttons Aesthetic */
        .stButton>button {
            width: 100%; 
            font-size: 7px !important; 
            height: 20px !important;
            padding: 0px !important; 
            background-color: #000000; 
            color: #d4af37;
            border: 1px solid #444; 
            margin-bottom: 2px; 
            text-transform: uppercase;
            font-family: 'Rajdhani', sans-serif; 
            letter-spacing: 1px;
            transition: all 0.2s ease;
        }
        .stButton>button:hover { 
            border-color: #d4af37; 
            color: #fff; 
            background-color: #d4af3722; 
        }

        /* Terminal Close Button (Upper Right) */
        .close-container {
            display: flex;
            justify-content: flex-end;
            margin-bottom: -35px;
        }

        /* Sidebar Terminal Styles */
        section[data-testid="stSidebar"] {
            background-color: #000000 !important;
            border-left: 1px solid #d4af37;
        }
        section[data-testid="stSidebar"] h3 {
            font-family: 'Cinzel', serif !important;
            color: #d4af37 !important;
            font-size: 14px !important;
            letter-spacing: 2px;
        }

        .terminal-box {
            border: 1px solid #d4af37;
            padding: 12px 14px;
            background: #0d1117;
            font-family: 'Courier New', monospace;
            font-size: 9px;
            color: #ffffff;
            border-radius: 3px;
            margin-bottom: 10px;
            line-height: 1.7;
        }
        .terminal-label {
            color: #d4af37;
            font-size: 8px;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 4px;
            font-family: 'Rajdhani', sans-serif;
        }
        .terminal-value {
            color: #ffffff;
            font-size: 11px;
            font-weight: bold;
        }
        .gold-divider {
            border: none;
            border-top: 1px solid #d4af37;
            margin: 10px 0;
            opacity: 0.4;
        }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="DELPHIA SOVEREIGN NEXUS | APEX SYSTEM_v12.0", page_icon="🏛️", layout="wide")
apply_theme()

# =============================================
# 2. HELPERS Y FUNCIONES AUXILIARES
# =============================================
def generate_asset_hash(asset_id, sovereign):
    return hashlib.sha256(f"{asset_id}-{sovereign}-2026-DELPHIA".encode()).hexdigest()[:24].upper()

def create_pdf_certificate(asset_name, asset_id, sovereign, value, a_hash):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(5, 5, 10)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(1.2)
    pdf.rect(8, 8, 194, 281)
    pdf.set_line_width(0.3)
    pdf.rect(12, 12, 186, 273)
    pdf.set_fill_color(212, 175, 55)
    pdf.rect(12, 12, 186, 0.5, 'F')
    pdf.rect(12, 285, 186, 0.5, 'F')

    pdf.set_text_color(212, 175, 55)
    pdf.set_font("Courier", "B", 7)
    pdf.set_xy(12, 18)
    pdf.cell(186, 4, "K A R D A S H E V V I | C I V I L I Z A T I O N A S S E T P R O T O C O L", 0, 1, "C")
    pdf.line(20, 26, 190, 26)

    pdf.set_xy(12, 30)
    pdf.set_font("Courier", "B", 20)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(186, 12, "DELPHIA NEXUS", 0, 1, "C")
    pdf.set_xy(12, 42)
    pdf.set_font("Courier", "B", 9)
    pdf.set_text_color(180, 150, 40)
    pdf.cell(186, 6, "S O V E R E I G N O W N E R S H I P C E R T I F I C A T E", 0, 1, "C")
    pdf.line(20, 52, 190, 52)

    pdf.set_xy(85, 56)
    pdf.set_font("Courier", "B", 28)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(40, 14, "◈", 0, 1, "C")

    fields = [
        ("ASSET DESIGNATION", str(asset_name).upper()),
        ("REGISTRY CODE", str(asset_id).upper()),
        ("SOVEREIGN CUSTODIAN", str(sovereign).upper()),
        ("APPRAISED VALUATION", f"{float(value):,.0f} DPX"),
        ("LEDGER EPOCH", "2026 · TRUTH LEDGER v7"),
        ("CLASSIFICATION", "TIER I — IMMUTABLE ASSET"),
    ]
    y_start = 76
    for label, val in fields:
        pdf.set_xy(25, y_start)
        pdf.set_font("Courier", "", 6)
        pdf.set_text_color(140, 110, 30)
        pdf.cell(160, 4, label, 0, 1, "L")
        pdf.set_xy(25, y_start + 4)
        pdf.set_font("Courier", "B", 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(160, 6, val, 0, 1, "L")
        pdf.set_draw_color(50, 45, 35)
        pdf.set_line_width(0.1)
        pdf.line(25, y_start + 11, 185, y_start + 11)
        y_start += 15

    pdf.set_xy(12, y_start + 5)
    pdf.set_fill_color(15, 12, 5)
    pdf.rect(18, y_start + 4, 174, 22, 'F')
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(0.4)
    pdf.rect(18, y_start + 4, 174, 22)
    pdf.set_xy(18, y_start + 6)
    pdf.set_font("Courier", "", 6)
    pdf.set_text_color(140, 110, 30)
    pdf.cell(174, 4, "CRYPTOGRAPHIC VERIFICATION HASH · SHA-256", 0, 1, "C")
    pdf.set_xy(18, y_start + 11)
    pdf.set_font("Courier", "B", 9)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(174, 8, a_hash, 0, 1, "C")

    pdf.line(20, y_start + 32, 190, y_start + 32)
    pdf.set_xy(12, y_start + 34)
    pdf.set_font("Courier", "I", 6)
    pdf.set_text_color(80, 70, 40)
    pdf.cell(186, 4, "This certificate constitutes an immutable record on the Delphia Truth Ledger.", 0, 1, "C")
    pdf.set_xy(12, y_start + 38)
    pdf.cell(186, 4, "Unauthorized duplication voids sovereign claim · KARDASHEV VI PROTOCOL ACTIVE", 0, 1, "C")

    serial = f"DPX-{a_hash[:8]}"
    pdf.set_font("Courier", "", 5)
    pdf.set_text_color(60, 55, 30)
    pdf.set_xy(14, 278)
    pdf.cell(40, 4, serial, 0, 0, "L")
    pdf.set_xy(156, 278)
    pdf.cell(40, 4, serial, 0, 0, "R")

    return pdf.output(dest='S').encode('latin-1')

# =============================================
# 3. CONFIGURACIÓN DE DATOS Y USUARIOS
# =============================================
TIERS = {
    "Arquitecto": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Delphi":     {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Matriarca":  {"LTV": 0.70, "Interest": 0.025, "Label": "TIER II - NOBLE"}
}

USERS = {"Arquitecto": "ROOT_777", "Delphi": "OMEGA_999", "Matriarca": "M_2026"}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# =============================================
# 4. AUTENTICACIÓN
# =============================================
if not st.session_state["authenticated"]:
    st.title("🏛️ NEXUS | SYSTEM ACCESS")
    u = st.selectbox("Select Identity", list(USERS.keys()))
    p = st.text_input("Access Key", type="password")
    if st.button("SYNC"):
        if USERS.get(u) == p:
            st.session_state["authenticated"] = True
            st.session_state["user"] = u
            st.rerun()
        else:
            st.error("Access Denied")
    st.stop()

# =============================================
# 5. CARGA DE DATOS
# =============================================
ledger = pd.read_csv("Truth_Ledger_Master.csv").rename(columns={'Nombre': 'Asset'})
accounts = pd.read_csv("Delphia_Bank_Accounts.csv")

ledger['Value'] = pd.to_numeric(
    ledger['Valor'].astype(str).replace('[\$,]', '', regex=True), 
    errors='coerce'
).fillna(0)

user = st.session_state["user"]
tier_data = TIERS.get(user, TIERS["Arquitecto"])

user_assets = (
    ledger if user in ["Arquitecto", "Delphi"]
    else ledger[ledger['Soberano'].str.contains(user, na=False)]
)

# =============================================
# 6. HEADER / DASHBOARD (COLORES CORREGIDOS)
# =============================================
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

# =============================================
# 7. ASSET GRID (6 COLUMNAS) - FIX FRAME VACÍO
# =============================================
cols = st.columns(6)

for i, (_, asset) in enumerate(user_assets.iterrows()):
    with cols[i % 6]:
        folder = asset['Soberano'].replace(" ", "_")
        asset_clean_name = str(asset['Asset']).split('.')[0]
        base_dir = f"Boveda_Activos/{folder}/"
        
        img_to_show = None
        if os.path.exists(base_dir):
            for f in os.listdir(base_dir):
                if f.startswith(asset_clean_name) and f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_to_show = base_dir + f
                    break

        # Renderizado de Tarjeta para evitar frames fantasmas
        st.markdown('<div class="asset-card">', unsafe_allow_html=True)
        
        if img_to_show:
            st.image(img_to_show, use_container_width=True)
        else:
            icon = "📄" if ".pdf" in str(asset['Asset']).lower() else "💎"
            st.markdown(
                f"<div class='img-container'><span style='font-size:40px;'>{icon}</span></div>",
                unsafe_allow_html=True
            )
        
        st.markdown(f"<div class='asset-title'>{asset['Asset']}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='color:#d4af37; font-weight:bold; font-size:11px; margin-bottom:10px;'>"
            f"{asset['Value']:,.0f} DPX</p>",
            unsafe_allow_html=True
        )
        
        # Botones de Acción
        b1, b2 = st.columns(2)
        if b1.button("📜 TITLE", key=f"t_{asset['Asset_ID']}"): 
            st.session_state['op'] = ('TITLE', asset)
        if b2.button("🔀 SPLIT", key=f"f_{asset['Asset_ID']}"): 
            st.session_state['op'] = ('SPLIT', asset)
        
        b3, b4 = st.columns(2)
        if b3.button("💰 LOAN", key=f"c_{asset['Asset_ID']}"): 
            st.session_state['op'] = ('LOAN', asset)
        if b4.button("🏷️ SELL", key=f"v_{asset['Asset_ID']}"): 
            st.session_state['op'] = ('SELL', asset)
        
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# 8. TRANSACTION TERMINAL (SIDEBAR) - VERSIÓN FINAL REPARADA
# =============================================
if 'op' in st.session_state:
    mode, data = st.session_state['op']
    with st.sidebar:
        # BOTÓN CERRAR SUPERIOR DERECHO
        st.markdown('<div class="close-container">', unsafe_allow_html=True)
        if st.button("✕", key="close_terminal_top"):
            del st.session_state['op']
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"### ⚡ TERMINAL: {mode}")
        st.divider()

        # Información básica del activo
        st.markdown(
            f"<div class='terminal-box'>"
            f"<span class='terminal-label'>ASSET</span><br>"
            f"<span class='terminal-value'>{data['Asset']}</span><br><br>"
            f"<span class='terminal-label'>REGISTRY ID</span><br>"
            f"<span class='terminal-value'>{data['Asset_ID']}</span><br><br>"
            f"<span class='terminal-label'>APPRAISED VALUE</span><br>"
            f"<span class='terminal-value' style='color:#d4af37;'>{data['Value']:,.0f} DPX</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        # ==================== TITLE (PDF FUNCIONAL) ====================
        if mode == 'TITLE':
            a_hash = generate_asset_hash(data['Asset_ID'], user)
            st.markdown(
                f"<div class='terminal-box'>"
                f"<span class='terminal-label'>SOVEREIGN OWNER</span><br>"
                f"<span class='terminal-value'>{user}</span><br><br>"
                f"<span class='terminal-label'>VERIFICATION HASH</span><br>"
                f"<span style='color:#d4af37; font-family:monospace; font-size:8px; word-break:break-all;'>{a_hash}</span><br><br>"
                f"<span class='terminal-label'>LEDGER STATUS</span><br>"
                f"<span style='color:#39d353; font-weight:bold;'>● SECURED · IMMUTABLE</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            # Generación y descarga de PDF vinculada correctamente
            pdf_bytes = create_pdf_certificate(
                data['Asset'], data['Asset_ID'], user, data['Value'], a_hash
            )
            
            st.download_button(
                label="⬇ DOWNLOAD SOVEREIGN TITLE",
                data=pdf_bytes,
                file_name=f"CERT_{data['Asset_ID']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # ==================== SPLIT (MÁRGENES CORREGIDOS) ====================
        elif mode == 'SPLIT':
            asset_value = data['Value']
            u_split = st.number_input(
                "Number of Fractions", 
                min_value=2, 
                max_value=10000, 
                value=100
            )
            
            fraction_value = asset_value / u_split if u_split > 0 else 0

            st.markdown(
                f"<div class='terminal-box'>"
                f"<span class='terminal-label'>VALUE PER INDIVIDUAL FRACTION</span><br>"
                f"<span class='terminal-value' style='color:#d4af37; font-size:15px;'>{fraction_value:,.2f} DPX</span><br>"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown('<div style="margin-top: 25px;">', unsafe_allow_html=True)
            if st.button("⚡ EXECUTE RE-LEDGERING", use_container_width=True):
                st.success(f"✔ RE-LEDGERING INITIATED: {u_split:,} units generated.")
            st.markdown('</div>', unsafe_allow_html=True)

        # ==================== LOAN ====================
        elif mode == 'LOAN':
            asset_value = data['Value']
            max_loan = asset_value * tier_data['LTV']

            st.markdown(
                f"<div class='terminal-box'>"
                f"<span class='terminal-label'>LOAN-TO-VALUE ({tier_data['LTV']*100:.0f}%)</span><br>"
                f"<span class='terminal-value' style='color:#ffffff; font-size:16px;'>{max_loan:,.0f} DPX</span><br><br>"
                f"<span class='terminal-label'>ANNUAL INTEREST</span><br>"
                f"<span class='terminal-value'>{tier_data['Interest']*100:.2f}%</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            if st.button("⚡ EXECUTE INSTANT LOAN", use_container_width=True):
                st.info("✔ LIQUIDITY INJECTED · ASSET LOCKED")

        # ==================== SELL ====================
        elif mode == 'SELL':
            list_price = st.number_input(
                "Listing Price (DPX)", 
                value=float(data['Value']), 
                min_value=0.0
            )

            st.markdown(
                f"<div class='terminal-box'>"
                f"<span class='terminal-label'>BROADCAST TARGET</span><br>"
                f"<span class='terminal-value'>DELPHIA OPEN MARKET</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            if st.button("📡 CONFIRM LISTING", use_container_width=True):
                st.success("✔ BROADCAST COMPLETED")