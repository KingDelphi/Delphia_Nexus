import streamlit as st
import pandas as pd
import os

# 1. ESTÉTICA SOBERANA (HIGH-DENSITY GRID)
def apply_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #0c0e12; color: #d4af37; }
        section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #d4af37; }
        div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #d4af37; padding: 10px; border-radius: 5px; }
        
        /* Grid de Activos */
        .asset-card { 
            background-color: #1c2128; 
            border: 1px solid #30363d; 
            padding: 12px; 
            border-radius: 8px; 
            margin-bottom: 10px;
            text-align: center;
            min-height: 280px;
        }
        .asset-card:hover { border: 1px solid #d4af37; background-color: #21262d; }
        
        /* Botones Pequeños para Grid denso */
        .stButton>button { 
            width: 100%; 
            font-size: 10px !important; 
            height: 25px; 
            line-height: 1;
            background-color: #000000;
            color: #d4af37;
            border: 1px solid #d4af37;
        }
        
        h1, h2, h3, h4 { font-family: 'Courier New', Courier, monospace; color: #d4af37 !important; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="NEXUS | Delphium", page_icon="🏛️", layout="wide")
apply_theme()

# 2. DEFINICIÓN DE TIERS Y LÓGICA FINANCIERA
TIERS = {
    "Arquitecto": {"LTV": 0.90, "Interes": 0.005, "Label": "TIER I - SOBERANO"},
    "Delphi": {"LTV": 0.90, "Interes": 0.005, "Label": "TIER I - SOBERANO"},
    "Matriarca": {"LTV": 0.70, "Interes": 0.025, "Label": "TIER II - NOBLE"},
    "Inversor_01": {"LTV": 0.50, "Interes": 0.050, "Label": "TIER III - ELITE"}
}

# 3. LOGIN SOBERANO
USERS = {"Arquitecto": "ROOT_777", "Delphi": "OMEGA_999", "Inversor_01": "INV_001"}

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
    # 4. CARGA DE DATOS
    ledger = pd.read_csv("Truth_Ledger_Master.csv")
    accounts = pd.read_csv("Delphia_Bank_Accounts.csv")
    
    # Normalización
    ledger = ledger.rename(columns={'Nombre': 'Activo'})
    ledger['Valor'] = pd.to_numeric(ledger['Valor'].astype(str).replace('[\$,]', '', regex=True), errors='coerce').fillna(0)
    
    user = st.session_state["user"]
    tier_data = TIERS.get(user, TIERS["Inversor_01"])
    
    # Filtrado por Rango
    if user in ["Arquitecto", "Delphi"]:
        user_assets = ledger
        display_title = f"🏛️ NEXUS APEX - {tier_data['Label']}"
    else:
        user_assets = ledger[ledger['Soberano'].str.contains(user, na=False)]
        display_title = f"🏛️ BÓVEDA PERSONAL - {tier_data['Label']}"

    # Balance bancario
    row_acc = accounts[accounts['Soberano'].str.contains(user, na=False)]
    balance = row_acc['Saldo_DPX'].values[0] if not row_acc.empty else 0.0

    st.title(display_title)
    
    # 5. MÉTRICAS FINANCIERAS (DASHBOARD)
    total_asset_value = user_assets['Valor'].sum()
    credit_capacity = total_asset_value * tier_data['LTV']
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Balance Bancario", f"{balance:,.2f} DPX")
    c2.metric("Valor Total Activos", f"{total_asset_value:,.2f} DPX")
    c3.metric("Capacidad de Crédito", f"{credit_capacity:,.2f} DPX")
    c4.metric("Tasa de Interés (Anual)", f"{tier_data['Interes']*100}%")

    st.divider()

    # 6. GRID DE ACTIVOS (5 COLUMNAS)
    st.subheader("💎 Inventario de Activos Soberanos")
    
    cols = st.columns(5)
    
    for i, (_, asset) in enumerate(user_assets.iterrows()):
        with cols[i % 5]:
            # Contenedor Visual del Activo
            st.markdown(f"""
                <div class="asset-card">
                    <p style='color: #8b949e; font-size:10px; margin:0;'>{asset['Asset_ID']}</p>
                    <h5 style='margin:10px 0;'>{asset['Activo']}</h5>
                    <p style='color: #d4af37; font-size:18px; font-weight:bold;'>{asset['Valor']:,.0f} DPX</p>
                    <p style='color: #8b949e; font-size:10px;'>Colateral: {asset['Valor']*tier_data['LTV']:,.0f} DPX</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Botonera de Funciones
            if st.button("📜 Título", key=f"t_{asset['Asset_ID']}"):
                st.info(f"Accediendo a documento: {asset['Asset_ID']}")
            
            if st.button("💸 Fraccionar", key=f"f_{asset['Asset_ID']}"):
                st.session_state['action_target'] = asset['Activo']
                st.session_state['action_type'] = 'FRACC'
                
            if st.button("🏦 Crédito", key=f"c_{asset['Asset_ID']}"):
                st.session_state['action_target'] = asset['Activo']
                st.session_state['action_type'] = 'CREDIT'

    # 7. MÓDULOS DE ACCIÓN (SIDEBAR)
    if 'action_target' in st.session_state:
        with st.sidebar:
            st.header("⚙️ Operación de Activo")
            st.write(f"**Activo:** {st.session_state['action_target']}")
            
            if st.session_state['action_type'] == 'FRACC':
                st.write("---")
                units = st.number_input("Unidades a generar", min_value=2, step=1, value=10)
                if st.button("Ejecutar División"):
                    st.success(f"Dividiendo {st.session_state['action_target']} en {units} fracciones...")
            
            if st.session_state['action_type'] == 'CREDIT':
                st.write("---")
                st.write(f"Tier: {tier_data['Label']}")
                st.write(f"Tasa aplicada: {tier_data['Interes']*100}%")
                if st.button("Confirmar Préstamo"):
                    st.success("Crédito inyectado en cuenta bancaria.")
            
            if st.button("Cancelar"):
                del st.session_state['action_target']
                st.rerun()