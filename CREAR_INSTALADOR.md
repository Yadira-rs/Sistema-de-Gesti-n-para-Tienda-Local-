# 📦 Cómo Crear un Instalador para Janet Rosa Bici

## Guía Completa para Convertir el Sistema en Aplicación Instalable

---

## 🎯 Objetivo

Convertir el sistema Python en un archivo ejecutable (.exe) que se pueda instalar en cualquier computadora Windows sin necesidad de tener Python instalado.

---

## 📋 Requisitos Previos

1. Python instalado en tu computadora
2. El sistema funcionando correctamente
3. Todas las dependencias instaladas

---

## 🚀 Método 1: PyInstaller (Recomendado)

### Paso 1: Instalar PyInstaller

```bash
pip install pyinstaller
```

### Paso 2: Crear el ejecutable

Opción A - Ejecutable simple:
```bash
pyinstaller --onefile --windowed --name="JanetRosaBici" --icon=logo.ico app.py
```

Opción B - Con todos los archivos (más estable):
```bash
pyinstaller --windowed --name="JanetRosaBici" --icon=logo.ico app.py
```

### Paso 3: Incluir archivos adicionales

Crea un archivo `JanetRosaBici.spec` con este contenido:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logo.png', '.'),
        ('mysql_config.ini', '.'),
        ('login_config.json', '.'),
        ('controllers', 'controllers'),
        ('database', 'database'),
        ('views', 'views'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'mysql.connector',
        'customtkinter',
        'openpyxl',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JanetRosaBici',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.ico'
)
```

Luego ejecuta:
```bash
pyinstaller JanetRosaBici.spec
```

### Paso 4: Encontrar el ejecutable

El archivo .exe estará en la carpeta `dist/`

---

## 🎨 Crear un Icono (.ico)

### Opción 1: Convertir tu logo

1. Ve a https://convertio.co/es/png-ico/
2. Sube tu logo.png
3. Descarga el archivo .ico
4. Guárdalo como `logo.ico` en la raíz del proyecto

### Opción 2: Usar Python

```bash
pip install pillow
```

```python
from PIL import Image

img = Image.open('logo.png')
img.save('logo.ico', format='ICO', sizes=[(256, 256)])
```

---

## 📦 Método 2: Crear Instalador con Inno Setup

### Paso 1: Descargar Inno Setup

1. Ve a https://jrsoftware.org/isdl.php
2. Descarga e instala Inno Setup

### Paso 2: Crear script de instalación

Crea un archivo `installer.iss`:

```ini
[Setup]
AppName=Janet Rosa Bici
AppVersion=2.0
DefaultDirName={pf}\JanetRosaBici
DefaultGroupName=Janet Rosa Bici
OutputDir=output
OutputBaseFilename=JanetRosaBici_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=logo.ico
UninstallDisplayIcon={app}\JanetRosaBici.exe

[Files]
Source: "dist\JanetRosaBici.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "mysql_config.ini"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Janet Rosa Bici"; Filename: "{app}\JanetRosaBici.exe"
Name: "{commondesktop}\Janet Rosa Bici"; Filename: "{app}\JanetRosaBici.exe"

[Run]
Filename: "{app}\JanetRosaBici.exe"; Description: "Ejecutar Janet Rosa Bici"; Flags: postinstall nowait skipifsilent
```

### Paso 3: Compilar el instalador

1. Abre Inno Setup
2. Abre el archivo `installer.iss`
3. Click en "Build" > "Compile"
4. El instalador estará en la carpeta `output/`

---

## 🗂️ Estructura de Archivos para Distribución

```
JanetRosaBici_Distribucion/
├── JanetRosaBici.exe          # Ejecutable principal
├── logo.png                    # Logo del sistema
├── mysql_config.ini            # Configuración de BD
├── README.md                   # Instrucciones
└── INSTALACION.txt            # Guía de instalación
```

---

## 📝 Crear Archivo de Instalación

Crea `INSTALACION.txt`:

```
================================================================================
INSTALACIÓN DE JANET ROSA BICI - SISTEMA DE PUNTO DE VENTA
================================================================================

REQUISITOS:
-----------
1. Windows 7 o superior
2. MySQL Server instalado y corriendo
3. Base de datos 'boutique_db' creada

PASOS DE INSTALACIÓN:
---------------------

1. Ejecutar el instalador: JanetRosaBici_Setup.exe

2. Seguir el asistente de instalación

3. Configurar la base de datos:
   - Abrir mysql_config.ini
   - Editar con tus credenciales de MySQL:
     [mysql]
     host = localhost
     user = root
     password = tu_contraseña
     database = boutique_db

4. Ejecutar la aplicación desde el escritorio o menú inicio

PRIMER USO:
-----------
Usuario: admin
Contraseña: 1234

SOPORTE:
--------
Para ayuda, contacta al administrador del sistema.

================================================================================
```

---

## 🔧 Script Automatizado de Compilación

Crea `compilar.py`:

```python
import os
import subprocess
import shutil

def compilar_sistema():
    print("=" * 70)
    print("📦 COMPILANDO JANET ROSA BICI")
    print("=" * 70)
    print()
    
    # Paso 1: Limpiar carpetas anteriores
    print("1️⃣  Limpiando compilaciones anteriores...")
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    print("   ✅ Limpieza completada")
    print()
    
    # Paso 2: Compilar con PyInstaller
    print("2️⃣  Compilando con PyInstaller...")
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=JanetRosaBici',
        '--add-data=logo.png;.',
        '--add-data=mysql_config.ini;.',
        '--add-data=controllers;controllers',
        '--add-data=database;database',
        '--add-data=views;views',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=mysql.connector',
        '--hidden-import=customtkinter',
        '--hidden-import=openpyxl',
        'app.py'
    ]
    
    if os.path.exists('logo.ico'):
        cmd.insert(4, '--icon=logo.ico')
    
    subprocess.run(cmd)
    print("   ✅ Compilación completada")
    print()
    
    # Paso 3: Copiar archivos necesarios
    print("3️⃣  Copiando archivos necesarios...")
    archivos_copiar = [
        'logo.png',
        'mysql_config.ini',
        'README.md',
        'INSTALACION.txt'
    ]
    
    for archivo in archivos_copiar:
        if os.path.exists(archivo):
            shutil.copy(archivo, 'dist/')
            print(f"   ✅ {archivo}")
    print()
    
    print("=" * 70)
    print("✅ COMPILACIÓN COMPLETADA")
    print("=" * 70)
    print()
    print("📁 El ejecutable está en: dist/JanetRosaBici.exe")
    print()
    print("Próximos pasos:")
    print("1. Prueba el ejecutable: dist/JanetRosaBici.exe")
    print("2. Crea el instalador con Inno Setup (opcional)")
    print()

if __name__ == "__main__":
    compilar_sistema()
    input("Presiona Enter para salir...")
```

Ejecuta:
```bash
python compilar.py
```

---

## ✅ Verificación Final

### Antes de distribuir, verifica:

- [ ] El ejecutable se abre correctamente
- [ ] El logo se muestra
- [ ] La conexión a MySQL funciona
- [ ] Todas las vistas se cargan
- [ ] Los botones funcionan
- [ ] Se pueden hacer ventas
- [ ] Los reportes se generan

---

## 📤 Distribución

### Opción 1: Carpeta Portable
Comprime la carpeta `dist/` en un ZIP y distribúyela.

### Opción 2: Instalador
Usa el instalador creado con Inno Setup.

### Opción 3: USB
Copia la carpeta `dist/` a una USB y ejecútala desde ahí.

---

## 🐛 Solución de Problemas

### Error: "No se puede conectar a MySQL"
- Verifica que MySQL esté corriendo
- Revisa las credenciales en mysql_config.ini

### Error: "Falta un módulo"
- Agrega el módulo a hiddenimports en el .spec

### El ejecutable es muy grande
- Usa `--onefile` para un solo archivo
- Usa UPX para comprimir: `--upx-dir=ruta/upx`

### No se ve el logo
- Asegúrate de incluir logo.png en datas
- Verifica la ruta en el código

---

## 💡 Consejos

1. **Prueba en otra computadora** antes de distribuir
2. **Incluye un README** con instrucciones
3. **Versiona tus releases** (v1.0, v2.0, etc.)
4. **Crea un backup** de la base de datos
5. **Documenta los cambios** en cada versión

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en la carpeta del ejecutable
2. Ejecuta desde CMD para ver errores
3. Verifica que todas las dependencias estén incluidas

---

**¡Tu sistema está listo para ser distribuido como aplicación profesional!** 🎉
