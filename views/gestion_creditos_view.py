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
        """Mostrar tab de Créditos a clientes - agrupados por cliente"""
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
        
        # Botón para crear nuevo crédito
        ctk.CTkButton(
            header,
            text="+ Nuevo Crédito",
            fg_color="#E91E63",
            hover_color="#C2185B",
            height=35,
            font=("Segoe UI", 12, "bold"),
            command=self.nuevo_credito
        ).pack(side="right")
        
        # Lista de clientes con créditos
        scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Obtener créditos agrupados por cliente
        try:
            from database.db import crear_conexion
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    c.id_cliente,
                    cl.nombre as cliente_nombre,
                    COUNT(*) as total_creditos,
                    SUM(CASE WHEN c.estado = 'Activo' THEN 1 ELSE 0 END) as activos,
                    SUM(c.saldo_pendiente) as saldo_total
                FROM creditos c
                LEFT JOIN clientes cl ON c.id_cliente = cl.id_cliente
                GROUP BY c.id_cliente, cl.nombre
                ORDER BY saldo_total DESC
            """)
            
            clientes_creditos = cursor.fetchall()
            conn.close()
            
            if not clientes_creditos:
                ctk.CTkLabel(
                    scroll,
                    text="📋 No hay créditos registrados",
                    font=("Segoe UI", 14),
                    text_color="#999999"
                ).pack(expand=True, pady=50)
            else:
                for cliente in clientes_creditos:
                    self.crear_tarjeta_cliente_credito(scroll, cliente)
                    
        except Exception as e:
            ctk.CTkLabel(
                scroll,
                text=f"❌ Error al cargar créditos: {str(e)}",
                font=("Segoe UI", 14),
                text_color="#F44336"
            ).pack(expand=True, pady=50)
    
    def crear_tarjeta_cliente_credito(self, parent, cliente):
        """Crear tarjeta de cliente con sus créditos"""
        card = ctk.CTkFrame(parent, fg_color="#F5F5F5", corner_radius=10)
        card.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)
        
        # Nombre del cliente
        ctk.CTkLabel(
            content,
            text=cliente.get('cliente_nombre', 'Cliente sin nombre'),
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Estadísticas
        stats_frame = ctk.CTkFrame(content, fg_color="transparent")
        stats_frame.pack(side="right")
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Créditos: {cliente.get('total_creditos', 0)} | Activos: {cliente.get('activos', 0)} | Saldo: ${cliente.get('saldo_total', 0):.2f}",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack()
    
    def mostrar_vencidos(self):
        """Mostrar tab de Créditos Vencidos"""
        # Contenedor principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=12)
        main_container.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            header,
            text="⚠️ Créditos Vencidos",
            font=("Segoe UI", 16, "bold"),
            text_color="#F44336"
        ).pack(side="left")
        
        # Lista de créditos vencidos
        scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Obtener créditos vencidos
        try:
            from database.db import crear_conexion
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    c.*,
                    cl.nombre as cliente_nombre,
                    cl.telefono as cliente_telefono,
                    DATEDIFF(NOW(), c.fecha_vencimiento) as dias_vencido
                FROM creditos c
                LEFT JOIN clientes cl ON c.id_cliente = cl.id_cliente
                WHERE c.estado = 'Activo' AND c.fecha_vencimiento < CURDATE()
                ORDER BY c.fecha_vencimiento ASC
            """)
            
            creditos_vencidos = cursor.fetchall()
            conn.close()
            
            if not creditos_vencidos:
                ctk.CTkLabel(
                    scroll,
                    text="✅ No hay créditos vencidos",
                    font=("Segoe UI", 14),
                    text_color="#4CAF50"
                ).pack(expand=True, pady=50)
            else:
                for credito in creditos_vencidos:
                    self.crear_tarjeta_credito_vencido(scroll, credito)
                    
        except Exception as e:
            ctk.CTkLabel(
                scroll,
                text=f"❌ Error al cargar créditos vencidos: {str(e)}",
                font=("Segoe UI", 14),
                text_color="#F44336"
            ).pack(expand=True, pady=50)
    
    def crear_tarjeta_credito_vencido(self, parent, credito):
        """Crear tarjeta de crédito vencido"""
        card = ctk.CTkFrame(parent, fg_color="#FFEBEE", corner_radius=10)
        card.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)
        
        # Info del cliente
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=f"#{credito.get('id_credito')} - {credito.get('cliente_nombre', 'N/A')}",
            font=("Segoe UI", 13, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=f"Vencido hace {credito.get('dias_vencido', 0)} días | Saldo: ${credito.get('saldo_pendiente', 0):.2f}",
            font=("Segoe UI", 11),
            text_color="#F44336"
        ).pack(anchor="w")
        
        # Botón de acción
        ctk.CTkButton(
            content,
            text="Registrar Abono",
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=120,
            height=30,
            font=("Segoe UI", 11),
            command=lambda c=credito: self.registrar_abono(c)
        ).pack(side="right")
        
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
        
        # Obtener abonos de hoy
        try:
            from controllers.creditos import obtener_abonos_hoy
            abonos_hoy = obtener_abonos_hoy()
            
            if abonos_hoy:
                total_abonos = len(abonos_hoy)
                monto_total = sum(float(abono['monto_abono']) for abono in abonos_hoy)
                
                # Actualizar resumen
                card1.winfo_children()[1].configure(text=str(total_abonos))
                card2.winfo_children()[1].configure(text=f"${monto_total:.2f}")
                
                # Mostrar cada abono
                for abono in abonos_hoy:
                    self.crear_item_abono_hoy(scroll, abono)
            else:
                # Mensaje si no hay abonos
                ctk.CTkLabel(
                    scroll,
                    text="📅 No se registraron abonos hoy",
                    font=("Segoe UI", 14),
                    text_color="#999999"
                ).pack(expand=True, pady=50)
                
        except Exception as e:
            ctk.CTkLabel(
                scroll,
                text=f"❌ Error al cargar abonos: {str(e)}",
                font=("Segoe UI", 14),
                text_color="#F44336"
            ).pack(expand=True, pady=50)
    
    def crear_item_abono_hoy(self, parent, abono):
        """Crear item de abono del día"""
        item_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        item_frame.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(item_frame, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Fila superior - Crédito y monto
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x")
        
        ctk.CTkLabel(
            top_row,
            text=f"Crédito #{abono.get('id_credito')} - Venta #{abono.get('id_venta', 'N/A')}",
            font=("Segoe UI", 13, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Badge de monto
        monto_badge = ctk.CTkFrame(top_row, fg_color="#4CAF50", corner_radius=15)
        monto_badge.pack(side="right")
        
        ctk.CTkLabel(
            monto_badge,
            text=f"${float(abono['monto_abono']):.2f}",
            font=("Segoe UI", 12, "bold"),
            text_color="white"
        ).pack(padx=15, pady=6)
        
        # Fila inferior - Detalles
        bottom_row = ctk.CTkFrame(content, fg_color="transparent")
        bottom_row.pack(fill="x", pady=(8, 0))
        
        # Hora
        hora = abono['fecha_abono'].strftime("%H:%M") if abono['fecha_abono'] else "-"
        ctk.CTkLabel(
            bottom_row,
            text=f"Hora: {hora}",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(side="left")
        
        # Método de pago
        if abono.get('metodo_pago'):
            ctk.CTkLabel(
                bottom_row,
                text=f"Método: {abono['metodo_pago']}",
                font=("Segoe UI", 11),
                text_color="#666666"
            ).pack(side="left", padx=(20, 0))
        
        # Monto total del crédito
        if abono.get('monto_total'):
            ctk.CTkLabel(
                bottom_row,
                text=f"Total crédito: ${float(abono['monto_total']):.2f}",
                font=("Segoe UI", 11),
                text_color="#666666"
            ).pack(side="right")

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
        """Crear una fila para un crédito con botones de acción"""
        row = ctk.CTkFrame(self.content_scroll, fg_color="transparent", height=50)
        row.pack(fill="x", pady=2)
        row.pack_propagate(False)
        
        # Determinar color según estado
        if credito['estado'] == 'Vencido':
            bg_color = "#FFEBEE"
        elif credito['estado'] == 'Pagado':
            bg_color = "#E8F5E9"
        else:
            bg_color = "white"
        
        row.configure(fg_color=bg_color)
        
        # Contenedor de información
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        # Fila superior - Información principal
        top_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        top_row.pack(fill="x")
        
        # ID y Venta
        ctk.CTkLabel(
            top_row,
            text=f"Crédito #{credito['id_credito']} - Venta #{credito['id_venta'] or 'N/A'}",
            font=("Segoe UI", 12, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Estado con color
        estado_colors = {
            'Activo': '#4CAF50',
            'Vencido': '#F44336', 
            'Pagado': '#2196F3',
            'Cancelado': '#9E9E9E'
        }
        
        estado_badge = ctk.CTkFrame(top_row, fg_color=estado_colors.get(credito['estado'], '#666666'), corner_radius=12)
        estado_badge.pack(side="right")
        
        ctk.CTkLabel(
            estado_badge,
            text=credito['estado'],
            font=("Segoe UI", 10, "bold"),
            text_color="white"
        ).pack(padx=10, pady=3)
        
        # Fila inferior - Detalles
        bottom_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        bottom_row.pack(fill="x", pady=(5, 0))
        
        # Fecha
        fecha = credito['fecha_credito'].strftime("%d/%m/%Y") if credito['fecha_credito'] else "-"
        ctk.CTkLabel(
            bottom_row,
            text=f"Fecha: {fecha}",
            font=("Segoe UI", 10),
            text_color="#666666"
        ).pack(side="left")
        
        # Montos
        monto_total = float(credito['monto_total'])
        monto_pagado = float(credito['monto_pagado'])
        saldo = float(credito['saldo_pendiente'])
        
        ctk.CTkLabel(
            bottom_row,
            text=f"Total: ${monto_total:.2f} | Pagado: ${monto_pagado:.2f} | Saldo: ${saldo:.2f}",
            font=("Segoe UI", 10),
            text_color="#666666"
        ).pack(side="left", padx=(20, 0))
        
        # Vencimiento
        vence = credito['fecha_vencimiento'].strftime("%d/%m/%Y") if credito['fecha_vencimiento'] else "-"
        ctk.CTkLabel(
            bottom_row,
            text=f"Vence: {vence}",
            font=("Segoe UI", 10),
            text_color="#F44336" if credito['estado'] == 'Vencido' else "#666666"
        ).pack(side="right")
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(row, fg_color="transparent", width=150)
        actions_frame.pack(side="right", padx=10, pady=5)
        actions_frame.pack_propagate(False)
        
        # Solo mostrar botón de abono si no está pagado
        if credito['estado'] in ['Activo', 'Vencido'] and saldo > 0:
            ctk.CTkButton(
                actions_frame,
                text="💰 Abono",
                fg_color="#4CAF50",
                hover_color="#45a049",
                width=70,
                height=30,
                font=("Segoe UI", 10, "bold"),
                command=lambda c=credito: self.registrar_abono(c)
            ).pack(side="top", pady=2)
        
        # Botón de detalles
        ctk.CTkButton(
            actions_frame,
            text="👁️ Ver",
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=70,
            height=30,
            font=("Segoe UI", 10),
            command=lambda c=credito: self.ver_detalle_credito(c)
        ).pack(side="top", pady=2)
    
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
        
        # Fecha de Vencimiento (calculada automáticamente)
        ctk.CTkLabel(form_frame, text="Fecha de Vencimiento:", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        
        from datetime import timedelta
        fecha_vencimiento_default = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
        
        fecha_venc_entry = ctk.CTkEntry(form_frame, placeholder_text="DD/MM/AAAA", height=45, font=("Segoe UI", 13))
        fecha_venc_entry.pack(fill="x", pady=(0, 15))
        fecha_venc_entry.insert(0, fecha_vencimiento_default)
        
        # Función para actualizar fecha de vencimiento cuando cambia el plazo
        def actualizar_fecha_vencimiento(*args):
            try:
                dias = int(plazo_entry.get())
                nueva_fecha = (datetime.now() + timedelta(days=dias)).strftime("%d/%m/%Y")
                fecha_venc_entry.delete(0, "end")
                fecha_venc_entry.insert(0, nueva_fecha)
            except:
                pass
        
        plazo_entry.bind("<KeyRelease>", actualizar_fecha_vencimiento)
        
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
                
                # Validar que el id_venta exista si se proporcionó
                if id_venta:
                    from database.db import crear_conexion
                    conn = crear_conexion()
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_venta FROM ventas WHERE id_venta = %s", (id_venta,))
                    venta_existe = cursor.fetchone()
                    conn.close()
                    
                    if not venta_existe:
                        messagebox.showwarning(
                            "Venta no encontrada",
                            f"No existe una venta con ID #{id_venta}.\n\n"
                            f"Puedes dejar el campo vacío para crear un crédito sin venta asociada."
                        )
                        return
                
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




    def registrar_abono(self, credito):
        """Abrir ventana para registrar un abono"""
        abono_window = ctk.CTkToplevel(self)
        abono_window.title("Registrar Abono")
        abono_window.geometry("450x600")
        abono_window.transient(self)
        abono_window.grab_set()
        
        # Centrar ventana
        abono_window.update_idletasks()
        x = (abono_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (abono_window.winfo_screenheight() // 2) - (600 // 2)
        abono_window.geometry(f"450x600+{x}+{y}")
        
        # Contenido principal
        main_frame = ctk.CTkFrame(abono_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(
            main_frame,
            text="💰 Registrar Abono",
            font=("Segoe UI", 22, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 20))
        
        # Información del crédito
        info_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5F5", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            info_content,
            text="Información del Crédito",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        # Detalles del crédito
        saldo_actual = float(credito.get('saldo_pendiente', 0))
        monto_total = float(credito.get('monto_total', 0))
        monto_pagado = float(credito.get('monto_pagado', 0))
        
        detalles = [
            f"Crédito #{credito.get('id_credito')}",
            f"Cliente: {credito.get('cliente_nombre', 'N/A')}",
            f"Monto Total: ${monto_total:.2f}",
            f"Pagado: ${monto_pagado:.2f}",
            f"Saldo Pendiente: ${saldo_actual:.2f}"
        ]
        
        for detalle in detalles:
            ctk.CTkLabel(
                info_content,
                text=detalle,
                font=("Segoe UI", 12),
                text_color="#666666"
            ).pack(anchor="w", pady=2)
        
        # Formulario de abono
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Monto del abono
        ctk.CTkLabel(
            form_frame,
            text="Monto del Abono: *",
            font=("Segoe UI", 13, "bold"),
            text_color="#666666"
        ).pack(anchor="w", pady=(0, 5))
        
        monto_abono_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="$0.00",
            height=45,
            font=("Segoe UI", 13)
        )
        monto_abono_entry.pack(fill="x", pady=(0, 15))
        
        # Botones de monto rápido
        quick_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        quick_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            quick_frame,
            text="Montos rápidos:",
            font=("Segoe UI", 11),
            text_color="#999999"
        ).pack(anchor="w", pady=(0, 5))
        
        buttons_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Botones de montos comunes
        montos_rapidos = [100, 200, 500, saldo_actual]  # Incluir saldo completo
        
        for i, monto in enumerate(montos_rapidos):
            if monto > 0:
                texto = f"${monto:.0f}" if monto != saldo_actual else "Pago Total"
                btn = ctk.CTkButton(
                    buttons_frame,
                    text=texto,
                    fg_color="#E0E0E0",
                    text_color="#666666",
                    hover_color="#D0D0D0",
                    width=80,
                    height=30,
                    font=("Segoe UI", 10),
                    command=lambda m=monto: monto_abono_entry.delete(0, "end") or monto_abono_entry.insert(0, str(m))
                )
                btn.pack(side="left", padx=2)
        
        # Método de pago
        ctk.CTkLabel(
            form_frame,
            text="Método de Pago:",
            font=("Segoe UI", 13, "bold"),
            text_color="#666666"
        ).pack(anchor="w", pady=(0, 5))
        
        metodo_combo = ctk.CTkComboBox(
            form_frame,
            values=["Efectivo", "Tarjeta", "Transferencia", "Cheque"],
            height=45,
            font=("Segoe UI", 13)
        )
        metodo_combo.pack(fill="x", pady=(0, 15))
        metodo_combo.set("Efectivo")
        
        # Notas del abono
        ctk.CTkLabel(
            form_frame,
            text="Notas (opcional):",
            font=("Segoe UI", 13, "bold"),
            text_color="#666666"
        ).pack(anchor="w", pady=(0, 5))
        
        notas_abono_entry = ctk.CTkTextbox(
            form_frame,
            height=80,
            font=("Segoe UI", 13)
        )
        notas_abono_entry.pack(fill="x", pady=(0, 20))
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def guardar_abono():
            monto_str = monto_abono_entry.get().strip()
            metodo = metodo_combo.get()
            notas = notas_abono_entry.get("1.0", "end").strip()
            
            if not monto_str:
                messagebox.showwarning("Datos incompletos", "Por favor ingresa el monto del abono")
                return
            
            try:
                monto_abono = float(monto_str.replace("$", "").replace(",", ""))
                
                if monto_abono <= 0:
                    messagebox.showwarning("Monto inválido", "El monto debe ser mayor a $0.00")
                    return
                
                if monto_abono > saldo_actual:
                    messagebox.showwarning(
                        "Monto excesivo",
                        f"El abono (${monto_abono:.2f}) no puede ser mayor al saldo pendiente (${saldo_actual:.2f})"
                    )
                    return
                
                # Registrar el abono
                from controllers.creditos import registrar_abono
                exito = registrar_abono(
                    id_credito=credito['id_credito'],
                    monto_abono=monto_abono,
                    metodo_pago=metodo,
                    notas=notas
                )
                
                if exito:
                    nuevo_saldo = saldo_actual - monto_abono
                    estado_final = "PAGADO COMPLETAMENTE" if nuevo_saldo <= 0 else f"Saldo restante: ${nuevo_saldo:.2f}"
                    
                    messagebox.showinfo(
                        "✅ Abono Registrado",
                        f"Abono registrado exitosamente\n\n"
                        f"Monto: ${monto_abono:.2f}\n"
                        f"Método: {metodo}\n"
                        f"Estado: {estado_final}"
                    )
                    abono_window.destroy()
                    self.cargar_datos()  # Recargar datos
                else:
                    messagebox.showerror("Error", "No se pudo registrar el abono")
                
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar abono: {str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Registrar Abono",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=50,
            font=("Segoe UI", 14, "bold"),
            command=guardar_abono
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=50,
            font=("Segoe UI", 14),
            command=abono_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def ver_detalle_credito(self, credito):
        """Mostrar ventana con detalles completos del crédito"""
        detalle_window = ctk.CTkToplevel(self)
        detalle_window.title(f"Detalle Crédito #{credito['id_credito']}")
        detalle_window.geometry("600x700")
        detalle_window.transient(self)
        detalle_window.grab_set()
        
        # Centrar ventana
        detalle_window.update_idletasks()
        x = (detalle_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (detalle_window.winfo_screenheight() // 2) - (700 // 2)
        detalle_window.geometry(f"600x700+{x}+{y}")
        
        # Contenido principal
        main_frame = ctk.CTkFrame(detalle_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text=f"📋 Crédito #{credito['id_credito']}",
            font=("Segoe UI", 22, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Estado
        estado_colors = {
            'Activo': '#4CAF50',
            'Vencido': '#F44336',
            'Pagado': '#2196F3',
            'Cancelado': '#9E9E9E'
        }
        
        estado_badge = ctk.CTkFrame(header_frame, fg_color=estado_colors.get(credito['estado'], '#666666'), corner_radius=15)
        estado_badge.pack(side="right")
        
        ctk.CTkLabel(
            estado_badge,
            text=credito['estado'],
            font=("Segoe UI", 12, "bold"),
            text_color="white"
        ).pack(padx=15, pady=8)
        
        # Información del crédito
        info_scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        info_scroll.pack(fill="both", expand=True, pady=(0, 15))
        
        # Información general
        general_frame = ctk.CTkFrame(info_scroll, fg_color="#F5F5F5", corner_radius=10)
        general_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            general_frame,
            text="Información General",
            font=("Segoe UI", 16, "bold"),
            text_color="#333333"
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        # Obtener información del cliente
        try:
            from database.db import crear_conexion
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT nombre, telefono, email FROM clientes WHERE id_cliente = %s", (credito.get('id_cliente'),))
            cliente_info = cursor.fetchone()
            conn.close()
        except:
            cliente_info = None
        
        info_items = [
            ("ID Crédito:", f"#{credito['id_credito']}"),
            ("ID Venta:", f"#{credito['id_venta']}" if credito['id_venta'] else "Sin venta asociada"),
            ("Cliente:", cliente_info['nombre'] if cliente_info else "N/A"),
            ("Teléfono:", cliente_info['telefono'] if cliente_info else "N/A"),
            ("Fecha Crédito:", credito['fecha_credito'].strftime("%d/%m/%Y %H:%M") if credito['fecha_credito'] else "-"),
            ("Fecha Vencimiento:", credito['fecha_vencimiento'].strftime("%d/%m/%Y") if credito['fecha_vencimiento'] else "-"),
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=2)
            
            ctk.CTkLabel(item_frame, text=label, font=("Segoe UI", 12, "bold"), text_color="#666666").pack(side="left")
            ctk.CTkLabel(item_frame, text=value, font=("Segoe UI", 12), text_color="#333333").pack(side="right")
        
        # Separador
        ctk.CTkFrame(general_frame, height=1, fg_color="#E0E0E0").pack(fill="x", padx=20, pady=10)
        
        # Información financiera
        monto_total = float(credito['monto_total'])
        monto_pagado = float(credito['monto_pagado'])
        saldo = float(credito['saldo_pendiente'])
        
        financial_items = [
            ("Monto Total:", f"${monto_total:.2f}", "#E91E63"),
            ("Monto Pagado:", f"${monto_pagado:.2f}", "#4CAF50"),
            ("Saldo Pendiente:", f"${saldo:.2f}", "#F44336" if saldo > 0 else "#4CAF50"),
        ]
        
        for label, value, color in financial_items:
            item_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=2)
            
            ctk.CTkLabel(item_frame, text=label, font=("Segoe UI", 12, "bold"), text_color="#666666").pack(side="left")
            ctk.CTkLabel(item_frame, text=value, font=("Segoe UI", 14, "bold"), text_color=color).pack(side="right")
        
        # Notas si existen
        if credito.get('notas'):
            ctk.CTkFrame(general_frame, height=1, fg_color="#E0E0E0").pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                general_frame,
                text="Notas:",
                font=("Segoe UI", 12, "bold"),
                text_color="#666666"
            ).pack(padx=20, anchor="w")
            
            ctk.CTkLabel(
                general_frame,
                text=credito['notas'],
                font=("Segoe UI", 12),
                text_color="#333333",
                wraplength=500,
                justify="left"
            ).pack(padx=20, pady=(5, 15), anchor="w")
        else:
            ctk.CTkFrame(general_frame, height=15, fg_color="transparent").pack()
        
        # Historial de abonos
        abonos_frame = ctk.CTkFrame(info_scroll, fg_color="#F5F5F5", corner_radius=10)
        abonos_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            abonos_frame,
            text="Historial de Abonos",
            font=("Segoe UI", 16, "bold"),
            text_color="#333333"
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        # Obtener abonos
        try:
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM abonos_creditos 
                WHERE id_credito = %s 
                ORDER BY fecha_abono DESC
            """, (credito['id_credito'],))
            abonos = cursor.fetchall()
            conn.close()
        except:
            abonos = []
        
        if abonos:
            for abono in abonos:
                abono_item = ctk.CTkFrame(abonos_frame, fg_color="white", corner_radius=8)
                abono_item.pack(fill="x", padx=20, pady=5)
                
                abono_content = ctk.CTkFrame(abono_item, fg_color="transparent")
                abono_content.pack(fill="x", padx=15, pady=10)
                
                # Fecha y monto
                top_row = ctk.CTkFrame(abono_content, fg_color="transparent")
                top_row.pack(fill="x")
                
                fecha_abono = abono['fecha_abono'].strftime("%d/%m/%Y %H:%M") if abono['fecha_abono'] else "-"
                ctk.CTkLabel(
                    top_row,
                    text=fecha_abono,
                    font=("Segoe UI", 12, "bold"),
                    text_color="#333333"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    top_row,
                    text=f"${float(abono['monto_abono']):.2f}",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#4CAF50"
                ).pack(side="right")
                
                # Método y notas
                if abono.get('metodo_pago') or abono.get('notas'):
                    bottom_row = ctk.CTkFrame(abono_content, fg_color="transparent")
                    bottom_row.pack(fill="x", pady=(5, 0))
                    
                    if abono.get('metodo_pago'):
                        ctk.CTkLabel(
                            bottom_row,
                            text=f"Método: {abono['metodo_pago']}",
                            font=("Segoe UI", 10),
                            text_color="#666666"
                        ).pack(side="left")
                    
                    if abono.get('notas'):
                        ctk.CTkLabel(
                            bottom_row,
                            text=f"Notas: {abono['notas']}",
                            font=("Segoe UI", 10),
                            text_color="#666666"
                        ).pack(side="right")
        else:
            ctk.CTkLabel(
                abonos_frame,
                text="📋 No hay abonos registrados",
                font=("Segoe UI", 12),
                text_color="#999999"
            ).pack(padx=20, pady=20)
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        # Solo mostrar botón de abono si no está pagado
        if credito['estado'] in ['Activo', 'Vencido'] and saldo > 0:
            ctk.CTkButton(
                btn_frame,
                text="💰 Registrar Abono",
                fg_color="#4CAF50",
                hover_color="#45a049",
                height=45,
                font=("Segoe UI", 13, "bold"),
                command=lambda: (detalle_window.destroy(), self.registrar_abono(credito))
            ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cerrar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=45,
            font=("Segoe UI", 13),
            command=detalle_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def mostrar_gestion_clientes(self):
        """Mostrar tab de Gestión de Clientes"""
        from views.clientes_view import ClientesView
        
        # Crear instancia de la vista de clientes dentro del content_frame
        clientes_view = ClientesView(self.content_frame, self.user)
