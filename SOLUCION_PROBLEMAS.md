# Solución de Problemas - Janet Rosa Bici

## Problemas Comunes y Soluciones

### 🔴 Problema: La ventana se cierra al abrir Punto de Venta

**Síntomas:**
- Al hacer clic en "Punto de Venta" la ventana desaparece
- El programa se cierra sin mensaje de error
- La consola muestra errores

**Causas posibles:**
1. Error en la base de datos
2. Falta alguna dependencia
3. Error en el código de la vista

**Soluciones:**

#### Solución 1: Verificar la consola
```bash
# Ejecuta el sistema y revisa los mensajes de error
python iniciar_sistema.py
```
La consola mostrará el error exacto. Busca líneas que digan "Error" o "Traceback".

#### Solución 2: Probar la vista independientemente
```bash
# Prueba solo el punto de venta
python test_punto_venta.py
```
Si funciona aquí pero no en el sistema completo, el problema está en la integración.

#### Solución 3: Verificar la base de datos
```bash
# Verifica que la tabla productos exista
mysql -u root -e "USE boutique_db; SHOW TABLES;"
```

#### Solución 4: Reinstalar dependencias
```bash
pip uninstall customtkinter
pip install customtkinter --upgrade
```

---

### 🔴 Problema: Error "Table doesn't exist"

**Síntomas:**
- Mensaje: "Table 'boutique_db.apartados' doesn't exist"
- O similar para otras tablas

**Solución:**
```bash
# Recrear la base de datos completa
mysql -u root < .sql
```

O desde MySQL Workbench:
```sql
DROP DATABASE IF EXISTS boutique_db;
SOURCE .sql;
```

---

### 🔴 Problema: Error "No module named 'customtkinter'"

**Síntomas:**
- Error al iniciar: ModuleNotFoundError

**Solución:**
```bash
pip install customtkinter mysql-connector-python pillow
```

---

### 🔴 Problema: La ventana principal no vuelve a aparecer

**Síntomas:**
- Cierras una vista moderna y no vuelve el menú
- El programa parece congelado

**Solución:**
1. Cierra completamente el programa (Ctrl+C en consola)
2. Reinicia con:
```bash
python iniciar_sistema.py
```

**Prevención:**
- Siempre cierra las ventanas con el botón X o "Cerrar"
- No uses Alt+F4 o cierres forzadamente

---

### 🔴 Problema: Error al conectar a MySQL

**Síntomas:**
- "Can't connect to MySQL server"
- "Access denied for user"

**Soluciones:**

#### Solución 1: Verificar que MySQL esté corriendo
**XAMPP:**
```
1. Abre XAMPP Control Panel
2. Inicia Apache y MySQL
3. Verifica que MySQL esté en verde
```

**WAMP:**
```
1. Abre WAMP
2. Verifica que el icono esté verde
3. Inicia todos los servicios
```

#### Solución 2: Verificar credenciales
Edita `database/db.py`:
```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Cambia si tienes contraseña
    database="boutique_db"
)
```

---

### 🔴 Problema: Código de barras no funciona

**Síntomas:**
- El lector no agrega productos
- No pasa nada al escanear

**Soluciones:**

#### Solución 1: Verificar configuración del lector
1. Abre un editor de texto (Notepad)
2. Escanea un código de barras
3. Debe escribir el código y presionar Enter

Si no funciona:
- Configura el lector para enviar Enter (CR/LF)
- Verifica que esté en modo teclado (HID)

#### Solución 2: Probar manualmente
1. Abre Punto de Venta
2. Escribe un código de barras: `7500100000101`
3. Presiona Enter
4. Debe agregar el producto

---

### 🔴 Problema: Stock no se actualiza

**Síntomas:**
- Procesas una venta pero el stock sigue igual
- El inventario no refleja los cambios

**Solución:**
```bash
# Verifica que la venta se haya registrado
mysql -u root -e "USE boutique_db; SELECT * FROM ventas ORDER BY id_venta DESC LIMIT 5;"

# Verifica el stock actual
mysql -u root -e "USE boutique_db; SELECT id_producto, nombre, stock FROM productos;"
```

Si el stock no cambió:
1. Verifica que no haya errores en la consola
2. Revisa que la transacción se haya completado
3. Reinicia el sistema

---

### 🔴 Problema: Ticket no se genera

**Síntomas:**
- La venta se procesa pero no aparece el ticket
- Error al mostrar el ticket

**Solución:**
```bash
# Prueba el ticket independientemente
python test_ticket.py
```

Si funciona aquí:
- El problema está en la integración
- Revisa la consola para ver el error exacto

---

### 🔴 Problema: Ventana muy pequeña o muy grande

**Síntomas:**
- La interfaz se ve cortada
- Los elementos están muy juntos o separados

**Solución:**
Edita el archivo de la vista y cambia la geometría:
```python
self.geometry("1400x800")  # Ajusta según tu pantalla
```

Resoluciones recomendadas:
- **1920x1080**: `1600x900`
- **1366x768**: `1300x700`
- **1280x720**: `1200x650`

---

### 🔴 Problema: Fuentes no se ven bien

**Síntomas:**
- El texto se ve pixelado
- Las fuentes no son las correctas

**Solución:**
Instala las fuentes recomendadas:
- **Segoe UI** (Windows, ya incluida)
- **Brush Script MT** (para el logo)

Si no tienes Brush Script MT:
- Edita los archivos y cambia a "Arial" o "Comic Sans MS"

---

## 🛠️ Herramientas de Diagnóstico

### Script de Verificación Completa
```bash
python iniciar_sistema.py
```
Este script verifica:
- ✅ Dependencias instaladas
- ✅ Archivos del sistema
- ✅ Conexión a MySQL
- ✅ Base de datos configurada

### Verificar Logs
Los errores se muestran en:
1. **Consola**: Donde ejecutaste el programa
2. **Pantalla**: Mensaje de error con detalles
3. **Archivos**: Algunos errores se guardan en logs

---

## 📞 Obtener Ayuda

### Información útil para reportar problemas:

1. **Sistema Operativo:**
   ```bash
   # Windows
   systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
   ```

2. **Versión de Python:**
   ```bash
   python --version
   ```

3. **Dependencias instaladas:**
   ```bash
   pip list | findstr "customtkinter mysql pillow"
   ```

4. **Error completo:**
   - Copia todo el texto de la consola
   - Incluye el "Traceback" completo

---

## 🔧 Reinstalación Completa

Si nada funciona, reinstala todo:

### Paso 1: Desinstalar dependencias
```bash
pip uninstall customtkinter mysql-connector-python pillow -y
```

### Paso 2: Reinstalar
```bash
pip install customtkinter mysql-connector-python pillow
```

### Paso 3: Recrear base de datos
```bash
mysql -u root -e "DROP DATABASE IF EXISTS boutique_db;"
mysql -u root < .sql
```

### Paso 4: Probar
```bash
python iniciar_sistema.py
```

---

## ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] MySQL está corriendo
- [ ] Base de datos `boutique_db` existe
- [ ] Dependencias instaladas correctamente
- [ ] Python 3.7 o superior
- [ ] Archivos del sistema completos
- [ ] Credenciales de MySQL correctas
- [ ] Consola muestra el error completo

---

## 🎯 Problemas Conocidos

### Windows 11
- Algunas veces las ventanas CustomTkinter tardan en aparecer
- **Solución**: Espera unos segundos

### Pantallas de alta resolución (4K)
- Los elementos pueden verse muy pequeños
- **Solución**: Ajusta la geometría de las ventanas

### MySQL en XAMPP
- A veces MySQL no inicia correctamente
- **Solución**: Reinicia XAMPP como administrador

---

## 📚 Recursos Adicionales

- `GUIA_COMPLETA_SISTEMA.md` - Guía completa
- `RESUMEN_FINAL.md` - Resumen de funcionalidades
- Scripts de prueba: `test_*.py`
- Documentación específica: `INSTRUCCIONES_*.md`

---

¿Sigues teniendo problemas? Revisa la consola y busca el error específico en este documento.
