-- Migración para agregar código de barras único a productos
USE boutique_db;

-- Agregar columna código de barras si no existe
ALTER TABLE productos 
ADD COLUMN IF NOT EXISTS codigo_barras VARCHAR(100) UNIQUE AFTER codigo;

-- Generar códigos de barras automáticos para productos existentes sin código de barras
-- Formato: EAN-13 simulado (13 dígitos)
UPDATE productos 
SET codigo_barras = CONCAT(
    '750', -- Prefijo de empresa
    LPAD(id_categoria, 2, '0'), -- Categoría (2 dígitos)
    LPAD(id_producto, 6, '0'), -- ID producto (6 dígitos)
    LPAD(FLOOR(RAND() * 100), 2, '0') -- Dígitos de control (2 dígitos)
)
WHERE codigo_barras IS NULL OR codigo_barras = '';

-- Ejemplos de códigos generados:
-- 7500100000101 para producto 1 de categoría 1
-- 7500200000201 para producto 1 de categoría 2
-- etc.

-- Crear índice para búsqueda rápida por código de barras
CREATE INDEX idx_codigo_barras ON productos(codigo_barras);
