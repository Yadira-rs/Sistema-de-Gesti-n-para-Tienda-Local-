import customtkinter as ctk
from tkinter import messagebox
from controllers.products import obtener_productos, buscar_por_codigo_barras
from controllers.ventas import agregar_al_carrito, obtener_carrito, finalizar_venta, vaciar_carrito

class VentasView(ctk.CTkFrame):
    """Punto de Venta Moderno - Estilo Janet Rosa Bici"""
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.user = user or {"id_usuario": 1, "nombre_completo": "Administrador"}
        self.carrito = []
        self.metodo_pago = ctk.StringVar(value="Efectivo")
        self.descuento_porcentaje = ctk.DoubleVar(value=0.0)
        
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
        
        # Contenedor principal
        body = ctk.CTkFrame(main, fg_color="transparent")
        body.pack(fill="both", expand=True)
        
        # Panel izquierdo - Productos (70%)
        left_panel = ctk.CTkFrame(body, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Panel derecho - Carrito (ancho ajustado para 3 botones)
        right_panel = ctk.CTkFrame(body, width=450, fg_color="white", corner_radius=15)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        self.crear_seccion_productos(left_panel)
        self.crear_seccion_carrito(right_panel)
    
    def crear_seccion_productos(self, parent):
        """Sección de productos con búsqueda y grid"""
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, height=55)
        search_frame.pack(fill="x", pady=(0, 15))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Segoe UI", 18),
            text_color="#999999"
        ).pack(side="left", padx=15)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Escanear código de barras o buscar producto...",
            border_width=0,
            fg_color="white",
            font=("Segoe UI", 13),
            text_color="#2C2C2C"
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.manejar_busqueda(e))
        self.search_entry.bind("<Return>", lambda e: self.procesar_codigo_escaneado())
        
        # Botón para producto personalizado
        self.boton_otro = ctk.CTkButton(
            parent,
            text="➕ Agregar Producto Personalizado",
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            height=38,
            font=("Segoe UI", 12, "bold"),
            command=self.agregar_producto_personalizado
        )
        self.boton_otro.pack(fill="x", pady=(0, 15))
        
        # Grid de productos
        self.productos_scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.productos_scroll.pack(fill="both", expand=True)
        
        self.productos_grid = ctk.CTkFrame(self.productos_scroll, fg_color="transparent")
        self.productos_grid.pack(fill="both", expand=True)
    
    def crear_seccion_carrito(self, parent):
        """Sección del carrito de compras"""
        # Header
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
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
            text="Carrito",
            font=("Segoe UI", 18, "bold"),
            text_color="#2C2C2C"
        ).pack(side="left")
        
        # Botón limpiar
        ctk.CTkButton(
            header,
            text="🗑️",
            width=40,
            height=40,
            fg_color="#FFE4E1",
            text_color="#E91E63",
            hover_color="#FFD0D0",
            font=("Segoe UI", 18),
            corner_radius=10,
            command=self.limpiar_carrito
        ).pack(side="right")
        
        # Contador
        self.contador_label = ctk.CTkLabel(
            parent,
            text="0 productos",
            font=("Segoe UI", 12),
            text_color="#666666"
        )
        self.contador_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Lista de productos (altura ajustada)
        self.carrito_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            height=200
        )
        self.carrito_scroll.pack(fill="x", padx=15, pady=(0, 10))
        
        # Descuento (compacto y centrado)
        desc_frame = ctk.CTkFrame(parent, fg_color="#FFF9F5", corner_radius=8)
        desc_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        desc_input = ctk.CTkFrame(desc_frame, fg_color="transparent")
        desc_input.pack(fill="x", padx=8, pady=8)
        
        ctk.CTkLabel(
            desc_input,
            text="💰 Descuento:",
            font=("Segoe UI", 11, "bold"),
            text_color="#666666"
        ).pack(side="left", padx=(5, 10))
        
        self.descuento_entry = ctk.CTkEntry(
            desc_input,
            textvariable=self.descuento_porcentaje,
            width=50,
            height=32,
            corner_radius=6,
            font=("Segoe UI", 11),
            placeholder_text="0"
        )
        self.descuento_entry.pack(side="left", padx=(0, 5))
        self.descuento_entry.bind("<KeyRelease>", lambda e: self.actualizar_totales())
        
        ctk.CTkLabel(
            desc_input,
            text="%",
            font=("Segoe UI", 11, "bold"),
            text_color="#666666"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            desc_input,
            text="Aplicar",
            width=70,
            height=32,
            fg_color="#FF9800",
            hover_color="#F57C00",
            corner_radius=6,
            font=("Segoe UI", 10, "bold"),
            command=self.actualizar_totales
        ).pack(side="left")
        
        # Método de pago (más compacto y ajustado)
        pago_frame = ctk.CTkFrame(parent, fg_color="#F5F5F5", corner_radius=8)
        pago_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(
            pago_frame,
            text="Método de pago",
            font=("Segoe UI", 11, "bold"),
            text_color="#2C2C2C"
        ).pack(anchor="w", padx=12, pady=(8, 5))
        
        metodos_frame = ctk.CTkFrame(pago_frame, fg_color="transparent")
        metodos_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Configurar grid para 3 columnas iguales
        metodos_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.metodo_btns = {}
        metodos = [
            ("💵", "Efectivo"),
            ("💳", "Tarjeta"),
            ("📱", "Transferencia")
        ]
        
        for i, (icono, metodo) in enumerate(metodos):
            btn = ctk.CTkButton(
                metodos_frame,
                text=f"{icono}\n{metodo}",
                fg_color="#E91E63" if metodo == "Efectivo" else "white",
                text_color="white" if metodo == "Efectivo" else "#666666",
                border_width=2 if metodo != "Efectivo" else 0,
                border_color="#E0E0E0",
                hover_color="#C2185B" if metodo == "Efectivo" else "#F5F5F5",
                corner_radius=10,
                height=60,
                font=("Segoe UI", 9, "bold"),
                command=lambda m=metodo: self.seleccionar_metodo(m)
            )
            btn.grid(row=0, column=i, padx=3, sticky="ew")
            self.metodo_btns[metodo] = btn
        
        # Totales (más compacto)
        totales_frame = ctk.CTkFrame(parent, fg_color="#FFF0F5", corner_radius=8)
        totales_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Subtotal
        subtotal_row = ctk.CTkFrame(totales_frame, fg_color="transparent")
        subtotal_row.pack(fill="x", padx=12, pady=(8, 3))
        
        ctk.CTkLabel(subtotal_row, text="Subtotal:", font=("Segoe UI", 11)).pack(side="left")
        self.subtotal_label = ctk.CTkLabel(subtotal_row, text="$0.00", font=("Segoe UI", 11))
        self.subtotal_label.pack(side="right")
        
        # Descuento
        descuento_row = ctk.CTkFrame(totales_frame, fg_color="transparent")
        descuento_row.pack(fill="x", padx=12, pady=3)
        
        ctk.CTkLabel(descuento_row, text="Descuento:", font=("Segoe UI", 11), text_color="#FF9800").pack(side="left")
        self.descuento_label = ctk.CTkLabel(descuento_row, text="- $0.00", font=("Segoe UI", 11), text_color="#FF9800")
        self.descuento_label.pack(side="right")
        
        # Separador
        ctk.CTkFrame(totales_frame, height=1, fg_color="#E0E0E0").pack(fill="x", padx=12, pady=4)
        
        # Total
        total_row = ctk.CTkFrame(totales_frame, fg_color="transparent")
        total_row.pack(fill="x", padx=12, pady=(3, 8))
        
        ctk.CTkLabel(total_row, text="Total:", font=("Segoe UI", 14, "bold")).pack(side="left")
        self.total_label = ctk.CTkLabel(total_row, text="$0.00", font=("Segoe UI", 14, "bold"), text_color="#E91E63")
        self.total_label.pack(side="right")
        
        # Botón procesar venta (destacado)
        ctk.CTkButton(
            parent,
            text="💳 Procesar Venta",
            fg_color="#E91E63",
            hover_color="#C2185B",
            corner_radius=10,
            height=50,
            font=("Segoe UI", 14, "bold"),
            command=self.procesar_venta
        ).pack(fill="x", padx=20, pady=(0, 20))

    
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
        for widget in self.productos_grid.winfo_children():
            widget.destroy()
        
        # Grid de 3 columnas
        for i, producto in enumerate(productos):
            row = i // 3
            col = i % 3
            self.crear_tarjeta_producto(self.productos_grid, producto, row, col)
    
    def crear_tarjeta_producto(self, parent, producto, row, col):
        """Crear tarjeta de producto"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, width=220, height=280)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        card.grid_propagate(False)
        
        # Hacer clickeable
        card.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        card.configure(cursor="hand2")
        
        # Icono
        icon_frame = ctk.CTkFrame(card, fg_color="#FFE4E1", corner_radius=10, height=140)
        icon_frame.pack(fill="x", padx=12, pady=12)
        icon_frame.pack_propagate(False)
        icon_frame.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        icon = ctk.CTkLabel(icon_frame, text="🛍️", font=("Segoe UI", 50))
        icon.pack(expand=True)
        icon.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Info
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        info.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Nombre
        nombre = producto.get("nombre", "Producto")
        nombre_label = ctk.CTkLabel(
            info,
            text=nombre[:30] + "..." if len(nombre) > 30 else nombre,
            font=("Segoe UI", 12, "bold"),
            text_color="#2C2C2C",
            wraplength=190,
            anchor="w"
        )
        nombre_label.pack(anchor="w", pady=(0, 8))
        nombre_label.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Precio y stock
        bottom = ctk.CTkFrame(info, fg_color="transparent")
        bottom.pack(fill="x", side="bottom")
        bottom.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        precio = float(producto.get("precio", 0))
        stock = int(producto.get("stock", 0))
        
        precio_label = ctk.CTkLabel(
            bottom,
            text=f"${precio:.2f}",
            font=("Segoe UI", 16, "bold"),
            text_color="#E91E63"
        )
        precio_label.pack(side="left")
        precio_label.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        stock_color = "#4CAF50" if stock > 10 else "#FF9800" if stock > 0 else "#F44336"
        stock_label = ctk.CTkLabel(
            bottom,
            text=f"Stock: {stock}",
            font=("Segoe UI", 10),
            text_color=stock_color
        )
        stock_label.pack(side="right")
        stock_label.bind("<Button-1>", lambda e, p=producto: self.agregar_producto(p))
        
        # Hover effect
        def on_enter(e):
            card.configure(fg_color="#FFF5F8")
        
        def on_leave(e):
            card.configure(fg_color="white")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
    
    def agregar_producto(self, producto):
        """Agregar producto al carrito"""
        stock = int(producto.get("stock", 0))
        if stock <= 0:
            messagebox.showwarning("Sin stock", f"El producto '{producto.get('nombre')}' no tiene stock disponible")
            return
        
        # Buscar si ya existe
        for item in self.carrito:
            if item["id_producto"] == producto["id_producto"]:
                if item["cantidad"] < stock:
                    item["cantidad"] += 1
                    self.actualizar_carrito()
                    return
                else:
                    messagebox.showwarning("Stock insuficiente", f"No hay más stock disponible")
                    return
        
        # Agregar nuevo
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
        for widget in self.carrito_scroll.winfo_children():
            widget.destroy()
        
        total_items = sum(item["cantidad"] for item in self.carrito)
        self.contador_label.configure(text=f"{total_items} producto{'s' if total_items != 1 else ''}")
        
        for item in self.carrito:
            self.crear_item_carrito(self.carrito_scroll, item)
        
        self.actualizar_totales()
    
    def crear_item_carrito(self, parent, item):
        """Crear item en el carrito"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#F0F0F0")
        card.pack(fill="x", pady=5, padx=5)
        
        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=12, pady=12)
        
        # Nombre
        nombre = item["nombre"]
        ctk.CTkLabel(
            container,
            text=nombre[:25] + "..." if len(nombre) > 25 else nombre,
            font=("Segoe UI", 11, "bold"),
            text_color="#2C2C2C",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        # Fila inferior
        bottom_row = ctk.CTkFrame(container, fg_color="transparent")
        bottom_row.pack(fill="x")
        
        # Precio unitario
        ctk.CTkLabel(
            bottom_row,
            text=f"${item['precio']:.2f}",
            font=("Segoe UI", 11),
            text_color="#E91E63"
        ).pack(side="left")
        
        # Subtotal
        subtotal = item["precio"] * item["cantidad"]
        ctk.CTkLabel(
            bottom_row,
            text=f"${subtotal:.2f}",
            font=("Segoe UI", 12, "bold"),
            text_color="#2C2C2C"
        ).pack(side="right")
        
        # Controles de cantidad
        qty_frame = ctk.CTkFrame(bottom_row, fg_color="#F8F8F8", corner_radius=8, height=32)
        qty_frame.pack(side="right", padx=(0, 15))
        
        ctk.CTkButton(
            qty_frame,
            text="−",
            width=30,
            height=30,
            fg_color="transparent",
            text_color="#666666",
            hover_color="#E0E0E0",
            font=("Segoe UI", 14),
            command=lambda: self.cambiar_cantidad(item, -1)
        ).pack(side="left", padx=2, pady=2)
        
        ctk.CTkLabel(
            qty_frame,
            text=str(item["cantidad"]),
            font=("Segoe UI", 12, "bold"),
            text_color="#2C2C2C",
            width=35
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            qty_frame,
            text="+",
            width=30,
            height=30,
            fg_color="transparent",
            text_color="#666666",
            hover_color="#E0E0E0",
            font=("Segoe UI", 14),
            command=lambda: self.cambiar_cantidad(item, 1)
        ).pack(side="left", padx=2, pady=2)
    
    def cambiar_cantidad(self, item, delta):
        """Cambiar cantidad de un producto"""
        nueva_cantidad = item["cantidad"] + delta
        
        if nueva_cantidad <= 0:
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
            descuento_pct = max(0, min(100, descuento_pct))
        except:
            descuento_pct = 0
            self.descuento_porcentaje.set(0)
        
        descuento_monto = subtotal * (descuento_pct / 100)
        total = subtotal - descuento_monto
        
        self.subtotal_label.configure(text=f"${subtotal:.2f}")
        self.descuento_label.configure(text=f"- ${descuento_monto:.2f}")
        self.total_label.configure(text=f"${total:.2f}")
    
    def seleccionar_metodo(self, metodo):
        """Cambiar método de pago"""
        self.metodo_pago.set(metodo)
        
        for nombre, btn in self.metodo_btns.items():
            if nombre == metodo:
                btn.configure(fg_color="#E91E63", text_color="white", border_width=0)
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
        """Procesar la venta y generar ticket"""
        if not self.carrito:
            messagebox.showwarning("Carrito vacío", "Agrega productos al carrito antes de procesar la venta")
            return
        
        subtotal = sum(item["precio"] * item["cantidad"] for item in self.carrito)
        descuento_pct = float(self.descuento_porcentaje.get())
        descuento_monto = subtotal * (descuento_pct / 100)
        total = subtotal - descuento_monto
        metodo = self.metodo_pago.get()
        
        mensaje = f"¿Confirmar venta?\n\nSubtotal: ${subtotal:.2f}\n"
        if descuento_pct > 0:
            mensaje += f"Descuento ({descuento_pct}%): -${descuento_monto:.2f}\n"
        mensaje += f"Total: ${total:.2f}\nMétodo de pago: {metodo}"
        
        if not messagebox.askyesno("Confirmar venta", mensaje):
            return
        
        try:
            from controllers.products import crear_producto_temporal
            
            vaciar_carrito()
            
            # Procesar productos personalizados primero
            for item in self.carrito:
                # Si es un producto personalizado (CUSTOM_), crear producto temporal
                if isinstance(item["id_producto"], str) and item["id_producto"].startswith("CUSTOM_"):
                    id_temporal = crear_producto_temporal(item["nombre"], item["precio"])
                    item["id_producto"] = id_temporal
                
                producto_data = {
                    "id_producto": item["id_producto"],
                    "nombre": item["nombre"],
                    "precio": item["precio"]
                }
                agregar_al_carrito(producto_data, item["cantidad"])
            
            resultado = finalizar_venta(
                usuario_id=self.user.get("id_usuario"),
                metodo=metodo,
                descuento_porcentaje=descuento_pct
            )
            
            if resultado:
                # Preparar datos para el ticket
                ticket_data = {
                    'id_venta': resultado.get('id_venta'),
                    'total': total,
                    'metodo': metodo,
                    'descuento': descuento_monto,
                    'items': self.carrito.copy()
                }
                
                # Mostrar ticket
                from views.ticket_venta_view import TicketVentaView
                TicketVentaView(self, ticket_data)
                
                # Limpiar carrito
                self.carrito.clear()
                self.descuento_porcentaje.set(0)
                self.actualizar_carrito()
                self.cargar_productos()
            else:
                messagebox.showerror("Error", "No se pudo procesar la venta")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la venta: {str(e)}")
    
    def manejar_busqueda(self, event):
        """Manejar búsqueda en tiempo real"""
        # Si el texto tiene más de 8 caracteres, podría ser un código de barras
        texto = self.search_entry.get().strip()
        
        if len(texto) >= 8 and texto.isdigit():
            # Esperar un momento para ver si sigue escribiendo
            if hasattr(self, '_busqueda_timer'):
                self.after_cancel(self._busqueda_timer)
            self._busqueda_timer = self.after(300, self.procesar_codigo_escaneado)
        else:
            # Búsqueda normal
            self.filtrar_productos()
    
    def procesar_codigo_escaneado(self):
        """Procesar código escaneado automáticamente"""
        codigo = self.search_entry.get().strip()
        
        if not codigo:
            return
        
        # Buscar por código de barras
        producto = buscar_por_codigo_barras(codigo)
        
        if producto:
            self.agregar_producto(producto)
            self.search_entry.delete(0, 'end')
            
            # Mostrar notificación breve
            self.mostrar_notificacion(f"✅ {producto.get('nombre')} agregado")
        else:
            # Si no se encuentra, hacer búsqueda normal
            self.filtrar_productos()
    
    def mostrar_notificacion(self, mensaje):
        """Mostrar notificación temporal"""
        # Crear label de notificación
        notif = ctk.CTkLabel(
            self,
            text=mensaje,
            font=("Segoe UI", 12, "bold"),
            text_color="white",
            fg_color="#4CAF50",
            corner_radius=8,
            padx=20,
            pady=10
        )
        notif.place(relx=0.5, rely=0.1, anchor="center")
        
        # Ocultar después de 2 segundos
        self.after(2000, notif.destroy)
    
    def buscar_codigo_barras(self):
        """Buscar producto por código de barras (método legacy)"""
        self.procesar_codigo_escaneado()
    
    def agregar_producto_personalizado(self):
        """Agregar producto personalizado que no está en el sistema"""
        # Crear ventana de producto personalizado
        custom_window = ctk.CTkToplevel(self)
        custom_window.title("Producto Personalizado")
        custom_window.geometry("450x400")
        custom_window.transient(self)
        custom_window.grab_set()
        
        # Centrar ventana
        custom_window.update_idletasks()
        x = (custom_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (custom_window.winfo_screenheight() // 2) - (400 // 2)
        custom_window.geometry(f"450x400+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(custom_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="➕ Producto Personalizado",
            font=("Segoe UI", 18, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            main_frame,
            text="Agrega un producto que no está en el sistema",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Nombre del producto
        ctk.CTkLabel(
            form_frame,
            text="Nombre del Producto:",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        nombre_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ej: Servicio de reparación",
            height=40,
            font=("Segoe UI", 12)
        )
        nombre_entry.pack(fill="x", pady=(0, 15))
        nombre_entry.focus()
        
        # Precio
        ctk.CTkLabel(
            form_frame,
            text="Precio:",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        precio_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="0.00",
            height=40,
            font=("Segoe UI", 12)
        )
        precio_entry.pack(fill="x", pady=(0, 15))
        
        # Cantidad
        ctk.CTkLabel(
            form_frame,
            text="Cantidad:",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        cantidad_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="1",
            height=40,
            font=("Segoe UI", 12)
        )
        cantidad_entry.pack(fill="x", pady=(0, 15))
        cantidad_entry.insert(0, "1")
        
        # Nota informativa
        info_frame = ctk.CTkFrame(form_frame, fg_color="#FFF9C4", corner_radius=8)
        info_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Este producto no se guardará en el inventario",
            font=("Segoe UI", 10),
            text_color="#F57C00"
        ).pack(padx=12, pady=8)
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def agregar_custom():
            nombre = nombre_entry.get().strip()
            precio_str = precio_entry.get().strip()
            cantidad_str = cantidad_entry.get().strip()
            
            if not nombre or not precio_str:
                messagebox.showwarning("Datos incompletos", "Por favor ingresa nombre y precio")
                return
            
            try:
                precio = float(precio_str)
                cantidad = int(cantidad_str) if cantidad_str else 1
                
                if precio <= 0:
                    messagebox.showwarning("Precio inválido", "El precio debe ser mayor a 0")
                    return
                
                if cantidad <= 0:
                    messagebox.showwarning("Cantidad inválida", "La cantidad debe ser mayor a 0")
                    return
                
                # Crear producto temporal
                producto_custom = {
                    'id_producto': f"CUSTOM_{len(self.carrito)}",
                    'nombre': nombre,
                    'precio': precio,
                    'stock': 9999  # Stock ilimitado para productos personalizados
                }
                
                # Agregar al carrito
                for _ in range(cantidad):
                    self.agregar_producto(producto_custom)
                
                custom_window.destroy()
                self.mostrar_notificacion(f"✅ {nombre} agregado ({cantidad}x)")
                
            except ValueError:
                messagebox.showerror("Error", "Precio y cantidad deben ser números válidos")
        
        ctk.CTkButton(
            btn_frame,
            text="✅ Agregar al Carrito",
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=agregar_custom
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=45,
            font=("Segoe UI", 12),
            command=custom_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))
    
    def filtrar_productos(self):
        """Filtrar productos por búsqueda"""
        termino = self.search_entry.get().lower()
        
        if not termino:
            self.mostrar_productos(self.productos)
            return
        
        productos_filtrados = [
            p for p in self.productos
            if termino in p.get("nombre", "").lower() or
               termino in str(p.get("id_producto", "")).lower() or
               termino in str(p.get("codigo", "")).lower() or
               termino in str(p.get("codigo_barras", "")).lower()
        ]
        
        self.mostrar_productos(productos_filtrados)
