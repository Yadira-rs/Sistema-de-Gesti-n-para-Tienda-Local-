"""
Script para actualizar la tabla de clientes con campos separados
Nombre, Apellido Paterno y Apellido Materno
Janet Rosa Bici - Sistema de Ventas
"""

from database.db import crear_conexion
from tkinter import messagebox
import tkinter as tk

def actualizar_tabla_clientes():
    """Actualizar tabla de clientes con nuevos campos"""
    try:
        conn = crear_conexion()
        if not conn:
            print("❌ No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor()
        
        print("🔄 Actualizando tabla de clientes...")
        
        # 1. Agregar nuevas columnas con tipos de datos correctos
        print("📝 Agregando columnas con tipos de datos apropiados...")
        
        try:
            cursor.execute("""
                ALTER TABLE clientes 
                ADD COLUMN nombre_cliente VARCHAR(50) NOT NULL DEFAULT '' 
                COMMENT 'Nombre(s) del cliente' 
                AFTER nombre
            """)
            print("✅ Columna 'nombre_cliente' agregada (VARCHAR(50))")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("ℹ️  Columna 'nombre_cliente' ya existe")
            else:
                print(f"⚠️  Error al agregar 'nombre_cliente': {e}")
        
        try:
            cursor.execute("""
                ALTER TABLE clientes 
                ADD COLUMN apellido_paterno VARCHAR(50) NOT NULL DEFAULT '' 
                COMMENT 'Apellido paterno del cliente' 
                AFTER nombre_cliente
            """)
            print("✅ Columna 'apellido_paterno' agregada (VARCHAR(50))")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("ℹ️  Columna 'apellido_paterno' ya existe")
            else:
                print(f"⚠️  Error al agregar 'apellido_paterno': {e}")
        
        try:
            cursor.execute("""
                ALTER TABLE clientes 
                ADD COLUMN apellido_materno VARCHAR(50) NOT NULL DEFAULT '' 
                COMMENT 'Apellido materno del cliente' 
                AFTER apellido_paterno
            """)
            print("✅ Columna 'apellido_materno' agregada (VARCHAR(50))")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("ℹ️  Columna 'apellido_materno' ya existe")
            else:
                print(f"⚠️  Error al agregar 'apellido_materno': {e}")
        
        conn.commit()
        
        # 1.5 Optimizar tipos de datos de otros campos
        print("\n🔧 Optimizando tipos de datos de otros campos...")
        
        try:
            cursor.execute("""
                ALTER TABLE clientes 
                MODIFY COLUMN telefono VARCHAR(15) NOT NULL 
                COMMENT 'Teléfono del cliente (10 dígitos)'
            """)
            print("✅ Campo 'telefono' optimizado (VARCHAR(15))")
        except Exception as e:
            print(f"ℹ️  Campo 'telefono': {e}")
        
        try:
            cursor.execute("""
                ALTER TABLE clientes 
                MODIFY COLUMN correo VARCHAR(100) DEFAULT NULL 
                COMMENT 'Correo electrónico del cliente'
            """)
            print("✅ Campo 'correo' optimizado (VARCHAR(100))")
        except Exception as e:
            print(f"ℹ️  Campo 'correo': {e}")
        
        try:
            cursor.execute("""
                ALTER TABLE clientes 
                MODIFY COLUMN nombre VARCHAR(150) NOT NULL 
                COMMENT 'Nombre completo del cliente (legacy)'
            """)
            print("✅ Campo 'nombre' optimizado (VARCHAR(150))")
        except Exception as e:
            print(f"ℹ️  Campo 'nombre': {e}")
        
        conn.commit()
        
        # 2. Migrar datos existentes
        print("\n🔄 Migrando datos existentes...")
        cursor.execute("""
            UPDATE clientes 
            SET 
                nombre_cliente = TRIM(SUBSTRING_INDEX(nombre, ' ', 1)),
                apellido_paterno = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(nombre, ' ', 2), ' ', -1)),
                apellido_materno = TRIM(CASE 
                    WHEN LENGTH(nombre) - LENGTH(REPLACE(nombre, ' ', '')) >= 2 
                    THEN SUBSTRING_INDEX(nombre, ' ', -1)
                    ELSE ''
                END)
            WHERE (nombre_cliente IS NULL OR nombre_cliente = '') AND nombre IS NOT NULL AND nombre != ''
        """)
        
        filas_actualizadas = cursor.rowcount
        conn.commit()
        
        print(f"✅ {filas_actualizadas} clientes actualizados")
        
        # 2.5 Limpiar espacios en blanco
        print("\n🧹 Limpiando espacios en blanco...")
        cursor.execute("""
            UPDATE clientes 
            SET 
                nombre_cliente = TRIM(nombre_cliente),
                apellido_paterno = TRIM(apellido_paterno),
                apellido_materno = TRIM(apellido_materno),
                telefono = TRIM(telefono),
                correo = TRIM(correo)
        """)
        conn.commit()
        print("✅ Datos limpiados")
        
        # 3. Crear índices para mejorar búsquedas
        print("\n📊 Creando índices para mejorar búsquedas...")
        
        try:
            cursor.execute("CREATE INDEX idx_nombre_cliente ON clientes(nombre_cliente)")
            print("✅ Índice 'idx_nombre_cliente' creado")
        except Exception as e:
            if "Duplicate key name" in str(e):
                print("ℹ️  Índice 'idx_nombre_cliente' ya existe")
            else:
                print(f"⚠️  Error al crear índice: {e}")
        
        try:
            cursor.execute("CREATE INDEX idx_apellido_paterno ON clientes(apellido_paterno)")
            print("✅ Índice 'idx_apellido_paterno' creado")
        except Exception as e:
            if "Duplicate key name" in str(e):
                print("ℹ️  Índice 'idx_apellido_paterno' ya existe")
            else:
                print(f"⚠️  Error al crear índice: {e}")
        
        try:
            cursor.execute("CREATE INDEX idx_apellido_materno ON clientes(apellido_materno)")
            print("✅ Índice 'idx_apellido_materno' creado")
        except Exception as e:
            if "Duplicate key name" in str(e):
                print("ℹ️  Índice 'idx_apellido_materno' ya existe")
            else:
                print(f"⚠️  Error al crear índice: {e}")
        
        conn.commit()
        
        # 4. Verificar estructura de la tabla
        print("\n📋 Estructura de la tabla clientes:")
        cursor.execute("DESCRIBE clientes")
        columnas = cursor.fetchall()
        print("-" * 80)
        print(f"{'Campo':<25} {'Tipo':<20} {'Nulo':<8} {'Comentario':<30}")
        print("-" * 80)
        for col in columnas:
            campo = col[0]
            tipo = col[1]
            nulo = col[2]
            print(f"{campo:<25} {tipo:<20} {nulo:<8}")
        print("-" * 80)
        
        # 5. Verificar resultados de migración
        print("\n📊 Verificando datos migrados...")
        cursor.execute("""
            SELECT 
                id_cliente,
                nombre as nombre_completo,
                nombre_cliente,
                apellido_paterno,
                apellido_materno,
                telefono
            FROM clientes
            ORDER BY id_cliente
            LIMIT 5
        """)
        
        resultados = cursor.fetchall()
        print("\nPrimeros 5 clientes:")
        print("-" * 100)
        for cliente in resultados:
            print(f"ID: {cliente[0]}")
            print(f"  Nombre completo (original): {cliente[1]}")
            print(f"  Nombre: {cliente[2]}")
            print(f"  Apellido Paterno: {cliente[3]}")
            print(f"  Apellido Materno: {cliente[4]}")
            print(f"  Teléfono: {cliente[5]}")
            print(f"  Reconstruido: {cliente[2]} {cliente[3]} {cliente[4]}")
            print("-" * 100)
        
        # 6. Estadísticas
        print("\n📈 Estadísticas de la migración:")
        cursor.execute("""
            SELECT 
                COUNT(*) as total_clientes,
                SUM(CASE WHEN nombre_cliente != '' THEN 1 ELSE 0 END) as con_nombre,
                SUM(CASE WHEN apellido_paterno != '' THEN 1 ELSE 0 END) as con_apellido_paterno,
                SUM(CASE WHEN apellido_materno != '' THEN 1 ELSE 0 END) as con_apellido_materno
            FROM clientes
        """)
        stats = cursor.fetchone()
        print(f"  Total de clientes: {stats[0]}")
        print(f"  Con nombre: {stats[1]}")
        print(f"  Con apellido paterno: {stats[2]}")
        print(f"  Con apellido materno: {stats[3]}")
        
        conn.close()
        
        print("\n✅ ¡Actualización completada exitosamente!")
        print("\n💡 Ahora puedes buscar clientes por:")
        print("   - Nombre")
        print("   - Apellido Paterno")
        print("   - Apellido Materno")
        print("   - Teléfono")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la actualización: {e}")
        return False

def mostrar_dialogo_confirmacion():
    """Mostrar diálogo de confirmación antes de actualizar"""
    root = tk.Tk()
    root.withdraw()
    
    respuesta = messagebox.askyesno(
        "Actualizar Base de Datos",
        "¿Deseas actualizar la tabla de clientes?\n\n"
        "Se agregarán los campos:\n"
        "• Nombre\n"
        "• Apellido Paterno\n"
        "• Apellido Materno\n\n"
        "Los datos existentes se migrarán automáticamente.\n\n"
        "¿Continuar?"
    )
    
    if respuesta:
        if actualizar_tabla_clientes():
            messagebox.showinfo(
                "Éxito",
                "✅ Base de datos actualizada correctamente\n\n"
                "Ahora puedes buscar clientes por nombre, apellidos y teléfono."
            )
        else:
            messagebox.showerror(
                "Error",
                "❌ No se pudo actualizar la base de datos\n\n"
                "Revisa la consola para más detalles."
            )
    
    root.destroy()

if __name__ == "__main__":
    print("=" * 80)
    print("ACTUALIZACIÓN DE BASE DE DATOS - CLIENTES")
    print("Janet Rosa Bici - Sistema de Ventas")
    print("=" * 80)
    print()
    
    mostrar_dialogo_confirmacion()
