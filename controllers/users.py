from database.db import crear_conexion

def listar_usuarios():
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id_usuario, nombre_completo, usuario, email, rol, activo FROM usuarios ORDER BY id_usuario DESC"); rows = cur.fetchall(); conn.close(); return rows

def crear_usuario(nombre_completo, email, contraseña, rol='Vendedor', activo=True, pregunta=None, respuesta=None):
    conn = crear_conexion(); cur = conn.cursor()
    # Generar usuario a partir del email (parte antes del @)
    usuario = email.split('@')[0] if '@' in email else email
    cur.execute(
        "INSERT INTO usuarios (nombre_completo, usuario, email, contraseña, rol, pregunta, respuesta, activo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", 
        (nombre_completo, usuario, email, contraseña, rol, pregunta, respuesta, activo)
    )
    conn.commit(); conn.close()

def recuperar_contraseña(usuario, respuesta, nueva):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT respuesta FROM usuarios WHERE usuario=%s", (usuario,))
    row = cur.fetchone()
    if not row: conn.close(); return False, 'Usuario no encontrado'
    if (row.get('respuesta') or '').strip().lower() != respuesta.strip().lower(): conn.close(); return False, 'Respuesta incorrecta'
    cur2 = conn.cursor(); cur2.execute("UPDATE usuarios SET contraseña=%s WHERE usuario=%s", (nueva, usuario)); conn.commit(); conn.close(); return True, 'Contraseña actualizada'
