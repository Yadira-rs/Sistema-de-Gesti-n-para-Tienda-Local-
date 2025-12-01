import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from controllers.apartados import listar_apartados, obtener_apartado_detalle, actualizar_estado_apartado

class GestionApartadosView(ctk.CTk):
    def __init__(self, usuario=None):
        super().__init__()
        self.title("Janet Rosa Bici - Apartados")
        self.geometry("1400x800")
        ctk.set_appearance_mode("light")
        
        self.usuario = usuario or {"nombre_completo": "Administrador", "email": "admin@janet.com"}
        self.apartados = []
        self.estado_filtro = "Todos los estados"
        
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
                fg_color="#F8BBD0" if text == "Apartado" else "transparent",
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
        """Panel principal con apartados"""
        panel = ctk.CTkFrame(parent, fg_color="#F5F5F5")
        panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Header con título y botón
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        # Título y subtítulo
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(title_frame, text="Apartados", font=("Segoe UI", 24, "bold"), 
                    text_color="#333333", anchor="w").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="sistemas de apartado para clientes", 
                    font=("Segoe UI", 12), text_color="#666666", anchor="w").pack(anchor="w")
        
        # Botón Nuevo Apartado
        ctk.CTkButton(
            header,
            text="+ Nuevo Apartado",
            fg_color="#F06292",
            hover_color="#E91E63",
            corner_radius=20,
            height=45,
            width=180,
            font=("Segoe UI", 13, "bold"),
            command=self.nuevo_apartado
        ).pack(side="right")
        
        # Tarjetas de estadísticas
        self.crear_tarjetas_estadisticas(panel)
        
        # Filtros
        self.crear_filtros(panel)
        
        # Tabla de apartados
        self.crear_tabla_apartados(panel)

    def crear_tarjetas_estadisticas(self, parent):
        """Crear tarjetas con estadísticas de apartados"""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 15))
        
        # Configurar grid
        stats_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        # Tarjeta 1: Total
        card1 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card1.grid(row=0, column=0, padx=5, sticky="ew")
        
        info_frame1 = ctk.CTkFrame(card1, fg_color="transparent")
        info_frame1.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(info_frame1, text="📋 Total", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.total_label = ctk.CTkLabel(info_frame1, text="1", 
                    font=("Segoe UI", 28, "bold"), text_color="#333333", anchor="w")
        self.total_label.pack(anchor="w")
        
        # Tarjeta 2: Activos
        card2 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        
        info_frame2 = ctk.CTkFrame(card2, fg_color="transparent")
        info_frame2.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(info_frame2, text="Activos", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.activos_label = ctk.CTkLabel(info_frame2, text="0", 
                    font=("Segoe UI", 28, "bold"), text_color="#333333", anchor="w")
        self.activos_label.pack(anchor="w")
        
        # Tarjeta 3: Completados
        card3 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card3.grid(row=0, column=2, padx=5, sticky="ew")
        
        info_frame3 = ctk.CTkFrame(card3, fg_color="transparent")
        info_frame3.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(info_frame3, text="✅ Completados", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.completados_label = ctk.CTkLabel(info_frame3, text="0", 
                    font=("Segoe UI", 28, "bold"), text_color="#4CAF50", anchor="w")
        self.completados_label.pack(anchor="w")
        
        # Tarjeta 4: Cancelados
        card4 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card4.grid(row=0, column=3, padx=5, sticky="ew")
        
        info_frame4 = ctk.CTkFrame(card4, fg_color="transparent")
        info_frame4.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(info_frame4, text="🚫 Cancelados", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.cancelados_label = ctk.CTkLabel(info_frame4, text="1", 
                    font=("Segoe UI", 28, "bold"), text_color="#E53935", anchor="w")
        self.cancelados_label.pack(anchor="w")
        
        # Tarjeta 5: Pendiente
        card5 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card5.grid(row=0, column=4, padx=5, sticky="ew")
        
        info_frame5 = ctk.CTkFrame(card5, fg_color="transparent")
        info_frame5.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(info_frame5, text="⏱ Pendiente", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.pendiente_label = ctk.CTkLabel(info_frame5, text="$0.00", 
                    font=("Segoe UI", 28, "bold"), text_color="#FF9800", anchor="w")
        self.pendiente_label.pack(anchor="w")

    def crear_filtros(self, parent):
        """Crear barra de filtros"""
        filtros_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(0, 10))
        
        # Búsqueda
        search_frame = ctk.CTkFrame(filtros_frame, fg_color="white", corner_radius=10, height=50)
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 16)).pack(side="left", padx=15)
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por cliente, teléfono o ID...",
            border_width=0,
            fg_color="white",
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filtrar_apartados())
        
        # Filtro de estado
        self.estado_combo = ctk.CTkComboBox(
            filtros_frame,
            values=["Todos los estados", "Pendiente", "Pagado", "Cancelado"],
            width=200,
            height=50,
            corner_radius=10,
            font=("Segoe UI", 12),
            command=lambda e: self.filtrar_apartados()
        )
        self.estado_combo.set("Todos los estados")
        self.estado_combo.pack(side="left", padx=5)
    
    def crear_tabla_apartados(self, parent):
        """Crear tabla de apartados"""
        # Contenedor de la tabla
        tabla_container = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        tabla_container.pack(fill="both", expand=True)
        
        # Header de la tabla
        header_frame = ctk.CTkFrame(tabla_container, fg_color="#F5F5F5", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        headers = [
            ("ID", 80),
            ("Cliente", 180),
            ("Total", 100),
            ("Anticipo", 100),
            ("Saldo", 100),
            ("Fecha límite", 120),
            ("Estado", 120),
            ("Acciones", 180)
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
        
        # Scroll frame para apartados
        self.apartados_scroll = ctk.CTkScrollableFrame(tabla_container, fg_color="white")
        self.apartados_scroll.pack(fill="both", expand=True, padx=0, pady=0)

    def cargar_datos(self):
        """Cargar apartados desde la base de datos"""
        try:
            self.apartados = listar_apartados()
            self.actualizar_estadisticas()
            self.mostrar_apartados(self.apartados)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los apartados: {str(e)}")
            self.apartados = []
    
    def actualizar_estadisticas(self):
        """Actualizar las tarjetas de estadísticas"""
        total = len(self.apartados)
        activos = sum(1 for a in self.apartados if a.get("estado") == "Pendiente")
        completados = sum(1 for a in self.apartados if a.get("estado") == "Pagado")
        cancelados = sum(1 for a in self.apartados if a.get("estado") == "Cancelado")
        pendiente_total = sum(float(a.get("saldo", 0)) for a in self.apartados if a.get("estado") == "Pendiente")
        
        self.total_label.configure(text=str(total))
        self.activos_label.configure(text=str(activos))
        self.completados_label.configure(text=str(completados))
        self.cancelados_label.configure(text=str(cancelados))
        self.pendiente_label.configure(text=f"${pendiente_total:,.2f}")
    
    def mostrar_apartados(self, apartados):
        """Mostrar apartados en la tabla"""
        # Limpiar tabla actual
        for widget in self.apartados_scroll.winfo_children():
            widget.destroy()
        
        # Mostrar cada apartado
        for apartado in apartados:
            self.crear_fila_apartado(self.apartados_scroll, apartado)
    
    def crear_fila_apartado(self, parent, apartado):
        """Crear fila individual de apartado"""
        fila = ctk.CTkFrame(parent, fg_color="white", height=70)
        fila.pack(fill="x", padx=0, pady=1)
        
        # ID
        id_apartado = apartado.get("id_apartado", "N/A")
        ctk.CTkLabel(
            fila,
            text=str(id_apartado),
            font=("Segoe UI", 11, "bold"),
            text_color="#333333",
            width=80,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Cliente
        cliente = apartado.get("cliente_nombre", "N/A")
        ctk.CTkLabel(
            fila,
            text=cliente[:25] + "..." if len(cliente) > 25 else cliente,
            font=("Segoe UI", 11),
            text_color="#333333",
            width=180,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Total
        total = float(apartado.get("total", 0))
        ctk.CTkLabel(
            fila,
            text=f"${total:.2f}",
            font=("Segoe UI", 11),
            text_color="#333333",
            width=100,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Anticipo (verde)
        anticipo = float(apartado.get("anticipo", 0))
        ctk.CTkLabel(
            fila,
            text=f"${anticipo:.2f}",
            font=("Segoe UI", 11, "bold"),
            text_color="#4CAF50",
            width=100,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Saldo (naranja)
        saldo = float(apartado.get("saldo", 0))
        ctk.CTkLabel(
            fila,
            text=f"${saldo:.2f}",
            font=("Segoe UI", 11, "bold"),
            text_color="#FF9800",
            width=100,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Fecha límite
        fecha_limite = apartado.get("fecha_limite", "N/A")
        if isinstance(fecha_limite, datetime):
            fecha_limite = fecha_limite.strftime("%d/%m/%Y")
        ctk.CTkLabel(
            fila,
            text=str(fecha_limite),
            font=("Segoe UI", 11),
            text_color="#666666",
            width=120,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Estado (badge)
        estado = apartado.get("estado", "Pendiente")
        estado_frame = ctk.CTkFrame(fila, fg_color="transparent", width=120)
        estado_frame.pack(side="left", padx=10)
        
        # Color según estado
        if estado == "Cancelado":
            bg_color = "#FFEBEE"
            text_color = "#E53935"
        elif estado == "Pagado":
            bg_color = "#E8F5E9"
            text_color = "#4CAF50"
        else:  # Pendiente
            bg_color = "#E0E0E0"
            text_color = "#666666"
        
        estado_badge = ctk.CTkFrame(estado_frame, fg_color=bg_color, corner_radius=12, height=28)
        estado_badge.pack(anchor="w")
        
        ctk.CTkLabel(
            estado_badge,
            text=estado,
            font=("Segoe UI", 10, "bold"),
            text_color=text_color
        ).pack(padx=15, pady=4)
        
        # Acciones
        acciones_frame = ctk.CTkFrame(fila, fg_color="transparent", width=180)
        acciones_frame.pack(side="left", padx=10)
        
        # Botón Ver
        ctk.CTkButton(
            acciones_frame,
            text="👁",
            fg_color="transparent",
            text_color="#2196F3",
            hover_color="#E3F2FD",
            width=35,
            height=35,
            font=("Segoe UI", 16),
            command=lambda a=apartado: self.ver_apartado(a)
        ).pack(side="left", padx=2)
        
        # Botón Pagar
        ctk.CTkButton(
            acciones_frame,
            text="💵",
            fg_color="transparent",
            text_color="#4CAF50",
            hover_color="#E8F5E9",
            width=35,
            height=35,
            font=("Segoe UI", 16),
            command=lambda a=apartado: self.pagar_apartado(a)
        ).pack(side="left", padx=2)
        
        # Botón Cancelar
        ctk.CTkButton(
            acciones_frame,
            text="🚫",
            fg_color="transparent",
            text_color="#E53935",
            hover_color="#FFEBEE",
            width=35,
            height=35,
            font=("Segoe UI", 16),
            command=lambda a=apartado: self.cancelar_apartado(a)
        ).pack(side="left", padx=2)

    def filtrar_apartados(self):
        """Filtrar apartados según búsqueda y estado"""
        termino = self.search_entry.get().lower()
        estado = self.estado_combo.get()
        
        apartados_filtrados = self.apartados.copy()
        
        # Filtrar por búsqueda
        if termino:
            apartados_filtrados = [
                a for a in apartados_filtrados
                if termino in str(a.get("cliente_nombre", "")).lower() or
                   termino in str(a.get("id_apartado", "")).lower() or
                   termino in str(a.get("cliente_telefono", "")).lower()
            ]
        
        # Filtrar por estado
        if estado != "Todos los estados":
            apartados_filtrados = [a for a in apartados_filtrados if a.get("estado") == estado]
        
        self.mostrar_apartados(apartados_filtrados)
    
    def nuevo_apartado(self):
        """Abrir formulario para crear nuevo apartado"""
        messagebox.showinfo("Nuevo Apartado", "Funcionalidad de nuevo apartado en desarrollo")
    
    def ver_apartado(self, apartado):
        """Ver detalles del apartado"""
        try:
            detalle = obtener_apartado_detalle(apartado["id_apartado"])
            
            # Crear ventana de detalles
            dialog = ctk.CTkToplevel(self)
            dialog.title(f"Apartado #{apartado['id_apartado']}")
            dialog.geometry("500x600")
            dialog.transient(self)
            dialog.grab_set()
            
            # Centrar ventana
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
            y = (dialog.winfo_screenheight() // 2) - (600 // 2)
            dialog.geometry(f"500x600+{x}+{y}")
            
            # Contenido
            main_frame = ctk.CTkFrame(dialog, fg_color="white")
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(
                main_frame,
                text=f"Apartado #{apartado['id_apartado']}",
                font=("Segoe UI", 20, "bold"),
                text_color="#333333"
            ).pack(pady=(0, 20))
            
            # Información del cliente
            info_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5F5", corner_radius=10)
            info_frame.pack(fill="x", pady=(0, 15))
            
            ctk.CTkLabel(info_frame, text="Cliente", font=("Segoe UI", 11), 
                        text_color="#666666").pack(anchor="w", padx=15, pady=(10, 2))
            ctk.CTkLabel(info_frame, text=apartado.get("cliente_nombre", "N/A"), 
                        font=("Segoe UI", 14, "bold"), text_color="#333333").pack(anchor="w", padx=15, pady=(0, 10))
            
            # Resumen financiero
            resumen_frame = ctk.CTkFrame(main_frame, fg_color="#FFF0F5", corner_radius=10)
            resumen_frame.pack(fill="x", pady=(0, 15))
            
            items = [
                ("Total:", f"${apartado.get('total', 0):.2f}", "#333333"),
                ("Anticipo:", f"${apartado.get('anticipo', 0):.2f}", "#4CAF50"),
                ("Saldo:", f"${apartado.get('saldo', 0):.2f}", "#FF9800")
            ]
            
            for label, value, color in items:
                row = ctk.CTkFrame(resumen_frame, fg_color="transparent")
                row.pack(fill="x", padx=15, pady=5)
                ctk.CTkLabel(row, text=label, font=("Segoe UI", 12), 
                            text_color="#666666").pack(side="left")
                ctk.CTkLabel(row, text=value, font=("Segoe UI", 12, "bold"), 
                            text_color=color).pack(side="right")
            
            # Productos
            ctk.CTkLabel(main_frame, text="Productos", font=("Segoe UI", 14, "bold"), 
                        text_color="#333333").pack(anchor="w", pady=(10, 5))
            
            productos_scroll = ctk.CTkScrollableFrame(main_frame, height=200)
            productos_scroll.pack(fill="both", expand=True, pady=(0, 15))
            
            if detalle and "productos" in detalle:
                for prod in detalle["productos"]:
                    prod_frame = ctk.CTkFrame(productos_scroll, fg_color="#F9F9F9", corner_radius=8)
                    prod_frame.pack(fill="x", pady=3)
                    
                    ctk.CTkLabel(
                        prod_frame,
                        text=f"{prod.get('nombre', 'N/A')} x{prod.get('cantidad', 0)}",
                        font=("Segoe UI", 11),
                        text_color="#333333"
                    ).pack(side="left", padx=10, pady=8)
                    
                    ctk.CTkLabel(
                        prod_frame,
                        text=f"${prod.get('subtotal', 0):.2f}",
                        font=("Segoe UI", 11, "bold"),
                        text_color="#E91E63"
                    ).pack(side="right", padx=10, pady=8)
            
            # Botón cerrar
            ctk.CTkButton(
                main_frame,
                text="Cerrar",
                fg_color="#E91E63",
                hover_color="#C2185B",
                height=40,
                font=("Segoe UI", 12, "bold"),
                command=dialog.destroy
            ).pack(fill="x", pady=(10, 0))
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el detalle: {str(e)}")
    
    def pagar_apartado(self, apartado):
        """Registrar pago de apartado"""
        if apartado.get("estado") != "Pendiente":
            messagebox.showwarning("Apartado no disponible", "Este apartado no está pendiente de pago")
            return
        
        saldo = float(apartado.get("saldo", 0))
        
        if messagebox.askyesno("Confirmar pago", f"¿Marcar apartado #{apartado['id_apartado']} como pagado?\n\nSaldo pendiente: ${saldo:.2f}"):
            try:
                if actualizar_estado_apartado(apartado["id_apartado"], "Pagado"):
                    messagebox.showinfo("Éxito", "Apartado marcado como pagado")
                    self.cargar_datos()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el apartado")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
    
    def cancelar_apartado(self, apartado):
        """Cancelar apartado"""
        if apartado.get("estado") == "Cancelado":
            messagebox.showwarning("Ya cancelado", "Este apartado ya está cancelado")
            return
        
        if messagebox.askyesno("Confirmar cancelación", f"¿Cancelar apartado #{apartado['id_apartado']}?\n\nEsta acción no se puede deshacer."):
            try:
                if actualizar_estado_apartado(apartado["id_apartado"], "Cancelado"):
                    messagebox.showinfo("Éxito", "Apartado cancelado")
                    self.cargar_datos()
                else:
                    messagebox.showerror("Error", "No se pudo cancelar el apartado")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cancelar: {str(e)}")


if __name__ == "__main__":
    app = GestionApartadosView()
    app.mainloop()
