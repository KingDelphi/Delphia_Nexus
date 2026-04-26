import pandas as pd
import os
# --- AQUÍ ACTUALIZAMOS LAS IMPORTACIONES ---
from generar_certificados_pro import emitir_titulos as regenerar_certs
from generar_nexus import ejecutar_nexus as actualizar_dashboard

LEDGER = "Truth_Ledger_Master.csv"
CUENTAS = "Delphia_Bank_Accounts.csv"

def limpiar_precio(valor):
    """Evita errores de comas y signos en el cálculo financiero."""
    if pd.isna(valor): return 0.0
    s = str(valor).replace('$', '').replace(',', '').strip()
    try:
        return float(s)
    except:
        return 0.0

def transferencia_soberana():
    df_ledger = pd.read_csv(LEDGER, quotechar='"')
    df_cuentas = pd.read_csv(CUENTAS)

    print("\n" + "═"*50)
    print("       SISTEMA DE TRANSFERENCIA DELPHIA v2.0")
    print("═"*50)

    asset_id = input("ID del Activo a transferir (DLPH-...): ").strip()
    comprador = input("Nombre del Soberano Comprador: ").strip()

    if asset_id not in df_ledger['Asset_ID'].values:
        print("[X] ERROR: El Asset_ID no existe.")
        return
    
    if comprador not in df_cuentas['Soberano'].values:
        print(f"[X] ERROR: El comprador '{comprador}' no tiene cuenta.")
        return

    activo = df_ledger[df_ledger['Asset_ID'] == asset_id].iloc[0]
    vendedor = activo['Soberano']
    
    # Usamos la limpieza Pro para el cálculo
    precio = limpiar_precio(activo['Valor'])
    
    saldo_comprador = df_cuentas.loc[df_cuentas['Soberano'] == comprador, 'Saldo_DPX'].values[0]

    print(f"\nACTIVO: {activo['Nombre']}")
    print(f"PRECIO: ${precio:,.2f} DPX")
    print(f"VENDEDOR: {vendedor} -> COMPRADOR: {comprador}")
    print(f"SALDO COMPRADOR: ${saldo_comprador:.2f} DPX")

    if saldo_comprador < precio:
        print("\n[!] TRANSACCIÓN RECHAZADA: Fondos insuficientes.")
        return

    confirmar = input("\n¿Confirmar transferencia soberana? (s/n): ").lower()
    if confirmar == 's':
        # --- PROCESO CONTABLE ---
        df_cuentas.loc[df_cuentas['Soberano'] == comprador, 'Saldo_DPX'] -= precio
        df_cuentas.loc[df_cuentas['Soberano'] == vendedor, 'Saldo_DPX'] += precio
        
        # --- CAMBIO DE PROPIEDAD ---
        df_ledger.loc[df_ledger['Asset_ID'] == asset_id, 'Soberano'] = comprador
        
        # Guardar Cambios
        df_cuentas.to_csv(CUENTAS, index=False)
        df_ledger.to_csv(LEDGER, index=False)

        print("\n" + "✔"*50)
        print("     TRANSFERENCIA Y TÍTULOS ACTUALIZADOS")
        print("✔"*50)

        # Ahora llaman a las versiones PRO y v2.7
        regenerar_certs() 
        actualizar_dashboard()
        
    else:
        print("[X] Transferencia cancelada.")

if __name__ == "__main__":
    transferencia_soberana()