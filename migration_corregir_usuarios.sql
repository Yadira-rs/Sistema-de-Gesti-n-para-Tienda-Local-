-- Migración para corregir la estructura de la tabla usuarios
USE boutique_db;

-- Renombrar columnas existentes
ALTER TABLE usuarios CHANGE COLUMN id id_usuario INT AUTO_INCREMENT;
ALTER TABLE usuarios CHANGE COLUMN nombre nombre_completo VARCHAR(100);
ALTER TABLE usuarios CHANGE COLUMN password contraseña VARCHAR(100);

-- Agregar columnas faltantes
ALTER TABLE usuarios ADD COLUMN email VARCHAR(100) AFTER usuario;
ALTER TABLE usuarios ADD COLUMN pregunta VARCHAR(100) AFTER rol;
ALTER TABLE usuarios ADD COLUMN respuesta VARCHAR(100) AFTER pregunta;
ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE AFTER respuesta;

-- Actualizar el ENUM de rol para incluir "Vendedor" y "Empleado"
ALTER TABLE usuarios 
MODIFY COLUMN rol ENUM('Administrador','Cajero','Empleado','Vendedor') NOT NULL;

-- Actualizar usuarios existentes con valores por defecto
UPDATE usuarios SET email = CONCAT(usuario, '@rosabici.com') WHERE email IS NULL OR email = '';
UPDATE usuarios SET activo = TRUE WHERE activo IS NULL;
UPDATE usuarios SET pregunta = 'Color favorito' WHERE usuario = 'admin' AND (pregunta IS NULL OR pregunta = '');
UPDATE usuarios SET respuesta = 'rosa' WHERE usuario = 'admin' AND (respuesta IS NULL OR respuesta = '');

-- Mostrar resultado
SELECT 'Migración completada exitosamente' AS mensaje;
SELECT * FROM usuarios;
