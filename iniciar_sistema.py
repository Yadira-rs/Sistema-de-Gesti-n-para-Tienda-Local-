"""
Sistema Janet Rosa Bici - Punto de Venta
Launcher Principal
"""

import os
import sys

def main():
    """Iniciar el sistema"""
    print("\n" + "=" * 60)
    print("🏪  SISTEMA JANET ROSA BICI")
    print("=" * 60)
    print("\n🚀 Iniciando sistema...\n")
    
    try:
        # Importar y ejecutar la aplicación
        from app import main as app_main
        app_main()
    except Exception as e:
        print(f"\n❌ Error al iniciar: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main()
