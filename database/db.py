import mysql.connector
from mysql.connector import errorcode
import json
import os

def crear_conexion():
    """
    Crea una conexión a la base de datos MySQL leyendo los detalles
    desde el archivo config_db.json.
    """
    # Construir la ruta absoluta al archivo de configuración
    # Se asume que config_db.json está en la carpeta raíz del proyecto,
    # un nivel arriba de este archivo (database/db.py)
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_config = os.path.join(ruta_base, 'config_db.json')

    try:
        # Asegurarse de que el archivo de configuración existe
        if not os.path.exists(ruta_config):
            print("❌ Error Crítico: No se encontró el archivo 'config_db.json'.")
            print(f"   Ruta esperada: {ruta_config}")
            return None
            
        with open(ruta_config, 'r', encoding='utf-8') as f:
            config = json.load(f)

        conn = mysql.connector.connect(**config)
        return conn

    except mysql.connector.Error as err:
        print("="*50)
        print("❌ ERROR DE CONEXIÓN A LA BASE DE DATOS MYSQL ❌")
        print(f"   Error: {err}")
        print("   Por favor, revisa los datos en tu archivo 'config_db.json'.")
        print("="*50)
        return None
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo de configuración en la ruta: {ruta_config}")
        return None