from database.db import crear_conexion

def listar_usuarios():
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id_usuario, usuario, rol FROM usuarios ORDER BY id_usuario DESC"); rows = cur.fetchall(); conn.close(); return rows

def crear_usuario(usuario, contraseña, rol='cajero', pregunta=None, respuesta=None):
    conn = crear_conexion(); cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (usuario, contraseña, rol, pregunta, respuesta) VALUES (%s,%s,%s,%s,%s)", (usuario, contraseña, rol, pregunta, respuesta))
    conn.commit(); conn.close()

def recuperar_contraseña(usuario, respuesta, nueva):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT respuesta FROM usuarios WHERE usuario=%s", (usuario,))
    row = cur.fetchone()
    if not row: conn.close(); return False, 'Usuario no encontrado'
    if (row.get('respuesta') or '').strip().lower() != respuesta.strip().lower(): conn.close(); return False, 'Respuesta incorrecta'
    cur2 = conn.cursor(); cur2.execute("UPDATE usuarios SET contraseña=%s WHERE usuario=%s", (nueva, usuario)); conn.commit(); conn.close(); return True, 'Contraseña actualizada'
