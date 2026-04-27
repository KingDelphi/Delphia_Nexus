import streamlit as st
import pandas as pd

# 1. ESTÉTICA SOBERANA (CSS CORREGIDO)
def apply_theme():
    st.markdown("""
        <style>
        /* Fondo y texto general */
        .stApp { background-color: #0e1117; color: #d4af37; }
        
        /* Sidebar oscura */
        section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #d4af37; }
        
        /* Métricas con estilo de Terminal Financiera */
        div[data-testid="stMetric"] {
            background-color: #161b22;
            border: 1px solid #d4af37;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0px 0px 15px rgba(212, 175, 55, 0.1);
        }
        
        /* Cards de Activos */
        .asset-card { 
            background-color: #1c2128; 
            border-left: 5px solid #d4af37; 
            padding: 20px; 
            border-radius: 8px; 
            margin-bottom: 15px;
            transition: 0.3s;
        }
        .asset-card:hover { background-color: #21262d; border-left: 8px solid #ffd700; }
        
        h1, h2, h3 { font-family: 'Courier New', Courier, monospace; color: #d4af37 !important; }
        </style>
    """, unsafe_allow_html=True) # <-- AQUÍ ESTABA EL ERROR

st.set_page_config(page_title="NEXUS | Delphium", page_icon="🏛️", layout="wide")
apply_theme()

# 2. LOGIN
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
    # 3. CARGA Y FILTRADO
    ledger = pd.read_csv("Truth_Ledger_Master.csv")
    accounts = pd.read_csv("Delphia_Bank_Accounts.csv")
    
    # Limpieza de datos
    ledger['Valor'] = pd.to_numeric(ledger['Valor'].astype(str).replace('[\$,]', '', regex=True), errors='coerce').fillna(0)
    
    user = st.session_state["user"]
    user_assets = ledger[ledger['Soberano'] == user]
    user_balance = accounts[accounts['Soberano'] == user]['Balance_DPX'].values[0] if user in accounts['Soberano'].values else 0

    # 4. INTERFAZ
    st.sidebar.title(f"Soberano: {user}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title("🏛️ Mi Bóveda Soberana")
    
    # Métricas de Wallet
    c1, c2, c3 = st.columns(3)
    c1.metric("Balance en Banco", f"{user_balance:,.2f} DPX")
    c2.metric("Valor en Activos", f"{user_assets['Valor'].sum():,.2f} DPX")
    c3.metric("Capacidad Crediticia", f"{(user_assets['Valor'].sum() * 0.5):,.2f} DPX") # Ejemplo 50% LTV

    st.divider()

    # 5. DESPLIEGUE DE ASSETS (No tablas, sino visualización)
    st.subheader("💎 Activos en Posesión")
    if user_assets.empty:
        st.warning("No se detectan activos en esta bóveda.")
    else:
        for _, asset in user_assets.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="asset-card">
                    <h3 style='margin:0;'>{asset['Activo']}</h3>
                    <p style='color: #8b949e;'>ID: {asset['ID_Unico']} | Categoría: {asset['Categoria']}</p>
                    <p style='font-size: 20px; color: #d4af37;'>Valor: {asset['Valor']:,.2f} DPX</p>
                </div>
                """, unsafe_allow_html=True)
                col_btn1, col_btn2 = st.columns([1, 4])
                if col_btn1.button("Ver Título", key=asset['ID_Unico']):
                    st.info(f"Generando certificado para {asset['ID_Unico']}...")