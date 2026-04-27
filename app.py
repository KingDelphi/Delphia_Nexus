import streamlit as st
import pandas as pd
import os

# 1. ESTÉTICA SOBERANA
def apply_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #0c0e12; color: #d4af37; }
        section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #d4af37; }
        div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #d4af37; padding: 15px; border-radius: 5px; }
        .asset-card { 
            background-color: #1c2128; border-left: 5px solid #d4af37; 
            padding: 15px; border-radius: 8px; margin-bottom: 20px;
        }
        .img-container { border: 1px solid #30363d; border-radius: 5px; margin-bottom: 10px; overflow: hidden; }
        h1, h2, h3 { font-family: 'Courier New', Courier, monospace; color: #d4af37 !important; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="NEXUS | Delphium", page_icon="🏛️", layout="wide")
apply_theme()

# 2. LOGIN SOBERANO
USERS = {"Arquitecto": "ROOT_777", "Delphi": "OMEGA_999"}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🏛️ NEXUS | Acceso")
    u = st.selectbox("Identidad", list(USERS.keys()))
    p = st.text_input("Clave", type="password")
    if st.button("Sincronizar"):
        if USERS[u] == p:
            st.session_state["authenticated"], st.session_state["user"] = True, u
            st.rerun()
else:
    # 3. CARGA DE DATOS Y NORMALIZACIÓN
    ledger = pd.read_csv("Truth_Ledger_Master.csv")
    accounts = pd.read_csv("Delphia_Bank_Accounts.csv")
    
    # Limpieza: Convertimos "Nombre" (CSV) a "Activo" (App) para evitar KeyErrors
    ledger = ledger.rename(columns={'Nombre': 'Activo'})
    ledger['Valor'] = pd.to_numeric(ledger['Valor'].astype(str).replace('[\$,]', '', regex=True), errors='coerce').fillna(0)
    
    user = st.session_state["user"]
    
    # 4. LÓGICA DE PODER (VISTAS)
    if user in ["Arquitecto", "Delphi"]:
        user_assets = ledger
        display_title = "🏛️ Master Ledger - Vista Global"
    else:
        user_assets = ledger[ledger['Soberano'] == user]
        display_title = "🏛️ Mi Bóveda Personal"

    # Datos específicos que me pasaste
    row_acc = accounts[accounts['Soberano'].str.contains(user, na=False)]
    balance = row_acc['Saldo_DPX'].values[0] if not row_acc.empty else 0.0

    st.title(display_title)
    
    # MÉTRICAS SOBERANAS
    c1, c2, c3 = st.columns(3)
    c1.metric("Balance Disponible", f"{balance:,.2f} DPX")
    c2.metric("Activos Bajo Control", f"{len(user_assets)} Unidades")
    c3.metric("Net Worth (Poder)", f"{(balance + user_assets['Valor'].sum()):,.2f} DPX")

    st.divider()

    # 5. GRID DE ACTIVOS (RESTAURACIÓN VISUAL)
    st.subheader("💎 Galería de Activos")
    
    # Crear columnas para el grid (3 activos por fila)
    cols = st.columns(3)
    
    for i, (_, asset) in enumerate(user_assets.iterrows()):
        with cols[i % 3]:
            with st.container():
                # LÓGICA DE IMAGEN: Buscamos en las carpetas que mencionaste
                soberano_folder = asset['Soberano'].replace("Boveda_", "Boveda_Activos/Boveda_")
                # Intentamos encontrar el archivo por ID o Nombre
                img_path = f"{soberano_folder}/{asset['Activo']}"
                
                st.markdown('<div class="asset-card">', unsafe_allow_html=True)
                
                # Mostrar imagen si existe, si no, un placeholder negro
                if os.path.exists(img_path) and img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    st.image(img_path, use_container_width=True)
                else:
                    st.markdown('<div style="height:150px; background:#000; border:1px solid #333; display:grid; place-items:center;">[Documento/No Preview]</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <h3 style='margin-bottom:5px; font-size:18px;'>{asset['Activo']}</h3>
                    <p style='color: #8b949e; font-size:12px;'>Soberano: {asset['Soberano']}</p>
                    <p style='color: #d4af37; font-size:20px; font-weight:bold;'>{asset['Valor']:,.2f} DPX</p>
                """, unsafe_allow_html=True)
                
                # Botones de Acción
                btn_col1, btn_col2 = st.columns(2)
                btn_col1.button("📜 Título", key=f"t_{asset['Asset_ID']}")
                btn_col2.button("💸 Vender", key=f"v_{asset['Asset_ID']}")
                
                st.markdown('</div>', unsafe_allow_html=True)