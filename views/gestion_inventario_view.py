import customtkinter as ctk
from tkinter import messagebox, simpledialog
from controllers.products import obtener_productos, ajustar_stock, obtener_categorias

class GestionInventarioView(ctk.CTk):
    def __init__(self, usuario=None):
        super().__init__()
        self.title("Janet Rosa Bici - Gestión de Inventario")
        self.geometry("1400x800")
        ctk.set_appearance_mode("light")
        
        self.usuario = usuario or {"nombre_completo": "Administrador", "email": "admin@janet.com"}
        self.productos = []
        self.productos_filtrados = []
        self.categoria_filtro = "Todas las categorías"
        self.nivel_filtro = "Todos los niveles"
        
        self.crear_interfaz()
        self.cargar_datos()
    
    def crear_interfaz(self):
        # Contenedor principal
        main = ctk.CTkFrame(self, fg_color="#F5F5F5")
        main.pack(fill="both", expand=True)
        
        # Sidebar izquierdo
        self.crear_sidebar(main)
        
        # Panel principal
        self.crear_panel_principal(main)

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
            ("📦", "Inventario"),
            ("💰", "Ventas"),
            ("👥", "Usuarios")
        ]
        
        for icon, text in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icon}  {text}",
                fg_color="#F8BBD0" if text == "Inventario" else "transparent",
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
        ctk.CTkLabel(user_frame, text="Admin", font=("Segoe UI", 10), text_color="#666666").pack()
        ctk.CTkLabel(user_frame, text=self.usuario.get("email", "admin@janet.com"), 
                    font=("Segoe UI", 9), text_color="#999999").pack(pady=(0, 10))

    def crear_panel_principal(self, parent):
        """Panel principal con inventario"""
        panel = ctk.CTkFrame(parent, fg_color="#F5F5F5")
        panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Header con título y botones
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        # Título y subtítulo
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(title_frame, text="Gestión de Inventario", font=("Segoe UI", 24, "bold"), 
                    text_color="#333333", anchor="w").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Controla y ajusta el stock de tus productos", 
                    font=("Segoe UI", 12), text_color="#666666", anchor="w").pack(anchor="w")
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(header, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        ctk.CTkButton(
            buttons_frame,
            text="+ Nuevo Producto",
            fg_color="#4CAF50",
            hover_color="#45a049",
            corner_radius=20,
            height=45,
            width=180,
            font=("Segoe UI", 13, "bold"),
            command=self.nuevo_producto
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="📊 Exportar",
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=20,
            height=45,
            width=140,
            font=("Segoe UI", 12, "bold"),
            command=self.exportar_inventario
        ).pack(side="left", padx=5)
        
        # Tarjetas de estadísticas
        self.crear_tarjetas_estadisticas(panel)
        
        # Filtros
        self.crear_filtros(panel)
        
        # Tabla de productos
        self.crear_tabla_productos(panel)

    def crear_tarjetas_estadisticas(self, parent):
        """Crear tarjetas con estadísticas del inventario"""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 15))
        
        # Configurar grid
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Tarjeta 1: Total Productos
        card1 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card1.grid(row=0, column=0, padx=5, sticky="ew")
        
        icon_frame1 = ctk.CTkFrame(card1, fg_color="#E3F2FD", corner_radius=8, width=50, height=50)
        icon_frame1.pack(side="left", padx=15, pady=15)
        icon_frame1.pack_propagate(False)
        ctk.CTkLabel(icon_frame1, text="📦", font=("Segoe UI", 24)).pack(expand=True)
        
        info_frame1 = ctk.CTkFrame(card1, fg_color="transparent")
        info_frame1.pack(side="left", fill="both", expand=True, pady=15)
        ctk.CTkLabel(info_frame1, text="Total Productos", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.total_productos_label = ctk.CTkLabel(info_frame1, text="8", 
                    font=("Segoe UI", 24, "bold"), text_color="#333333", anchor="w")
        self.total_productos_label.pack(anchor="w")
        
        # Tarjeta 2: Stock Total
        card2 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        
        icon_frame2 = ctk.CTkFrame(card2, fg_color="#E8F5E9", corner_radius=8, width=50, height=50)
        icon_frame2.pack(side="left", padx=15, pady=15)
        icon_frame2.pack_propagate(False)
        ctk.CTkLabel(icon_frame2, text="📈", font=("Segoe UI", 24)).pack(expand=True)
        
        info_frame2 = ctk.CTkFrame(card2, fg_color="transparent")
        info_frame2.pack(side="left", fill="both", expand=True, pady=15)
        ctk.CTkLabel(info_frame2, text="Stock Total", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.stock_total_label = ctk.CTkLabel(info_frame2, text="99 unidades", 
                    font=("Segoe UI", 24, "bold"), text_color="#333333", anchor="w")
        self.stock_total_label.pack(anchor="w")
        
        # Tarjeta 3: Stock Bajo
        card3 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card3.grid(row=0, column=2, padx=5, sticky="ew")
        
        icon_frame3 = ctk.CTkFrame(card3, fg_color="#FFEBEE", corner_radius=8, width=50, height=50)
        icon_frame3.pack(side="left", padx=15, pady=15)
        icon_frame3.pack_propagate(False)
        ctk.CTkLabel(icon_frame3, text="⚠️", font=("Segoe UI", 24)).pack(expand=True)
        
        info_frame3 = ctk.CTkFrame(card3, fg_color="transparent")
        info_frame3.pack(side="left", fill="both", expand=True, pady=15)
        ctk.CTkLabel(info_frame3, text="Stock Bajo", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.stock_bajo_label = ctk.CTkLabel(info_frame3, text="6 productos", 
                    font=("Segoe UI", 24, "bold"), text_color="#E53935", anchor="w")
        self.stock_bajo_label.pack(anchor="w")
        
        # Tarjeta 4: Valor Total
        card4 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card4.grid(row=0, column=3, padx=5, sticky="ew")
        
        icon_frame4 = ctk.CTkFrame(card4, fg_color="#FFF3E0", corner_radius=8, width=50, height=50)
        icon_frame4.pack(side="left", padx=15, pady=15)
        icon_frame4.pack_propagate(False)
        ctk.CTkLabel(icon_frame4, text="📊", font=("Segoe UI", 24)).pack(expand=True)
        
        info_frame4 = ctk.CTkFrame(card4, fg_color="transparent")
        info_frame4.pack(side="left", fill="both", expand=True, pady=15)
        ctk.CTkLabel(info_frame4, text="Valor Total", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.valor_total_label = ctk.CTkLabel(info_frame4, text="$16,014.02", 
                    font=("Segoe UI", 24, "bold"), text_color="#333333", anchor="w")
        self.valor_total_label.pack(anchor="w")

    def crear_filtros(self, parent):
        """Crear barra de filtros"""
        filtros_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(0, 10))
        
        # Búsqueda
        search_frame = ctk.CTkFrame(filtros_frame, fg_color="white", corner_radius=10, height=45)
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 16)).pack(side="left", padx=10)
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar producto...",
            border_width=0,
            fg_color="white",
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filtrar_productos())
        
        # Filtro de categoría
        self.categoria_combo = ctk.CTkComboBox(
            filtros_frame,
            values=["Todas las categorías", "Ropa", "Calzado", "Accesorios"],
            width=200,
            height=45,
            corner_radius=10,
            font=("Segoe UI", 12),
            command=lambda e: self.filtrar_productos()
        )
        self.categoria_combo.set("Todas las categorías")
        self.categoria_combo.pack(side="left", padx=5)
        
        # Filtro de nivel de stock
        self.nivel_combo = ctk.CTkComboBox(
            filtros_frame,
            values=["Todos los niveles", "Stock bajo", "Stock medio", "Stock alto"],
            width=200,
            height=45,
            corner_radius=10,
            font=("Segoe UI", 12),
            command=lambda e: self.filtrar_productos()
        )
        self.nivel_combo.set("Todos los niveles")
        self.nivel_combo.pack(side="left", padx=5)
    
    def crear_tabla_productos(self, parent):
        """Crear tabla de productos"""
        # Contenedor de la tabla
        tabla_container = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        tabla_container.pack(fill="both", expand=True)
        
        # Header de la tabla
        header_frame = ctk.CTkFrame(tabla_container, fg_color="#F5F5F5", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        headers = [
            ("Código", 100),
            ("Producto", 250),
            ("Categoría", 150),
            ("Precio", 100),
            ("Stock Actual", 120),
            ("Valor Total", 120),
            ("Acción", 100)
        ]
        
        for i, (header, width) in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Segoe UI", 12, "bold"),
                text_color="#333333",
                width=width,
                anchor="w" if i < len(headers) - 1 else "center"
            )
            label.pack(side="left", padx=10, pady=12)
        
        # Scroll frame para productos
        self.productos_scroll = ctk.CTkScrollableFrame(tabla_container, fg_color="white")
        self.productos_scroll.pack(fill="both", expand=True, padx=0, pady=0)

    def cargar_datos(self):
        """Cargar productos desde la base de datos"""
        try:
            self.productos = obtener_productos()
            self.actualizar_estadisticas()
            self.mostrar_productos(self.productos)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {str(e)}")
            self.productos = []
    
    def actualizar_estadisticas(self):
        """Actualizar las tarjetas de estadísticas"""
        total_productos = len(self.productos)
        stock_total = sum(p.get("stock", 0) for p in self.productos)
        stock_bajo = sum(1 for p in self.productos if p.get("stock", 0) < 10)
        valor_total = sum(float(p.get("precio", 0)) * int(p.get("stock", 0)) for p in self.productos)
        
        self.total_productos_label.configure(text=str(total_productos))
        self.stock_total_label.configure(text=f"{stock_total} unidades")
        self.stock_bajo_label.configure(text=f"{stock_bajo} productos")
        self.valor_total_label.configure(text=f"${valor_total:,.2f}")
    
    def mostrar_productos(self, productos):
        """Mostrar productos en la tabla"""
        # Limpiar tabla actual
        for widget in self.productos_scroll.winfo_children():
            widget.destroy()
        
        # Mostrar cada producto
        for producto in productos:
            self.crear_fila_producto(self.productos_scroll, producto)
    
    def crear_fila_producto(self, parent, producto):
        """Crear fila individual de producto"""
        fila = ctk.CTkFrame(parent, fg_color="white", height=60)
        fila.pack(fill="x", padx=0, pady=1)
        
        # Código
        codigo = producto.get("codigo") or producto.get("id_producto", "N/A")
        ctk.CTkLabel(
            fila,
            text=str(codigo),
            font=("Segoe UI", 11),
            text_color="#666666",
            width=100,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Producto
        nombre = producto.get("nombre", "N/A")
        ctk.CTkLabel(
            fila,
            text=nombre[:35] + "..." if len(nombre) > 35 else nombre,
            font=("Segoe UI", 11),
            text_color="#333333",
            width=250,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Categoría (badge rosa)
        categoria_frame = ctk.CTkFrame(fila, fg_color="transparent", width=150)
        categoria_frame.pack(side="left", padx=10)
        
        badge = ctk.CTkFrame(categoria_frame, fg_color="#FFE0E0", corner_radius=12, height=24)
        badge.pack(anchor="w")
        
        ctk.CTkLabel(
            badge,
            text="Ropa",
            font=("Segoe UI", 10),
            text_color="#E91E63"
        ).pack(padx=12, pady=2)
        
        # Precio
        precio = float(producto.get("precio", 0))
        ctk.CTkLabel(
            fila,
            text=f"${precio:.2f}",
            font=("Segoe UI", 11),
            text_color="#333333",
            width=100,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Stock Actual (badge verde)
        stock = int(producto.get("stock", 0))
        stock_frame = ctk.CTkFrame(fila, fg_color="transparent", width=120)
        stock_frame.pack(side="left", padx=10)
        
        # Color según nivel de stock
        if stock < 10:
            bg_color = "#FFEBEE"
            text_color = "#E53935"
        elif stock < 20:
            bg_color = "#FFF9C4"
            text_color = "#F57C00"
        else:
            bg_color = "#E8F5E9"
            text_color = "#43A047"
        
        stock_badge = ctk.CTkFrame(stock_frame, fg_color=bg_color, corner_radius=12, height=24)
        stock_badge.pack(anchor="w")
        
        ctk.CTkLabel(
            stock_badge,
            text=f"{stock} unidades",
            font=("Segoe UI", 10, "bold"),
            text_color=text_color
        ).pack(padx=12, pady=2)
        
        # Valor Total
        valor_total = precio * stock
        ctk.CTkLabel(
            fila,
            text=f"${valor_total:,.2f}",
            font=("Segoe UI", 11, "bold"),
            text_color="#333333",
            width=120,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Botón Ajustar
        ctk.CTkButton(
            fila,
            text="Ajustar",
            fg_color="transparent",
            text_color="#E91E63",
            hover_color="#FFE0E0",
            border_width=1,
            border_color="#E91E63",
            corner_radius=8,
            width=80,
            height=32,
            font=("Segoe UI", 11),
            command=lambda p=producto: self.ajustar_stock_producto(p)
        ).pack(side="left", padx=10)

    def filtrar_productos(self):
        """Filtrar productos según búsqueda y filtros"""
        termino = self.search_entry.get().lower()
        categoria = self.categoria_combo.get()
        nivel = self.nivel_combo.get()
        
        productos_filtrados = self.productos.copy()
        
        # Filtrar por búsqueda
        if termino:
            productos_filtrados = [
                p for p in productos_filtrados
                if termino in p.get("nombre", "").lower() or
                   termino in str(p.get("codigo", "")).lower() or
                   termino in str(p.get("id_producto", "")).lower()
            ]
        
        # Filtrar por nivel de stock
        if nivel == "Stock bajo":
            productos_filtrados = [p for p in productos_filtrados if p.get("stock", 0) < 10]
        elif nivel == "Stock medio":
            productos_filtrados = [p for p in productos_filtrados if 10 <= p.get("stock", 0) < 20]
        elif nivel == "Stock alto":
            productos_filtrados = [p for p in productos_filtrados if p.get("stock", 0) >= 20]
        
        self.mostrar_productos(productos_filtrados)
    
    def ajustar_stock_producto(self, producto):
        """Abrir diálogo para ajustar stock"""
        # Crear ventana de diálogo personalizada
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajustar Stock")
        dialog.geometry("400x350")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"400x350+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(dialog, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="Ajustar Stock",
            font=("Segoe UI", 20, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            main_frame,
            text=producto.get("nombre", "Producto"),
            font=("Segoe UI", 14),
            text_color="#666666"
        ).pack(pady=(0, 20))
        
        # Stock actual
        stock_actual = int(producto.get("stock", 0))
        ctk.CTkLabel(
            main_frame,
            text=f"Stock actual: {stock_actual} unidades",
            font=("Segoe UI", 12, "bold"),
            text_color="#E91E63"
        ).pack(pady=(0, 20))
        
        # Tipo de ajuste
        ctk.CTkLabel(
            main_frame,
            text="Tipo de ajuste",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        tipo_var = ctk.StringVar(value="Entrada")
        tipo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tipo_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkRadioButton(
            tipo_frame,
            text="Entrada (agregar)",
            variable=tipo_var,
            value="Entrada",
            font=("Segoe UI", 11)
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            tipo_frame,
            text="Salida (quitar)",
            variable=tipo_var,
            value="Salida",
            font=("Segoe UI", 11)
        ).pack(side="left", padx=10)
        
        # Cantidad
        ctk.CTkLabel(
            main_frame,
            text="Cantidad",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        cantidad_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ingresa la cantidad",
            height=40,
            font=("Segoe UI", 12)
        )
        cantidad_entry.pack(fill="x", pady=(0, 20))
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        def aplicar_ajuste():
            try:
                cantidad = int(cantidad_entry.get())
                if cantidad <= 0:
                    messagebox.showwarning("Cantidad inválida", "La cantidad debe ser mayor a 0")
                    return
                
                tipo = tipo_var.get()
                
                # Validar que no se quite más stock del disponible
                if tipo == "Salida" and cantidad > stock_actual:
                    messagebox.showwarning("Stock insuficiente", f"No puedes quitar {cantidad} unidades. Stock actual: {stock_actual}")
                    return
                
                # Aplicar ajuste
                if ajustar_stock(producto["id_producto"], cantidad, tipo):
                    messagebox.showinfo("Éxito", f"Stock ajustado correctamente\n\nTipo: {tipo}\nCantidad: {cantidad}")
                    dialog.destroy()
                    self.cargar_datos()
                else:
                    messagebox.showerror("Error", "No se pudo ajustar el stock")
            
            except ValueError:
                messagebox.showwarning("Cantidad inválida", "Ingresa un número válido")
        
        ctk.CTkButton(
            btn_frame,
            text="Aplicar",
            fg_color="#E91E63",
            hover_color="#C2185B",
            height=40,
            font=("Segoe UI", 12, "bold"),
            command=aplicar_ajuste
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="white",
            text_color="#666666",
            border_width=2,
            border_color="#E0E0E0",
            hover_color="#F5F5F5",
            height=40,
            font=("Segoe UI", 12),
            command=dialog.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))


if __name__ == "__main__":
    app = GestionInventarioView()
    app.mainloop()

    def nuevo_producto(self):
        """Abrir formulario para agregar nuevo producto"""
        from views.nuevo_producto_form_mejorado import NuevoProductoFormMejorado
        
        def on_producto_creado():
            self.cargar_datos()
        
        NuevoProductoFormMejorado(self, on_create=on_producto_creado)
    
    def exportar_inventario(self):
        """Exportar inventario a CSV"""
        try:
            import csv
            from datetime import datetime
            
            # Generar nombre de archivo con fecha
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"inventario_{fecha}.csv"
            
            # Crear archivo CSV
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Escribir encabezados
                writer.writerow(['Código', 'Código Barras', 'Nombre', 'Precio', 'Stock', 'Valor Total'])
                
                # Escribir datos
                for producto in self.productos:
                    codigo = producto.get('codigo', 'N/A')
                    codigo_barras = producto.get('codigo_barras', 'N/A')
                    nombre = producto.get('nombre', 'N/A')
                    precio = float(producto.get('precio', 0))
                    stock = int(producto.get('stock', 0))
                    valor_total = precio * stock
                    
                    writer.writerow([codigo, codigo_barras, nombre, f"${precio:.2f}", stock, f"${valor_total:.2f}"])
            
            messagebox.showinfo("Exportación exitosa", f"Inventario exportado a:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el inventario: {str(e)}")
