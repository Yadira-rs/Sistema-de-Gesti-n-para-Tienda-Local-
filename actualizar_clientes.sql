-- ============================================================================
-- Script para actualizar la tabla de clientes con tipos de datos correctos
-- Janet Rosa Bici - Sistema de Ventas
-- ============================================================================

-- 1. AGREGAR NUEVAS COLUMNAS CON TIPOS DE DATOS APROPIADOS
-- ============================================================================

-- Nombre del cliente (solo el primer nombre)
ALTER TABLE clientes 
ADD COLUMN IF NOT EXISTS nombre_cliente VARCHAR(50) NOT NULL DEFAULT '' 
COMMENT 'Nombre(s) del cliente' 
AFTER nombre;

-- Apellido paterno
ALTER TABLE clientes 
ADD COLUMN IF NOT EXISTS apellido_paterno VARCHAR(50) NOT NULL DEFAULT '' 
COMMENT 'Apellido paterno del cliente' 
AFTER nombre_cliente;

-- Apellido materno
ALTER TABLE clientes 
ADD COLUMN IF NOT EXISTS apellido_materno VARCHAR(50) NOT NULL DEFAULT '' 
COMMENT 'Apellido materno del cliente' 
AFTER apellido_paterno;

-- 2. OPTIMIZAR OTROS CAMPOS DE LA TABLA CLIENTES
-- ============================================================================

-- Asegurar que el teléfono tenga el tipo correcto (VARCHAR para mantener formato)
ALTER TABLE clientes 
MODIFY COLUMN telefono VARCHAR(15) NOT NULL 
COMMENT 'Teléfono del cliente (10 dígitos)';

-- Asegurar que el correo tenga el tipo correcto
ALTER TABLE clientes 
MODIFY COLUMN correo VARCHAR(100) DEFAULT NULL 
COMMENT 'Correo electrónico del cliente';

-- Asegurar que el nombre completo original se mantenga
ALTER TABLE clientes 
MODIFY COLUMN nombre VARCHAR(150) NOT NULL 
COMMENT 'Nombre completo del cliente (legacy)';

-- 3. MIGRAR DATOS EXISTENTES
-- ============================================================================

-- Dividir el nombre completo en partes
UPDATE clientes 
SET 
    nombre_cliente = TRIM(SUBSTRING_INDEX(nombre, ' ', 1)),
    apellido_paterno = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(nombre, ' ', 2), ' ', -1)),
    apellido_materno = TRIM(CASE 
        WHEN LENGTH(nombre) - LENGTH(REPLACE(nombre, ' ', '')) >= 2 
        THEN SUBSTRING_INDEX(nombre, ' ', -1)
        ELSE ''
    END)
WHERE (nombre_cliente IS NULL OR nombre_cliente = '') AND nombre IS NOT NULL AND nombre != '';

-- Limpiar espacios en blanco
UPDATE clientes 
SET 
    nombre_cliente = TRIM(nombre_cliente),
    apellido_paterno = TRIM(apellido_paterno),
    apellido_materno = TRIM(apellido_materno),
    telefono = TRIM(telefono),
    correo = TRIM(correo);

-- 4. AGREGAR ÍNDICES PARA MEJORAR BÚSQUEDAS
-- ============================================================================

-- Índice para búsqueda por nombre
CREATE INDEX IF NOT EXISTS idx_nombre_cliente ON clientes(nombre_cliente);

-- Índice para búsqueda por apellido paterno
CREATE INDEX IF NOT EXISTS idx_apellido_paterno ON clientes(apellido_paterno);

-- Índice para búsqueda por apellido materno
CREATE INDEX IF NOT EXISTS idx_apellido_materno ON clientes(apellido_materno);

-- Índice para búsqueda por teléfono (ya debería existir como UNIQUE)
CREATE UNIQUE INDEX IF NOT EXISTS idx_telefono ON clientes(telefono);

-- 5. VERIFICAR ESTRUCTURA DE LA TABLA
-- ============================================================================

DESCRIBE clientes;

-- 6. VERIFICAR DATOS MIGRADOS
-- ============================================================================

SELECT 
    id_cliente,
    nombre as nombre_completo_original,
    nombre_cliente,
    apellido_paterno,
    apellido_materno,
    telefono,
    correo,
    CONCAT_WS(' ', nombre_cliente, apellido_paterno, apellido_materno) as nombre_reconstruido
FROM clientes
ORDER BY id_cliente
LIMIT 10;

-- 7. ESTADÍSTICAS DE LA MIGRACIÓN
-- ============================================================================

SELECT 
    COUNT(*) as total_clientes,
    SUM(CASE WHEN nombre_cliente != '' THEN 1 ELSE 0 END) as con_nombre,
    SUM(CASE WHEN apellido_paterno != '' THEN 1 ELSE 0 END) as con_apellido_paterno,
    SUM(CASE WHEN apellido_materno != '' THEN 1 ELSE 0 END) as con_apellido_materno
FROM clientes;

-- ============================================================================
-- NOTAS IMPORTANTES:
-- ============================================================================
-- 
-- TIPOS DE DATOS UTILIZADOS:
-- - VARCHAR(50): Para nombres y apellidos (suficiente para nombres mexicanos)
-- - VARCHAR(15): Para teléfonos (formato: +52 XXX XXX XXXX)
-- - VARCHAR(100): Para correos electrónicos
-- - VARCHAR(150): Para nombre completo legacy
--
-- ÍNDICES CREADOS:
-- - Mejoran la velocidad de búsqueda por nombre y apellidos
-- - El índice UNIQUE en teléfono evita duplicados
--
-- COMPATIBILIDAD:
-- - El campo 'nombre' original se mantiene para compatibilidad
-- - Los nuevos campos tienen valores por defecto
-- - No se pierden datos en la migración
--
-- ============================================================================
