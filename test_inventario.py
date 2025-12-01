"""
Script de prueba para la pantalla de Gestión de Inventario
Ejecuta este archivo para probar el inventario independientemente
"""
import customtkinter as ctk
from views.gestion_inventario_view import GestionInventarioView

if __name__ == "__main__":
    # Usuario de prueba
    usuario = {
        "id_usuario": 1,
        "nombre_completo": "Administrador",
        "email": "admin@rosabici.com",
        "rol": "Administrador"
    }
    
    app = GestionInventarioView(usuario=usuario)
    app.mainloop()
