"""
Script de prueba para la pantalla de Ventas a Crédito
Ejecuta este archivo para probar los créditos independientemente
"""
import customtkinter as ctk
from views.gestion_creditos_view import GestionCreditosView

if __name__ == "__main__":
    # Usuario de prueba
    usuario = {
        "id_usuario": 1,
        "nombre_completo": "Administrador",
        "email": "admin@rosabici.com",
        "rol": "Administrador"
    }
    
    app = GestionCreditosView(usuario=usuario)
    app.mainloop()
