-- Migración para agregar campo código a productos
USE boutique_db;

-- Agregar columna código si no existe
ALTER TABLE productos 
ADD COLUMN IF NOT EXISTS codigo VARCHAR(50) UNIQUE AFTER id_producto;

-- Generar códigos automáticos para productos existentes sin código
UPDATE productos 
SET codigo = CONCAT(
    CASE 
        WHEN id_categoria = 1 THEN 'VEST-'
        WHEN id_categoria = 2 THEN 'CALZ-'
        WHEN id_categoria = 3 THEN 'ACCE-'
        WHEN id_categoria = 4 THEN 'PIEL-'
        WHEN id_categoria = 5 THEN 'PAPE-'
        WHEN id_categoria = 6 THEN 'DULC-'
        ELSE 'PROD-'
    END,
    LPAD(id_producto, 3, '0')
)
WHERE codigo IS NULL OR codigo = '';

-- Ejemplos de códigos generados:
-- VEST-001 para Vestidos
-- CALZ-001 para Calzado
-- ACCE-001 para Accesorios
-- etc.
