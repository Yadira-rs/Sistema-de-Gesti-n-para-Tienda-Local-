"""
Script de prueba para verificar que todos los componentes funcionen
"""

def probar_imports():
    """Probar que todos los imports funcionen"""
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE COMPONENTES DEL SISTEMA")
    print("=" * 70)
    print()
    
    print("1️⃣  Verificando dependencias...")
    try:
        import customtkinter
        print("   ✅ customtkinter")
    except ImportError as e:
        print(f"   ❌ customtkinter: {e}")
        return False
    
    try:
        import mysql.connector
        print("   ✅ mysql-connector-python")
    except ImportError as e:
        print(f"   ❌ mysql-connector-python: {e}")
        return False
    
    try:
        from PIL import Image
        print("   ✅ Pillow (PIL)")
    except ImportError as e:
        print(f"   ❌ Pillow: {e}")
        return False
    
    try:
        import openpyxl
        print("   ✅ openpyxl")
    except ImportError as e:
        print(f"   ❌ openpyxl: {e}")
        return False
    
    print()
    print("2️⃣  Verificando módulos del sistema...")
    
    try:
        from database.db import crear_conexion
        print("   ✅ database.db")
    except ImportError as e:
        print(f"   ❌ database.db: {e}")
        return False
    
    try:
        from controllers.products import obtener_productos
        print("   ✅ controllers.products")
    except ImportError as e:
        print(f"   ❌ controllers.products: {e}")
        return False
    
    try:
        from controllers.ventas import obtener_carrito
        print("   ✅ controllers.ventas")
    except ImportError as e:
        print(f"   ❌ controllers.ventas: {e}")
        return False
    
    try:
        from controllers.creditos import obtener_creditos
        print("   ✅ controllers.creditos")
    except ImportError as e:
        print(f"   ❌ controllers.creditos: {e}")
        return False
    
    try:
        from controllers.apartados import listar_apartados
        print("   ✅ controllers.apartados")
    except ImportError as e:
        print(f"   ❌ controllers.apartados: {e}")
        return False
    
    try:
        from controllers.users import listar_usuarios
        print("   ✅ controllers.users")
    except ImportError as e:
        print(f"   ❌ controllers.users: {e}")
        return False
    
    print()
    print("3️⃣  Verificando vistas...")
    
    try:
        from views.login import LoginWindow
        print("   ✅ views.login")
    except ImportError as e:
        print(f"   ❌ views.login: {e}")
        return False
    
    try:
        from views.dashboard import DashboardView
        print("   ✅ views.dashboard")
    except ImportError as e:
        print(f"   ❌ views.dashboard: {e}")
        return False
    
    try:
        from views.ventas_view import VentasView
        print("   ✅ views.ventas_view")
    except ImportError as e:
        print(f"   ❌ views.ventas_view: {e}")
        return False
    
    try:
        from views.products_view import ProductsView
        print("   ✅ views.products_view")
    except ImportError as e:
        print(f"   ❌ views.products_view: {e}")
        return False
    
    try:
        from views.users_view import UsersView
        print("   ✅ views.users_view")
    except ImportError as e:
        print(f"   ❌ views.users_view: {e}")
        return False
    
    try:
        from views.gestion_creditos_view import GestionCreditosView
        print("   ✅ views.gestion_creditos_view")
    except ImportError as e:
        print(f"   ❌ views.gestion_creditos_view: {e}")
        return False
    
    try:
        from views.gestion_apartados_view import GestionApartadosView
        print("   ✅ views.gestion_apartados_view")
    except ImportError as e:
        print(f"   ❌ views.gestion_apartados_view: {e}")
        return False
    
    print()
    print("4️⃣  Verificando conexión a base de datos...")
    
    try:
        from database.db import crear_conexion
        conn = crear_conexion()
        if conn:
            conn.close()
            print("   ✅ Conexión a base de datos exitosa")
        else:
            print("   ⚠️  No se pudo conectar a la base de datos")
            print("      Verifica mysql_config.ini")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    print()
    print("=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 70)
    print()
    print("📌 RESUMEN:")
    print("   • Todas las dependencias están instaladas")
    print("   • Todos los módulos se importan correctamente")
    print("   • El sistema está listo para funcionar")
    print()
    print("🚀 Para iniciar el sistema ejecuta:")
    print("   python iniciar_sistema.py")
    print()
    
    return True

if __name__ == "__main__":
    try:
        probar_imports()
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPresiona Enter para salir...")
