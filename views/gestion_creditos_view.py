import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class GestionCreditosView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.pack(fill="both", expand=True)
        
        self.user = user or {"nombre_completo": "Administrador", "email": "admin@janet.com"}
        self.creditos = []
        self.tab_actual = "Control de Ventas a Crédito"
        
        self.crear_interfaz()
        self.cargar_datos()
    
    def crear_interfaz(self):
        # Panel principal (sin sidebar, ya está en main.py)
        self.crear_panel_principal(self)



    def crear_panel_principal(self, parent):
        """Panel principal con créditos"""
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header con título
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header, text="Ventas a Crédito", font=("Segoe UI", 24, "bold"), 
                    text_color="#333333", anchor="w").pack(side="left")
        
        # Tabs de navegación
        self.crear_tabs(panel)
        
        # Contenedor para el contenido de cada tab
        self.content_frame = ctk.CTkFrame(panel, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Mostrar tab inicial
        self.mostrar_tab("Control de Ventas a Crédito")
    
    def crear_tabs(self, parent):
        """Crear pestañas de navegación"""
        tabs_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tabs_frame.pack(fill="x", pady=(0, 10))
        
        tabs = [
            "Control de Ventas a Crédito",
            "Créditos a clientes",
            "Vencidos",
            "Abonos de Hoy",
            "Gestión de Clientes"
        ]
        
        self.tab_buttons = {}
        
        for tab in tabs:
            btn = ctk.CTkButton(
                tabs_frame,
                text=tab,
                fg_color="white" if tab != self.tab_actual else "#E91E63",
                text_color="#666666" if tab != self.tab_actual else "white",
                hover_color="#F8BBD0",
                corner_radius=20,
                height=40,
                font=("Segoe UI", 13),
                command=lambda t=tab: self.cambiar_tab(t)
            )
            btn.pack(side="left", padx=5)
            self.tab_buttons[tab] = btn
    
    def cambiar_tab(self, tab):
        """Cambiar de pestaña"""
        self.tab_actual = tab
        
        # Actualizar estilos de botones
        for tab_name, btn in self.tab_buttons.items():
            if tab_name == tab:
                btn.configure(fg_color="#E91E63", text_color="white")
            else:
                btn.configure(fg_color="white", text_color="#666666")
        
        # Mostrar contenido del tab
        self.mostrar_tab(tab)
    
    def mostrar_tab(self, tab):
        """Mostrar contenido de la pestaña seleccionada"""
        # Limpiar contenido actual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if tab == "Control de Ventas a Crédito":
            self.mostrar_control_creditos()
        elif tab == "Créditos a clientes":
            self.mostrar_creditos_clientes()
        elif tab == "Vencidos":
            self.mostrar_vencidos()
        elif tab == "Abonos de Hoy":
            self.mostrar_abonos_hoy()
        elif tab == "Gestión de Clientes":
            self.mostrar_gestion_clientes()

    def mostrar_control_creditos(self):
        """Mostrar tab de Control de Ventas a Crédito"""
        # Contenedor principal dividido
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Panel izquierdo - Tabla
        left_panel = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Header de la tabla
        header_frame = ctk.CTkFrame(left_panel, fg_color="#F5F5F5")
        header_frame.pack(fill="x", padx=0, pady=0)
        
        headers = ["#", "Venta", "Fecha", "Monto", "Pagado", "Saldo", "Vence", "Estado"]
        widths = [50, 80, 120, 100, 100, 100, 120, 100]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Segoe UI", 11, "bold"),
                text_color="#333333",
                width=width
            )
            label.pack(side="left", padx=5, pady=12)
        
        # Área de contenido
        self.content_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="white")
        self.content_scroll.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Cargar créditos
        self.cargar_creditos_tabla()
        
        # Panel derecho - Acciones y Resumen
        right_panel = ctk.CTkFrame(main_container, fg_color="transparent", width=300)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # Botones de acción
        ctk.CTkButton(
            right_panel,
            text="+ Nuevo Crédito",
            fg_color="#F06292",
            hover_color="#E91E63",
            corner_radius=10,
            height=45,
            font=("Segoe UI", 13, "bold"),
            command=self.nuevo_credito
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(
            right_panel,
            text="Actualizar Lista",
            fg_color="white",
            text_color="#666666",
            border_width=2,
            border_color="#E0E0E0",
            hover_color="#F5F5F5",
            corner_radius=10,
            height=45,
            font=("Segoe UI", 12),
            command=self.cargar_datos
        ).pack(fill="x", pady=(0, 20))
        
        # Resumen
        resumen_frame = ctk.CTkFrame(right_panel, fg_color="white", corner_radius=10)
        resumen_frame.pack(fill="x")
        
        ctk.CTkLabel(
            resumen_frame,
            text="Resumen",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        # Total Por Cobrar
        total_frame = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        total_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(total_frame, text="Total Por Cobrar", font=("Segoe UI", 13), 
                    text_color="#666666").pack(side="left")
        self.total_cobrar_label = ctk.CTkLabel(total_frame, text="$0.00", 
                    font=("Segoe UI", 11, "bold"), text_color="#4CAF50")
        self.total_cobrar_label.pack(side="right")
        
        # Créditos Activos
        activos_frame = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        activos_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(activos_frame, text="Créditos Activos", font=("Segoe UI", 13), 
                    text_color="#666666").pack(side="left")
        self.creditos_activos_label = ctk.CTkLabel(activos_frame, text="0", 
                    font=("Segoe UI", 11, "bold"), text_color="#333333")
        self.creditos_activos_label.pack(side="right")
        
        # Créditos Vencidos
        vencidos_frame = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        vencidos_frame.pack(fill="x", padx=20, pady=(5, 15))
        
        ctk.CTkLabel(vencidos_frame, text="Créditos vencidos", font=("Segoe UI", 13), 
                    text_color="#666666").pack(side="left")
        self.creditos_vencidos_label = ctk.CTkLabel(vencidos_frame, text="0", 
                    font=("Segoe UI", 11, "bold"), text_color="#E53935")
        self.creditos_vencidos_label.pack(side="right")
    
    def mostrar_creditos_clientes(self):
        """Mostrar tab de Créditos a clientes"""
        # Contenedor principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=12)
        main_container.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            header,
            text="Créditos por Cliente",
            font=("Segoe UI", 16, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Búsqueda
        search_frame = ctk.CTkFrame(main_container, fg_color="#F5F5F5", corner_radius=10, height=45)
        search_frame.pack(fill="x", padx=20, pady=(0, 15))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 16)).pack(side="left", padx=10)
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar cliente...",
            border_width=0,
            fg_color="#F5F5F5",
            font=("Segoe UI", 13)
        )
        search_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Lista de clientes con créditos
        scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Mensaje si no hay datos
        ctk.CTkLabel(
            scroll,
            text="📋 No hay créditos registrados por cliente",
            font=("Segoe UI", 14),
            text_color="#999999"
        ).pack(expand=True, pady=50)
    
    def mostrar_vencidos(self):
        """Mostrar tab de Vencidos"""
        # Contenedor principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=12)
        main_container.pack(fill="both", expand=True)
        
        # Header con alerta
        header = ctk.CTkFrame(main_container, fg_color="#FFEBEE", corner_radius=10)
        header.pack(fill="x", padx=20, pady=15)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            header_content,
            text="⚠️",
            font=("Segoe UI", 24),
            text_color="#E53935"
        ).pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            text_frame,
            text="Créditos Vencidos",
            font=("Segoe UI", 14, "bold"),
            text_color="#E53935",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame,
            text="Estos créditos han superado su fecha de vencimiento",
            font=("Segoe UI", 12),
            text_color="#C62828",
            anchor="w"
        ).pack(anchor="w")
        
        # Lista de créditos vencidos
        scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Mensaje si no hay vencidos
        ctk.CTkLabel(
            scroll,
            text="✅ No hay créditos vencidos",
            font=("Segoe UI", 14),
            text_color="#4CAF50"
        ).pack(expand=True, pady=50)
    
    def mostrar_abonos_hoy(self):
        """Mostrar tab de Abonos de Hoy"""
        from datetime import datetime
        
        # Contenedor principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=12)
        main_container.pack(fill="both", expand=True)
        
        # Header con fecha
        header = ctk.CTkFrame(main_container, fg_color="#E8F5E9", corner_radius=10)
        header.pack(fill="x", padx=20, pady=15)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            header_content,
            text="💰",
            font=("Segoe UI", 24),
            text_color="#4CAF50"
        ).pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            text_frame,
            text="Abonos de Hoy",
            font=("Segoe UI", 14, "bold"),
            text_color="#2E7D32",
            anchor="w"
        ).pack(anchor="w")
        
        fecha_hoy = datetime.now().strftime("%d de %B de %Y")
        ctk.CTkLabel(
            text_frame,
            text=fecha_hoy,
            font=("Segoe UI", 12),
            text_color="#43A047",
            anchor="w"
        ).pack(anchor="w")
        
        # Resumen del día
        resumen_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        resumen_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        resumen_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Total abonos
        card1 = ctk.CTkFrame(resumen_frame, fg_color="#F5F5F5", corner_radius=10)
        card1.grid(row=0, column=0, padx=5, sticky="ew")
        
        ctk.CTkLabel(card1, text="Total Abonos", font=("Segoe UI", 12), text_color="#666666").pack(pady=(10, 2))
        ctk.CTkLabel(card1, text="0", font=("Segoe UI", 20, "bold"), text_color="#333333").pack(pady=(0, 10))
        
        # Monto total
        card2 = ctk.CTkFrame(resumen_frame, fg_color="#F5F5F5", corner_radius=10)
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        
        ctk.CTkLabel(card2, text="Monto Total", font=("Segoe UI", 12), text_color="#666666").pack(pady=(10, 2))
        ctk.CTkLabel(card2, text="$0.00", font=("Segoe UI", 20, "bold"), text_color="#4CAF50").pack(pady=(0, 10))
        
        # Lista de abonos
        scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Mensaje si no hay abonos
        ctk.CTkLabel(
            scroll,
            text="📅 No se registraron abonos hoy",
            font=("Segoe UI", 14),
            text_color="#999999"
        ).pack(expand=True, pady=50)

    def cargar_datos(self):
        """Cargar créditos desde la base de datos"""
        try:
            from controllers.creditos import obtener_creditos, obtener_resumen_creditos
            self.creditos = obtener_creditos()
            self.resumen = obtener_resumen_creditos()
            self.actualizar_resumen()
            
            # Recargar la tabla si existe
            if hasattr(self, 'content_scroll'):
                self.cargar_creditos_tabla()
        except Exception as e:
            print(f"Error al cargar créditos: {e}")
            self.creditos = []
            self.resumen = {
                'total_creditos': 0,
                'activos': 0,
                'vencidos': 0,
                'total_por_cobrar': 0
            }
    
    def cargar_creditos_tabla(self):
        """Cargar créditos en la tabla"""
        # Limpiar contenido
        for widget in self.content_scroll.winfo_children():
            widget.destroy()
        
        if not self.creditos:
            ctk.CTkLabel(
                self.content_scroll,
                text="📋 No hay créditos registrados",
                font=("Segoe UI", 14),
                text_color="#999999"
            ).pack(expand=True, pady=100)
            return
        
        # Mostrar créditos
        for credito in self.creditos:
            self.crear_fila_credito(credito)
    
    def crear_fila_credito(self, credito):
        """Crear una fila para un crédito"""
        row = ctk.CTkFrame(self.content_scroll, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        # Determinar color según estado
        if credito['estado'] == 'Vencido':
            bg_color = "#FFEBEE"
        elif credito['estado'] == 'Pagado':
            bg_color = "#E8F5E9"
        else:
            bg_color = "white"
        
        row.configure(fg_color=bg_color)
        
        widths = [50, 80, 120, 100, 100, 100, 120, 100]
        
        # ID Crédito
        ctk.CTkLabel(row, text=str(credito['id_credito']), width=widths[0], 
                    font=("Segoe UI", 12)).pack(side="left", padx=5)
        
        # ID Venta
        ctk.CTkLabel(row, text=f"#{credito['id_venta']}", width=widths[1], 
                    font=("Segoe UI", 12)).pack(side="left", padx=5)
        
        # Fecha
        fecha = credito['fecha_credito'].strftime("%d/%m/%Y %H:%M") if credito['fecha_credito'] else "-"
        ctk.CTkLabel(row, text=fecha, width=widths[2], 
                    font=("Segoe UI", 12)).pack(side="left", padx=5)
        
        # Monto Total
        ctk.CTkLabel(row, text=f"${float(credito['monto_total']):.2f}", width=widths[3], 
                    font=("Segoe UI", 10, "bold"), text_color="#E91E63").pack(side="left", padx=5)
        
        # Monto Pagado
        ctk.CTkLabel(row, text=f"${float(credito['monto_pagado']):.2f}", width=widths[4], 
                    font=("Segoe UI", 12), text_color="#4CAF50").pack(side="left", padx=5)
        
        # Saldo
        ctk.CTkLabel(row, text=f"${float(credito['saldo_pendiente']):.2f}", width=widths[5], 
                    font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        
        # Fecha Vencimiento
        vence = credito['fecha_vencimiento'].strftime("%d/%m/%Y") if credito['fecha_vencimiento'] else "-"
        ctk.CTkLabel(row, text=vence, width=widths[6], 
                    font=("Segoe UI", 12)).pack(side="left", padx=5)
        
        # Estado
        estado_colors = {
            'Activo': '#4CAF50',
            'Vencido': '#F44336',
            'Pagado': '#2196F3',
            'Cancelado': '#9E9E9E'
        }
        ctk.CTkLabel(row, text=credito['estado'], width=widths[7], 
                    font=("Segoe UI", 10, "bold"), 
                    text_color=estado_colors.get(credito['estado'], '#666666')).pack(side="left", padx=5)
    
    def actualizar_resumen(self):
        """Actualizar el resumen de créditos"""
        if hasattr(self, 'resumen'):
            self.total_cobrar_label.configure(text=f"${float(self.resumen['total_por_cobrar']):,.2f}")
            self.creditos_activos_label.configure(text=str(self.resumen['activos']))
            self.creditos_vencidos_label.configure(text=str(self.resumen['vencidos']))
    
    def nuevo_credito(self):
        """Abrir formulario para nuevo crédito"""
        # Crear ventana de nuevo crédito
        credito_window = ctk.CTkToplevel(self)
        credito_window.title("Nuevo Crédito")
        credito_window.geometry("550x700")
        credito_window.transient(self)
        credito_window.grab_set()
        
        # Centrar ventana
        credito_window.update_idletasks()
        x = (credito_window.winfo_screenwidth() // 2) - (550 // 2)
        y = (credito_window.winfo_screenheight() // 2) - (700 // 2)
        credito_window.geometry(f"550x700+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(credito_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="💳 Nuevo Crédito",
            font=("Segoe UI", 22, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Cargar clientes de la base de datos
        try:
            from database.db import crear_conexion
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            # Solo seleccionar columnas que existen
            cursor.execute("SELECT id_cliente, nombre, telefono FROM clientes ORDER BY nombre")
            clientes = cursor.fetchall()
            conn.close()
            
            # Crear diccionario de clientes
            clientes_dict = {}
            clientes_nombres = []
            for cliente in clientes:
                nombre_completo = f"{cliente['nombre']} - {cliente['telefono']}"
                clientes_nombres.append(nombre_completo)
                clientes_dict[nombre_completo] = cliente['id_cliente']
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
            clientes_nombres = []
            clientes_dict = {}
        
        # Cliente (ComboBox)
        ctk.CTkLabel(form_frame, text="Cliente: *", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        
        if clientes_nombres:
            cliente_combo = ctk.CTkComboBox(
                form_frame,
                values=clientes_nombres,
                height=45,
                font=("Segoe UI", 13),
                dropdown_font=("Segoe UI", 12),
                button_color="#E91E63",
                button_hover_color="#C2185B",
                border_color="#E0E0E0"
            )
            cliente_combo.pack(fill="x", pady=(0, 15))
            cliente_combo.set("Selecciona un cliente")
        else:
            # Si no hay clientes, mostrar mensaje
            no_clientes_frame = ctk.CTkFrame(form_frame, fg_color="#FFF3E0", corner_radius=10)
            no_clientes_frame.pack(fill="x", pady=(0, 15))
            
            ctk.CTkLabel(
                no_clientes_frame,
                text="⚠️ No hay clientes registrados\nPrimero debes agregar clientes en la sección de Clientes",
                font=("Segoe UI", 12),
                text_color="#F57C00",
                justify="center"
            ).pack(padx=15, pady=15)
            
            cliente_combo = None
        
        # ID Venta (opcional)
        ctk.CTkLabel(form_frame, text="ID Venta (opcional):", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        venta_entry = ctk.CTkEntry(form_frame, placeholder_text="Dejar vacío si no hay venta asociada", height=45, font=("Segoe UI", 13))
        venta_entry.pack(fill="x", pady=(0, 15))
        
        # Monto
        ctk.CTkLabel(form_frame, text="Monto del Crédito: *", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        monto_entry = ctk.CTkEntry(form_frame, placeholder_text="$0.00", height=45, font=("Segoe UI", 13))
        monto_entry.pack(fill="x", pady=(0, 15))
        
        # Plazo
        ctk.CTkLabel(form_frame, text="Plazo (días): *", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        plazo_entry = ctk.CTkEntry(form_frame, placeholder_text="30", height=45, font=("Segoe UI", 13))
        plazo_entry.pack(fill="x", pady=(0, 15))
        plazo_entry.insert(0, "30")
        
        # Tasa de interés
        ctk.CTkLabel(form_frame, text="Tasa de Interés (%):", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        tasa_entry = ctk.CTkEntry(form_frame, placeholder_text="0", height=45, font=("Segoe UI", 13))
        tasa_entry.pack(fill="x", pady=(0, 15))
        tasa_entry.insert(0, "0")
        
        # Notas
        ctk.CTkLabel(form_frame, text="Notas:", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        notas_entry = ctk.CTkTextbox(form_frame, height=100, font=("Segoe UI", 13))
        notas_entry.pack(fill="x", pady=(0, 15))
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def guardar_credito():
            if not cliente_combo or not clientes_nombres:
                messagebox.showwarning("Sin clientes", "Primero debes registrar clientes en el sistema")
                return
            
            cliente_seleccionado = cliente_combo.get()
            monto = monto_entry.get().strip()
            plazo = plazo_entry.get().strip()
            tasa = tasa_entry.get().strip() or "0"
            notas = notas_entry.get("1.0", "end").strip()
            id_venta = venta_entry.get().strip() or None
            
            if cliente_seleccionado == "Selecciona un cliente" or not monto or not plazo:
                messagebox.showwarning("Datos incompletos", "Por favor completa todos los campos obligatorios (*)")
                return
            
            try:
                id_cliente = clientes_dict[cliente_seleccionado]
                monto_float = float(monto.replace("$", "").replace(",", ""))
                plazo_int = int(plazo)
                tasa_float = float(tasa)
                
                # Guardar en la base de datos
                from controllers.creditos import crear_credito
                id_credito = crear_credito(
                    id_venta=id_venta,
                    id_cliente=id_cliente,
                    monto_total=monto_float,
                    plazo_dias=plazo_int,
                    tasa_interes=tasa_float,
                    notas=notas
                )
                
                if id_credito:
                    messagebox.showinfo(
                        "✅ Crédito Registrado",
                        f"Crédito #{id_credito} registrado exitosamente\n\n"
                        f"Cliente: {cliente_seleccionado.split(' - ')[0]}\n"
                        f"Monto: ${monto_float:,.2f}\n"
                        f"Plazo: {plazo_int} días"
                    )
                    credito_window.destroy()
                    self.cargar_datos()  # Recargar la lista
                else:
                    messagebox.showerror("Error", "No se pudo registrar el crédito")
                
            except ValueError:
                messagebox.showerror("Error", "Monto, plazo y tasa deben ser números válidos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Crédito",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=50,
            font=("Segoe UI", 14, "bold"),
            command=guardar_credito
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=50,
            font=("Segoe UI", 14),
            command=credito_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))




    def mostrar_gestion_clientes(self):
        """Mostrar tab de Gestión de Clientes"""
        from views.clientes_view import ClientesView
        
        # Crear instancia de la vista de clientes dentro del content_frame
        clientes_view = ClientesView(self.content_frame, self.user)
