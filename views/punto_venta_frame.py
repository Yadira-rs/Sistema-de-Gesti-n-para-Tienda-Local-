"""
Versión Frame del Punto de Venta para integración en el menú principal
"""
import customtkinter as ctk
from tkinter import messagebox
from controllers.products import obtener_productos
from controllers.ventas import agregar_al_carrito, obtener_carrito, finalizar_venta, vaciar_carrito

class PuntoVentaView(ctk.CTkFrame):
    """Punto de Venta como Frame para integración"""
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user or {"nombre_completo": "Administrador", "email": "admin@janet.com"}
        self.carrito = []
        self.metodo_pago = ctk.StringVar(value="Efectivo")
        self.descuento_porcentaje = ctk.DoubleVar(value=0.0)
        
        self.pack(fill="both", expand=True)
        
        # Mensaje temporal
        ctk.CTkLabel(
            self,
            text="🛒 Punto de Venta",
            font=("Segoe UI", 24, "bold")
        ).pack(expand=True)
        
        ctk.CTkLabel(
            self,
            text="Vista en desarrollo - Usa el test independiente",
            font=("Segoe UI", 14)
        ).pack()
        
        ctk.CTkButton(
            self,
            text="Abrir Punto de Venta Completo",
            command=self.abrir_completo
        ).pack(pady=20)
    
    def abrir_completo(self):
        """Abrir ventana completa del punto de venta"""
        from views.punto_venta_view import PuntoVentaView as PuntoVentaCompleto
        ventana = PuntoVentaCompleto(usuario=self.user)
        ventana.mainloop()
