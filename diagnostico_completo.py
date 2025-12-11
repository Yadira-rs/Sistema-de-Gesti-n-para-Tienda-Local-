#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico completo del sistema Janet Rosa Bici
"""

import os
import sys
import json
import mysql.connector
from datetime import datetime

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    print("🔍 VERIFICANDO ARCHIVOS NECESARIOS...")
    
    archivos_criticos = [
        'app.py',
        'config_db.json',
        'views/login.py',
        'views/main.py',
        'controllers/users.py'
    ]
    
    todos_ok = True
    for archivo in archivos_criticos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print("\n🔍 VERIFICANDO DEPENDENCIAS...")
    
    dependencias = [
        'tkinter',
        'mysql.connector',
        'pandas',
        'PIL',
        'reportlab'
    ]
    
    todos_ok = True
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NO INSTALADO")
            todos_ok = False
    
    return todos_ok

def verificar_mysql():
    """Verifica la conexión a MySQL"""
    print("\n🔍 VERIFICANDO MYSQL...")
    
    try:
        # Leer configuración
        with open('config_db.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ Configuración leída")
        
        # Probar conexión
        conn = mysql.connector.connect(**config)
        print(f"✅ Conexión a MySQL exitosa")
        
        # Verificar base de datos
        cursor = conn.cursor()
        cursor.execute("USE boutique_db")
        print(f"✅ Base de datos 'boutique_db' accesible")
        
        # Verificar tablas principales
        tablas = ['usuarios', 'productos', 'clientes', 'ventas']
        for tabla in tablas:
            cursor.execute(f"SHOW TABLES LIKE '{tabla}'")
            if cursor.fetchone():
                print(f"✅ Tabla '{tabla}' existe")
            else:
                print(f"⚠️ Tabla '{tabla}' no existe")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error con MySQL: {e}")
        return False

def verificar_usuario_admin():
    """Verifica que existe el usuario administrador"""
    print("\n🔍 VERIFICANDO USUARIO ADMINISTRADOR...")
    
    try:
        with open('config_db.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE email = 'admin@janetrosabici.com'")
        usuario = cursor.fetchone()
        
        if usuario:
            print(f"✅ Usuario administrador existe")
            print(f"   Email: admin@janetrosabici.com")
            print(f"   ID: {usuario[0]}")
        else:
            print(f"❌ Usuario administrador NO existe")
            print(f"   Creando usuario administrador...")
            
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, password, rol) 
                VALUES ('Administrador', 'admin@janetrosabici.com', 'admin123', 'admin')
            """)
            conn.commit()
            print(f"✅ Usuario administrador creado")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando usuario: {e}")
        return False

def probar_aplicacion():
    """Intenta importar y probar componentes de la aplicación"""
    print("\n🔍 PROBANDO COMPONENTES DE LA APLICACIÓN...")
    
    try:
        # Probar importación de app principal
        sys.path.append('.')
        import app
        print(f"✅ app.py se puede importar")
        
        # Probar importación de views
        from views import login
        print(f"✅ views.login se puede importar")
        
        # Probar importación de controllers
        from controllers import users
        print(f"✅ controllers.users se puede importar")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importando componentes: {e}")
        return False

def generar_reporte():
    """Genera un reporte completo del diagnóstico"""
    print("\n" + "="*60)
    print("📊 REPORTE DE DIAGNÓSTICO")
    print("="*60)
    
    archivos_ok = verificar_archivos()
    deps_ok = verificar_dependencias()
    mysql_ok = verificar_mysql()
    usuario_ok = verificar_usuario_admin()
    app_ok = probar_aplicacion()
    
    print(f"\n📋 RESUMEN:")
    print(f"   Archivos: {'✅' if archivos_ok else '❌'}")
    print(f"   Dependencias: {'✅' if deps_ok else '❌'}")
    print(f"   MySQL: {'✅' if mysql_ok else '❌'}")
    print(f"   Usuario Admin: {'✅' if usuario_ok else '❌'}")
    print(f"   Aplicación: {'✅' if app_ok else '❌'}")
    
    if all([archivos_ok, deps_ok, mysql_ok, usuario_ok, app_ok]):
        print(f"\n🎉 DIAGNÓSTICO: TODO FUNCIONAL")
        print(f"   Su aplicación debería funcionar correctamente")
        print(f"   Ejecute: python app.py")
        print(f"   Login: admin@janetrosabici.com / admin123")
    else:
        print(f"\n⚠️ DIAGNÓSTICO: PROBLEMAS ENCONTRADOS")
        print(f"   Revise los errores marcados con ❌")
    
    return all([archivos_ok, deps_ok, mysql_ok, usuario_ok, app_ok])

if __name__ == "__main__":
    print("🔧 DIAGNÓSTICO COMPLETO - JANET ROSA BICI")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    generar_reporte()