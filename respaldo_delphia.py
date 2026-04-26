import shutil
import os
from datetime import datetime

def respaldar():
    archivos_criticos = [
        "Truth_Ledger_Master.csv",
        "Delphia_Cap_Table.csv",
        "Delphia_Bank_Accounts.csv"
    ]
    
    # Crear carpeta de backups si no existe
    if not os.path.exists("backups"): os.makedirs("backups")
    
    # Nombre de la carpeta con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_respaldo = os.path.join("backups", f"Backup_{timestamp}")
    os.makedirs(ruta_respaldo)
    
    for archivo in archivos_criticos:
        if os.path.exists(archivo):
            shutil.copy(archivo, os.path.join(ruta_respaldo, archivo))
            print(f"[Backup] {archivo} guardado.")
    
    print(f"\n[✔] RESPALDO COMPLETADO EN: {ruta_respaldo}")

if __name__ == "__main__": respaldar()