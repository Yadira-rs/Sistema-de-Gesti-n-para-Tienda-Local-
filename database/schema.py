
import sqlite3
import os

DB_NAME = "boutique.db"

def init_db():
    """Inicializa la base de datos SQLite con las tablas requeridas."""
    if os.path.exists(DB_NAME):
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT,
        usuario TEXT UNIQUE,
        email TEXT,
        contraseña TEXT,
        rol TEXT DEFAULT 'Vendedor',
        activo BOOLEAN DEFAULT 1,
        pregunta TEXT,
        respuesta TEXT
    )
    """)
    
    # Insertar usuario admin por defecto
    cursor.execute("""
    INSERT OR IGNORE INTO usuarios (nombre_completo, usuario, email, contraseña, rol, activo)
    VALUES ('Administrador', 'admin', 'admin@boutique.com', 'admin123', 'Administrador', 1)
    """)
    
    # Tabla clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        telefono TEXT,
        email TEXT,
        nombre_cliente TEXT,
        apellido_paterno TEXT,
        apellido_materno TEXT
    )
    """)
    
    # Tabla productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        codigo_barras TEXT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL,
        stock INTEGER,
        imagen_url TEXT,
        id_categoria INTEGER,
        marca TEXT,
        tipo TEXT
    )
    """)
    
    # Tabla ventas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_usuario INTEGER,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        total REAL,
        metodo_pago TEXT,
        descuento REAL
    )
    """)
    
    # Tabla detalle_ventas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_ventas (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER,
        id_producto INTEGER,
        cantidad INTEGER,
        precio_unitario REAL,
        subtotal REAL,
        FOREIGN KEY(id_venta) REFERENCES ventas(id_venta),
        FOREIGN KEY(id_producto) REFERENCES productos(id_producto)
    )
    """)
    
    # Tabla creditos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS creditos (
        id_credito INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER,
        id_cliente INTEGER,
        fecha_credito DATETIME DEFAULT CURRENT_TIMESTAMP,
        monto_total REAL DEFAULT 0,
        monto_pagado REAL DEFAULT 0,
        saldo_pendiente REAL DEFAULT 0,
        plazo_dias INTEGER,
        fecha_vencimiento DATETIME,
        estado TEXT,
        notas TEXT,
        tasa_interes REAL DEFAULT 0,
        FOREIGN KEY(id_venta) REFERENCES ventas(id_venta),
        FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente)
    )
    """)
    
    # Tabla apartados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS apartados (
        id_apartado INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        total REAL,
        anticipo REAL,
        saldo REAL,
        fecha_limite DATETIME,
        estado TEXT,
        FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente)
    )
    """)

    # Tabla detalle_apartados (inferred needed for apartados logic)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_apartados (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        id_apartado INTEGER,
        id_producto INTEGER,
        cantidad INTEGER,
        precio_unitario REAL,
        FOREIGN KEY(id_apartado) REFERENCES apartados(id_apartado),
        FOREIGN KEY(id_producto) REFERENCES productos(id_producto)
    )
    """)
    
    conn.commit()
    conn.close()
