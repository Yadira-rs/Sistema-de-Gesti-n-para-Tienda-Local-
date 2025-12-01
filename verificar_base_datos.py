"""
Script para verificar y corregir la estructura de la base de datos
"""
from database.db import crear_conexion

def verificar_columnas_usuarios():
    """Verificar si las columnas necesarias existen en la tabla usuarios"""
    try:
        conn = crear_conexion()
        cur = conn.cursor()
        
        # Obtener columnas de la tabla usuarios
        cur.execute("DESCRIBE usuarios")
        columnas = [row[0] for row in cur.fetchall()]
        
        print("✓ Columnas actuales en tabla 'usuarios':")
        for col in columnas:
            print(f"  - {col}")
        
        # Verificar columnas necesarias
        columnas_necesarias = ['id_usuario', 'nombre_completo', 'email', 'activo']
        columnas_faltantes = [col for col in columnas_necesarias if col not in columnas]
        
        if columnas_faltantes:
            print(f"\n⚠ Faltan las siguientes columnas: {', '.join(columnas_faltantes)}")
            print("\n📝 Ejecuta el archivo 'migration_usuarios.sql' para agregar las columnas faltantes")
            print("   Puedes hacerlo desde MySQL Workbench o con el comando:")
            print("   mysql -u root -p boutique_db < migration_usuarios.sql")
        else:
            print("\n✓ Todas las columnas necesarias están presentes")
        
        conn.close()
        return len(columnas_faltantes) == 0
        
    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {str(e)}")
        return False

def verificar_tabla_existe(tabla):
    """Verificar si una tabla existe"""
    try:
        conn = crear_conexion()
        cur = conn.cursor()
        cur.execute(f"SHOW TABLES LIKE '{tabla}'")
        existe = cur.fetchone() is not None
        conn.close()
        return existe
    except:
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("VERIFICACIÓN DE BASE DE DATOS - Janet Rosa Bici")
    print("=" * 60)
    print()
    
    # Verificar conexión
    try:
        conn = crear_conexion()
        print("✓ Conexión a la base de datos exitosa")
        conn.close()
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        print("\n📝 Verifica el archivo mysql_config.ini")
        exit(1)
    
    print()
    
    # Verificar tablas principales
    tablas = ['usuarios', 'productos', 'ventas', 'clientes', 'apartados']
    print("Verificando tablas principales...")
    for tabla in tablas:
        existe = verificar_tabla_existe(tabla)
        if existe:
            print(f"  ✓ Tabla '{tabla}' existe")
        else:
            print(f"  ❌ Tabla '{tabla}' NO existe")
    
    print()
    
    # Verificar estructura de usuarios
    print("Verificando estructura de tabla 'usuarios'...")
    verificar_columnas_usuarios()
    
    print()
    print("=" * 60)
