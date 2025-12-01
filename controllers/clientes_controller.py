from database.db import crear_conexion

def agregar_cliente_y_obtener(nombre, telefono, email=None):
    """
    Agrega un nuevo cliente a la base de datos y devuelve sus datos, incluido el ID.
    """
    conn = crear_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        # Insertar el nuevo cliente
        cursor.execute(
            "INSERT INTO clientes (nombre, telefono, email) VALUES (%s, %s, %s)",
            (nombre, telefono, email)
        )
        id_cliente = cursor.lastrowid
        conn.commit()

        # Obtener los datos del cliente recién creado
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        cliente_creado = cursor.fetchone()
        return cliente_creado
    except Exception as e:
        conn.rollback()
        print(f"Error al agregar cliente: {e}")
        return None
    finally:
        conn.close()

def obtener_clientes():
    """
    Obtiene todos los clientes de la base de datos.
    """
    conn = crear_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_cliente, nombre, telefono, email FROM clientes ORDER BY nombre")
    datos = cursor.fetchall()
    conn.close()
    return datos

def agregar_cliente(nombre, telefono, email=None):
    """
    Agrega un nuevo cliente a la base de datos (versión simple).
    """
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, telefono, email) VALUES (%s, %s, %s)", (nombre, telefono, email))
    conn.commit()
    conn.close()
    return True