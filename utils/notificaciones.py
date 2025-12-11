# utils/notificaciones.py
"""
Sistema de notificaciones para actualizar vistas automáticamente
"""

# Variable global para mantener referencia a la aplicación principal
_app_principal = None

def registrar_app_principal(app):
    """Registrar la aplicación principal para notificaciones"""
    global _app_principal
    _app_principal = app

def notificar_nueva_venta():
    """Notificar que se ha realizado una nueva venta"""
    global _app_principal
    
    if _app_principal and hasattr(_app_principal, 'current_view'):
        try:
            # Si la vista actual es el historial de ventas, actualizarla
            if hasattr(_app_principal.current_view, 'cargar_ventas'):
                _app_principal.current_view.cargar_ventas()
                print("✓ Historial de ventas actualizado automáticamente")
            
            # También actualizar el dashboard si está abierto
            if hasattr(_app_principal.current_view, 'actualizar_estadisticas'):
                _app_principal.current_view.actualizar_estadisticas()
                print("✓ Dashboard actualizado automáticamente")
                
        except Exception as e:
            print(f"Nota: No se pudo actualizar automáticamente: {e}")

def notificar_nuevo_producto():
    """Notificar que se ha agregado un nuevo producto"""
    global _app_principal
    
    if _app_principal and hasattr(_app_principal, 'current_view'):
        try:
            # Si la vista actual es productos, actualizarla
            if hasattr(_app_principal.current_view, 'cargar_tabla_productos'):
                _app_principal.current_view.cargar_tabla_productos()
                print("✓ Lista de productos actualizada automáticamente")
                
        except Exception as e:
            print(f"Nota: No se pudo actualizar productos automáticamente: {e}")

def notificar_nuevo_apartado():
    """Notificar que se ha creado un nuevo apartado"""
    global _app_principal
    
    if _app_principal and hasattr(_app_principal, 'current_view'):
        try:
            # Si la vista actual es apartados, actualizarla
            if hasattr(_app_principal.current_view, 'cargar_datos'):
                _app_principal.current_view.cargar_datos()
                print("✓ Lista de apartados actualizada automáticamente")
                
        except Exception as e:
            print(f"Nota: No se pudo actualizar apartados automáticamente: {e}")

def notificar_nuevo_usuario():
    """Notificar que se ha creado un nuevo usuario"""
    global _app_principal
    
    if _app_principal and hasattr(_app_principal, 'current_view'):
        try:
            # Si la vista actual es usuarios, actualizarla
            if hasattr(_app_principal.current_view, 'cargar_usuarios'):
                _app_principal.current_view.cargar_usuarios()
                print("✓ Lista de usuarios actualizada automáticamente")
                
        except Exception as e:
            print(f"Nota: No se pudo actualizar usuarios automáticamente: {e}")