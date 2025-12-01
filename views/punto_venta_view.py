import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from controllers.products import obtener_productos
from controllers.ventas import agregar_al_carrito, obtener_carrito, finalizar_venta, vaciar_carrito

class PuntoVentaView(ctk.CTkFrame):
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
        # Contenedor principal (self ya es el frame principal)
        self.pack(fill="both", expand=True)
        
        # Sidebar izquierdo
        self.crear_sidebar(self)
        
        # Panel central - Productos
        self.crear_panel_productos(self)
        
        # Panel derecho - Carrito
        self.crear_panel_carrito(self)

    def crear_sidebar(self, parent):
        """Menú lateral izquierdo"""
        sidebar = ctk.CTkFrame(parent, width=220, fg_color="white")
        sidebar.pack(side="left", fill="y", padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        # Logo y título
        logo_frame = ctk.CTkFrame(sidebar, fg_color="white")
        logo_frame.pack(pady=(20, 10))
        
        ctk.CTkLabel(logo_frame, text="🚲", font=("Segoe UI", 30), text_color="#E91E63").pack()
        
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack()
        
        ctk.CTkLabel(title_frame, text="Janet ", font=("Brush Script MT", 20), text_color="#333333").pack(side="left")
        ctk.CTkLabel(title_frame, text="Rosa ", font=("Brush Script MT", 20), text_color="#E91E63").pack(side="left")
        ctk.CTkLabel(title_frame, text="Bici", font=("Brush Script MT", 20), text_color="#333333").pack(side="left")
        
        ctk.CTkLabel(sidebar, text="Sistema de ventas", font=("Segoe UI", 11), text_color="#666666").pack(pady=(0, 20))
        
        # Menú de navegación
        menu_items = [
            ("📊", "Dashboard"),
            ("🛒", "Punto de Venta"),
            ("📋", "Apartado"),
            ("📦", "Productos"),
            ("📊", "Inventario"),
            ("💰", "Ventas"),
            ("👥", "Usuarios")
        ]
        
        for icon, text in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icon}  {text}",
                fg_color="#F8BBD0" if text == "Punto de Venta" else "transparent",
                text_color="#333333",
                hover_color="#F8BBD0",
                anchor="w",
                height=40,
                font=("Segoe UI", 12)
            )
            btn.pack(fill="x", padx=10, pady=2)

        # Categorías
        ctk.CTkLabel(sidebar, text="Categorías  ›", font=("Segoe UI", 12), text_color="#666666", anchor="w").pack(fill="x", padx=15, pady=(30, 10))
        
        # Usuario info al final
        user_frame = ctk.CTkFrame(sidebar, fg_color="#FFF0F5", corner_radius=10)
        user_frame.pack(side="bottom", fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(user_frame, text="👤", font=("Segoe UI", 20), text_color="#E91E63").pack(pady=(10, 5))
        ctk.CTkLabel(user_frame, text=self.usuario.get("nombre_completo", "Administrador"), 
                    font=("Segoe UI", 12, "bold"), text_color="#333333").pack()
        ctk.CTkLabel(user_frame, text=self.usuario.get("email", "admin@janet.com"), 
                    font=("Segoe UI", 10), text_color="#666666").pack(pady=(0, 10))
    
    def crear_panel_productos(self, parent):
        """Panel central con catálogo de productos"""
        panel = ctk.CTkFrame(parent, fg_color="#F5F5F5")
        panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header, text="Punto de Venta", font=("Segoe UI", 24, "bold"), 
                    text_color="#333333").pack(side="left", padx=10)
        
        # Barra de búsqueda mejorada
        search_frame = ctk.CTkFrame(panel, fg_color="white", corner_radius=12, height=55)
        search_frame.pack(fill="x", pady=(0, 15))
        search_frame.pack_propagate(False)
        
        # Icono de búsqueda
        ctk.CTkLabel(
            search_frame, 
            text="🔍", 
            font=("Segoe UI", 18),
            text_color="#999999"
        ).pack(side="left", padx=15)
        
        # Campo de búsqueda
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar productos por Nombre, Código o Categoría...",
            border_width=0,
            fg_color="white",
            font=("Segoe UI", 13),
            text_color="#2C2C2C",
            placeholder_text_color="#AAAAAA"
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filtrar_productos())
        self.search_entry.bind("<Return>", lambda e: self.buscar_por_codigo_barras())

        # Filtros de categoría con scroll horizontal
        categorias_container = ctk.CTkFrame(panel, fg_color="transparent", height=45)
        categorias_container.pack(fill="x", pady=(0, 15))
        categorias_container.pack_propagate(False)
        
        categorias_frame = ctk.CTkScrollableFrame(
            categorias_container, 
            fg_color="transparent",
            orientation="horizontal",
            height=40
        )
        categorias_frame.pack(fill="both", expand=True)
        
        categorias = ["Todas las Categorías", "Vestidos", "Blusas", "Pantalones", "Serum", "Cremas", "Dulces", "short"]
        
        self.categoria_seleccionada = "Todas las Categorías"
        self.botones_categorias = []
        
        for i, cat in enumerate(categorias):
            btn = ctk.CTkButton(
                categorias_frame,
                text=cat,
                fg_color="#E91E63" if i == 0 else "white",
                text_color="white" if i == 0 else "#666666",
                hover_color="#C2185B" if i == 0 else "#F5F5F5",
                border_width=1 if i != 0 else 0,
                border_color="#E0E0E0" if i != 0 else None,
                corner_radius=20,
                height=36,
                font=("Segoe UI", 11),
                command=lambda c=cat: self.filtrar_por_categoria(c)
            )
            btn.pack(side="left", padx=4)
            self.botones_categorias.append((btn, cat))
        
        # Grid de productos
        self.productos_scroll = ctk.CTkScrollableFrame(panel, fg_color="transparent")
        self.productos_scroll.pack(fill="both", expand=True)
        
        # Contenedor para productos en grid
        self.productos_grid = ctk.CTkFrame(self.productos_scroll, fg_color="transparent")
        self.productos_grid.pack(fill="both", expand=True)
    
    def cargar_productos(self):
        """Cargar productos desde la base de datos"""
        try:
            self.productos = obtener_productos()
            self.mostrar_productos(self.productos)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {str(e)}")
            self.productos = []
    
    def mostrar_productos(self, productos):
        """Mostrar productos en grid"""
        # Limpiar grid actual
        for widget in self.productos_grid.winfo_children():
            widget.destroy()
        
        # Crear grid de productos (3 columnas)
        for i, producto in enumerate(productos):
            row = i // 3
            col = i % 3
            
            self.crear_tarjeta_producto(self.productos_grid, producto, row, col)

    def crear_tarjeta_producto(self, parent, producto, row, col):
        """Crear tarjeta individual de producto estilo moderno"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, width=220, height=300)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        card.grid_propagate(False)
        
        # Contenedor clickeable
        card.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        card.configure(cursor="hand2")
        
        # Imagen del producto (placeholder con gradiente rosa)
        img_frame = ctk.CTkFrame(card, fg_color="#FFE4E1", corner_radius=10, height=160)
        img_frame.pack(fill="x", padx=12, pady=12)
        img_frame.pack_propagate(False)
        img_frame.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Icono de producto
        icon_label = ctk.CTkLabel(img_frame, text="🛍️", font=("Segoe UI", 60))
        icon_label.pack(expand=True)
        icon_label.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Contenedor de información
        info_container = ctk.CTkFrame(card, fg_color="transparent")
        info_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        info_container.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Nombre del producto
        nombre = producto.get("nombre", "Producto")
        nombre_label = ctk.CTkLabel(
            info_container,
            text=nombre[:35] + "..." if len(nombre) > 35 else nombre,
            font=("Segoe UI", 12, "bold"),
            text_color="#2C2C2C",
            wraplength=190,
            anchor="w",
            justify="left"
        )
        nombre_label.pack(anchor="w", pady=(0, 8))
        nombre_label.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Categoría (si existe)
        categoria = producto.get("categoria", "General")
        cat_label = ctk.CTkLabel(
            info_container,
            text=categoria,
            font=("Segoe UI", 9),
            text_color="#999999",
            anchor="w"
        )
        cat_label.pack(anchor="w", pady=(0, 8))
        cat_label.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Precio y stock en la misma línea
        bottom_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        bottom_frame.pack(fill="x", side="bottom")
        bottom_frame.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        precio = float(producto.get("precio", 0))
        stock = int(producto.get("stock", 0))
        
        # Precio destacado
        precio_label = ctk.CTkLabel(
            bottom_frame,
            text=f"${precio:.2f}",
            font=("Segoe UI", 16, "bold"),
            text_color="#E91E63"
        )
        precio_label.pack(side="left")
        precio_label.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Stock con color según disponibilidad
        stock_color = "#4CAF50" if stock > 10 else "#FF9800" if stock > 0 else "#F44336"
        stock_label = ctk.CTkLabel(
            bottom_frame,
            text=f"Stock: {stock}",
            font=("Segoe UI", 10),
            text_color=stock_color
        )
        stock_label.pack(side="right")
        stock_label.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Efecto hover
        def on_enter(e):
            card.configure(fg_color="#FFF5F8")
        
        def on_leave(e):
            card.configure(fg_color="white")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        img_frame.bind("<Enter>", on_enter)
        img_frame.bind("<Leave>", on_leave)

    def crear_panel_carrito(self, parent):
        """Panel derecho con carrito de compras estilo moderno"""
        panel = ctk.CTkFrame(parent, width=400, fg_color="#FAFAFA")
        panel.pack(side="right", fill="y", padx=(0, 10), pady=10)
        panel.pack_propagate(False)
        
        # Header del carrito con diseño mejorado
        header_bg = ctk.CTkFrame(panel, fg_color="white", corner_radius=0)
        header_bg.pack(fill="x", pady=(0, 15))
        
        header = ctk.CTkFrame(header_bg, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        # Icono y título
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame, 
            text="🛒", 
            font=("Segoe UI", 24), 
            text_color="#E91E63"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame, 
            text="Carrito de\nCompras", 
            font=("Segoe UI", 16, "bold"), 
            text_color="#2C2C2C",
            justify="left"
        ).pack(side="left")
        
        # Botón limpiar carrito mejorado
        ctk.CTkButton(
            header,
            text="🗑️",
            width=45,
            height=45,
            fg_color="#FFE4E1",
            text_color="#E91E63",
            hover_color="#FFD0D0",
            font=("Segoe UI", 20),
            corner_radius=10,
            command=self.limpiar_carrito
        ).pack(side="right")
        
        # Contador de productos con badge
        contador_frame = ctk.CTkFrame(panel, fg_color="transparent")
        contador_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.contador_label = ctk.CTkLabel(
            contador_frame,
            text="0 Productos",
            font=("Segoe UI", 13),
            text_color="#666666"
        )
        self.contador_label.pack(side="left")
        
        # Lista de productos en el carrito con mejor diseño
        self.carrito_scroll = ctk.CTkScrollableFrame(
            panel, 
            fg_color="transparent", 
            height=280,
            corner_radius=0
        )
        self.carrito_scroll.pack(fill="x", padx=15, pady=(0, 15))
        
        # Sección de descuento mejorada
        descuento_frame = ctk.CTkFrame(panel, fg_color="white", corner_radius=12)
        descuento_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        desc_header = ctk.CTkFrame(descuento_frame, fg_color="transparent")
        desc_header.pack(fill="x", padx=15, pady=(12, 8))
        
        ctk.CTkLabel(
            desc_header,
            text="💰",
            font=("Segoe UI", 16)
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            desc_header,
            text="Descuento",
            font=("Segoe UI", 12, "bold"),
            text_color="#2C2C2C"
        ).pack(side="left")
        
        desc_input_frame = ctk.CTkFrame(descuento_frame, fg_color="transparent")
        desc_input_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        # Input de descuento
        input_container = ctk.CTkFrame(desc_input_frame, fg_color="#F5F5F5", corner_radius=8)
        input_container.pack(side="left", fill="x", expand=True)
        
        self.descuento_entry = ctk.CTkEntry(
            input_container,
            textvariable=self.descuento_porcentaje,
            width=100,
            height=40,
            border_width=0,
            corner_radius=8,
            fg_color="#F5F5F5",
            font=("Segoe UI", 13),
            placeholder_text="0"
        )
        self.descuento_entry.pack(side="left", padx=10, pady=5)
        self.descuento_entry.bind("<KeyRelease>", lambda e: self.actualizar_totales())
        
        ctk.CTkLabel(
            input_container,
            text="%",
            font=("Segoe UI", 13, "bold"),
            text_color="#666666"
        ).pack(side="left", padx=(0, 10))
        
        # Botón aplicar
        ctk.CTkButton(
            desc_input_frame,
            text="Aplicar",
            width=90,
            height=40,
            fg_color="#FF9800",
            hover_color="#F57C00",
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            command=self.actualizar_totales
        ).pack(side="left", padx=(10, 0))

        # Método de pago mejorado
        pago_frame = ctk.CTkFrame(panel, fg_color="white", corner_radius=12)
        pago_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            pago_frame,
            text="Método de pago",
            font=("Segoe UI", 13, "bold"),
            text_color="#2C2C2C"
        ).pack(anchor="w", padx=15, pady=(12, 10))
        
        # Botones de método de pago
        metodos_frame = ctk.CTkFrame(pago_frame, fg_color="transparent")
        metodos_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        metodos = ["Efectivo", "Tarjeta", "Transferencia"]
        self.metodo_pago_btns = {}
        
        for metodo in metodos:
            btn = ctk.CTkButton(
                metodos_frame,
                text=metodo,
                fg_color="white",
                text_color="#666666",
                border_width=1,
                border_color="#E0E0E0",
                hover_color="#F5F5F5",
                corner_radius=10,
                height=45,
                font=("Segoe UI", 12),
                command=lambda m=metodo: self.seleccionar_metodo_pago(m)
            )
            btn.pack(side="left", expand=True, fill="x", padx=3)
            self.metodo_pago_btns[metodo] = btn
            
            if metodo == "Efectivo":
                btn.configure(fg_color="#E91E63", text_color="white", border_width=0)
                self.metodo_pago_btn_activo = btn
        
        # Resumen de totales mejorado
        totales_frame = ctk.CTkFrame(panel, fg_color="white", corner_radius=12)
        totales_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Subtotal
        subtotal_row = ctk.CTkFrame(totales_frame, fg_color="transparent")
        subtotal_row.pack(fill="x", padx=18, pady=(15, 8))
        
        ctk.CTkLabel(
            subtotal_row, 
            text="Subtotal:", 
            font=("Segoe UI", 13), 
            text_color="#666666"
        ).pack(side="left")
        
        self.subtotal_label = ctk.CTkLabel(
            subtotal_row, 
            text="$0.00", 
            font=("Segoe UI", 13), 
            text_color="#666666"
        )
        self.subtotal_label.pack(side="right")
        
        # Descuento
        descuento_row = ctk.CTkFrame(totales_frame, fg_color="transparent")
        descuento_row.pack(fill="x", padx=18, pady=8)
        
        ctk.CTkLabel(
            descuento_row, 
            text="Descuento:", 
            font=("Segoe UI", 13), 
            text_color="#FF9800"
        ).pack(side="left")
        
        self.descuento_label = ctk.CTkLabel(
            descuento_row, 
            text="- $0.00", 
            font=("Segoe UI", 13), 
            text_color="#FF9800"
        )
        self.descuento_label.pack(side="right")
        
        # Separador elegante
        separador = ctk.CTkFrame(totales_frame, height=2, fg_color="#F0F0F0")
        separador.pack(fill="x", padx=18, pady=10)
        
        # Total destacado
        total_row = ctk.CTkFrame(totales_frame, fg_color="transparent")
        total_row.pack(fill="x", padx=18, pady=(8, 15))
        
        ctk.CTkLabel(
            total_row, 
            text="Total:", 
            font=("Segoe UI", 18, "bold"), 
            text_color="#2C2C2C"
        ).pack(side="left")
        
        self.total_label = ctk.CTkLabel(
            total_row, 
            text="$0.00", 
            font=("Segoe UI", 18, "bold"), 
            text_color="#E91E63"
        )
        self.total_label.pack(side="right")

        # Botón procesar venta mejorado
        ctk.CTkButton(
            panel,
            text="Procesar venta",
            fg_color="#E91E63",
            hover_color="#C2185B",
            corner_radius=12,
            height=55,
            font=("Segoe UI", 15, "bold"),
            command=self.procesar_venta
        ).pack(fill="x", padx=20, pady=(0, 20))
    
    def agregar_producto(self, producto):
        """Agregar producto al carrito"""
        stock = int(producto.get("stock", 0))
        if stock <= 0:
            messagebox.showwarning("Sin stock", f"El producto '{producto.get('nombre')}' no tiene stock disponible")
            return
        
        # Buscar si ya existe en el carrito
        for item in self.carrito:
            if item["id_producto"] == producto["id_producto"]:
                if item["cantidad"] < stock:
                    item["cantidad"] += 1
                    self.actualizar_carrito()
                    return
                else:
                    messagebox.showwarning("Stock insuficiente", f"No hay más stock disponible de '{producto.get('nombre')}'")
                    return
        
        # Agregar nuevo producto
        self.carrito.append({
            "id_producto": producto["id_producto"],
            "nombre": producto["nombre"],
            "precio": float(producto["precio"]),
            "cantidad": 1,
            "stock": stock
        })
        
        self.actualizar_carrito()
    
    def actualizar_carrito(self):
        """Actualizar visualización del carrito"""
        # Limpiar carrito actual
        for widget in self.carrito_scroll.winfo_children():
            widget.destroy()
        
        # Actualizar contador
        total_items = sum(item["cantidad"] for item in self.carrito)
        self.contador_label.configure(text=f"{total_items} Producto{'s' if total_items != 1 else ''}")
        
        # Mostrar productos
        for item in self.carrito:
            self.crear_item_carrito(self.carrito_scroll, item)
        
        # Actualizar totales
        self.actualizar_totales()

    def crear_item_carrito(self, parent, item):
        """Crear item individual en el carrito estilo moderno"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#F0F0F0")
        card.pack(fill="x", pady=6, padx=5)
        
        # Container principal
        main_container = ctk.CTkFrame(card, fg_color="transparent")
        main_container.pack(fill="x", padx=12, pady=12)
        
        # Fila superior: Nombre del producto
        nombre = item["nombre"]
        nombre_label = ctk.CTkLabel(
            main_container,
            text=nombre[:30] + "..." if len(nombre) > 30 else nombre,
            font=("Segoe UI", 12, "bold"),
            text_color="#2C2C2C",
            anchor="w"
        )
        nombre_label.pack(anchor="w", pady=(0, 8))
        
        # Fila inferior: Precio, cantidad y subtotal
        bottom_row = ctk.CTkFrame(main_container, fg_color="transparent")
        bottom_row.pack(fill="x")
        
        # Precio unitario
        precio_label = ctk.CTkLabel(
            bottom_row,
            text=f"${item['precio']:.2f}",
            font=("Segoe UI", 11),
            text_color="#E91E63"
        )
        precio_label.pack(side="left")
        
        # Subtotal (derecha)
        subtotal = item["precio"] * item["cantidad"]
        subtotal_label = ctk.CTkLabel(
            bottom_row,
            text=f"${subtotal:.2f}",
            font=("Segoe UI", 13, "bold"),
            text_color="#2C2C2C"
        )
        subtotal_label.pack(side="right")
        
        # Controles de cantidad (centro-derecha)
        qty_frame = ctk.CTkFrame(bottom_row, fg_color="#F8F8F8", corner_radius=8, height=32)
        qty_frame.pack(side="right", padx=(0, 15))
        
        # Botón menos
        btn_menos = ctk.CTkButton(
            qty_frame,
            text="−",
            width=32,
            height=32,
            fg_color="transparent",
            text_color="#666666",
            hover_color="#E0E0E0",
            font=("Segoe UI", 16),
            corner_radius=8,
            command=lambda: self.cambiar_cantidad(item, -1)
        )
        btn_menos.pack(side="left", padx=2, pady=2)
        
        # Cantidad
        qty_label = ctk.CTkLabel(
            qty_frame,
            text=str(item["cantidad"]),
            font=("Segoe UI", 12, "bold"),
            text_color="#2C2C2C",
            width=35
        )
        qty_label.pack(side="left", padx=5)
        
        # Botón más
        btn_mas = ctk.CTkButton(
            qty_frame,
            text="+",
            width=32,
            height=32,
            fg_color="transparent",
            text_color="#666666",
            hover_color="#E0E0E0",
            font=("Segoe UI", 16),
            corner_radius=8,
            command=lambda: self.cambiar_cantidad(item, 1)
        )
        btn_mas.pack(side="left", padx=2, pady=2)

    def cambiar_cantidad(self, item, delta):
        """Cambiar cantidad de un producto en el carrito"""
        nueva_cantidad = item["cantidad"] + delta
        
        if nueva_cantidad <= 0:
            # Eliminar del carrito
            self.carrito.remove(item)
        elif nueva_cantidad <= item["stock"]:
            item["cantidad"] = nueva_cantidad
        else:
            messagebox.showwarning("Stock insuficiente", f"Solo hay {item['stock']} unidades disponibles")
            return
        
        self.actualizar_carrito()
    
    def actualizar_totales(self):
        """Actualizar subtotal, descuento y total"""
        subtotal = sum(item["precio"] * item["cantidad"] for item in self.carrito)
        
        try:
            descuento_pct = float(self.descuento_porcentaje.get())
            descuento_pct = max(0, min(100, descuento_pct))  # Entre 0 y 100
        except:
            descuento_pct = 0
            self.descuento_porcentaje.set(0)
        
        descuento_monto = subtotal * (descuento_pct / 100)
        total = subtotal - descuento_monto
        
        self.subtotal_label.configure(text=f"${subtotal:.2f}")
        self.descuento_label.configure(text=f"- ${descuento_monto:.2f}")
        self.total_label.configure(text=f"${total:.2f}")
    
    def seleccionar_metodo_pago(self, metodo):
        """Cambiar método de pago seleccionado"""
        self.metodo_pago.set(metodo)
        
        # Actualizar estilos de botones
        for nombre_metodo, btn in self.metodo_pago_btns.items():
            if nombre_metodo == metodo:
                btn.configure(fg_color="#E91E63", text_color="white", border_width=0)
                self.metodo_pago_btn_activo = btn
            else:
                btn.configure(fg_color="white", text_color="#666666", border_width=1)
    
    def limpiar_carrito(self):
        """Vaciar el carrito"""
        if not self.carrito:
            return
        
        if messagebox.askyesno("Confirmar", "¿Deseas vaciar el carrito?"):
            self.carrito.clear()
            self.descuento_porcentaje.set(0)
            self.actualizar_carrito()

    def procesar_venta(self):
        """Procesar la venta"""
        if not self.carrito:
            messagebox.showwarning("Carrito vacío", "Agrega productos al carrito antes de procesar la venta")
            return
        
        # Calcular totales
        subtotal = sum(item["precio"] * item["cantidad"] for item in self.carrito)
        descuento_pct = float(self.descuento_porcentaje.get())
        descuento_monto = subtotal * (descuento_pct / 100)
        total = subtotal - descuento_monto
        metodo = self.metodo_pago.get()
        
        # Confirmar venta
        mensaje = f"¿Confirmar venta?\n\n"
        mensaje += f"Subtotal: ${subtotal:.2f}\n"
        if descuento_pct > 0:
            mensaje += f"Descuento ({descuento_pct}%): -${descuento_monto:.2f}\n"
        mensaje += f"Total: ${total:.2f}\n"
        mensaje += f"Método de pago: {metodo}"
        
        if not messagebox.askyesno("Confirmar venta", mensaje):
            return
        
        try:
            # Agregar productos al carrito del controlador
            vaciar_carrito()
            for item in self.carrito:
                producto_data = {
                    "id_producto": item["id_producto"],
                    "nombre": item["nombre"],
                    "precio": item["precio"]
                }
                agregar_al_carrito(producto_data, item["cantidad"])
            
            # Finalizar venta
            resultado = finalizar_venta(
                usuario_id=self.usuario.get("id_usuario"),
                metodo=metodo,
                descuento_porcentaje=descuento_pct
            )
            
            if resultado:
                # Mostrar ticket
                from views.ticket_venta_view import TicketVentaView
                
                # Preparar datos para el ticket
                ticket_data = {
                    'id_venta': resultado['id_venta'],
                    'total': total,
                    'metodo': metodo,
                    'descuento': descuento_monto,
                    'items': self.carrito.copy()
                }
                
                # Abrir ventana de ticket
                TicketVentaView(self, ticket_data)
                
                # Limpiar carrito
                self.carrito.clear()
                self.descuento_porcentaje.set(0)
                self.actualizar_carrito()
                
                # Recargar productos para actualizar stock
                self.cargar_productos()
            else:
                messagebox.showerror("Error", "No se pudo procesar la venta")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la venta: {str(e)}")
    
    def buscar_por_codigo_barras(self):
        """Buscar producto por código de barras y agregarlo automáticamente"""
        from controllers.products import buscar_por_codigo_barras
        
        codigo = self.search_entry.get().strip()
        
        if not codigo:
            return
        
        # Buscar por código de barras
        producto = buscar_por_codigo_barras(codigo)
        
        if producto:
            # Agregar automáticamente al carrito
            self.agregar_producto(producto)
            # Limpiar búsqueda
            self.search_entry.delete(0, 'end')
            messagebox.showinfo("Producto agregado", f"{producto.get('nombre')} agregado al carrito")
        else:
            # Si no se encuentra por código de barras, buscar normalmente
            self.filtrar_productos()
    
    def filtrar_productos(self):
        """Filtrar productos por búsqueda"""
        termino = self.search_entry.get().lower()
        
        if not termino:
            self.aplicar_filtros()
            return
        
        productos_filtrados = [
            p for p in self.productos
            if termino in p.get("nombre", "").lower() or
               termino in str(p.get("id_producto", "")).lower() or
               termino in str(p.get("codigo", "")).lower() or
               termino in str(p.get("codigo_barras", "")).lower()
        ]
        
        # Aplicar también filtro de categoría si hay uno activo
        if self.categoria_seleccionada != "Todas las Categorías":
            productos_filtrados = [
                p for p in productos_filtrados
                if p.get("categoria", "").lower() == self.categoria_seleccionada.lower()
            ]
        
        self.mostrar_productos(productos_filtrados)
    
    def filtrar_por_categoria(self, categoria):
        """Filtrar productos por categoría"""
        self.categoria_seleccionada = categoria
        
        # Actualizar estilos de botones
        for btn, cat in self.botones_categorias:
            if cat == categoria:
                btn.configure(
                    fg_color="#E91E63",
                    text_color="white",
                    border_width=0
                )
            else:
                btn.configure(
                    fg_color="white",
                    text_color="#666666",
                    border_width=1
                )
        
        self.aplicar_filtros()
    
    def aplicar_filtros(self):
        """Aplicar todos los filtros activos"""
        productos_filtrados = self.productos.copy()
        
        # Filtro de categoría
        if self.categoria_seleccionada != "Todas las Categorías":
            productos_filtrados = [
                p for p in productos_filtrados
                if p.get("categoria", "").lower() == self.categoria_seleccionada.lower()
            ]
        
        # Filtro de búsqueda
        termino = self.search_entry.get().lower()
        if termino:
            productos_filtrados = [
                p for p in productos_filtrados
                if termino in p.get("nombre", "").lower() or
                   termino in str(p.get("id_producto", "")).lower() or
                   termino in str(p.get("codigo", "")).lower() or
                   termino in str(p.get("codigo_barras", "")).lower()
            ]
        
        self.mostrar_productos(productos_filtrados)


if __name__ == "__main__":
    # Para pruebas independientes
    root = ctk.CTk()
    root.title("Janet Rosa Bici - Punto de Venta")
    root.geometry("1400x800")
    ctk.set_appearance_mode("light")
    
    usuario = {
        "id_usuario": 1,
        "nombre_completo": "Administrador",
        "email": "admin@janet.com"
    }
    
    app = PuntoVentaView(root, usuario=usuario)
    root.mainloop()
