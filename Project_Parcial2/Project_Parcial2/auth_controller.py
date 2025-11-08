# Controlador responsable de la logica de autenticacion.
# Separa la logica del login para mantener limpio el codigo de la interfaz.

from database import crear_conexion

def validar_creedenciales(usuario, password):
    print(f" Validando: usuario='{usuario}', password='{password}'")
    
    conexion = crear_conexion()

    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        
        # CONSULTA CORRECTA para tu tabla
        query = "SELECT * FROM usuarios WHERE usuario = %s AND password = %s"
        cursor.execute(query, (usuario, password))
        
        resultado = cursor.fetchone()
        
        if resultado:
            print(f"USUARIO ENCONTRADO: {resultado}")
            cursor.close()
            conexion.close()
            return True
        else:
            print("Credenciales incorrectas")
            
            # Verificar si existe el usuario
            cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
            user_exists = cursor.fetchone()
            
            if user_exists:
                print(f"Usuario existe pero contraseña incorrecta")
            else:
                print(f"Usuario no existe")
        
        cursor.close()
        conexion.close()
        return False
        
    except Exception as e:
        print(f" Error: {e}")
        return False