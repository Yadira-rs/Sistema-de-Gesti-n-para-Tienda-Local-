from database.db import crear_conexion

def listar_usuarios():
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    sql = """
    SELECT 
        u.id_usuario, u.nombre_completo, u.usuario, u.email, u.contraseña, u.rol, u.activo,
        (SELECT COUNT(*) FROM ventas v WHERE v.id_usuario = u.id_usuario) as ventas_cantidad,
        (SELECT COALESCE(SUM(v.total), 0) FROM ventas v WHERE v.id_usuario = u.id_usuario) as ventas_total
    FROM usuarios u 
    ORDER BY u.id_usuario DESC
    """
    cur.execute(sql); rows = cur.fetchall(); conn.close(); return rows

def crear_usuario(nombre_completo, email, contraseña, rol='Vendedor', activo=True, pregunta=None, respuesta=None):
    conn = crear_conexion(); cur = conn.cursor()
    # Generar usuario a partir del email (parte antes del @)
    usuario = email.split('@')[0] if '@' in email else email
    cur.execute(
        "INSERT INTO usuarios (nombre_completo, usuario, email, contraseña, rol, pregunta, respuesta, activo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", 
        (nombre_completo, usuario, email, contraseña, rol, pregunta, respuesta, activo)
    )
    conn.commit(); conn.close()

def editar_usuario(id_usuario, nombre_completo=None, email=None, contraseña=None, rol=None, activo=None):
    """
    Edita un usuario existente
    """
    conn = crear_conexion()
    cur = conn.cursor()
    
    # Construir la consulta dinámicamente
    campos = []
    valores = []
    
    if nombre_completo is not None:
        campos.append("nombre_completo = %s")
        valores.append(nombre_completo)
    
    if email is not None:
        campos.append("email = %s")
        valores.append(email)
        # Actualizar también el usuario basado en el email
        usuario = email.split('@')[0] if '@' in email else email
        campos.append("usuario = %s")
        valores.append(usuario)
    
    if contraseña is not None:
        campos.append("contraseña = %s")
        valores.append(contraseña)
    
    if rol is not None:
        campos.append("rol = %s")
        valores.append(rol)
    
    if activo is not None:
        campos.append("activo = %s")
        valores.append(activo)
    
    if not campos:
        conn.close()
        return False, "No hay campos para actualizar"
    
    # Agregar el ID al final
    valores.append(id_usuario)
    
    sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
    
    try:
        cur.execute(sql, valores)
        conn.commit()
        conn.close()
        return True, "Usuario actualizado correctamente"
    except Exception as e:
        conn.close()
        return False, f"Error al actualizar usuario: {e}"

def eliminar_usuario(id_usuario):
    """
    Elimina un usuario del sistema
    """
    conn = crear_conexion()
    cur = conn.cursor()
    
    try:
        # Verificar que el usuario existe
        cur.execute("SELECT id_usuario, usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario = cur.fetchone()
        
        if not usuario:
            conn.close()
            return False, "Usuario no encontrado"
        
        # Eliminar el usuario
        cur.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        conn.close()
        
        return True, "Usuario eliminado correctamente"
        
    except Exception as e:
        conn.close()
        return False, f"Error al eliminar usuario: {e}"

def recuperar_contraseña(usuario, respuesta, nueva):
    conn = crear_conexion(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT respuesta FROM usuarios WHERE usuario=%s", (usuario,))
    row = cur.fetchone()
    if not row: conn.close(); return False, 'Usuario no encontrado'
    if (row.get('respuesta') or '').strip().lower() != respuesta.strip().lower(): conn.close(); return False, 'Respuesta incorrecta'
    cur2 = conn.cursor(); cur2.execute("UPDATE usuarios SET contraseña=%s WHERE usuario=%s", (nueva, usuario)); conn.commit(); conn.close(); return True, 'Contraseña actualizada'
