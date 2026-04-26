import pandas as pd
import os
from generar_certificados_pro import emitir_titulos as regenerar_certs
from generar_nexus import ejecutar_nexus as actualizar_dashboard

LEDGER = "Truth_Ledger_Master.csv"
CUENTAS = "Delphia_Bank_Accounts.csv"
CAP_TABLE = "Delphia_Cap_Table.csv"

def limpiar_precio(valor):
    if pd.isna(valor): return 0.0
    s = str(valor).replace('$', '').replace(',', '').strip()
    try: return float(s)
    except: return 0.0

def transferencia_fraccionada():
    df_ledger = pd.read_csv(LEDGER, quotechar='"')
    df_cuentas = pd.read_csv(CUENTAS)
    df_cap = pd.read_csv(CAP_TABLE)

    print("\n" + "═"*60)
    print("      DELPHIA SHARES EXCHANGE - TRANSFERENCIA FRACCIONADA")
    print("═"*60)

    asset_id = input("ID del Activo (DLPH-...): ").strip()
    vendedor = input("Soberano Vendedor (Tú): ").strip()
    comprador = input("Soberano Comprador (Fede): ").strip()
    acciones_a_vender = int(input("¿Cuántas acciones (Shares) vas a transferir?: "))

    # 1. Validaciones
    if asset_id not in df_ledger['Asset_ID'].values:
        print("[X] ERROR: Activo no encontrado."); return
    
    # 2. Validar que el vendedor tenga las acciones
    filtro_vendedor = (df_cap['Asset_ID'] == asset_id) & (df_cap['Soberano'] == vendedor)
    if not filtro_vendedor.any() or df_cap.loc[filtro_vendedor, 'Acciones'].values[0] < acciones_a_vender:
        print(f"[X] ERROR: {vendedor} no tiene suficientes acciones."); return

    # 3. Calcular Precio Proporcional
    activo = df_ledger[df_ledger['Asset_ID'] == asset_id].iloc[0]
    valor_total = limpiar_precio(activo['Valor'])
    total_shares = activo['Total_Shares']
    precio_unitario = valor_total / total_shares
    costo_final = precio_unitario * acciones_a_vender

    # 4. Validar Fondos del Comprador
    saldo_comprador = df_cuentas.loc[df_cuentas['Soberano'] == comprador, 'Saldo_DPX'].values[0]
    
    print(f"\nDETALLE DE LA OPERACIÓN:")
    print(f"Activo: {activo['Nombre']}")
    print(f"Valor Unitario por Acción: ${precio_unitario:.2f} DPX")
    print(f"Total a pagar por {acciones_a_vender} acciones: ${costo_final:.2f} DPX")
    print(f"Saldo de {comprador}: ${saldo_comprador:.2f} DPX")

    if saldo_comprador < costo_final:
        print("\n[!] TRANSACCIÓN RECHAZADA: Fondos insuficientes."); return

    confirmar = input("\n¿Ejecutar transferencia de acciones? (s/n): ").lower()
    if confirmar == 's':
        # --- MOVIMIENTO FINANCIERO ---
        df_cuentas.loc[df_cuentas['Soberano'] == comprador, 'Saldo_DPX'] -= costo_final
        df_cuentas.loc[df_cuentas['Soberano'] == vendedor, 'Saldo_DPX'] += costo_final
        
        # --- MOVIMIENTO DE ACCIONES (CAP TABLE) ---
        # Restar al vendedor
        df_cap.loc[filtro_vendedor, 'Acciones'] -= acciones_a_vender
        
        # Sumar o Crear al comprador
        filtro_comprador = (df_cap['Asset_ID'] == asset_id) & (df_cap['Soberano'] == comprador)
        if filtro_comprador.any():
            df_cap.loc[filtro_comprador, 'Acciones'] += acciones_a_vender
        else:
            nueva_fila = {'Asset_ID': asset_id, 'Soberano': comprador, 'Acciones': acciones_a_vender}
            df_cap = pd.concat([df_cap, pd.DataFrame([nueva_fila])], ignore_index=True)
        
        # Guardar todo
        df_cuentas.to_csv(CUENTAS, index=False)
        df_cap.to_csv(CAP_TABLE, index=False)

        print("\n" + "✔"*60)
        print("     TRANSFERENCIA ACCIONARIA COMPLETADA")
        print("✔"*60)

        # Sincronizar Certificados y Nexus
        regenerar_certs()
        actualizar_dashboard()
    else:
        print("Operación cancelada.")

if __name__ == "__main__":
    transferencia_fraccionada()