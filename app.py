import streamlit as st
import pandas as pd
import os
import hashlib
from fpdf import FPDF
import io

# 1. APEX STELLAR AESTHETICS
def apply_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

        html, body, [data-testid="stAppViewContainer"] { 
            font-size: 11px !important; 
            background-color: #0c0e12; 
        }
        .stApp { background-color: #0c0e12; color: #d4af37; }
        
        /* ── FIX: Eliminar el cuadro gris fantasma encima de imágenes ── */
        [data-testid="stImage"] {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 0 !important;
            font-size: 0 !important;
        }
        /* Eliminar el wrapper invisible de Streamlit que genera espacio extra */
        div[data-testid="stVerticalBlock"] > div:has([data-testid="stImage"]) {
            gap: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        /* Suprimir cualquier elemento vacío antes de la imagen */
        .element-container:empty { display: none !important; }
        .element-container { margin-bottom: 0 !important; padding: 0 !important; }
        
        /* Metrics Header */
        div[data-testid="stMetricLabel"] > div { color: #d4af37 !important; font-weight: bold !important; font-size: 10px !important; font-family: 'Rajdhani', sans-serif; letter-spacing: 1px; }
        div[data-testid="stMetricValue"] > div { color: #ffffff !important; font-size: 16px !important; font-family: 'Cinzel', serif; }
        div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #d4af37; padding: 5px 10px !important; border-radius: 3px; }

        /* Asset Card */
        .asset-card { 
            background-color: #1c2128; border: 1px solid #30363d; 
            padding: 10px; border-radius: 4px; 
            height: 380px; 
            display: flex; flex-direction: column; justify-content: space-between;
            text-align: center; margin-bottom: 15px;
            overflow: hidden;
        }
        .asset-card:hover { border: 1px solid #d4af37; background-color: #21262d; }
        
        /* Image Container */
        .img-container {
            width: 100%; height: 180px; 
            overflow: hidden; border-radius: 2px;
            background-color: #111; display: flex; align-items: center; justify-content: center;
            margin-bottom: 5px;
        }
        [data-testid="stImage"] img {
            height: 180px !important;
            width: 100% !important;
            object-fit: cover !important;
            border-radius: 2px;
            display: block !important;
        }

        .asset-title {
            font-size: 9px !important; font-weight: bold; color: #ffffff !important;
            margin: 8px 0 !important; line-height: 1.2; height: 30px;
            display: flex; align-items: center; justify-content: center;
            text-transform: uppercase; overflow: hidden;
            font-family: 'Rajdhani', sans-serif; letter-spacing: 1px;
        }

        /* Buttons */
        .stButton>button { 
            width: 100%; font-size: 7px !important; height: 20px !important; 
            padding: 0px !important; background-color: #000000; color: #d4af37; 
            border: 1px solid #444; margin-bottom: 2px; text-transform: uppercase;
            font-family: 'Rajdhani', sans-serif; letter-spacing: 1px;
            transition: all 0.2s ease;
        }
        .stButton>button:hover { border-color: #d4af37; color: #fff; background-color: #d4af3722; }

        /* ── SIDEBAR TERMINAL STYLES ── */
        section[data-testid="stSidebar"] { 
            background-color: #000000 !important; 
            border-right: 1px solid #d4af37; 
        }
        section[data-testid="stSidebar"] h3 {
            font-family: 'Cinzel', serif !important;
            color: #d4af37 !important;
            font-size: 14px !important;
            letter-spacing: 2px;
        }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div {
            color: #ffffff !important;
            font-family: 'Rajdhani', sans-serif;
        }
        section[data-testid="stSidebar"] .stMetric {
            background-color: #0d1117 !important;
            border: 1px solid #d4af37 !important;
            border-radius: 3px;
        }
        section[data-testid="stSidebar"] [data-testid="stMetricValue"] > div {
            color: #d4af37 !important;
        }
        section[data-testid="stSidebar"] .stButton>button {
            font-size: 9px !important;
            height: 28px !important;
            letter-spacing: 2px;
            font-weight: 700;
        }
        /* Primary action button in sidebar */
        section[data-testid="stSidebar"] .stButton>button[kind="primary"],
        section[data-testid="stSidebar"] .primary-btn button {
            background-color: #d4af37 !important;
            color: #000 !important;
            border-color: #d4af37 !important;
        }
        section[data-testid="stSidebar"] .stNumberInput input {
            background-color: #0d1117 !important;
            color: #ffffff !important;
            border: 1px solid #444 !important;
            font-family: 'Rajdhani', sans-serif;
        }
        section[data-testid="stSidebar"] .stDownloadButton>button {
            background-color: #d4af37 !important;
            color: #000 !important;
            border: none !important;
            font-weight: 700 !important;
            letter-spacing: 2px;
            font-size: 9px !important;
            height: 30px !important;
            width: 100%;
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
        .warn-box {
            border: 1px solid #ff6b35;
            padding: 8px 12px;
            background: #1a0a00;
            font-family: 'Rajdhani', sans-serif;
            font-size: 9px;
            color: #ff9966;
            border-radius: 3px;
            letter-spacing: 1px;
            line-height: 1.6;
        }
        .success-box {
            border: 1px solid #39d353;
            padding: 8px 12px;
            background: #0a1a0a;
            font-family: 'Rajdhani', sans-serif;
            font-size: 9px;
            color: #39d353;
            border-radius: 3px;
            letter-spacing: 1px;
        }
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

    # ── Fondo negro total ──
    pdf.set_fill_color(5, 5, 10)
    pdf.rect(0, 0, 210, 297, 'F')

    # ── Marco dorado exterior ──
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(1.2)
    pdf.rect(8, 8, 194, 281)

    # ── Marco interior fino ──
    pdf.set_line_width(0.3)
    pdf.rect(12, 12, 186, 273)

    # ── Franja superior decorativa ──
    pdf.set_fill_color(212, 175, 55)
    pdf.rect(12, 12, 186, 0.5, 'F')
    pdf.rect(12, 285, 186, 0.5, 'F')

    # ── ENCABEZADO: KARDASHEV VI ──
    pdf.set_text_color(212, 175, 55)
    pdf.set_font("Courier", "B", 7)
    pdf.set_xy(12, 18)
    pdf.cell(186, 4, "K A R D A S H E V   V I   |   C I V I L I Z A T I O N   A S S E T   P R O T O C O L", 0, 1, "C")

    pdf.set_line_width(0.2)
    pdf.set_draw_color(212, 175, 55)
    pdf.line(20, 26, 190, 26)

    # ── Título principal ──
    pdf.set_xy(12, 30)
    pdf.set_font("Courier", "B", 20)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(186, 12, "DELPHIA NEXUS", 0, 1, "C")

    pdf.set_xy(12, 42)
    pdf.set_font("Courier", "B", 9)
    pdf.set_text_color(180, 150, 40)
    pdf.cell(186, 6, "S O V E R E I G N   O W N E R S H I P   C E R T I F I C A T E", 0, 1, "C")

    pdf.line(20, 52, 190, 52)

    # ── Sello central decorativo ──
    pdf.set_xy(85, 56)
    pdf.set_font("Courier", "B", 28)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(40, 14, "◈", 0, 1, "C")

    # ── Bloque de datos ──
    fields = [
        ("ASSET DESIGNATION", str(asset_name).upper()),
        ("REGISTRY CODE", str(asset_id).upper()),
        ("SOVEREIGN CUSTODIAN", str(sovereign).upper()),
        ("APPRAISED VALUATION", f"{float(value):,.0f}  DPX"),
        ("LEDGER EPOCH", "2026 · TRUTH LEDGER v7"),
        ("CLASSIFICATION", "TIER I — IMMUTABLE ASSET"),
    ]

    y_start = 76
    for label, val in fields:
        # Línea label
        pdf.set_xy(25, y_start)
        pdf.set_font("Courier", "", 6)
        pdf.set_text_color(140, 110, 30)
        pdf.cell(160, 4, label, 0, 1, "L")
        # Línea valor
        pdf.set_xy(25, y_start + 4)
        pdf.set_font("Courier", "B", 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(160, 6, val, 0, 1, "L")
        # Separador
        pdf.set_draw_color(50, 45, 35)
        pdf.set_line_width(0.1)
        pdf.line(25, y_start + 11, 185, y_start + 11)
        y_start += 15

    # ── Hash de verificación ──
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

    # ── Firma / sello final ──
    pdf.line(20, y_start + 32, 190, y_start + 32)
    pdf.set_xy(12, y_start + 34)
    pdf.set_font("Courier", "I", 6)
    pdf.set_text_color(80, 70, 40)
    pdf.cell(186, 4, "This certificate constitutes an immutable record on the Delphia Truth Ledger.", 0, 1, "C")
    pdf.set_xy(12, y_start + 38)
    pdf.cell(186, 4, "Unauthorized duplication voids sovereign claim · KARDASHEV VI PROTOCOL ACTIVE", 0, 1, "C")

    # ── Número de serie esquinas ──
    serial = f"DPX-{a_hash[:8]}"
    pdf.set_font("Courier", "", 5)
    pdf.set_text_color(60, 55, 30)
    pdf.set_xy(14, 278)
    pdf.cell(40, 4, serial, 0, 0, "L")
    pdf.set_xy(156, 278)
    pdf.cell(40, 4, serial, 0, 0, "R")

    return pdf.output(dest='S').encode('latin-1')


# 2. CONFIGURATION & DATA
TIERS = {
    "Arquitecto": {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Delphi":     {"LTV": 0.90, "Interest": 0.005, "Label": "TIER I - SOVEREIGN"},
    "Matriarca":  {"LTV": 0.70, "Interest": 0.025, "Label": "TIER II - NOBLE"}
}
USERS = {"Arquitecto": "ROOT_777", "Delphi": "OMEGA_999", "Matriarca": "M_2026"}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🏛️ NEXUS | SYSTEM ACCESS")
    u = st.selectbox("Select Identity", list(USERS.keys()))
    p = st.text_input("Access Key", type="password")
    if st.button("SYNC"):
        if USERS[u] == p:
            st.session_state["authenticated"], st.session_state["user"] = True, u
            st.rerun()
else:
    # 3. DATA LOAD
    ledger   = pd.read_csv("Truth_Ledger_Master.csv").rename(columns={'Nombre': 'Asset'})
    accounts = pd.read_csv("Delphia_Bank_Accounts.csv")
    ledger['Value'] = pd.to_numeric(
        ledger['Valor'].astype(str).replace('[\$,]', '', regex=True), errors='coerce'
    ).fillna(0)

    user       = st.session_state["user"]
    tier_data  = TIERS.get(user, TIERS["Arquitecto"])
    user_assets = (
        ledger if user in ["Arquitecto", "Delphi"]
        else ledger[ledger['Soberano'].str.contains(user, na=False)]
    )

    # 4. HEADER
    acc_row = accounts[accounts['Soberano'].str.contains(user, na=False)]
    balance = acc_row['Saldo_DPX'].values[0] if not acc_row.empty else 0.0

    c_head = st.columns([3, 1, 1, 1, 1])
    c_head[0].markdown(f"### 🏛️ {user} | {tier_data['Label']}")
    c_head[1].metric("BANK BALANCE",         f"{balance:,.0f} DPX")
    c_head[2].metric("TOTAL ASSETS",         f"{user_assets['Value'].sum():,.0f} DPX")
    c_head[3].metric("CREDIT LINE AVAILABLE", f"{(user_assets['Value'].sum() * tier_data['LTV']):,.0f} DPX")
    if c_head[4].button("LOGOUT"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.divider()

    # 5. ASSET GRID (6 COLUMNS)
    cols = st.columns(6)
    for i, (_, asset) in enumerate(user_assets.iterrows()):
        with cols[i % 6]:
            folder          = asset['Soberano'].replace(" ", "_")
            asset_clean_name = str(asset['Asset']).split('.')[0]
            base_dir        = f"Boveda_Activos/{folder}/"
            img_to_show     = None

            if os.path.exists(base_dir):
                for f in os.listdir(base_dir):
                    if f.startswith(asset_clean_name) and f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        img_to_show = base_dir + f
                        break

            # ── Card ──
            st.markdown('<div class="asset-card">', unsafe_allow_html=True)

            if img_to_show:
                # use_container_width evita el div fantasma que genera use_column_width
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

            b1, b2 = st.columns(2)
            if b1.button("TITLE", key=f"t_{asset['Asset_ID']}"): st.session_state['op'] = ('TITLE', asset)
            if b2.button("SPLIT", key=f"f_{asset['Asset_ID']}"): st.session_state['op'] = ('SPLIT', asset)
            b3, b4 = st.columns(2)
            if b3.button("LOAN",  key=f"c_{asset['Asset_ID']}"): st.session_state['op'] = ('LOAN',  asset)
            if b4.button("SELL",  key=f"v_{asset['Asset_ID']}"): st.session_state['op'] = ('SELL',  asset)

            st.markdown('</div>', unsafe_allow_html=True)

    # 6. TRANSACTION TERMINAL (SIDEBAR)
    if 'op' in st.session_state:
        mode, data = st.session_state['op']
        with st.sidebar:
            st.markdown(f"### ⚡ TERMINAL: {mode}")
            st.divider()

            # ── Datos base del activo ──
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

            # ════════════════════════════════
            if mode == 'TITLE':
                a_hash = generate_asset_hash(data['Asset_ID'], user)

                st.markdown(
                    f"<div class='terminal-box'>"
                    f"<span class='terminal-label'>SOVEREIGN OWNER</span><br>"
                    f"<span class='terminal-value'>{user}</span><br><br>"
                    f"<span class='terminal-label'>TIER STATUS</span><br>"
                    f"<span class='terminal-value' style='color:#d4af37;'>{tier_data['Label']}</span><br><br>"
                    f"<span class='terminal-label'>VERIFICATION HASH · SHA-256</span><br>"
                    f"<span style='color:#d4af37; font-family:monospace; font-size:8px; word-break:break-all;'>{a_hash}</span><br><br>"
                    f"<span class='terminal-label'>LEDGER STATUS</span><br>"
                    f"<span style='color:#39d353; font-weight:bold;'>● SECURED · IMMUTABLE</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                pdf_data = create_pdf_certificate(
                    data['Asset'], data['Asset_ID'], user, data['Value'], a_hash
                )
                st.download_button(
                    "⬇ DOWNLOAD CERTIFICATE · PDF",
                    data=pdf_data,
                    file_name=f"CERT_{data['Asset_ID']}.pdf",
                    mime="application/pdf"
                )

            # ════════════════════════════════
            elif mode == 'SPLIT':
                asset_value = data['Value']
                u_split = st.number_input(
                    "Fracciones a generar", min_value=2, max_value=10000, value=100,
                    help="Número de unidades soberanas en que se dividirá el activo"
                )
                fraction_value = asset_value / u_split if u_split > 0 else 0

                st.markdown(
                    f"<div class='terminal-box'>"
                    f"<span class='terminal-label'>VALOR TOTAL DEL ACTIVO</span><br>"
                    f"<span class='terminal-value' style='color:#d4af37;'>{asset_value:,.2f} DPX</span><br><br>"
                    f"<span class='terminal-label'>FRACCIONES A GENERAR</span><br>"
                    f"<span class='terminal-value'>{u_split:,} unidades</span><br><br>"
                    f"<span class='terminal-label'>VALOR POR FRACCIÓN INDIVIDUAL</span><br>"
                    f"<span class='terminal-value' style='color:#d4af37; font-size:15px;'>{fraction_value:,.4f} DPX</span><br><br>"
                    f"<hr class='gold-divider'>"
                    f"<span class='terminal-label'>PROTOCOLO</span><br>"
                    f"<span style='color:#aaa; font-size:8px;'>Re-Ledgering soberano · cada fracción es un activo independiente registrado en el Truth Ledger</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    "<div class='warn-box'>⚠ ESTA OPERACIÓN ES IRREVERSIBLE<br>"
                    "El activo original será reemplazado por las fracciones en el Ledger.</div>",
                    unsafe_allow_html=True
                )

                if st.button("⚡ EXECUTE RE-LEDGERING"):
                    st.markdown(
                        f"<div class='success-box'>✔ RE-LEDGERING INICIADO<br>"
                        f"{u_split:,} fracciones de {fraction_value:,.4f} DPX c/u registradas.</div>",
                        unsafe_allow_html=True
                    )

            # ════════════════════════════════
            elif mode == 'LOAN':
                asset_value = data['Value']
                ltv_pct     = tier_data['LTV']
                max_loan    = asset_value * ltv_pct
                interest    = tier_data['Interest']

                st.markdown(
                    f"<div class='terminal-box'>"
                    f"<span class='terminal-label'>TIER</span><br>"
                    f"<span class='terminal-value' style='color:#d4af37;'>{tier_data['Label']}</span><br><br>"
                    f"<span class='terminal-label'>LOAN-TO-VALUE RATIO</span><br>"
                    f"<span class='terminal-value' style='color:#d4af37; font-size:18px;'>{ltv_pct*100:.0f}%</span>"
                    f" <span style='color:#888; font-size:8px;'>del valor del activo</span><br><br>"
                    f"<span class='terminal-label'>CRÉDITO MÁXIMO DISPONIBLE</span><br>"
                    f"<span class='terminal-value' style='color:#ffffff; font-size:16px;'>{max_loan:,.0f} DPX</span><br><br>"
                    f"<span class='terminal-label'>TASA DE INTERÉS ANUAL</span><br>"
                    f"<span class='terminal-value'>{interest*100:.2f}%</span><br><br>"
                    f"<hr class='gold-divider'>"
                    f"<span class='terminal-label'>GARANTÍA</span><br>"
                    f"<span style='color:#aaa; font-size:8px;'>El activo quedará bloqueado en bóveda durante la vigencia del crédito.</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                if st.button("⚡ EXECUTE INSTANT LOAN"):
                    st.markdown(
                        f"<div class='success-box'>✔ LIQUIDEZ INYECTADA<br>"
                        f"{max_loan:,.0f} DPX acreditados · Activo bloqueado en Bóveda.</div>",
                        unsafe_allow_html=True
                    )

            # ════════════════════════════════
            elif mode == 'SELL':
                list_price = st.number_input(
                    "Precio de lista (DPX)", value=float(data['Value']), min_value=0.0, step=100.0
                )
                st.markdown(
                    f"<div class='terminal-box'>"
                    f"<span class='terminal-label'>MARKETPLACE DESTINO</span><br>"
                    f"<span class='terminal-value'>DELPHIA OPEN MARKET</span><br><br>"
                    f"<span class='terminal-label'>PRECIO DE LISTA</span><br>"
                    f"<span class='terminal-value' style='color:#d4af37;'>{list_price:,.0f} DPX</span><br><br>"
                    f"<hr class='gold-divider'>"
                    f"<span style='color:#aaa; font-size:8px;'>Al confirmar, el activo será visible para todos los participantes soberanos del mercado. "
                    f"Permanecerá en tu bóveda hasta que se complete la transacción.</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                if st.button("📡 CONFIRM LISTING · BROADCAST"):
                    st.markdown(
                        "<div class='success-box'>✔ ACTIVO PUBLICADO<br>"
                        "Broadcast al Open Market completado. Visible para compradores soberanos.</div>",
                        unsafe_allow_html=True
                    )

            # ── Cerrar terminal ──
            st.divider()
            if st.button("✕  CLOSE TERMINAL"):
                del st.session_state['op']
                st.rerun()