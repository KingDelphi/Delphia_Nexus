import pandas as pd
import os

LEDGER = "Truth_Ledger_Master.csv"
CAP_TABLE = "Delphia_Cap_Table.csv"
CARPETA = "Certificados_Emitidos"

def obtener_estilo():
    return """
    <style>
        body { background:#0a0a0a; color:#e0e0e0; font-family:'Helvetica Neue',sans-serif; display:flex; justify-content:center; padding:50px; }
        .cert { border:2px solid #c5a059; padding:40px; width:750px; background:linear-gradient(145deg, #121212, #1a1a1a); box-shadow:0 0 50px rgba(197,160,89,0.2); }
        .header { text-align:center; border-bottom:1px solid #333; padding-bottom:20px; }
        .header h1 { color:#c5a059; letter-spacing:5px; margin:0; font-size:24px; }
        .title { font-size:32px; text-align:center; margin:30px 0; font-weight:200; color:#fff; }
        .grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; font-size:13px; }
        .label { color:#c5a059; text-transform:uppercase; font-size:10px; font-weight:bold; }
        .value { margin-top:5px; color:#fff; font-family:'Courier New',monospace; border-bottom: 1px solid #222; padding-bottom:5px; }
        .hash-area { margin-top:30px; padding:20px; background:#000; border:1px solid #c5a059; border-radius:5px; }
        .hash-val { font-family:'Courier New',monospace; font-size:11px; word-break:break-all; color:#00ff88; text-align:center; }
        .footer { margin-top:40px; text-align:center; font-size:9px; color:#555; border-top:1px solid #333; padding-top:20px; }
    </style>
    """

def crear_html(row, sob, part, es_maestro=True):
    tipo = "CERTIFICADO DE AUTENTICIDAD MAESTRO" if es_maestro else "TÍTULO DE PROPIEDAD ACCIONARIA"
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8">{obtener_estilo()}</head>
    <body>
        <div class="cert">
            <div class="header"><h1>DELPHIA NEXUS</h1><p>REGISTRO INMUTABLE KARDASHEV VI</p></div>
            <div class="title">{tipo}</div>
            <div class="grid">
                <div><div class="label">ID ACTIVO</div><div class="value">{row['Asset_ID']}</div></div>
                <div><div class="label">SOBERANO REGISTRADO</div><div class="value">{sob}</div></div>
                <div><div class="label">NOMBRE DEL ACTIVO</div><div class="value">{row['Nombre']}</div></div>
                <div><div class="label">PARTICIPACIÓN</div><div class="value">{part}</div></div>
                <div><div class="label">FECHA DE REGISTRO</div><div class="value">{row['Fecha']}</div></div>
                <div><div class="label">ESTATUS</div><div class="value">VERIFICADO [CHRONOS-SIGMA]</div></div>
            </div>
            <div class="hash-area">
                <div class="label" style="text-align:center; margin-bottom:10px;">HASH DE VERDAD COMPLETO (SHA-256)</div>
                <div class="hash-val">{row['Hash']}</div>
            </div>
            <div class="footer">La alteración de este documento anula su validez en el Ledger de Delphia.</div>
        </div>
    </body></html>
    """

def ejecutar():
    if not os.path.exists(CARPETA): os.makedirs(CARPETA)
    df_l, df_c = pd.read_csv(LEDGER), pd.read_csv(CAP_TABLE)
    
    # 1. Maestros (100% - Independiente de dueños individuales)
    for _, r in df_l.iterrows():
        # Para el maestro usamos el soberano original del ledger
        html = crear_html(r, r['Soberano'], "100% (PROPIEDAD TOTAL)", True)
        with open(f"{CARPETA}/Certificado_{r['Asset_ID']}_{r['Nombre']}.html", "w", encoding="utf-8") as f:
            f.write(html)

    # 2. Títulos Individuales (Ej: El 1% de Fede)
    for _, r in df_c.iterrows():
        asset = df_l[df_l['Asset_ID'] == r['Asset_ID']].iloc[0]
        pct = (r['Acciones'] / asset['Total_Shares']) * 100
        part = f"{r['Acciones']} / {asset['Total_Shares']} SHARES ({pct:.1f}%)"
        html = crear_html(asset, r['Soberano'], part, False)
        with open(f"{CARPETA}/Titulo_{r['Soberano']}_{asset['Asset_ID']}.html", "w", encoding="utf-8") as f:
            f.write(html)
    print("[✔] Certificados y Títulos generados con éxito.")

if __name__ == "__main__": ejecutar()