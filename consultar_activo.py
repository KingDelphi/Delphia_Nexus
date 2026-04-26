import pandas as pd
import hashlib
import os

ARCHIVO_LEDGER = "Truth_Ledger_Master.csv"
RAIZ_BOVEDAS = "Boveda_Activos"

def generar_hash(ruta):
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""): sha.update(bloque)
    return sha.hexdigest()

def consulta_delphica():
    if not os.path.exists(ARCHIVO_LEDGER):
        print("[X] ERROR: El Ledger no existe. Corre la ingesta primero.")
        return

    df = pd.read_csv(ARCHIVO_LEDGER)
    busqueda = input("ID o Nombre del Activo a verificar: ").strip()
    
    # Buscar en el Ledger por ID o por Nombre
    resultado = df[(df['Asset_ID'] == busqueda) | (df['Nombre'] == busqueda)]
    
    if resultado.empty:
        print(f"\n[X] ERROR: '{busqueda}' no encontrado en el Ledger de Verdad.")
        return

    activo = resultado.iloc[0]
    nombre_sin_ext = activo['Nombre']
    
    # LOCALIZACIÓN INTELIGENTE DEL ARCHIVO
    ruta_encontrada = None
    hash_actual = None

    for raiz, dirs, archivos in os.walk(RAIZ_BOVEDAS):
        for f in archivos:
            # Comparamos el nombre del archivo sin su extensión
            if os.path.splitext(f)[0] == nombre_sin_ext or f == busqueda:
                ruta_encontrada = os.path.join(raiz, f)
                hash_actual = generar_hash(ruta_encontrada)
                break
    
    print("\n" + "="*50)
    print("         FICHA DE IDENTIDAD DELPHICA")
    print("="*50)
    print(f" ID SOBERANO: {activo['Asset_ID']}")
    print(f" NOMBRE:      {activo['Nombre']}")
    print(f" CATEGORÍA:   {activo['Categoria']}")
    print(f" PROPIETARIO: {activo['Soberano']}")
    print(f" VALOR REF:   {activo['Valor']}")
    print("-" * 50)
    
    if ruta_encontrada:
        if str(hash_actual) == str(activo['Hash']):
            print(" STATUS:      [✔] VERIFICADO - INTEGRIDAD TOTAL")
            print(f" RUTA:        {ruta_encontrada}")
        else:
            print(" STATUS:      [!] ALERTA - ARCHIVO ALTERADO")
            print(f" HASH ORIG:   {activo['Hash'][:15]}...")
            print(f" HASH ACTU:   {hash_actual[:15]}...")
    else:
        print(" STATUS:      [?] ARCHIVO FÍSICO NO LOCALIZADO")
        print(" NOTA:        Asegúrate de que el archivo esté en Boveda_Activos.")
    print("="*50 + "\n")

if __name__ == "__main__":
    consulta_delphica()