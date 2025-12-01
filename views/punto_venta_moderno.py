import customtkinter as ctk
from tkinter import messagebox
from controllers.products import obtener_productos
from controllers.ventas import agregar_al_carrito, obtener_carrito, finalizar_venta, vaciar_carrito

class PuntoVentaModerno(ctk.CTkFrame):
    """Punto de Venta Moderno sin sidebar - para integración con main.py"""
    def __init__(self, parent, usuario=None):
        super().__init__(parent, fg_color="#F5F5F5")
        
        self.usuario = usuario or {"nombre_completo": "Administrador", "email": "admin@janet.com"}
        self.carrito = []
        self.metodo_pago = ctk.StringVar(value="Efectivo")
        self.descuento_porcentaje = ctk.DoubleVar(value=0.0)
        self.categoria_seleccionada = "Todas las Categorías"
        self.botones_categorias = []
        self.metodo_pago_btns = {}
        self.metodo_pago_btn_activo = None
        
        self.crear_interfaz()
        self.cargar_productos()
    
    def crear_interfaz(self):
        self.pack(fill="both", expand=True)
        
        # Panel central - Productos
        self.crear_panel_productos(self)
        
        # Panel derecho - Carrito
        self.crear_panel_carrito(self)
    
    def crear_panel_productos(self, parent):
        """Panel central con catálogo de productos"""
        panel = ctk.CTkFrame(parent, fg_color="#F5F5F5")
        panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header, text="🛒 Punto de Venta", font=("Segoe UI", 24, "bold"), 
                    text_color="#333333").pack(side="left", padx=10)
