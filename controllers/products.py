# controllers/products.py
from database.db import crear_conexion

def obtener_productos():
    conn = crear_conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM productos ORDER BY id_producto DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def agregar_producto(nombre, descripcion, precio, stock):
    conn = crear_conexion()
    cur = conn.cursor()
    cur.execute("INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
                (nombre, descripcion, precio, stock))
    conn.commit()
    conn.close()
    return True

def ajustar_stock(id_producto, cantidad, tipo):
    conn = crear_conexion(); cur = conn.cursor()
    if tipo == 'Salida':
        cur.execute("UPDATE productos SET stock = stock - %s WHERE id_producto=%s", (cantidad, id_producto))
    else:
        cur.execute("UPDATE productos SET stock = stock + %s WHERE id_producto=%s", (cantidad, id_producto))
    cur.execute("INSERT INTO movimientos_inventario (id_producto, tipo, cantidad) VALUES (%s, %s, %s)", (id_producto, tipo, cantidad))
    conn.commit(); conn.close(); return True

def obtener_categorias():
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id_categoria, nombre FROM categorias ORDER BY nombre")
    rows = cur.fetchall(); conn.close(); return rows

def obtener_productos_por_categoria(id_categoria):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id_producto, nombre, precio, stock, imagen_url FROM productos WHERE id_categoria=%s ORDER BY id_producto DESC", (id_categoria,))
    rows = cur.fetchall(); conn.close(); return rows

def productos_count():
    conn = crear_conexion(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM productos")
    c = cur.fetchone()[0]; conn.close(); return int(c or 0)

def stock_total_sum():
    conn = crear_conexion(); cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(stock),0) FROM productos")
    s = cur.fetchone()[0]; conn.close(); return int(s or 0)

def stock_bajo_list(limit=10):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT nombre, precio, stock FROM productos WHERE stock<=5 ORDER BY stock ASC, id_producto DESC LIMIT %s", (limit,))
    rows = cur.fetchall(); conn.close(); return rows
