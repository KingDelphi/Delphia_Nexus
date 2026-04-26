import pandas as pd
import os
import uuid
from datetime import datetime

# INFRAESTRUCTURA
LEDGER = "Truth_Ledger_Master.csv"
CAP_TABLE = "Delphia_Cap_Table.csv"
CUENTAS = "Delphia_Bank_Accounts.csv"
MERCADO = "Market_Orders.csv"

def registrar_log(accion):
    with open("Delphia_Audit_Log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {accion}\n")

def crear_orden(asset_id, vendedor, precio_dpx):
    """Registra una intención de venta en el mercado."""
    df_mercado = pd.read_csv(MERCADO)
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    nueva_orden = {
        'Order_ID': order_id,
        'Asset_ID': asset_id,
        'Vendedor': vendedor,
        'Acciones': 1,
        'Precio_DPX': float(precio_dpx),
        'Status': 'OPEN'
    }
    
    df_mercado = pd.concat([df_mercado, pd.DataFrame([nueva_orden])], ignore_index=True)
    df_mercado.to_csv(MERCADO, index=False)
    registrar_log(f"ORDEN CREADA: {order_id} por {vendedor}")
    print(f"[🚀] Mercado Actualizado: {asset_id} a la venta.")

def ejecutar_pago_nomina(soberano_destino, monto_dpx, concepto):
    """
    Función especial para pagar a la VP o colaboradores desde la Boveda_Arquitecto
    o por emisión central.
    """
    df_cuentas = pd.read_csv(CUENTAS)
    arquitecto = "Boveda_Arquitecto"
    
    if arquitecto not in df_cuentas['Soberano'].values:
        return print("[!] Error: No existe la cuenta del Arquitecto.")

    saldo_arq = df_cuentas.loc[df_cuentas['Soberano'] == arquitecto, 'Saldo_DPX'].values[0]
    
    if saldo_arq < monto_dpx:
        return print(f"[!] Fondos insuficientes en Boveda_Arquitecto ({saldo_arq} DPX)")

    # Transferencia
    df_cuentas.loc[df_cuentas['Soberano'] == arquitecto, 'Saldo_DPX'] -= monto_dpx
    df_cuentas.loc[df_cuentas['Soberano'] == soberano_destino, 'Saldo_DPX'] += monto_dpx
    
    df_cuentas.to_csv(CUENTAS, index=False)
    registrar_log(f"NOMINA: {monto_dpx} DPX enviados a {soberano_destino} por: {concepto}")
    print(f"[👑] PAGO REALIZADO: {monto_dpx} DPX a {soberano_destino}.")

def ejecutar_compra(order_id, comprador):
    """Procesa el pago y transfiere la propiedad."""
    df_mercado = pd.read_csv(MERCADO)
    df_cuentas = pd.read_csv(CUENTAS)
    df_cap = pd.read_csv(CAP_TABLE)
    
    idx_orden = df_mercado.index[(df_mercado['Order_ID'] == order_id) & (df_mercado['Status'] == 'OPEN')]
    if idx_orden.empty: return print("[!] Orden inválida.")
    
    orden = df_mercado.loc[idx_orden[0]]
    asset_id, vendedor, precio = orden['Asset_ID'], orden['Vendedor'], orden['Precio_DPX']
    
    saldo_comp = df_cuentas.loc[df_cuentas['Soberano'] == comprador, 'Saldo_DPX'].values[0]
    
    if saldo_comp < precio: return print("[!] Fondos insuficientes.")

    # TRANSACCIÓN
    df_cuentas.loc[df_cuentas['Soberano'] == comprador, 'Saldo_DPX'] -= precio
    df_cuentas.loc[df_cuentas['Soberano'] == vendedor, 'Saldo_DPX'] += precio
    
    # Propiedad
    df_cap.loc[(df_cap['Asset_ID'] == asset_id) & (df_cap['Soberano'] == vendedor), 'Acciones'] -= 1
    reg_comp = df_cap[(df_cap['Asset_ID'] == asset_id) & (df_cap['Soberano'] == comprador)]
    
    if reg_comp.empty:
        df_cap = pd.concat([df_cap, pd.DataFrame([{'Asset_ID': asset_id, 'Soberano': comprador, 'Acciones': 1}])], ignore_index=True)
    else:
        df_cap.loc[(df_cap['Asset_ID'] == asset_id) & (df_cap['Soberano'] == comprador), 'Acciones'] += 1
    
    df_mercado.loc[idx_orden[0], 'Status'] = 'CLOSED'
    df_cap = df_cap[df_cap['Acciones'] > 0]
    
    # Persistencia
    df_cuentas.to_csv(CUENTAS, index=False)
    df_cap.to_csv(CAP_TABLE, index=False)
    df_mercado.to_csv(MERCADO, index=False)
    
    registrar_log(f"TRANSACCION: {comprador} compró {asset_id} a {vendedor}")
    print(f"[✔] ÉXITO: Propiedad de {asset_id} transferida a {comprador}.")