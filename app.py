import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="NEXUS | Delphium", page_icon="🏛️", layout="wide")

# 2. SISTEMA DE LOGIN (Base Provisoria)
USERS = {
    "Arquitecto": "ROOT_777",
    "Delphi": "OMEGA_999",
    "Inversor_01": "INV_001",
    "Inversor_02": "INV_002"
}

def check_login():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🏛️ NEXUS V7.5 - Acceso Soberano")
        user = st.selectbox("Seleccione su identidad", list(USERS.keys()))
        password = st.text_input("Clave de Acceso", type="password")
        if st.button("Entrar al Reino"):
            if USERS[user] == password:
                st.session_state["authenticated"] = True
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Acceso denegado. Verifique su clave.")
        return False
    return True

# 3. CARGA DE DATOS (Lectura de CSVs)
@st.cache_data
def load_data():
    ledger = pd.read_csv("Truth_Ledger_Master.csv")
    accounts = pd.read_csv("Delphia_Bank_Accounts.csv")
    return ledger, accounts

# 4. CUERPO PRINCIPAL DEL DASHBOARD
if check_login():
    st.sidebar.title(f"Soberano: {st.session_state['user']}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["authenticated"] = False
        st.rerun()

    ledger, accounts = load_data()
    
    st.title(f"🏛️ NEXUS Dashboard - Apex View")
    st.write(f"Bienvenido, {st.session_state['user']}. El estado del Reino está actualizado.")

    # MÉTRICAS RÁPIDAS
    col1, col2, col3 = st.columns(3)
    total_market_cap = ledger['Valor'].sum()
    total_assets = len(ledger)
    
    col1.metric("Market Cap (DPX)", f"{total_market_cap:,.0f}")
    col2.metric("Activos en Bóveda", f"{total_assets}")
    col3.metric("Estatus del Sistema", "ONLINE", delta="Sincronizado")

    # VISTA DE TABLAS
    st.subheader("📜 Master Ledger (Global)")
    st.dataframe(ledger, use_container_width=True)

    st.subheader("💰 Cuentas Bancarias del Reino")
    st.table(accounts)

    st.info("Nota: Esta es la versión Cloud V1. Los permisos de transferencia se activarán en el siguiente Vector.")