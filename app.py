import streamlit as st
import pandas as pd

# 1. ESTÉTICA SOBERANA
def apply_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #d4af37; }
        section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #d4af37; }
        div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #d4af37; padding: 15px; border-radius: 5px; }
        .asset-card { 
            background-color: #1c2128; border-left: 5px solid #d4af37; 
            padding: 20px; border-radius: 8px; margin-bottom: 15px;
        }
        h1, h2, h3 { font-family: 'Courier New', Courier, monospace; color: #d4af37 !important; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="NEXUS | Delphium", page_icon="🏛️", layout="wide")
apply_theme()

# 2. LOGIN Y PERMISOS
USERS = {
    "Arquitecto": "ROOT_777",
    "Delphi": "OMEGA_999",
    "Inversor_01": "INV_001"
}

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
    # 3. CARGA Y LÓGICA DE PODER
    ledger = pd.read_csv("Truth_Ledger_Master.csv")
    accounts = pd.read_csv("Delphia_Bank_Accounts.csv")
    
    # Limpieza de valores
    ledger['Valor'] = pd.to_numeric(ledger['Valor'].astype(str).replace('[\$,]', '', regex=True), errors='coerce').fillna(0)
    
    user = st.session_state["user"]
    
    # --- FILTRO SEGÚN RANGO ---
    if user in ["Arquitecto", "Delphi"]:
        # Acceso Total: Ven todo el Reino
        user_assets = ledger 
        display_title = "🏛️ Master Ledger - Vista Global"
    else:
        # Acceso Restringido: Solo sus activos
        user_assets = ledger[ledger['Soberano'] == user]
        display_title = "🏛️ Mi Bóveda Personal"

    # Obtener balance de la cuenta
    user_balance_row = accounts[accounts['Soberano'] == user]
    user_balance = user_balance_row['Balance_DPX'].values[0] if not user_balance_row.empty else 0

    # 4. INTERFAZ
    st.sidebar.title(f"Soberano: {user}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title(display_title)
    
    # Métricas
    c1, c2, c3 = st.columns(3)
    c1.metric("Balance Disponible", f"{user_balance:,.2f} DPX")
    c2.metric("Valor del Portafolio", f"{user_assets['Valor'].sum():,.2f} DPX")
    c3.metric("Capacidad de Crédito", f"{(user_assets['Valor'].sum() * 0.4):,.2f} DPX")

    st.divider()

    # 5. LISTADO DE ACTIVOS
    st.subheader("💎 Activos Identificados")
    if user_assets.empty:
        st.warning(f"No se encontraron activos vinculados a {user}. Verifique el Ledger.")
    else:
        for _, asset in user_assets.iterrows():
            with st.container():
                # Nota: Aquí después pondremos la imagen del activo
                st.markdown(f"""
                <div class="asset-card">
                    <h3 style='margin:0;'>{asset['Activo']}</h3>
                    <p style='color: #8b949e; margin: 5px 0;'>ID: {asset['ID_Unico']} | Soberano: {asset['Soberano']}</p>
                    <p style='font-size: 18px; color: #d4af37;'>Valoración: {asset['Valor']:,.2f} DPX</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Acciones rápidas por activo
                col_a, col_b, col_c = st.columns([1, 1, 3])
                col_a.button("Ver Título", key=f"title_{asset['ID_Unico']}")
                if user in ["Arquitecto", "Delphi"]:
                    col_b.button("Editar", key=f"edit_{asset['ID_Unico']}")