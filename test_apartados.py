"""
Script de prueba para la pantalla de Gestión de Apartados
Ejecuta este archivo para probar los apartados independientemente
"""
import customtkinter as ctk
from views.gestion_apartados_view import GestionApartadosView

if __name__ == "__main__":
    # Usuario de prueba
    usuario = {
        "id_usuario": 1,
        "nombre_completo": "Administrador",
        "email": "admin@rosabici.com",
        "rol": "Administrador"
    }
    
    app = GestionApartadosView(usuario=usuario)
    app.mainloop()
