"""
Script de prueba para el Punto de Venta modernizado
"""
import sys
sys.path.append('.')

from views.punto_venta_view import PuntoVentaView

if __name__ == "__main__":
    # Usuario de prueba
    usuario = {
        "id_usuario": 1,
        "nombre_completo": "Administrador",
        "email": "admin@janet.com"
    }
    
    print("🚀 Iniciando Punto de Venta Moderno...")
    print("✨ Diseño actualizado según la imagen de referencia")
    print("📦 Sin imágenes de productos (solo iconos)")
    print("🎨 Colores rosa (#E91E63) y diseño limpio")
    print("\n")
    
    app = PuntoVentaView(usuario=usuario)
    app.mainloop()
