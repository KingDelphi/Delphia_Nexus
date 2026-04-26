
import os
import csv
import uuid
import hashlib
from datetime import datetime

# CONFIGURACIÓN
RAIZ_BOVEDAS = "Boveda_Activos" 
ARCHIVO_LEDGER = "Truth_Ledger_Master.csv"

def generar_hash(ruta):
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha.update(bloque)
    return sha.hexdigest()

def cargar_metadata_externa(ruta_csv):
    metadata = {}
    if os.path.exists(ruta_csv):
        with open(ruta_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for fila in reader:
                metadata[fila['Archivo']] = fila
    return metadata

def procesar_sistema():
    activos_totales = []
    for usuario in os.listdir(RAIZ_BOVEDAS):
        ruta_u = os.path.join(RAIZ_BOVEDAS, usuario)
        if os.path.isdir(ruta_u) and not usuario.startswith('.'):
            # Cargar metadata si existe el CSV en la carpeta del usuario
            csv_meta = os.path.join(ruta_u, "Datos_Cuadros.csv")
            dic_meta = cargar_metadata_externa(csv_meta)
            
            for raiz, dirs, archivos in os.walk(ruta_u):
                for nombre_f in archivos:
                    if nombre_f.startswith('.') or nombre_f.endswith('.csv'): continue
                    
                    ruta_c = os.path.join(raiz, nombre_f)
                    meta = dic_meta.get(nombre_f, {})
                    
                    activos_totales.append({
                        "Asset_ID": "DLPH-" + str(uuid.uuid4())[:8].upper(),
                        "Soberano": usuario,
                        "Nombre": meta.get('Nombre_Obra', nombre_f),
                        "Hash": generar_hash(ruta_c),
                        "Categoria": meta.get('Tecnica', 'General'),
                        "Valor": meta.get('Precio', '0'),
                        "Status": "VERIFICADO",
                        "Fecha": datetime.now().strftime("%Y-%m-%d")
                    })
    return activos_totales

def guardar(activos):
    columnas = ["Asset_ID", "Soberano", "Nombre", "Hash", "Categoria", "Valor", "Status", "Fecha"]
    with open(ARCHIVO_LEDGER, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(activos)
    print(f"[✔] Ledger actualizado: {len(activos)} activos.")

if __name__ == "__main__":
    guardar(procesar_sistema())