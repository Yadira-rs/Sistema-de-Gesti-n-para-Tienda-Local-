"""
Script para crear tablas faltantes en la base de datos
"""
from database.db import crear_conexion

def crear_tabla_apartados():
    """Crear tabla apartados y detalle_apartados"""
    try:
        conn = crear_conexion()
        cur = conn.cursor()
        
        print("🔄 Creando tabla apartados...")
        
        # Crear tabla apartados
        cur.execute("""
            CREATE TABLE IF NOT EXISTS apartados (
                id_apartado INT PRIMARY KEY AUTO_INCREMENT,
                fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                id_cliente INT,
                total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                anticipo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                fecha_limite DATE NULL,
                estado ENUM('Pendiente','Pagado','Cancelado') NOT NULL DEFAULT 'Pendiente',
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
            )
        """)
        print("   ✓ Tabla 'apartados' creada")
        
        # Crear tabla detalle_apartados
        cur.execute("""
            CREATE TABLE IF NOT EXISTS detalle_apartados (
                id_detalle_apartado INT PRIMARY KEY AUTO_INCREMENT,
                id_apartado INT,
                id_producto INT,
                cantidad INT NOT NULL,
                subtotal DECIMAL(10,2),
                FOREIGN KEY (id_apartado) REFERENCES apartados(id_apartado),
                FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
            )
        """)
        print("   ✓ Tabla 'detalle_apartados' creada")
        
        conn.commit()
        conn.close()
        
        print()
        print("✅ Tablas de apartados creadas exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def crear_tabla_creditos():
    """Crear tabla creditos"""
    try:
        conn = crear_conexion()
        cur = conn.cursor()
        
        print("🔄 Creando tabla creditos...")
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS creditos (
                id_credito INT PRIMARY KEY AUTO_INCREMENT,
                fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                id_cliente INT,
                total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                abonado DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                fecha_limite DATE NULL,
                estado ENUM('Activo','Pagado','Vencido') NOT NULL DEFAULT 'Activo',
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
            )
        """)
        print("   ✓ Tabla 'creditos' creada")
        
        conn.commit()
        conn.close()
        
        print()
        print("✅ Tabla de créditos creada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("CREAR TABLAS FALTANTES - Janet Rosa Bici")
    print("=" * 60)
    print()
    
    crear_tabla_apartados()
    print()
    crear_tabla_creditos()
    
    print()
    print("=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
