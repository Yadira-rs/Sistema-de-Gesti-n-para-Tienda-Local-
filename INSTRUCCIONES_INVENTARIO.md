# Instrucciones - Gestión de Inventario

## Características Implementadas

### ✅ Pantalla de Gestión de Inventario
- **Diseño moderno** con 3 secciones: Menú lateral, Estadísticas, Tabla de productos
- **4 Tarjetas de estadísticas** con iconos y colores distintivos:
  - 📦 Total Productos (azul)
  - 📈 Stock Total (verde)
  - ⚠️ Stock Bajo (rojo)
  - 📊 Valor Total (naranja)

### ✅ Sistema de Filtros
- **Búsqueda en tiempo real** por:
  - Nombre del producto
  - Código del producto
  - ID del producto
- **Filtro por categoría**: Todas, Ropa, Calzado, Accesorios, etc.
- **Filtro por nivel de stock**:
  - Todos los niveles
  - Stock bajo (< 10 unidades)
  - Stock medio (10-19 unidades)
  - Stock alto (≥ 20 unidades)

### ✅ Tabla de Productos
Columnas mostradas:
1. **Código**: Código único del producto (ej: VEST-001)
2. **Producto**: Nombre del producto
3. **Categoría**: Badge rosa con la categoría
4. **Precio**: Precio unitario
5. **Stock Actual**: Badge con color según nivel:
   - 🔴 Rojo: Stock bajo (< 10)
   - 🟡 Amarillo: Stock medio (10-19)
   - 🟢 Verde: Stock alto (≥ 20)
6. **Valor Total**: Precio × Stock
7. **Acción**: Botón "Ajustar" para modificar stock

### ✅ Ajuste de Stock
Diálogo modal con:
- Nombre del producto
- Stock actual
- Tipo de ajuste:
  - **Entrada**: Agregar unidades al inventario
  - **Salida**: Quitar unidades del inventario
- Campo de cantidad
- Validaciones:
  - Cantidad debe ser mayor a 0
  - No se puede quitar más stock del disponible
- Registro en tabla `movimientos_inventario`

### ✅ Actualización Automática
- Las estadísticas se actualizan después de cada ajuste
- La tabla se recarga automáticamente
- Los filtros se mantienen después de ajustar

## Estructura de Archivos

### Nuevos Archivos
- ✅ `views/gestion_inventario_view.py` - Pantalla principal de inventario
- ✅ `test_inventario.py` - Script de prueba
- ✅ `migration_productos_codigo.sql` - Migración para códigos
- ✅ `INSTRUCCIONES_INVENTARIO.md` - Este archivo

### Archivos Modificados
- ✅ `.sql` - Agregado campo `codigo` a productos

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
# Aplicar migración de códigos:
SOURCE migration_productos_codigo.sql
```

### 2. Probar el Inventario
```bash
python test_inventario.py
```

## Uso del Sistema

### Ver Estadísticas
Las 4 tarjetas en la parte superior muestran:
- Total de productos en el catálogo
- Suma total de unidades en stock
- Cantidad de productos con stock bajo
- Valor total del inventario (precio × stock)

### Buscar Productos
1. Usa la barra de búsqueda para filtrar por nombre o código
2. Los resultados se actualizan en tiempo real mientras escribes

### Filtrar por Categoría
1. Selecciona una categoría del dropdown
2. La tabla mostrará solo productos de esa categoría

### Filtrar por Nivel de Stock
1. Selecciona un nivel del dropdown
2. Opciones:
   - **Stock bajo**: Productos con menos de 10 unidades
   - **Stock medio**: Productos con 10-19 unidades
   - **Stock alto**: Productos con 20 o más unidades

### Ajustar Stock
1. Haz clic en el botón "Ajustar" de cualquier producto
2. Selecciona el tipo de ajuste:
   - **Entrada**: Para agregar stock (compras, devoluciones)
   - **Salida**: Para quitar stock (mermas, ajustes)
3. Ingresa la cantidad
4. Haz clic en "Aplicar"
5. El sistema validará y aplicará el cambio

## Estructura de la Base de Datos

### Tabla `productos` (actualizada)
```sql
CREATE TABLE productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(50) UNIQUE,                    -- NUEVO
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(200),
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    id_categoria INT,
    imagen_url VARCHAR(255),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);
```

### Tabla `movimientos_inventario`
```sql
CREATE TABLE movimientos_inventario (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT,
    tipo ENUM('Entrada','Salida','Ajuste') NOT NULL,
    cantidad INT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);
```

## Códigos de Productos

Los códigos siguen el formato: `CATEGORIA-###`

Ejemplos:
- `VEST-001`: Vestido
- `BLUS-001`: Blusa
- `PANT-001`: Pantalón
- `CALZ-001`: Calzado
- `ACCE-001`: Accesorio
- `CHAM-001`: Chamarra
- `FALD-001`: Falda
- `CAMIS-001`: Camisa

## Colores del Diseño

### Tarjetas de Estadísticas
- **Azul**: `#E3F2FD` (Total Productos)
- **Verde**: `#E8F5E9` (Stock Total)
- **Rojo**: `#FFEBEE` (Stock Bajo)
- **Naranja**: `#FFF3E0` (Valor Total)

### Badges de Stock
- **Rojo**: `#FFEBEE` / `#E53935` (Stock bajo)
- **Amarillo**: `#FFF9C4` / `#F57C00` (Stock medio)
- **Verde**: `#E8F5E9` / `#43A047` (Stock alto)

### Badges de Categoría
- **Rosa**: `#FFE0E0` / `#E91E63`

### Botones
- **Rosa principal**: `#E91E63` (botones de acción)
- **Rosa claro**: `#F06292` (hover)
- **Rosa pastel**: `#F8BBD0` (menú activo)

## Validaciones Implementadas

1. ✅ **Cantidad válida**: Debe ser un número entero mayor a 0
2. ✅ **Stock suficiente**: No permite quitar más stock del disponible
3. ✅ **Tipo de ajuste**: Solo permite "Entrada" o "Salida"
4. ✅ **Confirmación**: Muestra mensaje de éxito o error
5. ✅ **Actualización automática**: Recarga datos después de ajustar

## Próximas Mejoras Sugeridas

- [ ] Agregar campo de categoría real desde la base de datos
- [ ] Implementar edición de productos (precio, nombre, etc.)
- [ ] Agregar productos nuevos desde la interfaz
- [ ] Eliminar productos
- [ ] Historial de movimientos de inventario
- [ ] Exportar inventario a Excel/CSV
- [ ] Alertas automáticas de stock bajo
- [ ] Códigos de barras
- [ ] Imágenes de productos
- [ ] Múltiples ubicaciones/almacenes
- [ ] Reportes de rotación de inventario

## Notas Técnicas

- **Framework**: CustomTkinter (modo light)
- **Resolución recomendada**: 1400x800 o superior
- **Python**: 3.7+
- **Base de datos**: MySQL 5.7+

## Soporte

Si encuentras algún problema:
1. Verifica que la base de datos esté actualizada con el campo `codigo`
2. Asegúrate de que la tabla `movimientos_inventario` exista
3. Revisa que la conexión a la base de datos funcione correctamente
4. Ejecuta el script de prueba para verificar la funcionalidad

## Integración con Punto de Venta

El inventario se actualiza automáticamente cuando:
- Se procesa una venta en el punto de venta
- Se ajusta manualmente el stock
- Se registra un movimiento de inventario

El stock se reduce automáticamente al:
- Completar una venta
- Registrar una salida manual
- Procesar un apartado (si aplica)
