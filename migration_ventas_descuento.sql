-- Migración para agregar campos de descuento a las ventas
USE boutique_db;

-- Agregar columnas de descuento a la tabla ventas
ALTER TABLE ventas 
ADD COLUMN descuento_porcentaje DECIMAL(5,2) DEFAULT 0.00 AFTER total,
ADD COLUMN descuento_monto DECIMAL(10,2) DEFAULT 0.00 AFTER descuento_porcentaje,
ADD COLUMN subtotal DECIMAL(10,2) DEFAULT 0.00 AFTER metodo_pago;

-- Actualizar ventas existentes
UPDATE ventas SET subtotal = total, descuento_porcentaje = 0, descuento_monto = 0 WHERE subtotal = 0;
