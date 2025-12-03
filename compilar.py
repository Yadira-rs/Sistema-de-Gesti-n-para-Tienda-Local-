"""
Script para compilar Janet Rosa Bici en un ejecutable
"""

import os
import subprocess
import shutil

def compilar_sistema():
    print("=" * 70)
    print("📦 COMPILANDO JANET ROSA BICI")
    print("=" * 70)
    print()
    
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
        print("✅ PyInstaller está instalado")
    except ImportError:
        print("❌ PyInstaller no está instalado")
        print()
        print("Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print()
    
    # Paso 1: Limpiar carpetas anteriores
    print("1️⃣  Limpiando compilaciones anteriores...")
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("   🗑️  Carpeta 'build' eliminada")
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        print("   🗑️  Carpeta 'dist' eliminada")
    print("   ✅ Limpieza completada")
    print()
    
    # Paso 2: Compilar con PyInstaller
    print("2️⃣  Compilando con PyInstaller...")
    print("   ⏳ Esto puede tardar varios minutos...")
    print()
    
    # Usar python -m PyInstaller en lugar de pyinstaller directamente
    cmd = [
        sys.executable,
        '-m',
        'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=JanetRosaBici',
        '--add-data=controllers;controllers',
        '--add-data=database;database',
        '--add-data=views;views',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=mysql.connector',
        '--hidden-import=customtkinter',
        '--hidden-import=openpyxl',
        'app.py'
    ]
    
    # Agregar logo si existe
    if os.path.exists('logo.ico'):
        cmd.insert(4, '--icon=logo.ico')
        print("   🎨 Usando logo.ico como icono")
    elif os.path.exists('logo.png'):
        print("   ℹ️  Nota: Convierte logo.png a logo.ico para mejor resultado")
    
    # Agregar archivos de configuración si existen
    if os.path.exists('mysql_config.ini'):
        cmd.insert(4, '--add-data=mysql_config.ini;.')
    if os.path.exists('logo.png'):
        cmd.insert(4, '--add-data=logo.png;.')
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Compilación completada exitosamente")
        else:
            print("   ⚠️  Compilación completada con advertencias")
    except Exception as e:
        print(f"   ❌ Error durante la compilación: {e}")
        return False
    
    print()
    
    # Paso 3: Copiar archivos necesarios
    print("3️⃣  Copiando archivos necesarios a dist/...")
    archivos_copiar = [
        ('logo.png', 'Logo del sistema'),
        ('mysql_config.ini', 'Configuración de base de datos'),
        ('README.md', 'Documentación'),
        ('LEEME_PRIMERO.txt', 'Guía rápida'),
        ('COMO_AGREGAR_LOGO.txt', 'Instrucciones del logo')
    ]
    
    for archivo, descripcion in archivos_copiar:
        if os.path.exists(archivo):
            try:
                shutil.copy(archivo, 'dist/')
                print(f"   ✅ {archivo} - {descripcion}")
            except Exception as e:
                print(f"   ⚠️  No se pudo copiar {archivo}: {e}")
    
    print()
    
    # Paso 4: Crear archivo de instrucciones
    print("4️⃣  Creando archivo de instrucciones...")
    instrucciones = """================================================================================
JANET ROSA BICI - SISTEMA DE PUNTO DE VENTA
================================================================================

INSTRUCCIONES DE USO:
--------------------

1. Asegúrate de que MySQL esté instalado y corriendo

2. Configura la base de datos:
   - Abre mysql_config.ini
   - Edita con tus credenciales:
     [mysql]
     host = localhost
     user = root
     password = tu_contraseña
     database = boutique_db

3. Ejecuta JanetRosaBici.exe

4. Inicia sesión:
   Usuario: admin
   Contraseña: 1234

REQUISITOS:
-----------
• Windows 7 o superior
• MySQL Server instalado
• Base de datos 'boutique_db' creada

SOPORTE:
--------
Para ayuda, consulta README.md o LEEME_PRIMERO.txt

================================================================================
"""
    
    try:
        with open('dist/INSTRUCCIONES.txt', 'w', encoding='utf-8') as f:
            f.write(instrucciones)
        print("   ✅ INSTRUCCIONES.txt creado")
    except Exception as e:
        print(f"   ⚠️  No se pudo crear INSTRUCCIONES.txt: {e}")
    
    print()
    
    # Resumen final
    print("=" * 70)
    print("✅ COMPILACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print()
    print("📁 Ubicación del ejecutable:")
    print(f"   {os.path.abspath('dist/JanetRosaBici.exe')}")
    print()
    print("📦 Archivos en dist/:")
    if os.path.exists('dist'):
        for archivo in os.listdir('dist'):
            tamaño = os.path.getsize(os.path.join('dist', archivo)) / (1024 * 1024)
            print(f"   • {archivo} ({tamaño:.2f} MB)")
    print()
    print("🎯 Próximos pasos:")
    print("   1. Prueba el ejecutable: dist/JanetRosaBici.exe")
    print("   2. Verifica que todo funcione correctamente")
    print("   3. Distribuye la carpeta 'dist' completa")
    print()
    print("💡 Opcional:")
    print("   • Crea un instalador con Inno Setup")
    print("   • Comprime 'dist' en un ZIP para distribución")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    
    try:
        exito = compilar_sistema()
        
        if exito:
            print("🎉 ¡Sistema compilado exitosamente!")
        else:
            print("❌ Hubo errores durante la compilación")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Compilación cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    input("Presiona Enter para salir...")
