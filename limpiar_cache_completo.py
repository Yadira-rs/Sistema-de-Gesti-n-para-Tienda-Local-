"""
Script para limpiar todo el caché de Python
"""
import os
import shutil

print("="*60)
print("LIMPIANDO CACHÉ DE PYTHON")
print("="*60)

# Directorios a limpiar
directorios = [
    'views/__pycache__',
    'controllers/__pycache__',
    'utils/__pycache__',
    'database/__pycache__',
    '__pycache__'
]

archivos_eliminados = 0

for directorio in directorios:
    if os.path.exists(directorio):
        try:
            shutil.rmtree(directorio)
            print(f"✓ Eliminado: {directorio}")
            archivos_eliminados += 1
        except Exception as e:
            print(f"✗ Error al eliminar {directorio}: {e}")
    else:
        print(f"- No existe: {directorio}")

print("\n" + "="*60)
print(f"✓ LIMPIEZA COMPLETADA - {archivos_eliminados} directorios eliminados")
print("="*60)
print("\nAhora cierra y vuelve a abrir el sistema para ver los cambios.")
