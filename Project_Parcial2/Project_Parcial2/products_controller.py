from database import crear_conexion

def ver_productos():
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre_producto, marca, precio, stock FROM productos")
        productos = cursor.fetchall()
        conexion.close()
        return productos
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []

def agregar_producto(nombre, marca, precio, stock):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre_producto, marca, precio, stock, proveedor, status, descripcion)
            VALUES (%s, %s, %s, %s, '', 1, '')
        """, (nombre, marca, precio, stock))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al agregar producto: {e}")
        return False

def actualizar_producto(id_producto, nombre, marca, precio, stock):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE productos SET nombre_producto = %s, marca = %s, precio = %s, stock = %s
            WHERE id_producto = %s
        """, (nombre, marca, precio, stock, id_producto))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
        return False

def eliminar_producto(id_producto):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return False