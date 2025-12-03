"""
Script para instalar todas las dependencias necesarias del sistema
"""

import subprocess
import sys

def instalar_dependencias():
    """Instalar todas las dependencias desde requirements.txt"""
    print("=" * 70)
    print("📦 INSTALACIÓN DE DEPENDENCIAS")
    print("=" * 70)
    print()
    
    dependencias = [
        'customtkinter',
        'mysql-connector-python',
        'Pillow',
        'openpyxl'
    ]
    
    print("Instalando dependencias necesarias...")
    print()
    
    for dep in dependencias:
        print(f"📦 Instalando {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"   ✅ {dep} instalado correctamente")
        except Exception as e:
            print(f"   ❌ Error al instalar {dep}: {e}")
        print()
    
    print("=" * 70)
    print("✅ INSTALACIÓN COMPLETADA")
    print("=" * 70)
    print()
    print("Ahora puedes ejecutar el sistema con:")
    print("   python iniciar_sistema.py")
    print()

if __name__ == "__main__":
    instalar_dependencias()
    input("Presiona Enter para salir...")
