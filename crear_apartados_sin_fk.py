"""
Script para crear tabla apartados sin foreign key primero
"""
from database.db import crear_conexion

def crear_apartados():
    try:
        conn = crear_conexion()
        cur = conn.cursor()
        
        print("🔄 Creando tabla apartados (sin foreign key)...")
        
        # Primero sin foreign key
        cur.execute("""
            CREATE TABLE IF NOT EXISTS apartados (
                id_apartado INT PRIMARY KEY AUTO_INCREMENT,
                fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                id_cliente INT,
                total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                anticipo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                fecha_limite DATE NULL,
                estado ENUM('Pendiente','Pagado','Cancelado') NOT NULL DEFAULT 'Pendiente'
            )
        """)
        print("   ✓ Tabla 'apartados' creada")
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS detalle_apartados (
                id_detalle_apartado INT PRIMARY KEY AUTO_INCREMENT,
                id_apartado INT,
                id_producto INT,
                cantidad INT NOT NULL,
                subtotal DECIMAL(10,2)
            )
        """)
        print("   ✓ Tabla 'detalle_apartados' creada")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Tablas creadas exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    crear_apartados()
