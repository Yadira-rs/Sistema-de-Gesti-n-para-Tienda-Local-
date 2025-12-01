"""
Script de prueba para la pantalla de Punto de Venta
Ejecuta este archivo para probar el punto de venta independientemente
"""
import customtkinter as ctk
from views.punto_venta_view import PuntoVentaView

if __name__ == "__main__":
    # Usuario de prueba
    usuario = {
        "id_usuario": 1,
        "nombre_completo": "Administrador",
        "email": "admin@rosabici.com",
        "rol": "Administrador"
    }
    
    app = PuntoVentaView(usuario=usuario)
    app.mainloop()
