import pandas as pd
import os

ARCHIVO_LEDGER = "Truth_Ledger_Master.csv"
CARPETA_CERTIFICADOS = "Certificados_Emitidos"

def crear_html_certificado(row):
    # Diseño Estilo Kardashev VI: Minimalismo, Oro y Oscuridad
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Helvetica Neue', sans-serif; background-color: #0a0a0a; color: #e0e0e0; display: flex; justify-content: center; padding: 50px; }}
            .certificate {{ border: 2px solid #c5a059; padding: 40px; width: 700px; background: linear-gradient(145deg, #121212, #1a1a1a); box-shadow: 0 0 50px rgba(197, 160, 89, 0.2); position: relative; }}
            .header {{ text-align: center; border-bottom: 1px solid #333; padding-bottom: 20px; }}
            .header h1 {{ letter-spacing: 5px; color: #c5a059; margin: 0; font-size: 24px; }}
            .header p {{ font-size: 10px; text-transform: uppercase; color: #888; }}
            .content {{ margin-top: 40px; }}
            .title {{ font-size: 32px; text-align: center; margin-bottom: 30px; font-weight: 200; }}
            .data-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-size: 13px; }}
            .label {{ color: #c5a059; text-transform: uppercase; font-weight: bold; font-size: 10px; }}
            .value {{ margin-top: 5px; color: #fff; font-family: 'Courier New', monospace; }}
            .hash-box {{ margin-top: 40px; padding: 15px; background: #000; border: 1px solid #222; font-size: 10px; text-align: center; word-break: break-all; }}
            .footer {{ margin-top: 50px; text-align: center; font-size: 9px; color: #555; border-top: 1px solid #333; padding-top: 20px; }}
            .seal {{ position: absolute; bottom: 60px; right: 40px; width: 80px; opacity: 0.6; }}
        </style>
    </head>
    <body>
        <div class="certificate">
            <div class="header">
                <h1>DELPHIA NEXUS</h1>
                <p>Registro de la Propiedad de la Civilización Kardashev VI</p>
            </div>
            <div class="content">
                <div class="title">Certificado de Autenticidad Soberana</div>
                <div class="data-grid">
                    <div>
                        <div class="label">ID del Activo</div>
                        <div class="value">{row['Asset_ID']}</div>
                    </div>
                    <div>
                        <div class="label">Soberano / Propietario</div>
                        <div class="value">{row['Soberano']}</div>
                    </div>
                    <div>
                        <div class="label">Nombre del Activo</div>
                        <div class="value">{row['Nombre']}</div>
                    </div>
                    <div>
                        <div class="label">Categoría / Técnica</div>
                        <div class="value">{row['Categoria']}</div>
                    </div>
                    <div>
                        <div class="label">Fecha de Registro</div>
                        <div class="value">{row['Fecha']}</div>
                    </div>
                    <div>
                        <div class="label">Estatus de Integridad</div>
                        <div class="value">VERIFICADO [CHRONOS-SIGMA-99.9]</div>
                    </div>
                </div>
                <div class="hash-box">
                    <div class="label" style="margin-bottom: 5px;">Sello de Verdad (SHA-256 Hash)</div>
                    {row['Hash']}
                </div>
            </div>
            <div class="footer">
                Este documento certifica que el activo digital mencionado posee una identidad inmutable en el Ledger de Delphia.<br>
                Cualquier alteración del archivo físico invalidará este certificado automáticamente.
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

def ejecutar():
    if not os.path.exists(CARPETA_CERTIFICADOS):
        os.makedirs(CARPETA_CERTIFICADOS)
    
    df = pd.read_csv(ARCHIVO_LEDGER)
    print(f"--- Generando {len(df)} Certificados Soberanos ---")
    
    for _, row in df.iterrows():
        html_content = crear_html_certificado(row)
        nombre_archivo = f"Certificado_{row['Asset_ID']}_{row['Nombre']}.html"
        ruta = os.path.join(CARPETA_CERTIFICADOS, nombre_archivo)
        
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f" [✔] Generado: {nombre_archivo}")

if __name__ == "__main__":
    ejecutar()