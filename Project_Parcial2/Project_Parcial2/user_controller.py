from auth_controller import validar_creedenciales
from database import crear_conexion


print(" PRUEBA COMPLETA DEL SISTEMA")
print("=" * 40)

def ver_usuarios():
    conexion = crear_conexion()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, usuario FROM usuarios")
        resultado = cursor.fetchall()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    

def eliminar_usuario(user_id):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False
    
def actualizar_usuario(user_id, nuevo_usuario, nueva_password):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET usuario = %s, password = %s WHERE id = %s", 
                       (nuevo_usuario, nueva_password, user_id))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False

# Probar con credenciales correctas
print("\n1. Probando con credenciales CORRECTAS:")
resultado1 = validar_creedenciales("Cindy", "1234")
print(f"Resultado: {resultado1}")

# Probar con credenciales incorrectas
print("\n2. Probando con credenciales INCORRECTAS:")
resultado2 = validar_creedenciales("admin", "1234")
print(f"Resultado: {resultado2}")

# Probar con usuario que no existe
print("\n3. Probando con usuario INEXISTENTE:")
resultado3 = validar_creedenciales("UsuarioInexistente", "1234")
print(f"Resultado: {resultado3}")

print("\n" + "=" * 40)
if resultado1:
    print("¡EL SISTEMA FUNCIONA CORRECTAMENTE!")
else:
    print("Hay problemas en el sistema")