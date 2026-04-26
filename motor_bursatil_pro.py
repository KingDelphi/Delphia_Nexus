import pandas as pd
import os

LEDGER = "Truth_Ledger_Master.csv"
CUENTAS = "Delphia_Bank_Accounts.csv"
CAP_TABLE = "Delphia_Cap_Table.csv"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_datos():
    return pd.read_csv(LEDGER), pd.read_csv(CUENTAS), pd.read_csv(CAP_TABLE)

def guardar_datos(df_cuentas, df_cap):
    df_cuentas.to_csv(CUENTAS, index=False)
    df_cap.to_csv(CAP_TABLE, index=False)
    print("\n[✔] REGISTROS INMUTABLES ACTUALIZADOS EN EL LEDGER.")
    
    try:
        from generar_nexus import ejecutar_nexus
        ejecutar_nexus()
        print("[✔] NEXUS DASHBOARD ACTUALIZADO AUTOMÁTICAMENTE.")
    except Exception as e:
        print(f"[!] No se pudo actualizar el Dashboard automáticamente: {e}")

def ver_cuentas(df_cuentas):
    print("\n--- 🏦 ESTADO DEL BANCO CENTRAL DE DELPHIA ---")
    for _, r in df_cuentas.iterrows():
        print(f"Soberano: {r['Soberano']} | Saldo: {r['Saldo_DPX']:.2f} DPX | Status: {r['Status']}")

def transferir_dpx():
    df_ledger, df_cuentas, df_cap = cargar_datos()
    ver_cuentas(df_cuentas)
    
    print("\n--- 💸 TRANSFERENCIA DE LIQUIDEZ P2P (MERCADO SECUNDARIO) ---")
    origen = input("ID Soberano Origen (Quien envía): ").strip()
    destino = input("ID Soberano Destino (Quien recibe): ").strip()
    
    if origen not in df_cuentas['Soberano'].values or destino not in df_cuentas['Soberano'].values:
        print("[!] Error: Uno de los Soberanos no existe en el registro bancario.")
        return

    try:
        monto = float(input("Cantidad de DPX a transferir: "))
    except:
        print("[!] Cantidad inválida.")
        return

    saldo_origen = df_cuentas.loc[df_cuentas['Soberano'] == origen, 'Saldo_DPX'].values[0]
    
    if monto <= 0:
        print("[!] El monto debe ser mayor a 0.")
        return
        
    if saldo_origen < monto:
        print(f"[!] FONDOS INSUFICIENTES. {origen} solo tiene {saldo_origen:.2f} DPX.")
        return

    # Ejecutar transacción
    df_cuentas.loc[df_cuentas['Soberano'] == origen, 'Saldo_DPX'] -= monto
    df_cuentas.loc[df_cuentas['Soberano'] == destino, 'Saldo_DPX'] += monto
    
    print(f"\n[⚡] TRANSACCIÓN EXITOSA: {monto} DPX transferidos de {origen} a {destino}.")
    guardar_datos(df_cuentas, df_cap)

def transferir_acciones():
    df_ledger, df_cuentas, df_cap = cargar_datos()
    
    print("\n--- 🤝 MERCADO SECUNDARIO DE ACTIVOS (P2P) ---")
    origen = input("ID Soberano Vendedor: ").strip()
    
    # Mostrar activos del vendedor
    activos_vendedor = df_cap[df_cap['Soberano'] == origen]
    if activos_vendedor.empty:
        print(f"[!] {origen} no posee activos.")
        return
        
    print(f"\nActivos de {origen}:")
    for _, r in activos_vendedor.iterrows():
        print(f"- {r['Asset_ID']} | Posee: {r['Acciones']} acciones")
        
    asset_id = input("\nID del Activo a transferir: ").strip()
    
    if asset_id not in activos_vendedor['Asset_ID'].values:
        print("[!] El vendedor no posee ese activo.")
        return
        
    destino = input("ID Soberano Comprador: ").strip()
    try:
        acciones = int(input("Cantidad de acciones a transferir: "))
    except:
        print("[!] Cantidad inválida.")
        return

    acciones_disponibles = activos_vendedor.loc[activos_vendedor['Asset_ID'] == asset_id, 'Acciones'].values[0]
    
    if acciones <= 0 or acciones > acciones_disponibles:
        print("[!] Cantidad de acciones inválida o insuficiente.")
        return

    # Restar al vendedor
    df_cap.loc[(df_cap['Soberano'] == origen) & (df_cap['Asset_ID'] == asset_id), 'Acciones'] -= acciones
    
    # Sumar al comprador (o crear registro si no lo tenía)
    registro_comprador = df_cap[(df_cap['Soberano'] == destino) & (df_cap['Asset_ID'] == asset_id)]
    if registro_comprador.empty:
        nueva_fila = pd.DataFrame([{'Asset_ID': asset_id, 'Soberano': destino, 'Acciones': acciones}])
        df_cap = pd.concat([df_cap, nueva_fila], ignore_index=True)
    else:
        df_cap.loc[(df_cap['Soberano'] == destino) & (df_cap['Asset_ID'] == asset_id), 'Acciones'] += acciones

    # Limpiar registros en cero
    df_cap = df_cap[df_cap['Acciones'] > 0]
    
    print(f"\n[⚡] TRASPASO EXITOSO: {acciones} acciones de {asset_id} transferidas a {destino}.")
    guardar_datos(df_cuentas, df_cap)

def menu():
    while True:
        print("\n=========================================")
        print("🏛️ MOTOR BURSÁTIL DELPHIA PRO (Fase P2P) ")
        print("=========================================")
        print("1. 💸 Transferir Liquidez (DPX entre usuarios)")
        print("2. 🤝 Transferir Propiedad (Acciones de activos)")
        print("3. 🏦 Ver Estado de Cuentas (Saldos)")
        print("4. 🚪 Salir")
        
        opc = input("\nSeleccione operación: ")
        
        if opc == '1': transferir_dpx()
        elif opc == '2': transferir_acciones()
        elif opc == '3': 
            _, df_cuentas, _ = cargar_datos()
            ver_cuentas(df_cuentas)
        elif opc == '4': 
            print("Cerrando terminal...")
            break
        else:
            print("[!] Opción no válida.")

if __name__ == "__main__":
    limpiar_pantalla()
    menu()