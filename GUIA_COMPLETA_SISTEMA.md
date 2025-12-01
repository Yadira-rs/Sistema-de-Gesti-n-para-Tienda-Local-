# Guía Completa del Sistema Janet Rosa Bici

## 🎉 Sistema Completamente Integrado

Este documento contiene toda la información necesaria para usar el sistema completo de Janet Rosa Bici con todas las funcionalidades modernas implementadas.

## 📋 Índice

1. [Instalación y Configuración](#instalación-y-configuración)
2. [Inicio del Sistema](#inicio-del-sistema)
3. [Funcionalidades Implementadas](#funcionalidades-implementadas)
4. [Guía de Uso](#guía-de-uso)
5. [Solución de Problemas](#solución-de-problemas)

---

## Instalación y Configuración

### 1. Requisitos Previos

- **Python 3.7+**
- **MySQL Server** (XAMPP, WAMP, o MySQL standalone)
- **Dependencias Python**:
  ```bash
  pip install customtkinter mysql-connector-python pillow
  ```

### 2. Configurar Base de Datos

#### Opción A: Base de Datos Nueva
```bash
# En MySQL Workbench o línea de comandos:
mysql -u root < .sql
```

#### Opción B: Base de Datos Existente (Aplicar Migraciones)
```bash
# Ejecutar en orden:
SOURCE migration_usuarios.sql
SOURCE migration_ventas_descuento.sql
SOURCE migration_productos_codigo.sql
SOURCE migration_codigo_barras.sql
```

### 3. Verificar Configuración

Edita `database/db.py` si es necesario:
```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Tu contraseña de MySQL
    database="boutique_db"
)
```

---

## Inicio del Sistema

### Método Recomendado (Con Verificación)
```bash
python iniciar_sistema.py
```

Este script verifica:
- ✅ Dependencias instaladas
- ✅ Archivos del sistema
- ✅ Conexión a MySQL
- ✅ Base de datos configurada

### Método Directo
```bash
python app.py
```

### Credenciales de Prueba
- **Usuario:** `admin` o `admin@rosabici.com`
- **Contraseña:** `1234`

---

## Funcionalidades Implementadas

### 🔐 1. Login Moderno
**Archivo:** `views/login.py`

**Características:**
- Diseño moderno con logo circular
- Título "Janet Rosa Bici" con "Rosa" en color rosa
- Campos de correo electrónico y contraseña
- Botón para mostrar/ocultar contraseña (👁)
- Soporte para login con usuario o email
- Validación de usuario activo

**Uso:**
1. Ingresa tu email o usuario
2. Ingresa tu contraseña
3. Haz clic en "Iniciar Sesión"

---

### 🛒 2. Punto de Venta Moderno
**Archivo:** `views/punto_venta_view.py`

**Características:**
- Grid de productos con tarjetas visuales
- Búsqueda en tiempo real
- **Soporte para código de barras**
- Carrito de compras interactivo
- **Sistema de descuentos** (0-100%)
- **3 métodos de pago**: Efectivo, Tarjeta, Transferencia
- Control de cantidad (+/-)
- Validación de stock
- Actualización automática de stock

**Uso:**
1. **Buscar productos:**
   - Escribe en la barra de búsqueda
   - O escanea código de barras y presiona Enter
2. **Agregar al carrito:**
   - Haz clic en "Agregar al carrito"
3. **Aplicar descuento:**
   - Ingresa el porcentaje en el campo amarillo
   - Haz clic en "Aplicar"
4. **Seleccionar método de pago:**
   - Haz clic en Efectivo, Tarjeta o Transferencia
5. **Procesar venta:**
   - Haz clic en "Procesar venta"
   - Confirma la venta
   - **Se genera automáticamente el ticket**
6. **Ticket de venta:**
   - Se muestra ventana con el ticket
   - Botón "🖨 Imprimir" para guardar en archivo .txt
   - Botón "Cerrar" para continuar

**Atajos:**
- Enter en búsqueda: Agregar producto por código de barras

---

### 📦 3. Gestión de Inventario y Productos (Unificado)
**Archivo:** `views/gestion_inventario_view.py`

**Características:**
- 4 tarjetas de estadísticas
- Tabla con badges de colores según stock
- Filtros por categoría y nivel de stock
- Búsqueda en tiempo real
- **Agregar nuevos productos** con código de barras
- Ajuste de stock (Entrada/Salida)
- **Exportar inventario a CSV**
- Códigos de barras únicos

**Uso:**
1. **Ver estadísticas:**
   - Total de productos
   - Stock total
   - Productos con stock bajo
   - Valor total del inventario

2. **Buscar productos:**
   - Usa la barra de búsqueda
   - Filtra por categoría
   - Filtra por nivel de stock

3. **Agregar nuevo producto:**
   - Haz clic en "+ Nuevo Producto"
   - Completa el formulario:
     - Código SKU
     - Código de barras (escanear o generar automático)
     - Nombre del producto
     - Descripción
     - Categoría
     - Precio
     - Stock inicial
   - Haz clic en "Crear Producto"

4. **Ajustar stock:**
   - Haz clic en "Ajustar"
   - Selecciona tipo: Entrada o Salida
   - Ingresa cantidad
   - Haz clic en "Aplicar"

5. **Exportar inventario:**
   - Haz clic en "📊 Exportar"
   - Se genera archivo CSV con fecha
   - Incluye: Código, Código Barras, Nombre, Precio, Stock, Valor Total

---

### 📋 4. Gestión de Apartados
**Archivo:** `views/gestion_apartados_view.py`

**Características:**
- 5 tarjetas de estadísticas
- Tabla con información completa
- Filtros por estado
- Búsqueda por cliente
- Ver detalles completos
- Marcar como pagado
- Cancelar apartados

**Uso:**
1. **Ver apartados:**
   - Lista completa con ID, cliente, montos
   - Estados con colores (Pendiente, Pagado, Cancelado)

2. **Ver detalles:**
   - Haz clic en 👁 (Ver)
   - Muestra productos incluidos
   - Resumen financiero

3. **Marcar como pagado:**
   - Haz clic en 💵 (Pagar)
   - Confirma la acción

4. **Cancelar:**
   - Haz clic en 🚫 (Cancelar)
   - Confirma la cancelación

---

### 👥 5. Gestión de Usuarios
**Archivo:** `views/gestion_usuarios_view.py`

**Características:**
- Formulario moderno de nuevo usuario
- Campos: Nombre completo, Email, Contraseña, Rol
- Checkbox "Usuario activo"
- Mensaje informativo sobre permisos
- Validación de campos

**Uso:**
1. **Crear usuario:**
   - Haz clic en "+ Nuevo Usuario"
   - Completa el formulario
   - Selecciona el rol
   - Marca "Usuario activo" si aplica
   - Haz clic en "Crear usuario"

---

### 🔢 6. Sistema de Códigos de Barras
**Archivos:** `controllers/products.py`, `migration_codigo_barras.sql`

**Características:**
- Códigos de barras únicos (EAN-13 simulado)
- Generación automática
- Búsqueda instantánea
- Compatible con lectores USB
- Validación de unicidad

**Formato:**
```
750 02 000001 01
│   │  │       │
│   │  │       └─ Dígitos de control (2)
│   │  └───────── ID del producto (6)
│   └──────────── ID de categoría (2)
└──────────────── Prefijo de empresa (3)
```

**Uso:**
1. **En Punto de Venta:**
   - Coloca cursor en búsqueda
   - Escanea código de barras
   - Presiona Enter
   - Producto se agrega automáticamente

2. **Agregar producto con código:**
   - Usa `views/nuevo_producto_form_mejorado.py`
   - Escanea o ingresa código
   - O haz clic en "Auto" para generar

---

## Guía de Uso

### Flujo de Trabajo Típico

#### 1. Venta Normal
```
Login → Punto de Venta → Buscar/Escanear Productos → 
Agregar al Carrito → Seleccionar Método de Pago → 
Procesar Venta → Stock se actualiza automáticamente
```

#### 2. Venta con Descuento
```
Login → Punto de Venta → Agregar Productos → 
Ingresar Descuento (%) → Aplicar → 
Seleccionar Método de Pago → Procesar Venta
```

#### 3. Crear Apartado
```
Login → Apartados → Nuevo Apartado → 
Seleccionar Cliente → Agregar Productos → 
Ingresar Anticipo → Confirmar → 
Stock se descuenta automáticamente
```

#### 4. Ajustar Inventario
```
Login → Inventario → Buscar Producto → 
Ajustar → Seleccionar Entrada/Salida → 
Ingresar Cantidad → Aplicar
```

#### 5. Gestionar Usuarios
```
Login (como Admin) → Usuarios → Nuevo Usuario → 
Completar Formulario → Crear Usuario
```

---

## Actualización Automática de Stock

El stock se actualiza automáticamente en:

### ✅ Ventas
```python
# Al procesar venta:
Stock Inicial: 20
Venta: 3 unidades
Stock Final: 17
```

### ✅ Apartados
```python
# Al crear apartado:
Stock Inicial: 20
Apartado: 5 unidades
Stock Final: 15
```

### ✅ Ajustes Manuales
```python
# Entrada:
Stock Inicial: 15
Entrada: +10
Stock Final: 25

# Salida:
Stock Inicial: 25
Salida: -5
Stock Final: 20
```

---

## Estructura de la Base de Datos

### Tablas Principales

#### `usuarios`
```sql
- id_usuario (PK)
- nombre_completo
- usuario (UNIQUE)
- email
- contraseña
- rol (Administrador, Cajero, Empleado, Vendedor)
- activo (BOOLEAN)
```

#### `productos`
```sql
- id_producto (PK)
- codigo (UNIQUE)
- codigo_barras (UNIQUE)
- nombre
- descripcion
- precio
- stock
- id_categoria (FK)
```

#### `ventas`
```sql
- id_venta (PK)
- fecha
- total
- descuento_porcentaje
- descuento_monto
- subtotal
- metodo_pago
```

#### `apartados`
```sql
- id_apartado (PK)
- fecha
- id_cliente (FK)
- total
- anticipo
- saldo
- fecha_limite
- estado (Pendiente, Pagado, Cancelado)
```

---

## Solución de Problemas

### Error: No se puede conectar a la base de datos
**Solución:**
1. Verifica que MySQL esté ejecutándose
2. Revisa las credenciales en `database/db.py`
3. Asegúrate de que la base de datos `boutique_db` exista

### Error: Módulo no encontrado
**Solución:**
```bash
pip install customtkinter mysql-connector-python pillow
```

### El lector de código de barras no funciona
**Solución:**
1. Verifica que esté conectado correctamente
2. Configura el lector para enviar Enter después de escanear
3. Prueba en un editor de texto primero

### Stock no se actualiza
**Solución:**
1. Verifica que la venta se haya procesado correctamente
2. Revisa los logs de la base de datos
3. Confirma que no haya errores en la transacción

### Ventana moderna no se abre
**Solución:**
1. Verifica que CustomTkinter esté instalado
2. Revisa la consola para ver errores
3. Asegúrate de que el usuario tenga permisos

---

## Archivos de Prueba

### Probar Punto de Venta
```bash
python test_punto_venta.py
```

### Probar Inventario
```bash
python test_inventario.py
```

### Probar Apartados
```bash
python test_apartados.py
```

### Probar Códigos de Barras
```bash
python test_codigo_barras.py
```

### Probar Login
```bash
python test_login.py
```

---

## Documentación Adicional

- `INSTRUCCIONES_PUNTO_VENTA.md` - Detalles del punto de venta
- `INSTRUCCIONES_INVENTARIO.md` - Detalles del inventario
- `INSTRUCCIONES_APARTADOS.md` - Detalles de apartados
- `INSTRUCCIONES_CODIGO_BARRAS.md` - Sistema de códigos de barras
- `INSTRUCCIONES_ACTUALIZACION.md` - Login y usuarios

---

## Características Destacadas

### ✅ Diseño Moderno
- Interfaz limpia y profesional
- Colores consistentes (rosa #E91E63)
- Iconos y badges visuales
- Responsive y adaptable

### ✅ Funcionalidad Completa
- Ventas con descuentos
- Apartados con seguimiento
- Inventario con control de stock
- Usuarios con roles
- Códigos de barras únicos

### ✅ Validaciones
- Stock disponible
- Códigos únicos
- Campos requeridos
- Permisos por rol
- Confirmaciones de acciones

### ✅ Automatización
- Stock se actualiza solo
- Cálculos automáticos
- Generación de códigos
- Búsqueda en tiempo real

---

## Soporte y Contacto

Para problemas o preguntas:
1. Revisa esta guía completa
2. Consulta los archivos de instrucciones específicos
3. Ejecuta los scripts de prueba
4. Revisa los logs de la consola

---

## Versión del Sistema

**Versión:** 2.0 - Sistema Completo Integrado
**Fecha:** Noviembre 2025
**Desarrollado para:** Janet Rosa Bici

---

¡Gracias por usar el Sistema Janet Rosa Bici! 🚲💖
