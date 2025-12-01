from database.db import crear_conexion

def obtener_creditos():
    """
    Obtiene todos los créditos de la base de datos.
    """
    conn = crear_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM creditos")
    datos = cursor.fetchall()
    conn.close()
    return datos

def crear_credito(cliente, serie, venta, dias, vence, monto):
    """
    Inserta un nuevo registro de crédito en la base de datos.
    """
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO creditos (cliente, serie, venta, dias, vence, monto) VALUES (%s, %s, %s, %s, %s, %s)",
        (cliente, serie, venta, dias, vence, monto)
    )
    conn.commit()
    conn.close()
