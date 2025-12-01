-- Migración para agregar campos al formulario de nuevo usuario
USE boutique_db;

-- Agregar columnas nuevas a la tabla usuarios
ALTER TABLE usuarios 
ADD COLUMN nombre_completo VARCHAR(100) AFTER id_usuario,
ADD COLUMN email VARCHAR(100) AFTER usuario,
ADD COLUMN activo BOOLEAN DEFAULT TRUE AFTER respuesta;

-- Actualizar el ENUM de rol para incluir "Vendedor"
ALTER TABLE usuarios 
MODIFY COLUMN rol ENUM('Administrador','Cajero','Empleado','Vendedor') NOT NULL;

-- Actualizar usuarios existentes con valores por defecto
UPDATE usuarios SET nombre_completo = 'Administrador' WHERE usuario = 'admin';
UPDATE usuarios SET nombre_completo = 'Cajero 1' WHERE usuario = 'cajero1';
UPDATE usuarios SET nombre_completo = 'Empleado 1' WHERE usuario = 'empleado1';

UPDATE usuarios SET email = CONCAT(usuario, '@rosabici.com') WHERE email IS NULL;
UPDATE usuarios SET activo = TRUE WHERE activo IS NULL;
