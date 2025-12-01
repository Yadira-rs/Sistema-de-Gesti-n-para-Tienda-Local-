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

        # Calcular saldo
        saldo = total_apartado - monto_anticipo

        # 1. Crear el registro principal del apartado
        sql_apartado = """
        INSERT INTO apartados (id_cliente, total, anticipo, saldo, fecha_limite, estado)
        VALUES (%s, %s, %s, %s, DATE_ADD(CURDATE(), INTERVAL %s DAY), 'Pendiente')
        """
        cursor.execute(sql_apartado, (cliente_id, total_apartado, monto_anticipo, saldo, dias_vencimiento))
        id_apartado = cursor.lastrowid

        # 2. Insertar cada producto en el detalle y descontar stock
        for item in productos:
            cursor.execute("SELECT id_producto, precio FROM productos WHERE nombre = %s", (item['nombre'],))
            producto_db = cursor.fetchone()
            id_producto = producto_db[0]
            precio_unitario = producto_db[1]
            subtotal = precio_unitario * item['cantidad']

            cursor.execute("INSERT INTO detalle_apartados (id_apartado, id_producto, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
                           (id_apartado, id_producto, item['cantidad'], subtotal))
            
            cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (item['cantidad'], id_producto))

        conn.commit()
        return id_apartado
    except Exception as e:
        conn.rollback()
        print(f"Error al crear apartado: {e}")
        return None
    finally:
        conn.close()

def listar_apartados():
    """Obtener lista de todos los apartados con información del cliente"""
    conn = crear_conexion()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT 
                a.id_apartado,
                a.fecha,
                a.total,
                a.anticipo,
                a.saldo,
                a.fecha_limite,
                a.estado,
                c.nombre AS cliente_nombre,
                c.telefono AS cliente_telefono,
                c.correo AS cliente_correo
            FROM apartados a
            LEFT JOIN clientes c ON a.id_cliente = c.id_cliente
            ORDER BY a.id_apartado DESC
        """)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error al listar apartados: {e}")
        conn.close()
        return []

def obtener_apartado_detalle(id_apartado):
    """Obtener detalle completo de un apartado incluyendo productos"""
    conn = crear_conexion()
    cur = conn.cursor(dictionary=True)
    try:
        # Obtener información del apartado
        cur.execute("""
            SELECT 
                a.*,
                c.nombre AS cliente_nombre,
                c.telefono AS cliente_telefono,
                c.correo AS cliente_correo
            FROM apartados a
            LEFT JOIN clientes c ON a.id_cliente = c.id_cliente
            WHERE a.id_apartado = %s
        """, (id_apartado,))
        apartado = cur.fetchone()
        
        if not apartado:
            conn.close()
            return None
        
        # Obtener productos del apartado
        cur.execute("""
            SELECT 
                da.cantidad,
                da.subtotal,
                p.nombre,
                p.precio
            FROM detalle_apartados da
            LEFT JOIN productos p ON da.id_producto = p.id_producto
            WHERE da.id_apartado = %s
        """, (id_apartado,))
        productos = cur.fetchall()
        
        apartado['productos'] = productos
        conn.close()
        return apartado
    except Exception as e:
        print(f"Error al obtener detalle del apartado: {e}")
        conn.close()
        return None

def actualizar_estado_apartado(id_apartado, nuevo_estado):
    """Actualizar el estado de un apartado"""
    conn = crear_conexion()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE apartados SET estado = %s WHERE id_apartado = %s", (nuevo_estado, id_apartado))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar estado: {e}")
        conn.rollback()
        conn.close()
        return False

def registrar_pago_apartado(id_apartado, monto_pago):
    """Registrar un pago adicional a un apartado"""
    conn = crear_conexion()
    cur = conn.cursor(dictionary=True)
    try:
        # Obtener apartado actual
        cur.execute("SELECT anticipo, saldo, total FROM apartados WHERE id_apartado = %s", (id_apartado,))
        apartado = cur.fetchone()
        
        if not apartado:
            conn.close()
            return False
        
        nuevo_anticipo = float(apartado['anticipo']) + monto_pago
        nuevo_saldo = float(apartado['total']) - nuevo_anticipo
        
        # Determinar nuevo estado
        nuevo_estado = 'Pagado' if nuevo_saldo <= 0 else 'Pendiente'
        
        # Actualizar apartado
        cur.execute("""
            UPDATE apartados 
            SET anticipo = %s, saldo = %s, estado = %s 
            WHERE id_apartado = %s
        """, (nuevo_anticipo, nuevo_saldo, nuevo_estado, id_apartado))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al registrar pago: {e}")
        conn.rollback()
        conn.close()
        return False