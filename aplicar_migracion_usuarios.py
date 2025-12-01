"""
Script para aplicar la migración de usuarios automáticamente
"""
from database.db import crear_conexion

def aplicar_migracion():
    """Aplicar migración para corregir la tabla usuarios"""
    try:
        conn = crear_conexion()
        cur = conn.cursor()
        
        print("🔄 Aplicando migración de usuarios...")
        print()
        
        # 1. Renombrar columnas existentes
        print("1. Renombrando columnas...")
        try:
            cur.execute("ALTER TABLE usuarios CHANGE COLUMN id id_usuario INT AUTO_INCREMENT")
            print("   ✓ id -> id_usuario")
        except Exception as e:
            if "Unknown column 'id'" in str(e):
                print("   ℹ id_usuario ya existe")
            else:
                print(f"   ⚠ {str(e)}")
        
        try:
            cur.execute("ALTER TABLE usuarios CHANGE COLUMN nombre nombre_completo VARCHAR(100)")
            print("   ✓ nombre -> nombre_completo")
        except Exception as e:
            if "Unknown column 'nombre'" in str(e):
                print("   ℹ nombre_completo ya existe")
            else:
                print(f"   ⚠ {str(e)}")
        
        try:
            cur.execute("ALTER TABLE usuarios CHANGE COLUMN password contraseña VARCHAR(100)")
            print("   ✓ password -> contraseña")
        except Exception as e:
            if "Unknown column 'password'" in str(e):
                print("   ℹ contraseña ya existe")
            else:
                print(f"   ⚠ {str(e)}")
        
        conn.commit()
        print()
        
        # 2. Agregar columnas faltantes
        print("2. Agregando columnas faltantes...")
        
        columnas_agregar = [
            ("email", "ALTER TABLE usuarios ADD COLUMN email VARCHAR(100) AFTER usuario"),
            ("pregunta", "ALTER TABLE usuarios ADD COLUMN pregunta VARCHAR(100) AFTER rol"),
            ("respuesta", "ALTER TABLE usuarios ADD COLUMN respuesta VARCHAR(100) AFTER pregunta"),
            ("activo", "ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE AFTER respuesta")
        ]
        
        for nombre, sql in columnas_agregar:
            try:
                cur.execute(sql)
                print(f"   ✓ Columna '{nombre}' agregada")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print(f"   ℹ Columna '{nombre}' ya existe")
                else:
                    print(f"   ⚠ Error en '{nombre}': {str(e)}")
        
        conn.commit()
        print()
        
        # 3. Actualizar ENUM de rol
        print("3. Actualizando roles...")
        try:
            cur.execute("""
                ALTER TABLE usuarios 
                MODIFY COLUMN rol ENUM('Administrador','Cajero','Empleado','Vendedor') NOT NULL
            """)
            print("   ✓ Roles actualizados")
        except Exception as e:
            print(f"   ⚠ {str(e)}")
        
        conn.commit()
        print()
        
        # 4. Actualizar datos existentes
        print("4. Actualizando datos existentes...")
        
        cur.execute("UPDATE usuarios SET email = CONCAT(usuario, '@rosabici.com') WHERE email IS NULL OR email = ''")
        print(f"   ✓ {cur.rowcount} emails actualizados")
        
        cur.execute("UPDATE usuarios SET activo = TRUE WHERE activo IS NULL")
        print(f"   ✓ {cur.rowcount} estados de activo actualizados")
        
        cur.execute("UPDATE usuarios SET pregunta = 'Color favorito' WHERE usuario = 'admin' AND (pregunta IS NULL OR pregunta = '')")
        cur.execute("UPDATE usuarios SET respuesta = 'rosa' WHERE usuario = 'admin' AND (respuesta IS NULL OR respuesta = '')")
        print("   ✓ Pregunta de seguridad del admin configurada")
        
        conn.commit()
        print()
        
        # 5. Verificar resultado
        print("5. Verificando resultado...")
        cur.execute("SELECT id_usuario, usuario, nombre_completo, email, rol, activo FROM usuarios")
        usuarios = cur.fetchall()
        
        print(f"   ✓ {len(usuarios)} usuarios en la base de datos:")
        for u in usuarios:
            print(f"      - ID: {u[0]}, Usuario: {u[1]}, Nombre: {u[2]}, Email: {u[3]}, Rol: {u[4]}, Activo: {u[5]}")
        
        conn.close()
        
        print()
        print("=" * 60)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ ERROR EN LA MIGRACIÓN: {str(e)}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRACIÓN DE TABLA USUARIOS - Janet Rosa Bici")
    print("=" * 60)
    print()
    
    aplicar_migracion()
