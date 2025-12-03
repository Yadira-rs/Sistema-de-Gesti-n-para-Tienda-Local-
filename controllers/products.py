# controllers/products.py
from database.db import crear_conexion

def obtener_productos():
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id_producto, codigo, codigo_barras, nombre, precio, stock, imagen_url FROM productos ORDER BY id_producto DESC")
    except Exception:
        try:
            cur.execute("SELECT id_producto, codigo, nombre, precio, stock, imagen_url FROM productos ORDER BY id_producto DESC")
        except Exception:
            try:
                cur.execute("SELECT id_producto, codigo, nombre, precio, stock FROM productos ORDER BY id_producto DESC")
            except Exception:
                cur.execute("SELECT id_producto, nombre, precio, stock FROM productos ORDER BY id_producto DESC")
    rows = cur.fetchall(); 
    for r in rows:
        if 'imagen_url' not in r:
            r['imagen_url'] = None
        if 'codigo' not in r:
            r['codigo'] = None
        if 'codigo_barras' not in r:
            r['codigo_barras'] = None
    conn.close(); return rows

def agregar_producto(nombre, descripcion, precio, stock, codigo=None, codigo_barras=None, id_categoria=None):
    conn = crear_conexion()
    cur = conn.cursor()
    try:
        # Si no se proporciona código de barras, generar uno
        if not codigo_barras or not str(codigo_barras).strip():
            # Insertar primero para obtener el ID
            if codigo and str(codigo).strip():
                try:
                    cur.execute("INSERT INTO productos (codigo, nombre, descripcion, precio, stock, id_categoria) VALUES (%s, %s, %s, %s, %s, %s)", 
                               (codigo, nombre, descripcion, precio, stock, id_categoria))
                except Exception:
                    cur.execute("INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria) VALUES (%s, %s, %s, %s, %s)", 
                               (nombre, descripcion, precio, stock, id_categoria))
            else:
                cur.execute("INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria) VALUES (%s, %s, %s, %s, %s)", 
                           (nombre, descripcion, precio, stock, id_categoria))
            
            # Obtener el ID insertado
            id_producto = cur.lastrowid
            
            # Generar código de barras
            codigo_barras = generar_codigo_barras(id_categoria or 7, id_producto)
            
            # Actualizar con el código de barras
            cur.execute("UPDATE productos SET codigo_barras = %s WHERE id_producto = %s", (codigo_barras, id_producto))
        else:
            # Si se proporciona código de barras, insertarlo directamente
            if codigo and str(codigo).strip():
                try:
                    cur.execute("INSERT INTO productos (codigo, codigo_barras, nombre, descripcion, precio, stock, id_categoria) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                               (codigo, codigo_barras, nombre, descripcion, precio, stock, id_categoria))
                except Exception:
                    cur.execute("INSERT INTO productos (codigo_barras, nombre, descripcion, precio, stock, id_categoria) VALUES (%s, %s, %s, %s, %s, %s)", 
                               (codigo_barras, nombre, descripcion, precio, stock, id_categoria))
            else:
                cur.execute("INSERT INTO productos (codigo_barras, nombre, descripcion, precio, stock, id_categoria) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (codigo_barras, nombre, descripcion, precio, stock, id_categoria))
        
        conn.commit(); ok = True
    except Exception as e:
        print(f"Error al agregar producto: {e}")
        ok = False
    conn.close(); return ok

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

def crear_categoria(nombre):
    conn = crear_conexion(); cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
        conn.commit(); ok = True
    except Exception:
        ok = False
    conn.close(); return ok

def obtener_productos_por_categoria(id_categoria):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id_producto, codigo, nombre, precio, stock, imagen_url FROM productos WHERE id_categoria=%s ORDER BY id_producto DESC", (id_categoria,))
    except Exception:
        try:
            cur.execute("SELECT id_producto, codigo, nombre, precio, stock FROM productos WHERE id_categoria=%s ORDER BY id_producto DESC", (id_categoria,))
        except Exception:
            cur.execute("SELECT id_producto, nombre, precio, stock FROM productos WHERE id_categoria=%s ORDER BY id_producto DESC", (id_categoria,))
    rows = cur.fetchall(); 
    for r in rows:
        if 'imagen_url' not in r:
            r['imagen_url'] = None
        if 'codigo' not in r:
            r['codigo'] = None
    conn.close(); return rows

def buscar_productos(query):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    q = f"%{query}%"
    try:
        # Intentar incluir búsqueda por código único si existe
        try:
            cur.execute("SELECT id_producto FROM productos LIMIT 1")
            cur.execute("SELECT id_producto, nombre, precio, stock, imagen_url FROM productos WHERE nombre LIKE %s OR CAST(id_producto AS CHAR) LIKE %s OR codigo LIKE %s ORDER BY id_producto DESC", (q, q, q))
        except Exception:
            cur.execute("SELECT id_producto, nombre, precio, stock, imagen_url FROM productos WHERE nombre LIKE %s OR CAST(id_producto AS CHAR) LIKE %s ORDER BY id_producto DESC", (q, q))
    except Exception:
        try:
            cur.execute("SELECT id_producto, nombre, precio, stock FROM productos WHERE nombre LIKE %s OR CAST(id_producto AS CHAR) LIKE %s OR codigo LIKE %s ORDER BY id_producto DESC", (q, q, q))
        except Exception:
            cur.execute("SELECT id_producto, nombre, precio, stock FROM productos WHERE nombre LIKE %s OR CAST(id_producto AS CHAR) LIKE %s ORDER BY id_producto DESC", (q, q))
    rows = cur.fetchall(); 
    for r in rows:
        if 'imagen_url' not in r:
            r['imagen_url'] = None
        if 'codigo' not in r:
            r['codigo'] = None
    conn.close(); return rows

def obtener_productos_favoritos(limit=12):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT p.id_producto, p.nombre, p.precio, p.stock, p.imagen_url
            FROM productos p
            LEFT JOIN detalle_ventas dv ON dv.id_producto = p.id_producto
            GROUP BY p.id_producto, p.nombre, p.precio, p.stock, p.imagen_url
            ORDER BY COALESCE(SUM(dv.cantidad), 0) DESC, p.id_producto DESC
            LIMIT %s
            """,
            (limit,)
        )
    except Exception:
        cur.execute(
            """
            SELECT p.id_producto, p.nombre, p.precio, p.stock
            FROM productos p
            LEFT JOIN detalle_ventas dv ON dv.id_producto = p.id_producto
            GROUP BY p.id_producto, p.nombre, p.precio, p.stock
            ORDER BY COALESCE(SUM(dv.cantidad), 0) DESC, p.id_producto DESC
            LIMIT %s
            """,
            (limit,)
        )
    rows = cur.fetchall(); 
    for r in rows:
        if 'imagen_url' not in r:
            r['imagen_url'] = None
    conn.close(); return rows

def obtener_productos_stock_bajo(limit=12):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT id_producto, nombre, precio, stock, imagen_url FROM productos WHERE stock<=5 ORDER BY stock ASC, id_producto DESC LIMIT %s",
            (limit,)
        )
    except Exception:
        cur.execute(
            "SELECT id_producto, nombre, precio, stock FROM productos WHERE stock<=5 ORDER BY stock ASC, id_producto DESC LIMIT %s",
            (limit,)
        )
    rows = cur.fetchall(); 
    for r in rows:
        if 'imagen_url' not in r:
            r['imagen_url'] = None
    conn.close(); return rows

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

def codigo_disponible(codigo):
    conn = crear_conexion(); cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM productos WHERE codigo=%s", (codigo,))
        c = cur.fetchone()[0]
        conn.close(); return int(c or 0) == 0
    except Exception:
        conn.close(); return True

def buscar_por_codigo_barras(codigo_barras):
    """Buscar producto por código de barras único"""
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id_producto, codigo, codigo_barras, nombre, precio, stock, imagen_url FROM productos WHERE codigo_barras=%s LIMIT 1", (codigo_barras,))
        producto = cur.fetchone()
        conn.close()
        return producto
    except Exception as e:
        print(f"Error al buscar por código de barras: {e}")
        conn.close()
        return None

def codigo_barras_disponible(codigo_barras):
    """Verificar si un código de barras está disponible"""
    conn = crear_conexion(); cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM productos WHERE codigo_barras=%s", (codigo_barras,))
        c = cur.fetchone()[0]
        conn.close(); return int(c or 0) == 0
    except Exception:
        conn.close(); return True

def generar_codigo_barras(id_categoria, id_producto):
    """Generar código de barras único en formato EAN-13 simulado"""
    import random
    prefijo = "750"  # Prefijo de empresa
    categoria = str(id_categoria).zfill(2)  # 2 dígitos
    producto = str(id_producto).zfill(6)  # 6 dígitos
    control = str(random.randint(0, 99)).zfill(2)  # 2 dígitos de control
    return f"{prefijo}{categoria}{producto}{control}"

def crear_producto_temporal(nombre, precio):
    """Crear un producto temporal para ventas personalizadas"""
    conn = crear_conexion()
    cur = conn.cursor()
    try:
        # Insertar producto temporal con stock 0 (no afecta inventario)
        cur.execute(
            "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
            (nombre, "Producto personalizado - Venta única", precio, 0)
        )
        id_producto = cur.lastrowid
        conn.commit()
        conn.close()
        return id_producto
    except Exception as e:
        print(f"Error al crear producto temporal: {e}")
        conn.close()
        return None
