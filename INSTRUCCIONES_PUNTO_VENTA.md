# Instrucciones - Punto de Venta Moderno

## Características Implementadas

### ✅ Pantalla de Punto de Venta
- **Diseño moderno** con 3 paneles: Menú lateral, Catálogo de productos, Carrito de compras
- **Búsqueda de productos** por nombre, código o categoría
- **Filtros por categoría** con botones estilizados
- **Grid de productos** con tarjetas visuales que muestran:
  - Imagen del producto (placeholder)
  - Nombre del producto
  - Precio en color rosa
  - Stock disponible
  - Botón "Agregar al carrito"

### ✅ Carrito de Compras
- **Visualización de productos** agregados con:
  - Nombre del producto
  - Precio unitario
  - Controles de cantidad (+/-)
  - Subtotal por producto
- **Contador de productos** en el carrito
- **Botón para vaciar** el carrito completo

### ✅ Sistema de Descuentos
- **Campo de descuento** en porcentaje (0-100%)
- **Botón "Aplicar"** para aplicar el descuento
- **Visualización clara** de:
  - Subtotal (antes del descuento)
  - Descuento aplicado (en color naranja)
  - Total final (después del descuento)
- **Guardado en base de datos** del descuento aplicado

### ✅ Métodos de Pago
Tres opciones disponibles con botones estilizados:
1. **Efectivo** (seleccionado por defecto)
2. **Tarjeta**
3. **Transferencia**

### ✅ Procesamiento de Ventas
- **Validación de stock** antes de agregar productos
- **Confirmación de venta** con resumen completo
- **Actualización automática** del stock después de la venta
- **Generación de ticket** con número de venta
- **Limpieza automática** del carrito después de procesar

## Estructura de Archivos

### Nuevos Archivos
- ✅ `views/punto_venta_view.py` - Pantalla principal de punto de venta
- ✅ `test_punto_venta.py` - Script de prueba
- ✅ `migration_ventas_descuento.sql` - Migración para descuentos
- ✅ `INSTRUCCIONES_PUNTO_VENTA.md` - Este archivo

### Archivos Modificados
- ✅ `controllers/ventas.py` - Agregado soporte para descuentos
- ✅ `.sql` - Actualizada estructura de tabla ventas

## Instalación y Configuración

### 1. Actualizar Base de Datos

#### Opción A: Base de datos nueva
```bash
# En MySQL Workbench o línea de comandos:
DROP DATABASE IF EXISTS boutique_db;
SOURCE .sql
```

#### Opción B: Migración (base de datos existente)
```bash
# Aplicar migración de descuentos:
SOURCE migration_ventas_descuento.sql
```

### 2. Probar el Punto de Venta
```bash
python test_punto_venta.py
```

## Uso del Sistema

### Agregar Productos al Carrito
1. Busca productos usando la barra de búsqueda
2. Filtra por categoría si lo deseas
3. Haz clic en "Agregar al carrito" en la tarjeta del producto
4. Ajusta la cantidad usando los botones +/-

### Aplicar Descuentos
1. Ingresa el porcentaje de descuento (0-100) en el campo amarillo
2. Haz clic en "Aplicar" o presiona Enter
3. El descuento se aplicará automáticamente al total

### Seleccionar Método de Pago
1. Haz clic en uno de los tres botones: Efectivo, Tarjeta o Transferencia
2. El botón seleccionado se resaltará en color rosa

### Procesar la Venta
1. Revisa el resumen en el panel derecho
2. Haz clic en "Procesar venta"
3. Confirma la venta en el diálogo
4. El sistema generará un ticket y actualizará el stock

## Estructura de la Base de Datos

### Tabla `ventas` (actualizada)
```sql
CREATE TABLE ventas (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_cliente INT,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    descuento_porcentaje DECIMAL(5,2) DEFAULT 0.00,  -- NUEVO
    descuento_monto DECIMAL(10,2) DEFAULT 0.00,      -- NUEVO
    metodo_pago VARCHAR(20),
    subtotal DECIMAL(10,2) DEFAULT 0.00,             -- NUEVO
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);
```

## Colores del Diseño

- **Rosa principal**: `#E91E63` (botones activos, precios, total)
- **Rosa claro**: `#F06292` (hover, categorías)
- **Rosa muy claro**: `#FFF0F5` (fondos de resumen)
- **Rosa pastel**: `#F8BBD0` (menú activo)
- **Naranja**: `#FF9800` (descuentos)
- **Amarillo claro**: `#FFF9C4` (fondo de descuento)
- **Verde**: `#4CAF50` (botón agregar)
- **Gris claro**: `#F5F5F5` (fondo general)
- **Blanco**: `#FFFFFF` (tarjetas, carrito)

## Validaciones Implementadas

1. ✅ **Stock disponible**: No permite agregar más productos que el stock disponible
2. ✅ **Carrito vacío**: No permite procesar venta sin productos
3. ✅ **Descuento válido**: Limita el descuento entre 0% y 100%
4. ✅ **Confirmación**: Solicita confirmación antes de procesar la venta
5. ✅ **Limpieza de carrito**: Confirma antes de vaciar el carrito

## Próximas Mejoras Sugeridas

- [ ] Agregar imágenes reales de productos
- [ ] Implementar selección de cliente
- [ ] Agregar impresión de tickets
- [ ] Historial de ventas del día
- [ ] Atajos de teclado para acciones rápidas
- [ ] Escaneo de códigos de barras
- [ ] Múltiples métodos de pago en una sola venta
- [ ] Devoluciones y cancelaciones
- [ ] Reportes de ventas por método de pago
- [ ] Integración con caja registradora

## Notas Técnicas

- **Framework**: CustomTkinter (modo light)
- **Resolución recomendada**: 1400x800 o superior
- **Python**: 3.7+
- **Base de datos**: MySQL 5.7+

## Soporte

Si encuentras algún problema:
1. Verifica que la base de datos esté actualizada
2. Revisa que todos los productos tengan stock > 0
3. Asegúrate de que la conexión a la base de datos funcione correctamente
4. Ejecuta el script de prueba para verificar la funcionalidad
