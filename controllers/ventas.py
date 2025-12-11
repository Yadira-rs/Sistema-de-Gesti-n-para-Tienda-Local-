from database.db import crear_conexion
import csv

carrito = []

def buscar_producto(codigo):
    conn = crear_conexion()
    cur = conn.cursor(dictionary=True)
    producto = None
    # Buscar por código único si existe la columna
    try:
        cur.execute("SELECT * FROM productos WHERE codigo=%s LIMIT 1", (str(codigo),))
        producto = cur.fetchone()
        if producto:
            conn.close(); return producto
    except Exception:
        pass
    # Buscar por ID numérico
    try:
        pid = int(codigo)
        cur.execute("SELECT * FROM productos WHERE id_producto=%s LIMIT 1", (pid,))
        producto = cur.fetchone()
        if producto:
            conn.close(); return producto
    except Exception:
        pass
    # Buscar por nombre
    cur.execute("SELECT * FROM productos WHERE nombre LIKE %s LIMIT 1", (f"%{codigo}%",))
    producto = cur.fetchone()
    conn.close()
    return producto

def obtener_carrito():
    return list(carrito)

def agregar_al_carrito(producto, cantidad):
    for item in carrito:
        if item["id_producto"] == producto["id_producto"]:
            item["cantidad"] += cantidad
            return True
    carrito.append({
        "id_producto": producto["id_producto"],
        "nombre": producto["nombre"],
        "precio": producto["precio"],
        "cantidad": cantidad
    })
    return True

def set_cantidad(id_producto, cantidad):
    for item in carrito:
        if item["id_producto"] == id_producto:
            item["cantidad"] = max(0, int(cantidad))
            return True
    return False

def eliminar_item(id_producto):
    global carrito
    carrito = [i for i in carrito if i["id_producto"] != id_producto]
    return True

def finalizar_venta(usuario_id=None, metodo="Efectivo", descuento_porcentaje=0):
    if not carrito:
        return False
    conn = crear_conexion()
    cur = conn.cursor()
    subtotal = 0
    for item in carrito:
        subtotal += float(item["precio"]) * int(item["cantidad"])
    
    # Aplicar descuento
    descuento_monto = subtotal * (descuento_porcentaje / 100)
    total = subtotal - descuento_monto
    
    # Insertar venta (solo columnas que existen en la tabla)
    try:
        cur.execute(
            "INSERT INTO ventas (id_cliente, id_usuario, total, metodo_pago, descuento) VALUES (%s, %s, %s, %s, %s)", 
            (None, usuario_id, total, metodo, descuento_monto)
        )
    except Exception:
        # Si la columna id_usuario no existe, usar la versión sin ella
        cur.execute(
            "INSERT INTO ventas (id_cliente, total, metodo_pago, descuento) VALUES (%s, %s, %s, %s)", 
            (None, total, metodo, descuento_monto)
        )
    id_venta = cur.lastrowid
    
    for item in carrito:
        precio_unitario = float(item["precio"])
        cantidad = int(item["cantidad"])
        subtotal_item = precio_unitario * cantidad
        cur.execute(
            "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)",
            (id_venta, item["id_producto"], cantidad, precio_unitario, subtotal_item)
        )
        cur.execute(
            "UPDATE productos SET stock = stock - %s WHERE id_producto=%s",
            (item["cantidad"], item["id_producto"])
        )
    
    # Si el método de pago es Crédito, crear registro en tabla creditos
    if metodo == "Crédito":
        from datetime import datetime, timedelta
        plazo_dias = 30  # Plazo por defecto
        fecha_vencimiento = (datetime.now() + timedelta(days=plazo_dias)).date()
        
        try:
            cur.execute(
                """INSERT INTO creditos (id_venta, id_cliente, monto_total, saldo_pendiente, 
                   plazo_dias, fecha_vencimiento, estado) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (id_venta, None, total, total, plazo_dias, fecha_vencimiento, 'Activo')
            )
        except Exception as e:
            print(f"Nota: No se pudo crear el crédito (tabla puede no existir): {e}")
    
    conn.commit()
    conn.close()
    sale_items = list(carrito)
    carrito.clear()
    return {"id_venta": id_venta, "total": total, "metodo": metodo, "items": sale_items, "descuento": descuento_monto}

def vaciar_carrito():
    carrito.clear()

def resumen_ventas(start_date=None, end_date=None, metodo=None):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    where = []
    params = []
    if start_date and end_date:
        where.append("fecha BETWEEN %s AND %s")
        params.extend([start_date, end_date])
    if metodo:
        where.append("metodo_pago=%s")
        params.append(metodo)
    wsql = (" WHERE "+" AND ".join(where)) if where else ""
    cur.execute(f"SELECT COUNT(*) AS total_ventas, COALESCE(SUM(total),0) AS ingreso_total, COALESCE(AVG(total),0) AS promedio FROM ventas{wsql}", params)
    r = cur.fetchone()
    cur.execute("SELECT COALESCE(SUM(cantidad),0) AS productos_vendidos FROM detalle_ventas")
    p = cur.fetchone()
    conn.close(); r.update(p); return r

def listar_ventas(limit=50, start_date=None, end_date=None, metodo=None):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    where = []
    params = []
    if start_date and end_date:
        where.append("fecha BETWEEN %s AND %s")
        params.extend([start_date, end_date])
    if metodo and metodo != "Todos":
        where.append("metodo_pago=%s")
        params.append(metodo)
    wsql = (" WHERE "+" AND ".join(where)) if where else ""
    sql = f"SELECT id_venta, fecha, total, metodo_pago, (SELECT COALESCE(SUM(cantidad),0) FROM detalle_ventas dv WHERE dv.id_venta=ventas.id_venta) AS items_count FROM ventas{wsql} ORDER BY id_venta DESC LIMIT %s"
    params.append(limit)
    cur.execute(sql, params)
    rows = cur.fetchall(); conn.close(); return rows

def exportar_ventas_csv(path, start_date=None, end_date=None, metodo=None):
    rows = listar_ventas(limit=1000000, start_date=start_date, end_date=end_date, metodo=metodo)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Ticket", "Fecha", "Método", "Total"])
        for r in rows:
            w.writerow([r["id_venta"], str(r["fecha"]), r.get("metodo_pago") or "-", f"{float(r['total']):.2f}"])
    return path

def listar_ultimas_ventas(limit=5):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id_venta, fecha, total, metodo_pago, descuento FROM ventas ORDER BY fecha DESC LIMIT %s", (limit,))
    except:
        # Si no existe la columna metodo_pago o descuento, usar consulta básica
        cur.execute("SELECT id_venta, fecha, total, 'Efectivo' as metodo_pago, 0 as descuento FROM ventas ORDER BY fecha DESC LIMIT %s", (limit,))
    rows = cur.fetchall(); conn.close(); return rows

def ventas_hoy_total():
    conn = crear_conexion(); cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(total),0) FROM ventas WHERE DATE(fecha)=CURDATE()")
    total = cur.fetchone()[0]; conn.close(); return float(total or 0)

def ingresos_mes_total():
    conn = crear_conexion(); cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(total),0) FROM ventas WHERE DATE_FORMAT(fecha, '%Y-%m') = DATE_FORMAT(NOW(), '%Y-%m')")
    total = cur.fetchone()[0]; conn.close(); return float(total or 0)

def ventas_diarias(dias=7):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT DATE(fecha) AS dia, COALESCE(SUM(total),0) AS total FROM ventas GROUP BY DATE(fecha) ORDER BY DATE(fecha) DESC LIMIT %s", (dias,))
    rows = cur.fetchall(); conn.close(); return list(reversed(rows))

def obtener_ventas(limit=100):
    """Obtener lista de ventas - alias para listar_ventas"""
    return listar_ventas(limit=limit)

def obtener_ticket(id_venta):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id_venta, fecha, total, metodo_pago FROM ventas WHERE id_venta=%s", (id_venta,))
    v = cur.fetchone()
    if not v:
        conn.close(); return None
    cur.execute("SELECT dv.id_producto, dv.cantidad, dv.subtotal, p.nombre, p.precio FROM detalle_ventas dv LEFT JOIN productos p ON p.id_producto=dv.id_producto WHERE dv.id_venta=%s", (id_venta,))
    items = []
    for r in cur.fetchall():
        qty = int(r["cantidad"])
        unit = float(r.get("precio") or 0)
        if unit == 0:
            unit = float(r["subtotal"]) / max(qty,1)
        items.append({"id_producto": r["id_producto"], "nombre": r["nombre"], "cantidad": qty, "precio": unit})
    conn.close(); return {"id_venta": v["id_venta"], "total": float(v["total"]), "metodo": v.get("metodo_pago") or "-", "items": items}
