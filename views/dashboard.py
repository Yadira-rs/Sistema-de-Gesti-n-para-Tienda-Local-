import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from controllers.products import productos_count, stock_total_sum, stock_bajo_list
from controllers.ventas import ventas_hoy_total, resumen_ventas, listar_ultimas_ventas, ingresos_mes_total, ventas_diarias
from datetime import datetime

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.pack(fill="both", expand=True)

        # --- Cargar datos de los controladores ---
        resumen = resumen_ventas()
        stock_bajo = stock_bajo_list(5)
        ultimas_ventas = listar_ultimas_ventas(5)
        v_hoy = ventas_hoy_total()
        p_count = productos_count()
        s_sum = stock_total_sum()

        # --- Área principal ---
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # Header
        header = ctk.CTkFrame(main, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            header,
            text="Dashboard",
            font=("Segoe UI", 24, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Bienvenido al sistema de punto de venta",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w")

        # Tarjetas de estadísticas principales
        stats_frame = ctk.CTkFrame(main, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Ventas Hoy
        self.crear_tarjeta_stat(
            stats_frame, 0,
            "💵", "#4CAF50",
            "Ventas Hoy",
            f"${v_hoy:.2f}"
        )
        
        # Total Ventas
        self.crear_tarjeta_stat(
            stats_frame, 1,
            "🛒", "#E91E63",
            "Total Ventas",
            str(resumen.get('total_ventas', 0))
        )
        
        # Productos
        self.crear_tarjeta_stat(
            stats_frame, 2,
            "📦", "#2196F3",
            "Productos",
            str(p_count)
        )
        
        # Stock Total
        self.crear_tarjeta_stat(
            stats_frame, 3,
            "📊", "#FF9800",
            "Stock Total",
            str(s_sum)
        )

        # Contenedor de dos columnas
        content_frame = ctk.CTkFrame(main, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Columna izquierda - Stock Bajo
        left_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Columna derecha - Últimas Ventas
        right_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Stock Bajo
        self.crear_seccion_stock_bajo(left_column, stock_bajo)
        
        # Últimas Ventas
        self.crear_seccion_ultimas_ventas(right_column, ultimas_ventas)
    
    def crear_tarjeta_stat(self, parent, column, icono, color, titulo, valor):
        """Crear tarjeta de estadística"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.grid(row=0, column=column, padx=8, sticky="ew")
        
        # Contenedor interno
        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Fila superior: Icono
        top_row = ctk.CTkFrame(container, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 10))
        
        # Icono con fondo de color
        icon_frame = ctk.CTkFrame(top_row, fg_color=color, corner_radius=10, width=50, height=50)
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text=icono,
            font=("Segoe UI", 24),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        ctk.CTkLabel(
            container,
            text=titulo,
            font=("Segoe UI", 11),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w")
        
        # Valor
        ctk.CTkLabel(
            container,
            text=valor,
            font=("Segoe UI", 24, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
    
    def crear_seccion_stock_bajo(self, parent, productos):
        """Crear sección de productos con stock bajo"""
        # Header
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            header,
            text="Productos con Stock Bajo:",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        # Contenedor de productos
        productos_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        productos_frame.pack(fill="both", expand=True)
        
        # Scroll frame
        scroll = ctk.CTkScrollableFrame(productos_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        if not productos:
            ctk.CTkLabel(
                scroll,
                text="No hay productos con stock bajo",
                font=("Segoe UI", 11),
                text_color="#999999"
            ).pack(pady=20)
        else:
            for producto in productos:
                self.crear_item_stock_bajo(scroll, producto)
    
    def crear_item_stock_bajo(self, parent, producto):
        """Crear item de producto con stock bajo"""
        item = ctk.CTkFrame(parent, fg_color="#FFF5F5", corner_radius=10)
        item.pack(fill="x", pady=5)
        
        container = ctk.CTkFrame(item, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=12)
        
        # Columna izquierda - Info del producto
        left = ctk.CTkFrame(container, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        
        # Nombre
        nombre = producto.get('nombre', 'Producto')
        ctk.CTkLabel(
            left,
            text=nombre[:30] + "..." if len(nombre) > 30 else nombre,
            font=("Segoe UI", 12, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        # Categoría (si existe)
        categoria = producto.get('categoria', 'Sin categoría')
        ctk.CTkLabel(
            left,
            text=categoria,
            font=("Segoe UI", 9),
            text_color="#999999",
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))
        
        # Columna derecha - Stock y precio
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="right")
        
        # Stock con badge rojo
        stock = producto.get('stock', 0)
        stock_badge = ctk.CTkFrame(right, fg_color="#FFE0E0", corner_radius=8)
        stock_badge.pack(side="top", anchor="e")
        
        ctk.CTkLabel(
            stock_badge,
            text=f"{stock} Unidades",
            font=("Segoe UI", 10, "bold"),
            text_color="#E91E63",
            padx=10,
            pady=4
        ).pack()
        
        # Precio
        precio = float(producto.get('precio', 0))
        ctk.CTkLabel(
            right,
            text=f"${precio:.2f}",
            font=("Segoe UI", 11, "bold"),
            text_color="#666666"
        ).pack(side="top", anchor="e", pady=(5, 0))
    
    def crear_seccion_ultimas_ventas(self, parent, ventas):
        """Crear sección de últimas ventas"""
        # Header
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            header,
            text="Últimas Ventas:",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        # Contenedor de ventas
        ventas_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        ventas_frame.pack(fill="both", expand=True)
        
        # Scroll frame
        scroll = ctk.CTkScrollableFrame(ventas_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        if not ventas:
            ctk.CTkLabel(
                scroll,
                text="No hay ventas registradas",
                font=("Segoe UI", 11),
                text_color="#999999"
            ).pack(pady=20)
        else:
            for venta in ventas:
                self.crear_item_venta(scroll, venta)
    
    def crear_item_venta(self, parent, venta):
        """Crear item de venta"""
        item = ctk.CTkFrame(parent, fg_color="#F5FFF5", corner_radius=10)
        item.pack(fill="x", pady=5)
        
        container = ctk.CTkFrame(item, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=12)
        
        # Columna izquierda - Info de la venta
        left = ctk.CTkFrame(container, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        
        # ID de venta
        id_venta = venta.get('id_venta', '?')
        ctk.CTkLabel(
            left,
            text=f"Venta #{id_venta}",
            font=("Segoe UI", 12, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        # Fecha
        fecha = venta.get('fecha', datetime.now())
        if isinstance(fecha, datetime):
            fecha_str = fecha.strftime("%d/%m/%Y - %H:%M")
        else:
            fecha_str = str(fecha)
        
        # Obtener cantidad de unidades
        unidades = venta.get('cantidad_productos', 1)
        
        ctk.CTkLabel(
            left,
            text=f"{fecha_str} - {unidades} Unidad{'es' if unidades != 1 else ''}",
            font=("Segoe UI", 9),
            text_color="#999999",
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))
        
        # Columna derecha - Total y método
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="right")
        
        # Total con badge verde
        total = float(venta.get('total', 0))
        total_badge = ctk.CTkFrame(right, fg_color="#E8F5E9", corner_radius=8)
        total_badge.pack(side="top", anchor="e")
        
        ctk.CTkLabel(
            total_badge,
            text=f"${total:.2f}",
            font=("Segoe UI", 11, "bold"),
            text_color="#4CAF50",
            padx=12,
            pady=4
        ).pack()
        
        # Método de pago
        metodo = venta.get('metodo_pago', 'Efectivo')
        ctk.CTkLabel(
            right,
            text=metodo,
            font=("Segoe UI", 9),
            text_color="#666666"
        ).pack(side="top", anchor="e", pady=(5, 0))
