from database.db import crear_conexion

def crear_apartado_completo(cliente_id, productos, monto_anticipo=0.0, dias_vencimiento=15):
    """
    Crea un registro de apartado, su detalle de productos y descuenta el stock.
    Devuelve el ID del nuevo apartado si tiene éxito.
    """
    conn = crear_conexion()
    cursor = conn.cursor()
    total_apartado = 0

    try:
        # Calcular el total basado en los precios de la BD
        for item in productos:
            cursor.execute("SELECT precio, stock FROM productos WHERE nombre = %s", (item['nombre'],))
            producto_db = cursor.fetchone()
            if not producto_db or producto_db[1] < item['cantidad']:
                conn.rollback() # No hay suficiente stock
                conn.close()
                return None
            total_apartado += producto_db[0] * item['cantidad']

        # 1. Crear el registro principal del apartado
        sql_apartado = """
        INSERT INTO apartados (id_cliente, total, anticipo, fecha_vencimiento)
        VALUES (%s, %s, %s, CURDATE() + INTERVAL %s DAY)
        """
        cursor.execute(sql_apartado, (cliente_id, total_apartado, monto_anticipo, dias_vencimiento))
        id_apartado = cursor.lastrowid

        # 2. Insertar cada producto en el detalle y descontar stock
        for item in productos:
            cursor.execute("SELECT id_producto, precio FROM productos WHERE nombre = %s", (item['nombre'],))
            producto_db = cursor.fetchone()
            id_producto = producto_db[0]
            precio_unitario = producto_db[1]

            cursor.execute("INSERT INTO detalle_apartado (id_apartado, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                           (id_apartado, id_producto, item['cantidad'], precio_unitario))
            
            cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (item['cantidad'], id_producto))

        conn.commit()
        return id_apartado
    except Exception as e:
        conn.rollback()
        print(f"Error al crear apartado: {e}")
        return None
    finally:
        conn.close()