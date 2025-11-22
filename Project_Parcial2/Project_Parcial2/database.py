import mysql.connector
from mysql.connector import Error

def crear_conexion():
    #Crear la conexion con la base de datos Mysql
    try:
        conexion = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'poo_proyecto_parcial2'
            )

        if conexion.is_connected():
            print("Conexion con Msql establecida")
            return conexion
        return None
        
    except Error as e:
        print(f"Error al conectar con Msql: {e}")
        return None
    