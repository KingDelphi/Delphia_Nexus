import pandas as pd
import os

ARCHIVO_LEDGER = "Truth_Ledger_Master.csv"

def generar_reporte():
    if not os.path.exists(ARCHIVO_LEDGER):
        print("[X] No hay Ledger activo.")
        return

    df = pd.read_csv(ARCHIVO_LEDGER)
    
    # Limpiar la columna Valor por si tiene signos de pesos o comas
    df['Valor_Num'] = df['Valor'].replace('[\$,]', '', regex=True).astype(float)
    
    print("\n" + "═"*60)
    print("         REPORTE DE PATRIMONIO TOTAL - DELPHIA")
    print("═"*60)
    
    # Resumen por Soberano
    resumen = df.groupby('Soberano').agg({
        'Asset_ID': 'count',
        'Valor_Num': 'sum'
    }).rename(columns={'Asset_ID': 'Total Activos', 'Valor_Num': 'Valor Total (USD)'})
    
    print(resumen)
    print("─"*60)
    
    gran_total_activos = df['Asset_ID'].count()
    gran_total_valor = df['Valor_Num'].sum()
    
    print(f" TOTAL ACTIVOS EN EL REINO:  {gran_total_activos}")
    print(f" VALOR TOTAL CERTIFICADO:    ${gran_total_valor:,.2f}")
    print("═"*60 + "\n")
    
    # Alerta de integridad
    if 'Status' in df.columns and (df['Status'] != 'VERIFICADO').any():
        print(" [!] ATENCIÓN: Existen activos con alertas de integridad.")
    else:
        print(" [✔] Estatus del Reino: INTEGRIDAD TOTAL CONFIRMADA")

if __name__ == "__main__":
    generar_reporte()