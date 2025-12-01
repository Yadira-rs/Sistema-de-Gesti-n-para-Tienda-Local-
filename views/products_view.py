import customtkinter as ctk
from tkinter import messagebox
from controllers.products import obtener_productos, agregar_producto, ajustar_stock
from views.nuevo_producto_form_mejorado import NuevoProductoFormMejorado

class ProductsView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.user = user
        self.productos = []
        self.pack(fill="both", expand=True)

        # Header con título y botones
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 5))

        # Título
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame, 
            text="📦 Inventario y Productos", 
            font=("Segoe UI", 20, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame, 
            text="Gestión completa de productos y stock", 
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(anchor="w")

        # Botones de acción
        buttons_frame = ctk.CTkFrame(header, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        ctk.CTkButton(
            buttons_frame,
            text="+ Nuevo Producto",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=40,
            width=150,
            font=("Segoe UI", 12, "bold"),
            command=self.abrir_formulario_nuevo
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🔄 Actualizar",
            fg_color="#2196F3",
            hover_color="#1976D2",
            height=40,
            width=120,
            font=("Segoe UI", 12, "bold"),
            command=self.cargar_tabla_productos
        ).pack(side="left", padx=5)

        # Estadísticas
        self.crear_estadisticas()

        # Barra de búsqueda
        search_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10, height=45)
        search_frame.pack(fill="x", padx=20, pady=(10, 5))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 16)).pack(side="left", padx=10)
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar producto por nombre o código...",
            border_width=0,
            fg_color="white",
            font=("Segoe UI", 11)
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filtrar_productos())

        # Tabla de productos
        self.tabla_frame = ctk.CTkScrollableFrame(self, fg_color="white", corner_radius=10)
        self.tabla_frame.pack(fill="both", expand=True, padx=20, pady=(5, 10))

        self.cargar_tabla_productos()
    
    def crear_estadisticas(self):
        """Crear tarjetas de estadísticas"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=(5, 10))
        
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Total Productos
        card1 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=8)
        card1.grid(row=0, column=0, padx=5, sticky="ew")
        
        ctk.CTkLabel(card1, text="Total Productos", font=("Segoe UI", 10), text_color="#666666").pack(pady=(10, 2))
        self.total_productos_label = ctk.CTkLabel(card1, text="0", font=("Segoe UI", 20, "bold"), text_color="#333333")
        self.total_productos_label.pack(pady=(0, 10))
        
        # Stock Total
        card2 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=8)
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        
        ctk.CTkLabel(card2, text="Stock Total", font=("Segoe UI", 10), text_color="#666666").pack(pady=(10, 2))
        self.stock_total_label = ctk.CTkLabel(card2, text="0", font=("Segoe UI", 20, "bold"), text_color="#4CAF50")
        self.stock_total_label.pack(pady=(0, 10))
        
        # Stock Bajo
        card3 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=8)
        card3.grid(row=0, column=2, padx=5, sticky="ew")
        
        ctk.CTkLabel(card3, text="Stock Bajo", font=("Segoe UI", 10), text_color="#666666").pack(pady=(10, 2))
        self.stock_bajo_label = ctk.CTkLabel(card3, text="0", font=("Segoe UI", 20, "bold"), text_color="#E53935")
        self.stock_bajo_label.pack(pady=(0, 10))
        
        # Valor Total
        card4 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=8)
        card4.grid(row=0, column=3, padx=5, sticky="ew")
        
        ctk.CTkLabel(card4, text="Valor Total", font=("Segoe UI", 10), text_color="#666666").pack(pady=(10, 2))
        self.valor_total_label = ctk.CTkLabel(card4, text="$0.00", font=("Segoe UI", 20, "bold"), text_color="#FF9800")
        self.valor_total_label.pack(pady=(0, 10))

    def cargar_tabla_productos(self):
        """Carga o recarga los productos en la tabla."""
        # Limpiar el frame de la tabla
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        self.productos = obtener_productos()
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()

        # Header de la tabla
        header_frame = ctk.CTkFrame(self.tabla_frame, fg_color="#F5F5F5")
        header_frame.pack(fill="x", pady=(0, 5))

        headers = [("Código", 100), ("Nombre", 250), ("Precio", 100), ("Stock", 100), ("Valor", 120), ("Acciones", 150)]
        
        for header, width in headers:
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Segoe UI", 11, "bold"),
                text_color="#333333",
                width=width
            ).pack(side="left", padx=5)

        # Filas de productos
        for producto in self.productos:
            self.crear_fila_producto(producto)
    
    def actualizar_estadisticas(self):
        """Actualizar las tarjetas de estadísticas"""
        total = len(self.productos)
        stock_total = sum(p.get("stock", 0) for p in self.productos)
        stock_bajo = sum(1 for p in self.productos if p.get("stock", 0) < 10)
        valor_total = sum(float(p.get("precio", 0)) * int(p.get("stock", 0)) for p in self.productos)
        
        self.total_productos_label.configure(text=str(total))
        self.stock_total_label.configure(text=f"{stock_total} unid.")
        self.stock_bajo_label.configure(text=str(stock_bajo))
        self.valor_total_label.configure(text=f"${valor_total:,.2f}")
    
    def crear_fila_producto(self, producto):
        """Crear fila de producto"""
        fila = ctk.CTkFrame(self.tabla_frame, fg_color="white")
        fila.pack(fill="x", pady=1)
        
        # Código
        codigo = producto.get("codigo", producto.get("id_producto", "N/A"))
        ctk.CTkLabel(fila, text=str(codigo), font=("Segoe UI", 10), text_color="#666666", width=100).pack(side="left", padx=5)
        
        # Nombre
        nombre = producto.get("nombre", "N/A")
        ctk.CTkLabel(fila, text=nombre[:35], font=("Segoe UI", 10), text_color="#333333", width=250, anchor="w").pack(side="left", padx=5)
        
        # Precio
        precio = float(producto.get("precio", 0))
        ctk.CTkLabel(fila, text=f"${precio:.2f}", font=("Segoe UI", 10), text_color="#333333", width=100).pack(side="left", padx=5)
        
        # Stock con color
        stock = int(producto.get("stock", 0))
        color = "#E53935" if stock < 10 else "#FF9800" if stock < 20 else "#4CAF50"
        ctk.CTkLabel(fila, text=f"{stock} unid.", font=("Segoe UI", 10, "bold"), text_color=color, width=100).pack(side="left", padx=5)
        
        # Valor total
        valor = precio * stock
        ctk.CTkLabel(fila, text=f"${valor:,.2f}", font=("Segoe UI", 10), text_color="#333333", width=120).pack(side="left", padx=5)
        
        # Botón Ajustar
        ctk.CTkButton(
            fila,
            text="⚙ Ajustar",
            fg_color="transparent",
            text_color="#2196F3",
            hover_color="#E3F2FD",
            width=70,
            height=28,
            font=("Segoe UI", 10),
            command=lambda p=producto: self.ajustar_stock(p)
        ).pack(side="left", padx=2)
    
    def ajustar_stock(self, producto):
        """Ajustar stock de un producto"""
        from tkinter import simpledialog
        
        cantidad = simpledialog.askinteger(
            "Ajustar Stock",
            f"Producto: {producto['nombre']}\nStock actual: {producto['stock']}\n\nIngresa la cantidad:",
            parent=self,
            minvalue=0
        )
        
        if cantidad is None:
            return
        
        tipo = simpledialog.askstring(
            "Tipo de Ajuste",
            "Tipo de ajuste:\n- Entrada (agregar stock)\n- Salida (quitar stock)\n\nEscribe 'Entrada' o 'Salida':",
            parent=self
        )
        
        if tipo and tipo.capitalize() in ["Entrada", "Salida"]:
            try:
                ajustar_stock(producto['id_producto'], cantidad, tipo.capitalize())
                messagebox.showinfo("Éxito", f"Stock ajustado correctamente\n\nTipo: {tipo}\nCantidad: {cantidad}")
                self.cargar_tabla_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo ajustar el stock: {str(e)}")
        else:
            messagebox.showwarning("Tipo inválido", "Debes escribir 'Entrada' o 'Salida'")
    
    def filtrar_productos(self):
        """Filtrar productos por búsqueda"""
        termino = self.search_entry.get().lower()
        
        # Limpiar tabla
        for widget in self.tabla_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.tabla_frame.winfo_children()[0]:
                widget.destroy()
        
        # Filtrar y mostrar
        productos_filtrados = [
            p for p in self.productos
            if termino in p.get("nombre", "").lower() or
               termino in str(p.get("codigo", "")).lower()
        ]
        
        for producto in productos_filtrados:
            self.crear_fila_producto(producto)

    def abrir_formulario_nuevo(self):
        """Abre la ventana para crear un nuevo producto."""
        def handle_creacion():
            self.cargar_tabla_productos()

        # Usa el formulario mejorado con código de barras
        NuevoProductoFormMejorado(self, on_create=handle_creacion)
