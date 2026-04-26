import pandas as pd
import os

ARCHIVO_CUENTAS = "Delphia_Bank_Accounts.csv"

def gestionar_banco():
    # 1. Crear el banco si no existe
    if not os.path.exists(ARCHIVO_CUENTAS):
        data = {
            'Soberano': ['Boveda_Arquitecto', 'Boveda_Matriarca'],
            'Saldo_DPX': [100000.0, 0.0], # El Arquitecto inicia con reserva técnica
            'Status': ['ACTIVO', 'ACTIVO'],
            'Tipo': ['FUNDADOR', 'FUNDADOR']
        }
        pd.DataFrame(data).to_csv(ARCHIVO_CUENTAS, index=False)
        print("[✔] Banco Central de Delphia Inicializado.")

    # 2. Función para dar de alta a tus inversores
    def dar_de_alta(nombre, inversion_convertida):
        df = pd.read_csv(ARCHIVO_CUENTAS)
        if nombre not in df['Soberano'].values:
            nueva_fila = {
                'Soberano': nombre, 
                'Saldo_DPX': inversion_convertida, 
                'Status': 'ACTIVO',
                'Tipo': 'INVERSIONISTA_BETA'
            }
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            df.to_csv(ARCHIVO_CUENTAS, index=False)
            print(f"[✔] Soberano reconocido: {nombre} | Saldo: {inversion_convertida} DPX")

    # --- LISTA DE SOCIOS FUNDADORES ---
    # dar_de_alta("SOCIO_NOMBRE_01", monto_mxn / 18.0)

# El de inversión máxima
    dar_de_alta("SOCIO_FEDE_BARRERA_01", 30000 / 18.0)
    dar_de_alta("SOCIO_RICK_CATARIO_02", 20000 / 18.0)
    dar_de_alta("SOCIO_EDUARDO_ROJO_03", 20000 / 18.0)
    dar_de_alta("SOCIO_RAFA_RAPTHOR_04", 10000 / 18.0)
    dar_de_alta("SOCIO_ROBERTO_RIOS_05", 10000 / 18.0)
    dar_de_alta("SOCIO_ROB_CATARIO_06", 6000 / 18.0)
    dar_de_alta("SOCIO_DENISE_RICK_CATARIO_07", 4000 / 18.0)
    dar_de_alta("SOCIO_MAURICIO_BARRERA_08", 2000 / 18.0)
    dar_de_alta("SOCIO_SERGIO_CHAVEZ_09", 2000 / 18.0)
# El de inversión mínima

if __name__ == "__main__":
    gestionar_banco()