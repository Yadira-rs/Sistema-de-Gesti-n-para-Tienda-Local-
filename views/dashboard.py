import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from controllers.products import productos_count, stock_total_sum, stock_bajo_list
from controllers.ventas import ventas_hoy_total, resumen_ventas, listar_ultimas_ventas, ingresos_mes_total, ventas_diarias
from datetime import datetime

class DashboardView(ctk.CTkFrame):
    """Dashboard - Janet Rosa Bici"""
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.user = user or {"nombre_completo": "Vendedor Demo"}
        self.pack(fill="both", expand=True)
        self.crear_interfaz()
        self.cargar_datos()
    

    def crear_logo_header(self, parent):
        """Crear header con logo de Janet Rosa Bici"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Logo pequeño a la izquierda
        logo_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_container.pack(side="left", padx=(0, 15))
        
        try:
            # Intentar cargar logo circular pequeño
            logo_paths = [
                "logo_limpio_small.png",  # LOGO LIMPIO
                "assets/logo_limpio_small.png",
                "logo_limpio_small.png",  # IMAGEN ORIGINAL
                "assets/logo_limpio_small.png",
                "logo_limpio_small.png",
                "logo_nuevo_sidebar.png", 
                "WhatsApp Image 2025-12-02 at 11.52.41 AM.jpeg",
                "logo_original.png"
            ]
            
            logo_loaded = False
            for path in logo_paths:
                if os.path.exists(path):
                    try:
                        from PIL import Image
                        img = Image.open(path).resize((40, 40), Image.Resampling.LANCZOS)
                        logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
                        
                        ctk.CTkLabel(
                            logo_container,
                            image=logo_image,
                            text=""
                        ).pack()
                        
                        logo_loaded = True
                        break
                    except Exception:
                        continue
            
            if not logo_loaded:
                # Fallback: emoji de bicicleta
                ctk.CTkLabel(
                    logo_container,
                    text="🚲",
                    font=("Segoe UI", 24),
                    text_color="#E91E63"
                ).pack()
                
        except Exception:
            # Fallback: emoji de bicicleta
            ctk.CTkLabel(
                logo_container,
                text="🚲",
                font=("Segoe UI", 24),
                text_color="#E91E63"
            ).pack()
        
        # Título de la pantalla
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        
        return title_frame

    def crear_interfaz(self):
        # Contenedor principal con menos padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header del Dashboard
        self.crear_header(main_container)
        
        # Instrucciones de navegación
        self.crear_instrucciones_navegacion(main_container)
        
        # Tarjetas de estadísticas (4 en fila)
        self.crear_tarjetas_estadisticas(main_container)
        
        # Contenedor de las dos secciones principales
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.pack(fill="both", expand=True, pady=(20, 0))
        
        # Configurar grid para dos columnas iguales
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_columnconfigure(1, weight=1)
        
        # Panel izquierdo - Productos con Stock Bajo
        left_panel = ctk.CTkFrame(content_container, fg_color="white", corner_radius=8)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Panel derecho - Últimas Ventas (mismo ancho que el izquierdo)
        right_panel = ctk.CTkFrame(content_container, fg_color="white", corner_radius=8)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.crear_seccion_stock_bajo(left_panel)
        self.crear_seccion_ultimas_ventas(right_panel)
    
    def crear_header(self, parent):
        """Crear header del dashboard"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título principal
        ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=("Segoe UI", 28, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        # Subtítulo
        ctk.CTkLabel(
            header_frame,
            text="Bienvenido al sistema de punto de venta",
            font=("Segoe UI", 14),
            text_color="#666666"
        ).pack(anchor="w", pady=(5, 0))
    
    def crear_instrucciones_navegacion(self, parent):
        """Crear panel de ayuda para el usuario"""
        ayuda_frame = ctk.CTkFrame(parent, fg_color="#F3E5F5", corner_radius=8, height=45)
        ayuda_frame.pack(fill="x", pady=(0, 15))
        ayuda_frame.pack_propagate(False)
        
        content_frame = ctk.CTkFrame(ayuda_frame, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        ctk.CTkLabel(
            content_frame,
            text="📋",
            font=("Segoe UI", 18)
        ).pack(side="left", padx=(0, 12))
        
        ctk.CTkLabel(
            content_frame,
            text="Qué hacer aquí: Ver resumen de ventas • Revisar productos con poco stock • Consultar últimas transacciones",
            font=("Segoe UI", 11),
            text_color="#7B1FA2",
            anchor="w",
            wraplength=800
        ).pack(side="left", fill="x", expand=True)
    
    def crear_tarjetas_estadisticas(self, parent):
        """Crear las 4 tarjetas de estadísticas principales"""
        stats_container = ctk.CTkFrame(parent, fg_color="transparent")
        stats_container.pack(fill="x", pady=(0, 20))
        
        # Configurar grid para 4 columnas
        stats_container.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Datos de las tarjetas (icono, color, título, valor_key) - colores como en la imagen
        self.tarjetas_data = [
            ("💰", "#4CAF50", "Ventas Hoy", "ventas_hoy"),
            ("🛒", "#E91E63", "Total Ventas", "total_ventas"),
            ("📦", "#2196F3", "Productos", "productos"),
            ("📊", "#FF9800", "Stock Total", "stock_total")
        ]
        
        self.tarjetas_widgets = []
        
        for i, (icono, color, titulo, key) in enumerate(self.tarjetas_data):
            tarjeta = self.crear_tarjeta_estadistica(stats_container, i, icono, color, titulo, "0")
            self.tarjetas_widgets.append((tarjeta, key))
    
    def crear_tarjeta_estadistica(self, parent, column, icono, color, titulo, valor):
        """Crear una tarjeta de estadística individual"""
        # Contenedor de la tarjeta
        card_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=8, height=140)
        card_frame.grid(row=0, column=column, padx=10, pady=0, sticky="ew")
        card_frame.grid_propagate(False)
        
        # Contenido de la tarjeta
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono con fondo de color (más grande)
        icon_frame = ctk.CTkFrame(content_frame, fg_color=color, corner_radius=8, width=60, height=60)
        icon_frame.pack(anchor="w")
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=icono,
            font=("Segoe UI", 28),
            text_color="white"
        )
        icon_label.pack(expand=True)
        
        # Título
        titulo_label = ctk.CTkLabel(
            content_frame,
            text=titulo,
            font=("Segoe UI", 12),
            text_color="#666666"
        )
        titulo_label.pack(anchor="w", pady=(15, 5))
        
        # Valor principal (más grande)
        valor_label = ctk.CTkLabel(
            content_frame,
            text=valor,
            font=("Segoe UI", 32, "bold"),
            text_color="#333333"
        )
        valor_label.pack(anchor="w")
        
        # Guardar referencia al label del valor para actualizarlo
        card_frame.valor_label = valor_label
        
        return card_frame
    
    def crear_seccion_stock_bajo(self, parent):
        """Crear sección de productos con stock bajo"""
        # Header de la sección
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 15))
        
        # Título de la sección
        ctk.CTkLabel(
            header_frame,
            text="Productos con Stock Bajo:",
            font=("Segoe UI", 18, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        # Lista scrollable de productos
        self.stock_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            height=400
        )
        self.stock_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 25))
    
    def crear_seccion_ultimas_ventas(self, parent):
        """Crear sección de últimas ventas"""
        # Header de la sección
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 15))
        
        # Título de la sección
        ctk.CTkLabel(
            header_frame,
            text="Últimas Ventas:",
            font=("Segoe UI", 18, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        # Lista scrollable de ventas
        self.ventas_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            height=400
        )
        self.ventas_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 25))
    
    def cargar_datos(self):
        """Cargar datos desde los controladores"""
        try:
            # Cargar estadísticas
            self.resumen = resumen_ventas()
            self.v_hoy = ventas_hoy_total()
            self.p_count = productos_count()
            self.s_sum = stock_total_sum()
            self.total_ventas = self.resumen.get('total_ventas', 0) if self.resumen else 0
            
            # Cargar productos con stock bajo
            self.stock_bajo = stock_bajo_list(10)
            
            # Cargar últimas ventas
            self.ultimas_ventas = listar_ultimas_ventas(5)
            
            # Actualizar interfaz
            self.actualizar_estadisticas()
            self.actualizar_stock_bajo()
            self.actualizar_ultimas_ventas()
            
        except Exception as e:
            print(f"Error cargando datos del dashboard: {e}")
            # Valores por defecto en caso de error
            self.v_hoy = 0
            self.p_count = 0
            self.s_sum = 0
            self.total_ventas = 0
            self.stock_bajo = []
            self.ultimas_ventas = []
    
    def actualizar_estadisticas(self):
        """Actualizar valores en las tarjetas de estadísticas"""
        # Datos actualizados
        valores = {
            "ventas_hoy": f"${self.v_hoy:.2f}",
            "total_ventas": str(self.total_ventas),
            "productos": str(self.p_count),
            "stock_total": str(self.s_sum)
        }
        
        # Actualizar cada tarjeta
        for tarjeta_widget, key in self.tarjetas_widgets:
            if key in valores:
                tarjeta_widget.valor_label.configure(text=valores[key])
    
    def actualizar_stock_bajo(self):
        """Actualizar lista de productos con stock bajo"""
        # Limpiar lista
        for widget in self.stock_scroll.winfo_children():
            widget.destroy()
        
        if not self.stock_bajo:
            # Estado sin productos con stock bajo
            empty_frame = ctk.CTkFrame(self.stock_scroll, fg_color="#F8F9FA", corner_radius=8)
            empty_frame.pack(fill="x", pady=20, padx=10)
            
            ctk.CTkLabel(
                empty_frame,
                text="✅ Todos los productos tienen stock suficiente",
                font=("Segoe UI", 14),
                text_color="#666666"
            ).pack(pady=30)
        else:
            # Mostrar productos con stock bajo
            for producto in self.stock_bajo:
                self.crear_item_stock_bajo(self.stock_scroll, producto)
    
    def crear_item_stock_bajo(self, parent, producto):
        """Crear item de producto con stock bajo - diseño simple y centrado"""
        stock = producto.get('stock', 0)
        nombre = producto.get('nombre', 'Producto')
        precio = float(producto.get('precio', 0))
        
        # Contenedor del item
        item_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=6)
        item_frame.pack(fill="x", pady=3, padx=5)
        
        # Contenido del item con padding vertical para centrado
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=18)
        
        # Fila superior - Nombre del producto
        ctk.CTkLabel(
            content_frame,
            text=nombre,
            font=("Segoe UI", 14, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        # Fila inferior - Categoría, precio y stock
        bottom_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(8, 0))
        
        # Categoría
        ctk.CTkLabel(
            bottom_frame,
            text="Sin categoría",
            font=("Segoe UI", 11),
            text_color="#999999"
        ).pack(side="left")
        
        # Precio
        ctk.CTkLabel(
            bottom_frame,
            text=f"${precio:.2f}",
            font=("Segoe UI", 11),
            text_color="#999999"
        ).pack(side="right", padx=(0, 15))
        
        # Badge de stock (rosa como en la imagen)
        stock_badge = ctk.CTkFrame(bottom_frame, fg_color="#FF6B9D", corner_radius=15)
        stock_badge.pack(side="right")
        
        ctk.CTkLabel(
            stock_badge,
            text=f"{stock} Unidades",
            font=("Segoe UI", 10, "bold"),
            text_color="white"
        ).pack(padx=15, pady=6)
    
    def actualizar_ultimas_ventas(self):
        """Actualizar lista de últimas ventas"""
        # Limpiar lista
        for widget in self.ventas_scroll.winfo_children():
            widget.destroy()
        
        if not self.ultimas_ventas:
            # Estado sin ventas
            empty_frame = ctk.CTkFrame(self.ventas_scroll, fg_color="#F8F9FA", corner_radius=8)
            empty_frame.pack(fill="x", pady=20, padx=10)
            
            ctk.CTkLabel(
                empty_frame,
                text="📋 No hay ventas registradas",
                font=("Segoe UI", 14),
                text_color="#666666"
            ).pack(pady=30)
        else:
            for i, venta in enumerate(self.ultimas_ventas):
                self.crear_item_venta(self.ventas_scroll, venta, i + 35)  # Simular IDs
    
    def crear_item_venta(self, parent, venta, venta_id):
        """Crear item de venta - diseño simple y centrado"""
        total = float(venta.get('total', 150.00))  # Valor por defecto
        fecha = venta.get('fecha', datetime.now())
        
        # Formatear fecha
        if isinstance(fecha, datetime):
            fecha_str = fecha.strftime("%d/%m/%Y - %H:%M - 1 minuto")
        else:
            fecha_str = "06/12/2024 - 14:30 - 1 minuto"
        
        # Contenedor del item
        item_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=6)
        item_frame.pack(fill="x", pady=3, padx=5)
        
        # Contenido del item con padding vertical para centrado
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=18)
        
        # Fila superior - ID de venta y total
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x")
        
        # ID de venta
        ctk.CTkLabel(
            top_frame,
            text=f"Venta #{venta_id}",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Total con badge verde (como en la imagen)
        total_badge = ctk.CTkFrame(top_frame, fg_color="#4CAF50", corner_radius=15)
        total_badge.pack(side="right")
        
        ctk.CTkLabel(
            total_badge,
            text=f"${total:.2f}",
            font=("Segoe UI", 11, "bold"),
            text_color="white"
        ).pack(padx=15, pady=6)
        
        # Fila inferior - Fecha y estado
        bottom_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(8, 0))
        
        # Fecha y tiempo
        ctk.CTkLabel(
            bottom_frame,
            text=fecha_str,
            font=("Segoe UI", 11),
            text_color="#999999"
        ).pack(side="left")
        
        # Estado (Efectivo)
        ctk.CTkLabel(
            bottom_frame,
            text="Efectivo",
            font=("Segoe UI", 11),
            text_color="#999999"
        ).pack(side="right")
    
    def actualizar_dashboard(self):
        """Actualizar todos los datos del dashboard"""
        try:
            self.cargar_datos()
            self.mostrar_notificacion("✅ Dashboard actualizado")
        except Exception as e:
            print(f"Error al actualizar dashboard: {e}")
            self.mostrar_notificacion("❌ Error al actualizar")
    
    def mostrar_notificacion(self, mensaje):
        """Mostrar notificación temporal"""
        # Crear label de notificación
        notif = ctk.CTkLabel(
            self,
            text=mensaje,
            font=("Segoe UI", 12, "bold"),
            text_color="white",
            fg_color="#27AE60",
            corner_radius=8
        )
        notif.place(relx=0.5, rely=0.05, anchor="center")
        
        # Ocultar después de 2 segundos
        self.after(2000, notif.destroy)
    



    def actualizar_dashboard(self):
        """Actualizar todos los datos del dashboard"""
        try:
            self.cargar_datos()
            self.mostrar_notificacion("✅ Dashboard actualizado")
        except Exception as e:
            print(f"Error al actualizar dashboard: {e}")
            self.mostrar_notificacion("❌ Error al actualizar")
    
    def mostrar_notificacion(self, mensaje):
        """Mostrar notificación temporal"""
        # Crear label de notificación
        notif = ctk.CTkLabel(
            self,
            text=mensaje,
            font=("Segoe UI", 12, "bold"),
            text_color="white",
            fg_color="#27AE60",
            corner_radius=8
        )
        notif.place(relx=0.5, rely=0.05, anchor="center")
        
        # Ocultar después de 2 segundos
        self.after(2000, notif.destroy)