import pandas as pd
from datetime import datetime

# INFRAESTRUCTURA
LEDGER = "Truth_Ledger_Master.csv"
CAP_TABLE = "Delphia_Cap_Table.csv"
CUENTAS = "Delphia_Bank_Accounts.csv"

def ejecutar_distribucion_yield():
    print(f"\n--- ⏳ INICIANDO EMISIÓN Y DISTRIBUCIÓN DE RENTAS ({datetime.now().strftime('%Y-%m')}) ---")
    
    df_ledger = pd.read_csv(LEDGER)
    df_cap = pd.read_csv(CAP_TABLE)
    df_cuentas = pd.read_csv(CUENTAS)

    if 'Yield_Anual_DPX' not in df_ledger.columns:
        print("[!] No se encontró la columna 'Yield_Anual_DPX' en el Ledger. Ejecuta Nexus primero o créala manualmente.")
        return

    pagos_realizados = 0

    # 1. Iterar sobre activos que generen valor (Yield > 0)
    for _, asset in df_ledger[df_ledger['Yield_Anual_DPX'] > 0].iterrows():
        a_id = asset['Asset_ID']
        
        # Matemática: Yield Anual Total dividido entre 12 meses
        yield_mensual_total = asset['Yield_Anual_DPX'] / 12  
        total_shares = asset['Total_Shares']
        
        # Buscar dueños de este activo en el Cap Table
        owners = df_cap[df_cap['Asset_ID'] == a_id]
        
        for _, owner in owners.iterrows():
            soberano = owner['Soberano']
            acciones = owner['Acciones']
            
            # Cálculo proporcional de la tajada del pastel
            pago = (acciones / total_shares) * yield_mensual_total
            
            # Depositar en cuenta bancaria si el pago es mayor a 0
            if pago > 0 and soberano in df_cuentas['Soberano'].values:
                df_cuentas.loc[df_cuentas['Soberano'] == soberano, 'Saldo_DPX'] += pago
                print(f"[💰] PAYOUT: {soberano} recibió {pago:.2f} DPX por {acciones} acciones de {a_id}")
                pagos_realizados += 1

    # 2. Guardar cambios en el banco
    if pagos_realizados > 0:
        df_cuentas.to_csv(CUENTAS, index=False)
        print(f"\n[✔] DISTRIBUCIÓN COMPLETADA. Se realizaron {pagos_realizados} depósitos automáticos.")
        
        # Intentar refrescar Nexus
        try:
            from generar_nexus import ejecutar_nexus
            ejecutar_nexus()
            print("[✔] NEXUS ACTUALIZADO CON NUEVOS SALDOS.")
        except Exception as e: 
            print(f"[!] No se pudo actualizar Nexus automáticamente: {e}")
    else:
        print("\n[!] No hubo pagos que realizar este ciclo.")

if __name__ == "__main__":
    ejecutar_distribucion_yield()