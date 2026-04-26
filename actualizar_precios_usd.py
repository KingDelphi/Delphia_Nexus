import pandas as pd
import os

ARCHIVO_LEDGER = "Truth_Ledger_Master.csv"
TIPO_CAMBIO = 18.00  # 1 USD = 18 MXN

def actualizar_moneda():
    if not os.path.exists(ARCHIVO_LEDGER):
        print("[X] El Ledger no existe.")
        return

    df = pd.read_csv(ARCHIVO_LEDGER)
    
    # 1. Actualizar Activos de la Matriarca (De MXN a USD con incremento)
    def convertir_a_usd(valor):
        try:
            # Limpiar el string de moneda
            num = float(str(valor).replace('$', '').replace(',', ''))
            # Convertir y redondear a la centena superior para "subir el precio"
            precio_usd = (num / TIPO_CAMBIO) * 1.15  # Agregamos un 15% de prima Delphica
            return round(precio_usd, 2)
        except:
            return 0.0

    # 2. Definir valores para los documentos del Arquitecto
    valores_documentos = {
        "Carta Magna - Celestia (v5.0).pages": 5000.00,
        "ANGELOGENESIS Y METAVERSO FUNDACIONAL.pdf": 4500.00,
        "Introducción a los Principios de la Arquitectura del Sistema Delphis.pdf": 3500.00,
        "Codex Pingoloide Absoluto": 3000.00, # Búsqueda parcial
        "_DelphiON_v.1.delphicLoop.numbers": 3000.00,
        "The K-VI Multiversal Menagerie.png": 2500.00
    }

    print("--- Iniciando Revaluación a USD ---")

    for index, row in df.iterrows():
        # Caso Matriarca: Conversión
        if row['Soberano'] == 'Boveda_Matriarca':
            df.at[index, 'Valor'] = f"${convertir_a_usd(row['Valor'])}"
        
        # Caso Arquitecto: Asignación por tipo
        elif row['Soberano'] == 'Boveda_Arquitecto':
            nombre = row['Nombre']
            
            # Es un Documento Fundacional?
            asignado = False
            for doc, precio in valores_documentos.items():
                if doc in nombre:
                    df.at[index, 'Valor'] = f"${precio}"
                    df.at[index, 'Categoria'] = "Documento Fundacional"
                    asignado = True
                    break
            
            # Es un Himno? (MP3)
            if not asignado and (".mp3" in nombre.lower() or "DΞLPHI" in nombre or "DΞLPHIVM" in nombre):
                df.at[index, 'Valor'] = "$500.00"
                df.at[index, 'Categoria'] = "Himno Nacional"
            
            # Otros archivos del Arquitecto (PNG, etc que no sean fundacionales)
            elif not asignado:
                df.at[index, 'Valor'] = "$100.00"

    # Guardar cambios
    df.to_csv(ARCHIVO_LEDGER, index=False)
    print("[✔] Ledger revaluado exitosamente a USD.")

if __name__ == "__main__":
    actualizar_moneda()