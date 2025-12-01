-- Crear Base de Datos
CREATE DATABASE IF NOT EXISTS boutique_db;
USE boutique_db;

-- Tabla Usuarios
CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contraseña VARCHAR(100) NOT NULL,
    rol ENUM('Administrador','Cajero','Empleado') NOT NULL,
    pregunta VARCHAR(100),
    respuesta VARCHAR(100)
);

INSERT INTO usuarios (usuario, contraseña, rol, pregunta, respuesta) VALUES
('admin', '1234', 'Administrador', 'Color favorito', 'rosa'),
('cajero1', '1234', 'Cajero', NULL, NULL),
('empleado1', '1234', 'Empleado', NULL, NULL);

-- Tabla Clientes
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    correo VARCHAR(100),
    telefono VARCHAR(20)
);

INSERT INTO clientes (nombre, correo, telefono) VALUES
('Cliente General', 'general@correo.com', '0000000000');

CREATE TABLE categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(50) UNIQUE,
    codigo_barras VARCHAR(100) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(200),
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    id_categoria INT,
    imagen_url VARCHAR(255),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    INDEX idx_codigo_barras (codigo_barras)
);

INSERT INTO categorias (nombre) VALUES
('Ropa'), ('Calzado'), ('Accesorios'), ('Cuidado de la piel'), ('Papelería'), ('Dulcería'), ('Otros');

INSERT INTO productos (codigo, codigo_barras, nombre, descripcion, precio, stock, id_categoria) VALUES
('BLUS-001', '7500100000101', 'Blusa Rosa', 'Blusa talla única', 199.00, 20, 1),
('PANT-001', '7500100000201', 'Pantalón Negro', 'Pantalón dama talla M', 299.00, 15, 1),
('VEST-001', '7500100000301', 'Vestido Casual', 'Vestido color azul', 399.00, 10, 1),
('CALZ-001', '7500200000101', 'Tenis Blancos', 'Tenis unisex', 499.00, 12, 2),
('ACCE-001', '7500300000101', 'Bolsa de Mano', 'Bolsa cuero sintético', 250.00, 25, 3);

-- Tabla Ventas
CREATE TABLE ventas (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_cliente INT,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    descuento_porcentaje DECIMAL(5,2) DEFAULT 0.00,
    descuento_monto DECIMAL(10,2) DEFAULT 0.00,
    metodo_pago VARCHAR(20),
    subtotal DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Tabla Detalle Ventas
CREATE TABLE detalle_ventas (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_venta INT,
    id_producto INT,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla Apartados
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

CREATE TABLE detalle_apartados (
    id_detalle_apartado INT PRIMARY KEY AUTO_INCREMENT,
    id_apartado INT,
    id_producto INT,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_apartado) REFERENCES apartados(id_apartado),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Movimientos de Inventario
CREATE TABLE movimientos_inventario (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT,
    tipo ENUM('Entrada','Salida','Ajuste') NOT NULL,
    cantidad INT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);
