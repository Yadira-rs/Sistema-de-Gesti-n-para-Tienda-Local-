# Instrucciones - Gestión de Apartados

## Características Implementadas

### ✅ Pantalla de Gestión de Apartados
- **Diseño moderno** con 3 secciones: Menú lateral, Estadísticas, Tabla de apartados
- **5 Tarjetas de estadísticas**:
  - 📋 Total: Total de apartados registrados
  - Activos: Apartados pendientes de pago
  - ✅ Completados: Apartados pagados completamente
  - 🚫 Cancelados: Apartados cancelados
  - ⏱ Pendiente: Monto total pendiente de cobro

### ✅ Sistema de Filtros
- **Búsqueda en tiempo real** por:
  - Nombre del cliente
  - Teléfono del cliente
  - ID del apartado
- **Filtro por estado**:
  - Todos los estados
  - Pendiente
  - Pagado
  - Cancelado

### ✅ Tabla de Apartados
Columnas mostradas:
1. **ID**: Número único del apartado
2. **Cliente**: Nombre del cliente
3. **Total**: Monto total del apartado
4. **Anticipo**: Monto pagado (verde)
5. **Saldo**: Monto pendiente (naranja)
6. **Fecha límite**: Fecha de vencimiento
7. **Estado**: Badge con color según estado:
   - 🔴 Rojo: Cancelado
   - 🟢 Verde: Pagado
   - ⚪ Gris: Pendiente
8. **Acciones**: 3 botones de acción

### ✅ Acciones Disponibles
1. **👁 Ver**: Muestra detalles completos del apartado
   - Información del cliente
   - Resumen financiero (Total, Anticipo, Saldo)
   - Lista de productos incluidos
   
2. **💵 Pagar**: Marca el apartado como pagado
   - Solo disponible para apartados pendientes
   - Actualiza el estado a "Pagado"
   - Actualiza las estadísticas automáticamente

3. **🚫 Cancelar**: Cancela el apartado
   - Solicita confirmación
   - Actualiza el estado a "Cancelado"
   - Acción irreversible

### ✅ Ventana de Detalles
Al hacer clic en "Ver", se muestra:
- Número de apartado
- Información del cliente
- Resumen financiero con colores:
  - Total (negro)
  - Anticipo (verde)
  - Saldo (naranja)
- Lista scrolleable de productos con:
  - Nombre y cantidad
  - Subtotal por producto

## Estructura de Archivos

### Nuevos Archivos
- ✅ `views/gestion_apartados_view.py` - Pantalla principal de apartados
- ✅ `test_apartados.py` - Script de prueba
- ✅ `INSTRUCCIONES_APARTADOS.md` - Este archivo

### Archivos Modificados
- ✅ `controllers/apartados.py` - Agregadas funciones de listado, detalle y actualización

## Instalación y Configuración

### 1. Verificar Base de Datos
Asegúrate de que las tablas `apartados` y `detalle_apartados` existan:

```sql
-- Tabla apartados
CREATE TABLE apartados (
    id_apartado INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_cliente INT,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    anticipo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    fecha_limite DATE NULL,
    estado ENUM('Pendiente','Pagado','Cancelado') NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Tabla detalle_apartados
CREATE TABLE detalle_apartados (
    id_detalle_apartado INT PRIMARY KEY AUTO_INCREMENT,
    id_apartado INT,
    id_producto INT,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_apartado) REFERENCES apartados(id_apartado),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);
```

### 2. Probar Apartados
```bash
python test_apartados.py
```

## Uso del Sistema

### Ver Estadísticas
Las 5 tarjetas en la parte superior muestran:
- Total de apartados en el sistema
- Cantidad de apartados activos (pendientes)
- Cantidad de apartados completados (pagados)
- Cantidad de apartados cancelados
- Monto total pendiente de cobro

### Buscar Apartados
1. Usa la barra de búsqueda para filtrar por cliente, teléfono o ID
2. Los resultados se actualizan en tiempo real mientras escribes

### Filtrar por Estado
1. Selecciona un estado del dropdown
2. La tabla mostrará solo apartados con ese estado

### Ver Detalles de un Apartado
1. Haz clic en el botón 👁 (Ver) de cualquier apartado
2. Se abrirá una ventana modal con:
   - Información del cliente
   - Resumen financiero
   - Lista de productos incluidos
3. Haz clic en "Cerrar" para regresar

### Marcar como Pagado
1. Haz clic en el botón 💵 (Pagar) de un apartado pendiente
2. Confirma la acción
3. El apartado se marcará como "Pagado"
4. Las estadísticas se actualizarán automáticamente

### Cancelar un Apartado
1. Haz clic en el botón 🚫 (Cancelar)
2. Confirma la cancelación
3. El apartado se marcará como "Cancelado"
4. Esta acción no se puede deshacer

### Crear Nuevo Apartado
1. Haz clic en el botón "+ Nuevo Apartado"
2. (Funcionalidad en desarrollo - se integrará con formularios existentes)

## Estructura de la Base de Datos

### Tabla `apartados`
```sql
CREATE TABLE apartados (
    id_apartado INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_cliente INT,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    anticipo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    fecha_limite DATE NULL,
    estado ENUM('Pendiente','Pagado','Cancelado') NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);
```

### Tabla `detalle_apartados`
```sql
CREATE TABLE detalle_apartados (
    id_detalle_apartado INT PRIMARY KEY AUTO_INCREMENT,
    id_apartado INT,
    id_producto INT,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_apartado) REFERENCES apartados(id_apartado),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);
```

## Colores del Diseño

### Tarjetas de Estadísticas
- **Blanco**: `#FFFFFF` (fondo de tarjetas)
- **Gris**: `#F5F5F5` (fondo general)

### Badges de Estado
- **Rojo**: `#FFEBEE` / `#E53935` (Cancelado)
- **Verde**: `#E8F5E9` / `#4CAF50` (Pagado)
- **Gris**: `#E0E0E0` / `#666666` (Pendiente)

### Colores de Montos
- **Verde**: `#4CAF50` (Anticipo)
- **Naranja**: `#FF9800` (Saldo)
- **Negro**: `#333333` (Total)

### Botones de Acción
- **Azul**: `#2196F3` (Ver)
- **Verde**: `#4CAF50` (Pagar)
- **Rojo**: `#E53935` (Cancelar)
- **Rosa**: `#F06292` (Nuevo Apartado)

## Validaciones Implementadas

1. ✅ **Estado válido**: Solo se puede pagar apartados pendientes
2. ✅ **Confirmación**: Solicita confirmación antes de pagar o cancelar
3. ✅ **Actualización automática**: Recarga datos después de cada acción
4. ✅ **Manejo de errores**: Muestra mensajes claros en caso de error
5. ✅ **Filtros persistentes**: Los filtros se mantienen después de acciones

## Funciones del Controlador

### `listar_apartados()`
Obtiene todos los apartados con información del cliente.

### `obtener_apartado_detalle(id_apartado)`
Obtiene el detalle completo de un apartado incluyendo productos.

### `actualizar_estado_apartado(id_apartado, nuevo_estado)`
Actualiza el estado de un apartado (Pendiente, Pagado, Cancelado).

### `registrar_pago_apartado(id_apartado, monto_pago)`
Registra un pago adicional y actualiza anticipo y saldo.

### `crear_apartado_completo(cliente_id, productos, monto_anticipo, dias_vencimiento)`
Crea un nuevo apartado con sus productos y descuenta el stock.

## Próximas Mejoras Sugeridas

- [ ] Implementar formulario de nuevo apartado integrado
- [ ] Agregar registro de pagos parciales
- [ ] Historial de pagos por apartado
- [ ] Notificaciones de apartados próximos a vencer
- [ ] Impresión de comprobantes de apartado
- [ ] Exportar lista de apartados a Excel/CSV
- [ ] Gráficas de apartados por mes
- [ ] Devolución de productos de apartados cancelados
- [ ] Edición de apartados existentes
- [ ] Búsqueda avanzada con múltiples filtros

## Notas Técnicas

- **Framework**: CustomTkinter (modo light)
- **Resolución recomendada**: 1400x800 o superior
- **Python**: 3.7+
- **Base de datos**: MySQL 5.7+

## Soporte

Si encuentras algún problema:
1. Verifica que las tablas `apartados` y `detalle_apartados` existan
2. Asegúrate de que la tabla `clientes` tenga datos
3. Revisa que la conexión a la base de datos funcione correctamente
4. Ejecuta el script de prueba para verificar la funcionalidad

## Integración con Otros Módulos

### Con Clientes
- Los apartados se vinculan con clientes existentes
- Muestra nombre, teléfono y correo del cliente

### Con Productos
- Los apartados incluyen productos del inventario
- El stock se descuenta al crear el apartado
- Se muestra el detalle de productos en la vista

### Con Ventas
- Los apartados pagados pueden generar ventas
- Se registra el método de pago
- Se actualiza el historial de transacciones
