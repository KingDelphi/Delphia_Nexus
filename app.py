import streamlit as st
import pandas as pd
import os
import hashlib
import io
import tempfile
from fpdf import FPDF

# =============================================
# 1. CONFIGURACIÓN INICIAL Y TEMA VISUAL
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

        /* =============================================
           GRID SIMÉTRICA — SOLUCIÓN DEFINITIVA v17
           
           El problema real: Streamlit Cloud no respeta height
           en stVerticalBlockBorderWrapper porque el layout engine
           de React reescribe esas propiedades.
           
           Solución: envolvemos cada card en un div HTML de altura
           fija (card-shell) que SÍ respeta height, y dentro
           usamos position:relative para que los elementos de ST
           queden contenidos. Los botones se sacan del container
           y se renderizan fuera del div HTML (como hermanos),
           pero la VISUAL de la card la damos con el div.
           
           Para lograr una grid 100% simétrica usamos el truco
           de CSS Grid externo + cards de dimensiones absolutas.
        ============================================= */

        /* Reset agresivo del wrapper de ST */
        [data-testid="stVerticalBlockBorderWrapper"] {
            all: unset !important;
            display: block !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            all: unset !important;
            display: block !important;
        }

        /* La card visual real */
        .card-shell {
            background-color: #1c2128;
            border: 1px solid #30363d;
            border-radius: 4px;
            overflow: hidden;
            width: 100%;
            /* Altura fija en px — no rem, no %, no vh */
            height: 295px;
            display: flex;
            flex-direction: column;
            margin-bottom: 8px;
            box-sizing: border-box;
            transition: border-color 0.15s ease, background-color 0.15s ease;
            position: relative;
        }
        .card-shell:hover {
            border-color: #d4af37;
            background-color: #21262d;
        }

        /* Zona de imagen — altura fija 150px */
        .card-img-zone {
            width: 100%;
            height: 150px;
            min-height: 150px;
            max-height: 150px;
            overflow: hidden;
            flex-shrink: 0;
            background-color: #0d1117;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card-img-zone img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            object-position: center center;
            display: block;
        }

        /* Título */
        .card-title {
            font-size: 7px;
            font-weight: 700;
            color: #ffffff;
            text-transform: uppercase;
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 0.6px;
            text-align: center;
            padding: 4px 4px 0 4px;
            height: 22px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1.1;
        }

        /* Precio */
        .card-price {
            font-size: 9px;
            font-weight: 700;
            color: #d4af37;
            font-family: 'Cinzel', serif;
            text-align: center;
            padding: 1px 0 2px 0;
            height: 16px;
        }

        /* Zona de botones dentro de la card */
        .card-btns {
            padding: 0 4px 3px 4px;
            display: flex;
            flex-direction: column;
            gap: 2px;
            flex: 1;
            justify-content: flex-end;
        }
        .card-btn-row {
            display: flex;
            gap: 3px;
        }

        /* Botones ST dentro de la card-shell */
        [data-testid="stVerticalBlockBorderWrapper"] .stButton > button,
        .card-shell .stButton > button {
            font-size: 6px !important;
            height: 17px !important;
            padding: 0 !important;
            background-color: #000 !important;
            color: #d4af37 !important;
            border: 1px solid #2a2a2a !important;
            text-transform: uppercase !important;
            font-family: 'Rajdhani', sans-serif !important;
            letter-spacing: 0.5px !important;
            line-height: 1 !important;
            width: 100% !important;
            transition: border-color 0.15s ease !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {
            border-color: #d4af37 !important;
            color: #fff !important;
            background-color: #d4af3710 !important;
        }

        /* Override ST image dentro de card */
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"],
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] img {
            margin: 0 !important;
            padding: 0 !important;
            display: block !important;
            width: 100% !important;
            height: 150px !important;
            object-fit: cover !important;
            object-position: center center !important;
            line-height: 0 !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"] .element-container {
            margin: 0 !important;
            padding: 0 !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
        }

        /* Botones globales (sidebar y header) */
        .stButton > button {
            font-size: 7px !important;
            height: 20px !important;
            padding: 0 !important;
            background-color: #000;
            color: #d4af37;
            border: 1px solid #444;
            text-transform: uppercase;
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 1px;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            border-color: #d4af37;
            color: #fff;
            background-color: #d4af3722;
        }

        /* MÉTRICAS */
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] {
            color: #ffffff !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-size: 9px !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
        }
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] > div {
            color: #d4af37 !important;
            font-family: 'Cinzel', serif !important;
            font-size: 15px !important;
            font-weight: 700 !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #000000 !important;
            border-right: 1px solid #d4af37;
            z-index: 100 !important;
        }
        section[data-testid="stSidebar"] h3 {
            font-family: 'Cinzel', serif !important;
            color: #d4af37 !important;
            font-size: 14px !important;
            letter-spacing: 2px;
        }

        /* Terminal */
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
        .split-spacer { height: 12px; }

        /* Download button en sidebar */
        section[data-testid="stSidebar"] [data-testid="stDownloadButton"] button {
            background-color: #1a1400 !important;
            color: #d4af37 !important;
            border: 1px solid #d4af37 !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-size: 8px !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            height: 28px !important;
            width: 100% !important;
        }
        section[data-testid="stSidebar"] [data-testid="stDownloadButton"] button:hover {
            background-color: #d4af3722 !important;
            color: #ffffff !important;
        }

        /* =============================================
           UPLOAD MODAL
        ============================================= */
        .upload-section {
            background: #0d1117;
            border: 1px solid #d4af37;
            border-radius: 4px;
            padding: 16px;
            margin-bottom: 12px;
        }
        .upload-title {
            font-family: 'Cinzel', serif;
            color: #d4af37;
            font-size: 11px;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        /* =============================================
           MARKETPLACE PANEL
        ============================================= */
        .market-card {
            background: #1c2128;
            border: 1px solid #30363d;
            border-radius: 4px;
            padding: 10px;
            margin-bottom: 8px;
            transition: border-color 0.15s ease;
        }
        .market-card:hover { border-color: #d4af37; }
        .market-badge {
            display: inline-block;
            background: #d4af3722;
            color: #d4af37;
            border: 1px solid #d4af37;
            border-radius: 2px;
            font-size: 7px;
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 1px;
            padding: 1px 5px;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .market-badge.locked {
            background: #ff6b3522;
            color: #ff9966;
            border-color: #ff6b35;
        }
        </style>
    """, unsafe_allow_html=True)


st.set_page_config(
    page_title="DELPHIA SOVEREIGN NEXUS | APEX SYSTEM_v17.0",
    page_icon="🏛️",
    layout="wide"
)
apply_theme()


# =============================================
# 2. HELPERS
# =============================================
def generate_asset_hash(asset_id, sovereign):
    return hashlib.sha256(
        f"{asset_id}-{sovereign}-2026-DELPHIA".encode()
    ).hexdigest()[:24].upper()


def generate_asset_id(name, sovereign):
    """Genera un Asset_ID único tipo DLPH-XXXXXXXX"""
    raw = f"{name}-{sovereign}-{pd.Timestamp.now().isoformat()}"
    return "DLPH-" + hashlib.sha256(raw.encode()).hexdigest()[:8].upper()


def create_pdf_certificate(asset_name, asset_id, sovereign, value, a_hash):
    """
    PDF con Unicode activado (uni=True en FPDF).
    Esto resuelve el error latin-1 con caracteres como ♦ (u2666).
    Exporta via archivo temporal para garantizar bytes puros.
    """
    # uni=True activa soporte UTF-8 completo en fpdf (legacy)
    # En fpdf2 >= 2.x ya no existe uni=True; el UTF-8 es nativo.
    # Detectamos la versión para compatibilidad total.
    try:
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        # fpdf2 >= 2.x: UTF-8 nativo, no necesita uni=True
        # Simplemente evitamos el símbolo ◈ (U+25C8) y usamos [*] ASCII
        _fpdf2 = True
    except Exception:
        _fpdf2 = False

    pdf.add_page()
    pdf.set_auto_page_break(False)

    # Fondo
    pdf.set_fill_color(5, 5, 10)
    pdf.rect(0, 0, 210, 297, 'F')

    # Marcos
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(1.2)
    pdf.rect(8, 8, 194, 281)
    pdf.set_line_width(0.3)
    pdf.rect(12, 12, 186, 273)
    pdf.set_fill_color(212, 175, 55)
    pdf.rect(12, 12, 186, 0.5, 'F')
    pdf.rect(12, 285, 186, 0.5, 'F')

    # Encabezado
    pdf.set_text_color(212, 175, 55)
    pdf.set_font("Courier", "B", 7)
    pdf.set_xy(12, 18)
    pdf.cell(186, 4, "KARDASHEV VI | CIVILIZATION ASSET PROTOCOL", 0, 1, "C")
    pdf.line(20, 26, 190, 26)

    # Título
    pdf.set_xy(12, 30)
    pdf.set_font("Courier", "B", 20)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(186, 12, "DELPHIA NEXUS", 0, 1, "C")
    pdf.set_xy(12, 42)
    pdf.set_font("Courier", "B", 9)
    pdf.set_text_color(180, 150, 40)
    pdf.cell(186, 6, "SOVEREIGN OWNERSHIP CERTIFICATE", 0, 1, "C")
    pdf.line(20, 52, 190, 52)

    # Símbolo central — ASCII puro, sin Unicode especial
    pdf.set_xy(85, 56)
    pdf.set_font("Courier", "B", 24)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(40, 14, "[ * ]", 0, 1, "C")

    # Campos — sanitización total a ASCII + latin-1 safe
    def safe(text):
        """Convierte a string, elimina caracteres fuera de latin-1."""
        return str(text).encode('latin-1', errors='replace').decode('latin-1')

    fields = [
        ("ASSET DESIGNATION",   safe(str(asset_name).upper())),
        ("REGISTRY CODE",       safe(str(asset_id).upper())),
        ("SOVEREIGN CUSTODIAN", safe(str(sovereign).upper())),
        ("APPRAISED VALUATION", f"{float(value):,.0f} DPX"),
        ("LEDGER EPOCH",        "2026 - TRUTH LEDGER v7"),
        ("CLASSIFICATION",      "TIER I - IMMUTABLE ASSET"),
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

    # Hash box
    pdf.set_fill_color(15, 12, 5)
    pdf.rect(18, y_start + 4, 174, 22, 'F')
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(0.4)
    pdf.rect(18, y_start + 4, 174, 22)
    pdf.set_xy(18, y_start + 6)
    pdf.set_font("Courier", "", 6)
    pdf.set_text_color(140, 110, 30)
    pdf.cell(174, 4, "CRYPTOGRAPHIC VERIFICATION HASH - SHA-256", 0, 1, "C")
    pdf.set_xy(18, y_start + 11)
    pdf.set_font("Courier", "B", 9)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(174, 8, a_hash, 0, 1, "C")   # a_hash es hexadecimal puro, siempre ASCII

    # Pie
    pdf.line(20, y_start + 32, 190, y_start + 32)
    pdf.set_xy(12, y_start + 34)
    pdf.set_font("Courier", "I", 6)
    pdf.set_text_color(80, 70, 40)
    pdf.cell(186, 4, "This certificate constitutes an immutable record on the Delphia Truth Ledger.", 0, 1, "C")
    pdf.set_xy(12, y_start + 38)
    pdf.cell(186, 4, "Unauthorized duplication voids sovereign claim - KARDASHEV VI PROTOCOL ACTIVE", 0, 1, "C")

    serial = f"DPX-{a_hash[:8]}"
    pdf.set_font("Courier", "", 5)
    pdf.set_text_color(60, 55, 30)
    pdf.set_xy(14, 278)
    pdf.cell(40, 4, serial, 0, 0, "L")
    pdf.set_xy(156, 278)
    pdf.cell(40, 4, serial, 0, 0, "R")

    # Export a bytes via archivo temporal
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        pdf.output(tmp_path)
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


# =============================================
# 3. DATOS Y USUARIOS
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
@st.cache_data(ttl=30)
def load_ledger():
    df = pd.read_csv("Truth_Ledger_Master.csv").rename(columns={'Nombre': 'Asset'})
    df['Value'] = pd.to_numeric(
        df['Valor'].astype(str).replace('[\$,]', '', regex=True),
        errors='coerce'
    ).fillna(0)
    # Columnas opcionales con defaults
    if 'Status' not in df.columns:
        df['Status'] = 'active'
    if 'Fracciones' not in df.columns:
        df['Fracciones'] = 1
    if 'FraccionesVendidas' not in df.columns:
        df['FraccionesVendidas'] = 0
    return df

@st.cache_data(ttl=30)
def load_accounts():
    return pd.read_csv("Delphia_Bank_Accounts.csv")

ledger   = load_ledger()
accounts = load_accounts()

user      = st.session_state["user"]
tier_data = TIERS.get(user, TIERS["Arquitecto"])

user_assets = (
    ledger if user in ["Arquitecto", "Delphi"]
    else ledger[ledger['Soberano'].str.contains(user, na=False)]
)

# Assets activos (no bloqueados ni vendidos)
active_assets = user_assets[user_assets['Status'] == 'active']
locked_assets = user_assets[user_assets['Status'] == 'locked']

# =============================================
# 6. HEADER / DASHBOARD
# =============================================
acc_row = accounts[accounts['Soberano'].str.contains(user, na=False)]
balance = acc_row['Saldo_DPX'].values[0] if not acc_row.empty else 0.0

c_head = st.columns([3, 1, 1, 1, 1])
c_head[0].markdown(f"### 🏛️ {user} | {tier_data['Label']}")
c_head[1].metric("BANK BALANCE",          f"{balance:,.0f} DPX")
c_head[2].metric("TOTAL ASSETS",          f"{user_assets['Value'].sum():,.0f} DPX")
c_head[3].metric("CREDIT LINE AVAILABLE", f"{(active_assets['Value'].sum() * tier_data['LTV']):,.0f} DPX")

if c_head[4].button("LOGOUT"):
    st.session_state["authenticated"] = False
    st.rerun()

st.divider()

# =============================================
# 7. TABS DE NAVEGACIÓN
# =============================================
tab_vault, tab_market, tab_upload = st.tabs([
    "🏛️  SOVEREIGN VAULT",
    "🏪  OPEN MARKETPLACE",
    "⬆️  REGISTER ASSET"
])

# ╔══════════════════════════════════════════╗
# ║         TAB 1 — SOVEREIGN VAULT          ║
# ╚══════════════════════════════════════════╝
with tab_vault:

    # ── Indicador de assets bloqueados ──────────────────
    if not locked_assets.empty:
        st.markdown(
            f"<div class='warn-box' style='margin-bottom:10px;'>"
            f"🔒 {len(locked_assets)} asset(s) currently locked as collateral · "
            f"<span style='color:#ff9966;'>Cannot be sold, split, or re-collateralized</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    # ── Asset Grid ──────────────────────────────────────
    # GRID SIMÉTRICA v17:
    # Cada asset se renderiza en un st.container(border=True).
    # La card VISUAL (.card-shell) es un div HTML con altura fija 295px.
    # La imagen se renderiza con st.image() ANTES del div y se posiciona
    # con CSS overflow:hidden en .card-img-zone (puro HTML).
    # Los botones se renderizan con st.columns() dentro del container.
    # El div HTML cierra DESPUÉS de los elementos de texto pero ANTES
    # de los botones (que Streamlit posiciona inmediatamente debajo).

    cols = st.columns(6)
    for i, (_, asset) in enumerate(user_assets.iterrows()):
        with cols[i % 6]:
            folder      = asset['Soberano'].replace(" ", "_")
            asset_clean = str(asset['Asset']).split('.')[0]
            base_dir    = f"Boveda_Activos/{folder}/"
            status      = asset.get('Status', 'active')

            img_to_show = None
            if os.path.exists(base_dir):
                for f in sorted(os.listdir(base_dir)):
                    if f.startswith(asset_clean) and f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        img_to_show = base_dir + f
                        break

            # Badge de estado
            badge_html = ""
            if status == 'locked':
                badge_html = "<span style='position:absolute;top:4px;right:4px;background:#ff6b35;color:#fff;font-size:5px;padding:1px 4px;border-radius:2px;font-family:Rajdhani,sans-serif;letter-spacing:1px;'>LOCKED</span>"
            elif status == 'listed':
                badge_html = "<span style='position:absolute;top:4px;right:4px;background:#1a6b1a;color:#39d353;font-size:5px;padding:1px 4px;border-radius:2px;font-family:Rajdhani,sans-serif;letter-spacing:1px;border:1px solid #39d353;'>FOR SALE</span>"

            with st.container(border=True):
                # Imagen — dentro del container, CSS la recorta a 150px
                if img_to_show:
                    st.image(img_to_show, use_container_width=True)
                else:
                    icon = "📄" if ".pdf" in str(asset['Asset']).lower() else "💎"
                    st.markdown(
                        f"<div style='width:100%;height:150px;background:#0d1117;"
                        f"display:flex;align-items:center;justify-content:center;"
                        f"border-bottom:1px solid #30363d;position:relative;'>"
                        f"<span style='font-size:32px;line-height:1;'>{icon}</span>"
                        f"{badge_html}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                # Info textual
                st.markdown(
                    f"<div style='font-size:7px;font-weight:700;color:#fff;"
                    f"font-family:Rajdhani,sans-serif;letter-spacing:0.6px;"
                    f"text-transform:uppercase;text-align:center;"
                    f"padding:3px 3px 0 3px;height:20px;overflow:hidden;"
                    f"display:flex;align-items:center;justify-content:center;'>"
                    f"{asset['Asset']}</div>"
                    f"<div style='font-size:9px;font-weight:700;color:#d4af37;"
                    f"font-family:Cinzel,serif;text-align:center;padding:1px 0 2px 0;'>"
                    f"{asset['Value']:,.0f} DPX</div>",
                    unsafe_allow_html=True
                )

                # Botones — deshabilitados si el asset está locked
                disabled = (status == 'locked')
                b1, b2 = st.columns(2)
                if b1.button("📜 TITLE", key=f"t_{asset['Asset_ID']}", disabled=False):
                    st.session_state['op'] = ('TITLE', asset)
                if b2.button("🔀 SPLIT", key=f"f_{asset['Asset_ID']}", disabled=disabled):
                    st.session_state['op'] = ('SPLIT', asset)

                b3, b4 = st.columns(2)
                if b3.button("💰 LOAN", key=f"c_{asset['Asset_ID']}", disabled=disabled):
                    st.session_state['op'] = ('LOAN', asset)
                if b4.button("🏷️ SELL", key=f"v_{asset['Asset_ID']}", disabled=disabled):
                    st.session_state['op'] = ('SELL', asset)

# ╔══════════════════════════════════════════╗
# ║       TAB 2 — OPEN MARKETPLACE           ║
# ╚══════════════════════════════════════════╝
with tab_market:
    st.markdown("### 🏪 DELPHIA OPEN MARKET")
    st.markdown(
        "<div class='terminal-box' style='margin-bottom:12px;'>"
        "<span class='terminal-label'>MARKET STATUS</span><br>"
        "<span style='color:#39d353; font-weight:bold;'>● LIVE · SOVEREIGN EXCHANGE ACTIVE</span><br><br>"
        "<span class='terminal-label'>PROTOCOL</span><br>"
        "<span style='color:#aaa;font-size:8px;'>All listed assets are verified on the Truth Ledger. "
        "Transactions are atomic: ownership transfers only upon full payment confirmation.</span>"
        "</div>",
        unsafe_allow_html=True
    )

    # Assets listados para venta
    listed = ledger[ledger['Status'] == 'listed'] if 'Status' in ledger.columns else pd.DataFrame()

    if listed.empty:
        st.markdown(
            "<div style='text-align:center;color:#444;font-family:Rajdhani,sans-serif;"
            "font-size:11px;letter-spacing:2px;padding:40px 0;'>"
            "NO ASSETS CURRENTLY LISTED FOR SALE<br>"
            "<span style='font-size:8px;color:#333;'>Sovereign participants may list assets from the Vault tab</span>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        mcols = st.columns(4)
        for i, (_, asset) in enumerate(listed.iterrows()):
            with mcols[i % 4]:
                seller = asset.get('Soberano', 'Unknown')
                price  = asset.get('ListPrice', asset['Value'])

                folder      = seller.replace(" ", "_")
                asset_clean = str(asset['Asset']).split('.')[0]
                base_dir    = f"Boveda_Activos/{folder}/"
                img_to_show = None
                if os.path.exists(base_dir):
                    for f in sorted(os.listdir(base_dir)):
                        if f.startswith(asset_clean) and f.lower().endswith(('.jpg', '.jpeg', '.png')):
                            img_to_show = base_dir + f
                            break

                with st.container(border=True):
                    if img_to_show:
                        st.image(img_to_show, use_container_width=True)
                    else:
                        st.markdown(
                            "<div style='width:100%;height:150px;background:#0d1117;"
                            "display:flex;align-items:center;justify-content:center;'>"
                            "<span style='font-size:32px;'>💎</span></div>",
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        f"<div style='font-size:7px;font-weight:700;color:#fff;"
                        f"font-family:Rajdhani,sans-serif;text-transform:uppercase;"
                        f"text-align:center;padding:3px;'>{asset['Asset']}</div>"
                        f"<div style='font-size:9px;color:#d4af37;font-family:Cinzel,serif;"
                        f"text-align:center;font-weight:700;'>{float(price):,.0f} DPX</div>"
                        f"<div style='font-size:7px;color:#888;font-family:Rajdhani,sans-serif;"
                        f"text-align:center;padding-bottom:4px;'>Seller: {seller}</div>",
                        unsafe_allow_html=True
                    )

                    # Solo otros usuarios pueden comprar
                    if seller != user:
                        if st.button(f"⚡ BUY NOW", key=f"buy_{asset['Asset_ID']}",
                                     use_container_width=True):
                            # Verificar saldo
                            buyer_row = accounts[accounts['Soberano'].str.contains(user, na=False)]
                            buyer_bal = buyer_row['Saldo_DPX'].values[0] if not buyer_row.empty else 0
                            if buyer_bal >= float(price):
                                st.success(f"✔ Purchase initiated · {float(price):,.0f} DPX transfer pending confirmation")
                            else:
                                st.error(f"Insufficient balance · You have {buyer_bal:,.0f} DPX")
                    else:
                        if st.button("✕ DELIST", key=f"delist_{asset['Asset_ID']}",
                                     use_container_width=True):
                            st.info("Delist order submitted")

# ╔══════════════════════════════════════════╗
# ║       TAB 3 — REGISTER ASSET             ║
# ╚══════════════════════════════════════════╝
with tab_upload:
    st.markdown("### ⬆️ REGISTER NEW SOVEREIGN ASSET")
    st.markdown(
        "<div class='terminal-box'>"
        "<span class='terminal-label'>PROTOCOL</span><br>"
        "<span style='color:#aaa;font-size:8px;'>New assets are registered on the Truth Ledger "
        "and stored in your Sovereign Vault. Supported formats: JPG, PNG (artwork/photo), "
        "PDF (documents/contracts).</span>"
        "</div>",
        unsafe_allow_html=True
    )

    col_form, col_preview = st.columns([2, 1])

    with col_form:
        asset_name_input  = st.text_input("ASSET NAME", placeholder="e.g. Autorretrato 2026",
                                          key="upload_name")
        asset_value_input = st.number_input("APPRAISED VALUE (DPX)", min_value=1.0,
                                            value=1000.0, step=50.0, key="upload_value")
        asset_desc_input  = st.text_area("DESCRIPTION (optional)", height=80,
                                         placeholder="Provenance, medium, dimensions...",
                                         key="upload_desc")
        uploaded_file     = st.file_uploader(
            "UPLOAD ASSET FILE",
            type=["jpg", "jpeg", "png", "pdf"],
            key="upload_file"
        )

        col_btn1, col_btn2 = st.columns(2)
        register_clicked = col_btn1.button("⚡ REGISTER ASSET", use_container_width=True,
                                            key="do_register")

    with col_preview:
        st.markdown(
            "<div class='terminal-box'>"
            "<span class='terminal-label'>PREVIEW</span><br>",
            unsafe_allow_html=True
        )
        if uploaded_file:
            if uploaded_file.type.startswith("image"):
                st.image(uploaded_file, use_container_width=True)
            else:
                st.markdown(
                    "<div style='height:120px;background:#0d1117;display:flex;"
                    "align-items:center;justify-content:center;'>"
                    "<span style='font-size:36px;'>📄</span></div>",
                    unsafe_allow_html=True
                )
        st.markdown("</div>", unsafe_allow_html=True)

    # Lógica de registro
    if register_clicked:
        if not asset_name_input:
            st.error("Asset name is required")
        elif not uploaded_file:
            st.error("Please upload a file for your asset")
        else:
            # Crear directorio del soberano si no existe
            vault_dir = f"Boveda_Activos/{user.replace(' ', '_')}/"
            os.makedirs(vault_dir, exist_ok=True)

            # Guardar el archivo
            ext       = uploaded_file.name.split('.')[-1].lower()
            safe_name = asset_name_input.replace(' ', '_').replace('/', '-')
            file_path = f"{vault_dir}{safe_name}.{ext}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Generar ID único
            new_id = generate_asset_id(asset_name_input, user)

            # Construir nueva fila para el ledger
            new_row = {
                'Asset':              asset_name_input,
                'Asset_ID':           new_id,
                'Soberano':           user,
                'Valor':              f"{asset_value_input:,.0f}",
                'Value':              asset_value_input,
                'Status':             'active',
                'Fracciones':         1,
                'FraccionesVendidas': 0,
                'Descripcion':        asset_desc_input or '',
            }

            # Append al CSV
            try:
                existing = pd.read_csv("Truth_Ledger_Master.csv")
                updated  = pd.concat([existing, pd.DataFrame([new_row])], ignore_index=True)
                updated.to_csv("Truth_Ledger_Master.csv", index=False)
                load_ledger.clear()   # Limpiar caché para refrescar
                st.markdown(
                    f"<div class='success-box'>"
                    f"✔ ASSET REGISTERED ON TRUTH LEDGER<br>"
                    f"ID: {new_id} · Value: {asset_value_input:,.0f} DPX<br>"
                    f"File stored at: {file_path}"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.balloons()
            except Exception as e:
                st.error(f"Registration error: {e}")


# =============================================
# 8. TRANSACTION TERMINAL (SIDEBAR)
# =============================================
if 'op' in st.session_state:
    mode, data = st.session_state['op']

    with st.sidebar:
        col_title, col_x = st.columns([4, 1])
        with col_title:
            st.markdown(f"### ⚡ TERMINAL: {mode}")
        with col_x:
            if st.button("✕", key="close_top", help="Cerrar terminal"):
                pk = f"pdf_cache_{data['Asset_ID']}"
                if pk in st.session_state:
                    del st.session_state[pk]
                del st.session_state['op']
                st.rerun()

        st.divider()

        # Info básica
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

        # ══════════ TITLE ══════════
        if mode == 'TITLE':
            cache_key = f"pdf_cache_{data['Asset_ID']}"
            if cache_key not in st.session_state:
                a_hash = generate_asset_hash(data['Asset_ID'], user)
                try:
                    pdf_bytes = create_pdf_certificate(
                        data['Asset'], data['Asset_ID'],
                        user, data['Value'], a_hash
                    )
                    st.session_state[cache_key] = {"hash": a_hash, "pdf": pdf_bytes, "ok": True}
                except Exception as e:
                    st.session_state[cache_key] = {
                        "hash": generate_asset_hash(data['Asset_ID'], user),
                        "pdf": None, "ok": False, "err": str(e)
                    }

            cached    = st.session_state[cache_key]
            a_hash    = cached["hash"]
            pdf_bytes = cached["pdf"]
            pdf_ok    = cached["ok"]

            st.markdown(
                f"<div class='terminal-box'>"
                f"<span class='terminal-label'>SOVEREIGN OWNER</span><br>"
                f"<span class='terminal-value'>{user}</span><br><br>"
                f"<span class='terminal-label'>TIER STATUS</span><br>"
                f"<span class='terminal-value' style='color:#d4af37;'>{tier_data['Label']}</span><br><br>"
                f"<span class='terminal-label'>VERIFICATION HASH</span><br>"
                f"<span style='color:#d4af37;font-family:monospace;font-size:8px;"
                f"word-break:break-all;'>{a_hash}</span><br><br>"
                f"<span class='terminal-label'>LEDGER STATUS</span><br>"
                f"<span style='color:#39d353;font-weight:bold;'>● SECURED · IMMUTABLE</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            if pdf_ok and pdf_bytes:
                st.download_button(
                    label="⬇  DOWNLOAD SOVEREIGN CERTIFICATE",
                    data=pdf_bytes,
                    file_name=f"CERT_{data['Asset_ID']}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"dl_{data['Asset_ID']}"
                )
            else:
                st.error(f"PDF error: {cached.get('err', 'unknown')}")
                if st.button("🔄 RETRY", use_container_width=True, key="retry_pdf"):
                    del st.session_state[cache_key]
                    st.rerun()

        # ══════════ SPLIT ══════════
        elif mode == 'SPLIT':
            asset_value = data['Value']
            u_split = st.number_input("Number of Fractions", min_value=2,
                                       max_value=10000, value=100)
            fraction_value = asset_value / u_split if u_split > 0 else 0

            st.markdown(
                f"<div class='terminal-box'>"
                f"<span class='terminal-label'>TOTAL ASSET VALUE</span><br>"
                f"<span class='terminal-value' style='color:#d4af37;'>{asset_value:,.2f} DPX</span><br><br>"
                f"<span class='terminal-label'>FRACTIONS</span><br>"
                f"<span class='terminal-value'>{u_split:,} shares</span><br><br>"
                f"<span class='terminal-label'>VALUE PER SHARE</span><br>"
                f"<span class='terminal-value' style='color:#d4af37;font-size:15px;'>"
                f"{fraction_value:,.2f} DPX</span><br><br>"
                f"<hr class='gold-divider'>"
                f"<span style='color:#aaa;font-size:8px;'>"
                f"Fractions are recorded as shares on the original asset entry — "
                f"the ledger remains a single record. No duplicated rows.</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div class='warn-box'>⚠ IRREVERSIBLE · "
                "Asset will be converted to fractional ownership.</div>",
                unsafe_allow_html=True
            )
            st.markdown("<div class='split-spacer'></div>", unsafe_allow_html=True)

            if st.button("⚡ EXECUTE RE-LEDGERING", use_container_width=True):
                try:
                    df = pd.read_csv("Truth_Ledger_Master.csv")
                    idx = df[df['Asset_ID'] == data['Asset_ID']].index
                    if not idx.empty:
                        df.loc[idx, 'Fracciones']         = u_split
                        df.loc[idx, 'FraccionesVendidas'] = 0
                        df.to_csv("Truth_Ledger_Master.csv", index=False)
                        load_ledger.clear()
                        st.markdown(
                            f"<div class='success-box'>✔ RE-LEDGERING COMPLETE<br>"
                            f"{u_split:,} shares of {fraction_value:,.2f} DPX · "
                            f"Single ledger entry preserved.</div>",
                            unsafe_allow_html=True
                        )
                except Exception as e:
                    st.error(f"Split error: {e}")

        # ══════════ LOAN ══════════
        elif mode == 'LOAN':
            asset_value = data['Value']
            ltv_pct  = tier_data['LTV']
            max_loan = asset_value * ltv_pct
            interest = tier_data['Interest']

            st.markdown(
                f"<div class='terminal-box'>"
                f"<span class='terminal-label'>TIER</span><br>"
                f"<span class='terminal-value' style='color:#d4af37;'>{tier_data['Label']}</span><br><br>"
                f"<span class='terminal-label'>LOAN-TO-VALUE RATIO</span><br>"
                f"<span class='terminal-value' style='color:#d4af37;font-size:18px;'>"
                f"{ltv_pct*100:.0f}%</span>"
                f" <span style='color:#888;font-size:8px;'>of asset value</span><br><br>"
                f"<span class='terminal-label'>CREDIT AVAILABLE</span><br>"
                f"<span class='terminal-value' style='color:#fff;font-size:16px;'>"
                f"{max_loan:,.0f} DPX</span><br><br>"
                f"<span class='terminal-label'>ANNUAL RATE</span><br>"
                f"<span class='terminal-value'>{interest*100:.2f}%</span><br><br>"
                f"<hr class='gold-divider'>"
                f"<span style='color:#aaa;font-size:8px;'>"
                f"Asset will be LOCKED as collateral until loan is repaid. "
                f"Locked assets cannot be sold, split, or re-collateralized.</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            if st.button("⚡ EXECUTE INSTANT LOAN", use_container_width=True):
                try:
                    # Bloquear asset en el ledger
                    df = pd.read_csv("Truth_Ledger_Master.csv")
                    idx = df[df['Asset_ID'] == data['Asset_ID']].index
                    if not idx.empty:
                        df.loc[idx, 'Status'] = 'locked'
                        df.to_csv("Truth_Ledger_Master.csv", index=False)
                        load_ledger.clear()

                    # Acreditar DPX en la cuenta
                    acc = pd.read_csv("Delphia_Bank_Accounts.csv")
                    aidx = acc[acc['Soberano'].str.contains(user, na=False)].index
                    if not aidx.empty:
                        acc.loc[aidx, 'Saldo_DPX'] = acc.loc[aidx, 'Saldo_DPX'].values[0] + max_loan
                        acc.to_csv("Delphia_Bank_Accounts.csv", index=False)
                        load_accounts.clear()

                    st.markdown(
                        f"<div class='success-box'>✔ LIQUIDITY INJECTED<br>"
                        f"{max_loan:,.0f} DPX credited to your account.<br>"
                        f"Asset <b>{data['Asset_ID']}</b> locked as collateral.</div>",
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"Loan execution error: {e}")

        # ══════════ SELL ══════════
        elif mode == 'SELL':
            list_price = st.number_input("Listing Price (DPX)",
                                          value=float(data['Value']),
                                          min_value=0.0, step=100.0)

            st.markdown(
                f"<div class='terminal-box'>"
                f"<span class='terminal-label'>MARKETPLACE</span><br>"
                f"<span class='terminal-value'>DELPHIA OPEN MARKET</span><br><br>"
                f"<span class='terminal-label'>LISTING PRICE</span><br>"
                f"<span class='terminal-value' style='color:#d4af37;'>{list_price:,.0f} DPX</span><br><br>"
                f"<hr class='gold-divider'>"
                f"<span style='color:#aaa;font-size:8px;'>"
                f"Asset will be LISTED on the Open Market and locked against "
                f"other operations until sold or delisted.</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            if st.button("📡 CONFIRM LISTING · BROADCAST", use_container_width=True):
                try:
                    df = pd.read_csv("Truth_Ledger_Master.csv")
                    idx = df[df['Asset_ID'] == data['Asset_ID']].index
                    if not idx.empty:
                        df.loc[idx, 'Status']    = 'listed'
                        df.loc[idx, 'ListPrice'] = list_price
                        df.to_csv("Truth_Ledger_Master.csv", index=False)
                        load_ledger.clear()
                    st.markdown(
                        "<div class='success-box'>✔ ASSET LISTED ON OPEN MARKET<br>"
                        "Visible to all sovereign participants.</div>",
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"Listing error: {e}")