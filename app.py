import streamlit as st
import pandas as pd
import os

# 1. ESTÉTICA APEX (8 COLUMNAS Y COMPRESIÓN VISUAL)
def apply_theme():
    st.markdown("""
        <style>
        /* Zoom Out General */
        html, body, [data-testid="stAppViewContainer"] { 
            font-size: 11px !important; 
            background-color: #0c0e12; 
        }
        .stApp { background-color: #0c0e12; color: #d4af37; }
        
        /* Sidebar Compacta */
        section[data-testid="stSidebar"] { 
            background-color: #000000; 
            border-right: 1px solid #d4af37; 
            width: 250px !important;
        }

        /* Header y Métricas Mini */
        div[data-testid="stMetric"] { 
            background-color: #161b22; 
            border: 1px solid #d4af37; 
            padding: 5px 10px !important; 
            border-radius: 3px;
        }
        div[data-testid="stMetricLabel"] > div { font-size: 10px !important; color: #8b949e !important; }
        div[data-testid="stMetricValue"] > div { font-size: 14px !important; color: #d4af37 !important; }

        /* Grid de 8 Columnas */
        .asset-card { 
            background-color: #1c2128; 
            border: 1px solid #30363d; 
            padding: 6px; 
            border-radius: 4px; 
            margin-bottom: 5px;
            text-align: center;
            transition: 0.2s;
        }
        .asset-card:hover { border: 1px solid #d4af37; background-color: #21262d; }
        
        /* Previsualización de Imagen */
        .img-preview {
            width: 100%;
            height: 60px;
            object-fit: cover;
            border-radius: 2px;
            margin-bottom: 4px;
            background-color: #000;
        }
        
        /* Botonera Micro (8 columnas requiere botones muy pequeños) */
        .stButton>button { 
            width: 100%; 
            font-size: 8px !important; 
            height: 18px !important; 
            padding: 0px !important; 
            min-height: 18px !important;
            background-color: #000000;
            color: #d4af37;
            border: 1px solid #444;
            margin-bottom: 1px;
        }
        .stButton>button:hover { border-color: #d4af37; color: #fff; }
        
        h1 { font-size: 18px !important; margin-bottom: 10px !important; }
        h5 { font-size: 9px !important; margin: 2px 0 !important; color: #eee !important; }
        .small-text { font-size: 8px; color: #8b949e; margin: 0; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="NEXUS | Apex", page_icon="🏛️", layout="wide")
apply_theme()

# 2. LÓGICA DE TIERS
TIERS = {
    "Arquitecto": {"LTV": 0.90, "Interes": 0.005, "Label": "TIER I"},
    "Delphi": {"LTV": 0.90, "Interes": 0.005, "Label": "TIER I"},
    "Matriarca": {"LTV": 0.70, "Interes": 0.025, "Label": "TIER II"},
    "Inversor_01": {"LTV": 0.50, "Interes": 0.050, "Label": "TIER III"}
}

# 3. LOGIN
USERS = {"Arquitecto": "ROOT_777", "Delphi": "OMEGA_999", "Inversor_01": "INV_001"}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🏛️ NEXUS | Acceso")
    u = st.selectbox("Soberano", list(USERS.keys()))
    p = st.text_input("Clave", type="password")
    if st.button("Sincronizar"):
        if USERS[u] == p:
            st.session_state["authenticated"], st.session_state["user"] = True, u
            st.rerun()
else:
    # 4. CARGA DE DATOS
    ledger = pd.read_csv("Truth_Ledger_Master.csv").rename(columns={'Nombre': 'Activo'})
    accounts = pd.read_csv("Delphia_Bank_Accounts.csv")
    ledger['Valor'] = pd.to_numeric(ledger['Valor'].astype(str).replace('[\$,]', '', regex=True), errors='coerce').fillna(0)
    
    user = st.session_state["user"]
    tier_data = TIERS.get(user, TIERS["Inversor_01"])
    
    # Filtrado APEX vs Personal
    user_assets = ledger if user in ["Arquitecto", "Delphi"] else ledger[ledger['Soberano'].str.contains(user, na=False)]
    row_acc = accounts[accounts['Soberano'].str.contains(user, na=False)]
    balance = row_acc['Saldo_DPX'].values[0] if not row_acc.empty else 0.0

    # HEADER COMPACTO (Ajustado para ocupar poco espacio vertical)
    c_head = st.columns([3, 1, 1, 1, 1])
    c_head[0].markdown(f"### 🏛️ {user} | {tier_data['Label']}")
    c_head[1].metric("BANK", f"{balance:,.0f}")
    c_head[2].metric("ASSETS", f"{user_assets['Valor'].sum():,.0f}")
    c_head[3].metric("CREDIT", f"{(user_assets['Valor'].sum() * tier_data['LTV']):,.0f}")
    if c_head[4].button("LOGOUT"):
        st.session_state["authenticated"] = False
        st.rerun()

    # 5. GRID DE 8 COLUMNAS
    st.subheader("💎 Master Ledger - High Density View")
    cols = st.columns(8)
    
    for i, (_, asset) in enumerate(user_assets.iterrows()):
        with cols[i % 8]:
            # Lógica de Imagen / Preview
            # Carpeta dinámica según el soberano del activo
            folder_name = asset['Soberano'].replace(" ", "_")
            img_path = f"Boveda_Activos/{folder_name}/{asset['Activo']}"
            
            st.markdown('<div class="asset-card">', unsafe_allow_html=True)
            
            # Intento de mostrar imagen o placeholder
            if os.path.exists(img_path) and img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                st.image(img_path, use_column_width=True)
            else:
                icon = "📄" if ".pdf" in str(asset['Activo']).lower() else "💎"
                st.markdown(f"<div style='height:40px; display:grid; place-items:center; font-size:20px;'>{icon}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<h5>{asset['Activo'][:15]}</h5>", unsafe_allow_html=True)
            st.markdown(f"<p class='small-text'>{asset['Asset_ID']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#d4af37; font-weight:bold; margin:2px 0;'>{asset['Valor']:,.0f} DPX</p>", unsafe_allow_html=True)
            
            # Botonera Micro-Funcional
            if st.button("TIT", key=f"t_{asset['Asset_ID']}", help="Ver Título"):
                st.session_state['op'] = ('TIT', asset['Activo'], asset['Asset_ID'])
            
            if st.button("FRA", key=f"f_{asset['Asset_ID']}", help="Fraccionar"):
                st.session_state['op'] = ('FRA', asset['Activo'], asset['Asset_ID'])
                
            if st.button("CRE", key=f"c_{asset['Asset_ID']}", help="Solicitar Crédito"):
                st.session_state['op'] = ('CRE', asset['Activo'], asset['Asset_ID'])

            if st.button("VEN", key=f"v_{asset['Asset_ID']}", help="Poner en Venta"):
                st.session_state['op'] = ('VEN', asset['Activo'], asset['Asset_ID'])
                
            st.markdown('</div>', unsafe_allow_html=True)

    # 6. TERMINAL DE OPERACIONES (SIDEBAR)
    if 'op' in st.session_state:
        op_type, name, aid = st.session_state['op']
        with st.sidebar:
            st.markdown(f"### ⚡ TERMINAL: {op_type}")
            st.markdown(f"**Activo:** {name}")
            st.markdown(f"**ID:** {aid}")
            st.divider()
            
            if op_type == 'VEN':
                price = st.number_input("Precio de Salida (DPX)", value=float(ledger[ledger['Asset_ID']==aid]['Valor'].values[0]))
                if st.button("CONFIRMAR VENTA"):
                    st.success("Orden publicada en el mercado abierto.")
            
            elif op_type == 'FRA':
                st.write("Dividir activo en unidades soberanas.")
                parts = st.number_input("Fracciones", min_value=2, value=100)
                if st.button("EJECUTAR FRACCIONAMIENTO"):
                    st.success(f"Activo fraccionado en {parts} unidades.")
            
            elif op_type == 'CRE':
                val = ledger[ledger['Asset_ID']==aid]['Valor'].values[0]
                max_loan = val * tier_data['LTV']
                st.write(f"Máximo Crédito (LTV): {max_loan:,.2f} DPX")
                st.write(f"Tasa: {tier_data['Interes']*100}%")
                if st.button("INYECTAR LIQUIDEZ"):
                    st.success("Crédito aprobado y enviado a cuenta.")

            if st.button("CERRAR TERMINAL"):
                del st.session_state['op']
                st.rerun()