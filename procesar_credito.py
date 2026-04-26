import pandas as pd
import datetime

LEDGER = "Truth_Ledger_Master.csv"
CUENTAS = "Delphia_Bank_Accounts.csv"

def otorgar_credito(soberano, lista_asset_ids):
    df_l = pd.read_csv(LEDGER)
    df_c = pd.read_csv(CUENTAS)
    
    monto_total_credito = 0
    
    # 1. Bloquear Activos y calcular valor
    for aid in lista_asset_ids:
        # Limpiar el precio (quitar $ y ,)
        valor_str = str(df_l.loc[df_l['Asset_ID'] == aid, 'Valor'].values[0])
        valor = float(valor_str.replace('$', '').replace(',', ''))
        
        # El crédito es el 50% del valor del activo
        monto_total_credito += (valor * 0.5)
        
        # Cambiar status a COLATERAL
        df_l.loc[df_l['Asset_ID'] == aid, 'Status'] = "COLATERAL_BANCARIO"
    
    # 2. Inyectar DPX a la cuenta del usuario
    # Restamos de la Bóveda Arquitecto (Emisor) y sumamos al usuario
    df_c.loc[df_c['Soberano'] == 'Boveda_Arquitecto', 'Saldo_DPX'] -= monto_total_credito
    df_c.loc[df_c['Soberano'] == soberano, 'Saldo_DPX'] += monto_total_credito
    
    # 3. Guardar cambios
    df_l.to_csv(LEDGER, index=False)
    df_c.to_csv(CUENTAS, index=False)
    
    print(f"--- 🏛️ CRÉDITO APROBADO ---")
    print(f"Soberano: {soberano}")
    print(f"Monto: {monto_total_credito} DPX")
    print(f"Activos pignorados: {len(lista_asset_ids)}")

if __name__ == "__main__":
    # Esto es para pruebas manuales, luego lo activará el Dashboard
    # otorgar_credito('Boveda_Matriarca', ['DLPH-BA7B9E7C'])
    pass