# 🏪 GUÍA COMPLETA PARA USAR JANET ROSA BICI EN TU TIENDA

## 🚀 PASO 1: INSTALACIÓN (Solo una vez)

### 📥 Descargar e Instalar
1. **Descargar** el archivo `JanetRosaBici_Distribuible_XXXXXX.zip`
2. **Descomprimir** en una carpeta (ej: Escritorio)
3. **Hacer clic derecho** en `INSTALAR.bat` → "Ejecutar como administrador"
4. **Esperar** a que termine la instalación (2-3 minutos)
5. **Listo!** Ya tienes el sistema instalado

### 🔐 Primer Acceso
1. **Ejecutar** `INICIAR_SISTEMA.bat`
2. **Iniciar sesión** con:
   - Email: `janet.rb00@gmail.com`
   - Contraseña: `admin123`

---

## 📋 PASO 2: CONFIGURACIÓN INICIAL

### 👥 Crear Usuarios para tu Tienda
1. Ir a **"Usuarios"** en el menú
2. Hacer clic **"+ Nuevo Usuario"**
3. Crear usuarios para tu personal:
   - **Gerente**: Rol "Administrador"
   - **Vendedores**: Rol "Empleado"

### 🏪 Agregar Información de tu Tienda
1. Ir a **"Perfil"** en el menú
2. Cambiar:
   - Nombre de la tienda
   - Dirección
   - Teléfono
   - Logo (opcional)

---

## 📦 PASO 3: AGREGAR TUS PRODUCTOS

### ✅ Opción 1: Agregar Productos Uno por Uno
1. Ir a **"Productos"**
2. Hacer clic **"+ Nuevo Producto"**
3. Llenar información:
   - **Nombre**: Ej. "Blusa Rosa Talla M"
   - **Precio**: Ej. 299.00
   - **Stock**: Cantidad que tienes
   - **Código** (opcional): Para organizar

### 📊 Opción 2: Importar desde Excel (Recomendado)
1. En **"Productos"** hacer clic **"📥 Importar Excel"**
2. Hacer clic **"📄 Descargar Plantilla Excel"**
3. **Abrir** la plantilla con Excel
4. **Llenar** con tus productos:
   ```
   Código    | Código Barras | Nombre           | Precio | Stock
   BLUSA001  | 123456789     | Blusa Rosa M     | 299.00 | 15
   PANT001   | 123456790     | Pantalón Negro L | 450.00 | 8
   ```
5. **Guardar** el archivo
6. **Importar** el archivo en el sistema

---

## 💰 PASO 4: REALIZAR VENTAS

### 🛒 Venta Normal
1. Ir a **"Punto de Venta"**
2. **Buscar** productos por nombre o código
3. **Agregar** al carrito
4. **Seleccionar cliente** (opcional)
5. **Elegir método de pago**:
   - Efectivo
   - Tarjeta
   - Transferencia
6. **Finalizar venta**
7. **Imprimir ticket** (si tienes impresora)

### 💳 Venta a Crédito
1. En **"Punto de Venta"** seleccionar **"Crédito"**
2. **Elegir cliente** (obligatorio)
3. **Agregar productos**
4. **Definir plazo** (ej: 30 días)
5. **Finalizar venta a crédito**

---

## 👥 PASO 5: GESTIONAR CLIENTES

### ➕ Agregar Clientes
1. Ir a **"Clientes"**
2. Hacer clic **"+ Nuevo Cliente"**
3. Llenar datos:
   - **Nombre completo**
   - **Teléfono** (obligatorio)
   - **Email** (opcional)

### 💰 Controlar Créditos
1. Ir a **"Ventas a Crédito"**
2. Ver todos los créditos pendientes
3. **Registrar abonos**:
   - Hacer clic **"💰 Abono"**
   - Ingresar monto pagado
   - El sistema calcula automáticamente el saldo

---

## 📊 PASO 6: REVISAR REPORTES

### 📈 Dashboard
- **Ventas del día**
- **Total de productos**
- **Stock bajo** (productos que se están agotando)
- **Últimas ventas**

### 📋 Historial de Ventas
1. Ir a **"Ventas"** → **"Historial"**
2. Ver todas las ventas por fecha
3. **Exportar reportes** a Excel/PDF

### 📦 Control de Inventario
1. Ir a **"Productos"**
2. Ver stock actual
3. **Exportar inventario** completo

---

## 🎯 RUTINA DIARIA RECOMENDADA

### 🌅 Al Abrir la Tienda
1. **Iniciar sistema**: `INICIAR_SISTEMA.bat`
2. **Revisar dashboard**: Ver ventas del día anterior
3. **Verificar stock bajo**: Productos que necesitas reponer

### 💼 Durante el Día
1. **Realizar ventas** normales y a crédito
2. **Agregar nuevos clientes** cuando sea necesario
3. **Registrar abonos** de créditos

### 🌙 Al Cerrar la Tienda
1. **Revisar ventas del día** en el dashboard
2. **Exportar reporte** si es necesario
3. **Cerrar sistema** normalmente

---

## 🆘 PROBLEMAS COMUNES Y SOLUCIONES

### ❌ "No se puede iniciar el sistema"
**Solución**: Ejecutar `INSTALAR.bat` como administrador

### ❌ "Error de base de datos"
**Solución**: Verificar que existe el archivo `boutique.db`

### ❌ "No se pueden agregar productos"
**Solución**: Verificar que tienes permisos de administrador

### ❌ "No imprime tickets"
**Solución**: 
1. Verificar que la impresora esté conectada
2. Configurar impresora en Windows
3. Probar impresión desde otra aplicación

### ❌ "Se perdieron los datos"
**Solución**: Los datos están en `boutique.db` - hacer respaldo regular

---

## 💾 RESPALDOS IMPORTANTES

### 📁 Archivos a Respaldar (Copiar a USB/Drive)
- `boutique.db` (Base de datos con todos los datos)
- `config_db.json` (Configuración)
- Carpeta completa del sistema

### ⏰ Frecuencia Recomendada
- **Diario**: Copiar `boutique.db` a USB
- **Semanal**: Respaldar carpeta completa
- **Mensual**: Exportar reportes a Excel

---

## 📞 SOPORTE TÉCNICO

### 🔧 Autoayuda
1. Reiniciar el sistema
2. Ejecutar `INSTALAR.bat` nuevamente
3. Verificar conexión a internet
4. Revisar que no hay antivirus bloqueando

### 📱 Contacto
Para problemas técnicos complejos, contactar al desarrollador del sistema.

---

## 🎉 ¡LISTO PARA VENDER!

Con esta guía ya puedes:
✅ Instalar el sistema
✅ Configurar tu tienda
✅ Agregar productos
✅ Realizar ventas
✅ Controlar créditos
✅ Generar reportes
✅ Mantener el sistema

**¡Tu tienda ahora tiene un sistema profesional de punto de venta!** 🏪💰

---

*Janet Rosa Bici - Sistema de Punto de Venta v1.0*
*Desarrollado para hacer crecer tu negocio* ❤️