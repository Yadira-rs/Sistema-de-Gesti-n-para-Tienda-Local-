from database.db import crear_conexion
from datetime import datetime, timedelta

def listar_creditos():
    """
    Función alias para obtener_creditos() - mantiene compatibilidad
    """
    return obtener_creditos()

def obtener_creditos():
    """
    Obtiene todos los créditos de la base de datos con información de la venta.
    """
    conn = crear_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                c.id_credito,
                c.id_venta,
                c.fecha_credito,
                c.monto_total,
                c.monto_pagado,
                c.saldo_pendiente,
                c.plazo_dias,
                c.fecha_vencimiento,
                c.estado,
                c.notas,
                v.fecha as fecha_venta,
                v.metodo_pago,
                DATEDIFF(NOW(), c.fecha_credito) as dias_transcurridos,
                DATEDIFF(c.fecha_vencimiento, NOW()) as dias_para_vencer
            FROM creditos c
            LEFT JOIN ventas v ON c.id_venta = v.id_venta
            ORDER BY c.fecha_credito DESC
        """)
        datos = cursor.fetchall()
        
        # Actualizar estado de créditos vencidos
        for credito in datos:
            if credito['dias_para_vencer'] < 0 and credito['estado'] == 'Activo':
                cursor.execute(
                    "UPDATE creditos SET estado = 'Vencido' WHERE id_credito = %s",
                    (credito['id_credito'],)
                )
                credito['estado'] = 'Vencido'
        
        conn.commit()
        conn.close()
        return datos
    except Exception as e:
        print(f"Error al obtener créditos: {e}")
        conn.close()
        return []

def obtener_creditos_activos():
    """Obtiene solo los créditos activos"""
    conn = crear_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                c.*,
                v.fecha as fecha_venta,
                DATEDIFF(c.fecha_vencimiento, NOW()) as dias_para_vencer
            FROM creditos c
            LEFT JOIN ventas v ON c.id_venta = v.id_venta
            WHERE c.estado = 'Activo'
            ORDER BY c.fecha_vencimiento ASC
        """)
        datos = cursor.fetchall()
        conn.close()
        return datos
    except Exception as e:
        print(f"Error: {e}")
        conn.close()
        return []

def obtener_creditos_vencidos():
    """Obtiene los créditos vencidos"""
    conn = crear_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                c.*,
                v.fecha as fecha_venta,
                DATEDIFF(NOW(), c.fecha_vencimiento) as dias_vencido
            FROM creditos c
            LEFT JOIN ventas v ON c.id_venta = v.id_venta
            WHERE c.estado = 'Vencido' OR (c.estado = 'Activo' AND c.fecha_vencimiento < CURDATE())
            ORDER BY c.fecha_vencimiento ASC
        """)
        datos = cursor.fetchall()
        conn.close()
        return datos
    except Exception as e:
        print(f"Error: {e}")
        conn.close()
        return []

def obtener_abonos_hoy():
    """Obtiene los abonos realizados hoy"""
    conn = crear_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                a.*,
                c.id_venta,
                c.monto_total
            FROM abonos_creditos a
            LEFT JOIN creditos c ON a.id_credito = c.id_credito
            WHERE DATE(a.fecha_abono) = CURDATE()
            ORDER BY a.fecha_abono DESC
        """)
        datos = cursor.fetchall()
        conn.close()
        return datos
    except Exception as e:
        print(f"Error: {e}")
        conn.close()
        return []

def crear_credito(id_venta, id_cliente, monto_total, plazo_dias=30, tasa_interes=0, notas=""):
    """
    Crea un nuevo crédito asociado a una venta (o sin venta si id_venta es None).
    """
    conn = crear_conexion()
    cursor = conn.cursor()
    try:
        fecha_vencimiento = (datetime.now() + timedelta(days=plazo_dias)).date()
        
        # Convertir id_venta vacío a None
        if id_venta == "" or id_venta == "None":
            id_venta = None
        
        cursor.execute(
            """INSERT INTO creditos (id_venta, id_cliente, monto_total, saldo_pendiente, 
               plazo_dias, fecha_vencimiento, tasa_interes, estado, notas) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (id_venta, id_cliente, monto_total, monto_total, plazo_dias, 
             fecha_vencimiento, tasa_interes, 'Activo', notas)
        )
        conn.commit()
        id_credito = cursor.lastrowid
        conn.close()
        return id_credito
    except Exception as e:
        print(f"Error al crear crédito: {e}")
        import traceback
        traceback.print_exc()
        conn.close()
        return None

def registrar_abono(id_credito, monto_abono, metodo_pago="Efectivo", notas=""):
    """
    Registra un abono a un crédito y actualiza el saldo.
    """
    conn = crear_conexion()
    cursor = conn.cursor()
    try:
        # Registrar el abono
        cursor.execute(
            """INSERT INTO abonos_creditos (id_credito, monto_abono, metodo_pago, notas)
               VALUES (%s, %s, %s, %s)""",
            (id_credito, monto_abono, metodo_pago, notas)
        )
        
        # Actualizar el crédito
        cursor.execute(
            """UPDATE creditos 
               SET monto_pagado = monto_pagado + %s,
                   saldo_pendiente = saldo_pendiente - %s
               WHERE id_credito = %s""",
            (monto_abono, monto_abono, id_credito)
        )
        
        # Verificar si el crédito está pagado
        cursor.execute(
            "SELECT saldo_pendiente FROM creditos WHERE id_credito = %s",
            (id_credito,)
        )
        saldo = cursor.fetchone()[0]
        
        if saldo <= 0:
            cursor.execute(
                "UPDATE creditos SET estado = 'Pagado' WHERE id_credito = %s",
                (id_credito,)
            )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al registrar abono: {e}")
        conn.close()
        return False

def obtener_resumen_creditos():
    """Obtiene un resumen de los créditos"""
    conn = crear_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_creditos,
                SUM(CASE WHEN estado = 'Activo' THEN 1 ELSE 0 END) as activos,
                SUM(CASE WHEN estado = 'Vencido' THEN 1 ELSE 0 END) as vencidos,
                SUM(CASE WHEN estado = 'Pagado' THEN 1 ELSE 0 END) as pagados,
                COALESCE(SUM(CASE WHEN estado IN ('Activo', 'Vencido') THEN saldo_pendiente ELSE 0 END), 0) as total_por_cobrar,
                COALESCE(SUM(monto_pagado), 0) as total_cobrado
            FROM creditos
        """)
        resumen = cursor.fetchone()
        conn.close()
        return resumen
    except Exception as e:
        print(f"Error: {e}")
        conn.close()
        return {
            'total_creditos': 0,
            'activos': 0,
            'vencidos': 0,
            'pagados': 0,
            'total_por_cobrar': 0,
            'total_cobrado': 0
        }

def obtener_abonos_credito(id_credito):
    """Obtiene todos los abonos de un crédito específico"""
    conn = crear_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                id_abono,
                monto_abono,
                fecha_abono,
                metodo_pago,
                notas
            FROM abonos_creditos 
            WHERE id_credito = %s
            ORDER BY fecha_abono DESC
        """, (id_credito,))
        abonos = cursor.fetchall()
        conn.close()
        return abonos
    except Exception as e:
        print(f"Error al obtener abonos: {e}")
        conn.close()
        return []

def cerrar_credito_manual(id_credito):
    """Cierra un crédito manualmente"""
    conn = crear_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE creditos SET estado = 'Pagado' WHERE id_credito = %s",
            (id_credito,)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al cerrar crédito: {e}")
        conn.close()
        return False

def actualizar_saldo_credito(id_credito):
    """Actualiza el saldo de un crédito basado en los abonos"""
    conn = crear_conexion()
    cursor = conn.cursor()
    try:
        # Obtener total de abonos
        cursor.execute(
            "SELECT COALESCE(SUM(monto_abono), 0) as total_abonos FROM abonos_creditos WHERE id_credito = %s",
            (id_credito,)
        )
        total_abonos = cursor.fetchone()[0]
        
        # Obtener monto total del crédito
        cursor.execute(
            "SELECT monto_total FROM creditos WHERE id_credito = %s",
            (id_credito,)
        )
        monto_total = cursor.fetchone()[0]
        
        # Calcular nuevo saldo
        nuevo_saldo = monto_total - total_abonos
        
        # Actualizar crédito
        cursor.execute("""
            UPDATE creditos 
            SET monto_pagado = %s, 
                saldo_pendiente = %s,
                estado = CASE 
                    WHEN %s <= 0 THEN 'Pagado'
                    ELSE estado
                END
            WHERE id_credito = %s
        """, (total_abonos, nuevo_saldo, nuevo_saldo, id_credito))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar saldo: {e}")
        conn.close()
        return False
