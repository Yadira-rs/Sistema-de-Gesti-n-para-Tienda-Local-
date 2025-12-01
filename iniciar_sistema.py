"""
Script de inicio del Sistema Janet Rosa Bici
Verifica dependencias y configuración antes de iniciar
"""
import sys
import os

def verificar_dependencias():
    """Verificar que todas las dependencias estén instaladas"""
    print("=" * 60)
    print("SISTEMA JANET ROSA BICI - Verificación de Inicio")
    print("=" * 60)
    
    dependencias = {
        'customtkinter': 'CustomTkinter',
        'mysql.connector': 'MySQL Connector',
        'PIL': 'Pillow (PIL)'
    }
    
    print("\n📦 Verificando dependencias...")
    faltantes = []
    
    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
            print(f"  ✅ {nombre}")
        except ImportError:
            print(f"  ❌ {nombre} - NO INSTALADO")
            faltantes.append(nombre)
    
    if faltantes:
        print("\n⚠️  Dependencias faltantes:")
        for dep in faltantes:
            print(f"     - {dep}")
        print("\n💡 Instala las dependencias con:")
        print("     pip install customtkinter mysql-connector-python pillow")
        return False
    
    return True

def verificar_base_datos():
    """Verificar conexión a la base de datos"""
    print("\n🗄️  Verificando base de datos...")
    
    try:
        import mysql.connector
        
        # Intentar conectar al servidor MySQL
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )
            print("  ✅ Conexión a MySQL exitosa")
            
            # Verificar si existe la base de datos
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES LIKE 'boutique_db'")
            result = cursor.fetchone()
            
            if result:
                print("  ✅ Base de datos 'boutique_db' encontrada")
                conn.close()
                return True
            else:
                print("  ⚠️  Base de datos 'boutique_db' NO encontrada")
                print("\n💡 Crea la base de datos ejecutando:")
                print("     mysql -u root < .sql")
                print("     o desde MySQL Workbench: SOURCE .sql")
                conn.close()
                return False
                
        except mysql.connector.Error as e:
            print(f"  ❌ Error de conexión: {e}")
            print("\n💡 Verifica que MySQL esté ejecutándose:")
            print("     - XAMPP: Inicia Apache y MySQL")
            print("     - WAMP: Inicia los servicios")
            print("     - MySQL Workbench: Verifica la conexión")
            return False
            
    except ImportError:
        print("  ❌ MySQL Connector no instalado")
        return False

def verificar_archivos():
    """Verificar que existan los archivos necesarios"""
    print("\n📁 Verificando archivos del sistema...")
    
    archivos_criticos = [
        'app.py',
        'database/db.py',
        'views/login.py',
        'controllers/ventas.py',
        'controllers/products.py'
    ]
    
    faltantes = []
    for archivo in archivos_criticos:
        if os.path.exists(archivo):
            print(f"  ✅ {archivo}")
        else:
            print(f"  ❌ {archivo} - NO ENCONTRADO")
            faltantes.append(archivo)
    
    if faltantes:
        print("\n⚠️  Archivos faltantes. El sistema puede no funcionar correctamente.")
        return False
    
    return True

def iniciar_aplicacion():
    """Iniciar la aplicación principal"""
    print("\n🚀 Iniciando aplicación...")
    print("=" * 60)
    
    try:
        import customtkinter as ctk
        from views.login import LoginWindow
        
        # Configurar CustomTkinter
        try:
            ctk.deactivate_automatic_dpi_awareness()
        except:
            pass  # Ignorar si falla
        
        # Crear y mostrar ventana de login
        app = LoginWindow()
        
        print("\n✅ Sistema iniciado correctamente")
        print("📱 Credenciales de prueba:")
        print("   Usuario: admin")
        print("   Contraseña: 1234")
        print("\n💡 Consejos:")
        print("   - Si una ventana se cierra inesperadamente, revisa la consola")
        print("   - Los errores se mostrarán en pantalla con opción de reintentar")
        print("\n" + "=" * 60)
        
        # Iniciar loop principal
        app.mainloop()
        
        print("\n👋 Aplicación cerrada correctamente")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Aplicación interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error crítico al iniciar la aplicación:")
        print(f"   {e}")
        print("\n📋 Detalles técnicos:")
        import traceback
        traceback.print_exc()
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que todas las dependencias estén instaladas")
        print("   2. Asegúrate de que la base de datos esté configurada")
        print("   3. Revisa el archivo database/db.py")
        input("\nPresiona Enter para salir...")
        sys.exit(1)

def main():
    """Función principal"""
    try:
        # Verificar dependencias
        if not verificar_dependencias():
            input("\n⚠️  Instala las dependencias faltantes y vuelve a intentar.\nPresiona Enter para salir...")
            sys.exit(1)
        
        # Verificar archivos
        if not verificar_archivos():
            respuesta = input("\n⚠️  Algunos archivos faltan. ¿Continuar de todos modos? (s/n): ")
            if respuesta.lower() != 's':
                sys.exit(1)
        
        # Verificar base de datos
        if not verificar_base_datos():
            respuesta = input("\n⚠️  Base de datos no configurada. ¿Continuar de todos modos? (s/n): ")
            if respuesta.lower() != 's':
                sys.exit(1)
        
        # Iniciar aplicación
        iniciar_aplicacion()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Aplicación interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main()
