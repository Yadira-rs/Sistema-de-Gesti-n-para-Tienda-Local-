import customtkinter as ctk
from tkinter import messagebox
from controllers.products import obtener_productos
from controllers.ventas import agregar_al_carrito, obtener_carrito, finalizar_venta, vaciar_carrito

class VentasView(ctk.CTkFrame):
    """Punto de Venta Moderno - Estilo consistente con UsersView"""
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.user = user or {"nombre_completo": "Administrador", "email": "admin@janet.com"}
        self.carrito = []
        self.metodo_pago = ctk.StringVar(value="Efectivo")
        self.descuento_porcentaje = ctk.DoubleVar(value=0.0)
        self.categoria_seleccionada = "Todas"
        
        self.pack(fill="both", expand=True)
        self.crear_interfaz()
        self.cargar_productos()
    
    def crear_interfaz(self):
        # Panel principal
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = ctk.CTkFrame(main, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            header, 
            text="Punto de Venta", 
            font=("Segoe UI", 24, "bold"),
            text_color="#2C2C2C"
        ).pack(side="left")
        
        # Contenedor de dos columnas
        body = ctk.CTkFrame(main, fg_color="transparent")
        body.pack(fill="both", expand=True)
        
        # Panel izquierdo - Productos
        self.crear_panel_productos(body)
        
        # Panel derecho - Carrito
        self.crear_panel_carrito(body)
    
    def crear_panel_productos(self, parent):
        """Panel de productos"""
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(panel, fg_color="white", corner_radius=10, height=50)
        search_frame.pack(fill="x", pady=(0, 15))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Segoe UI", 16)
        ).pack(side="left", padx=15)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar productos por nombre, código o escanear código de barras...",
            border_width=0,
            fg_color="white",
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filtrar_productos())
        self.search_entry.bind("<Return>", lambda e: self.buscar_por_codigo_barras())
        
        # Filtros de categoría
        categorias_frame = ctk.CTkFrame(panel, fg_color="transparent")
        categorias_frame.pack(fill="x", pady=(0, 15))
        
        categorias = ["Todas", "Ropa", "Calzado", "Accesorios", "Cuidado de la piel"]
        for cat in categorias:
            btn = ctk.CTkButton(
                categorias_frame,
                text=cat,
                fg_color="#E91E63" if cat == "Todas" else "#E0E0E0",
                text_color="white" if cat == "Todas" else "#666666",
                hover_color="#C2185B" if cat == "Todas" else "#CCCCCC",
                corner_radius=20,
                height=35,
                font=("Segoe UI", 11),
                command=lambda c=cat: self.filtrar_por_categoria(c)
            )
            btn.pack(side="left", padx=5)
        
        # Grid de productos
        self.productos_scroll = ctk.CTkScrollableFrame(panel, fg_color="transparent")
        self.productos_scroll.pack(fill="both", expand=True)
        
        self.productos_grid = ctk.CTkFrame(self.productos_scroll, fg_color="transparent")
        self.productos_grid.pack(fill="both", expand=True)
    
    def crear_panel_carrito(self, parent):
        """Panel del carrito"""
        panel = ctk.CTkFrame(parent, width=400, fg_color="white", corner_radius=15)
        panel.pack(side="right", fill="y")
        panel.pack_propagate(False)
        
        # Header del carrito
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
