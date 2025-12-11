import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from controllers.apartados import listar_apartados, obtener_apartado_detalle, actualizar_estado_apartado

class GestionApartadosView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.pack(fill="both", expand=True)
        
        self.user = user or {"nombre_completo": "Administrador", "email": "admin@janet.com"}
        self.apartados = []
        self.estado_filtro = "Todos los estados"
        
        self.crear_interfaz()
        self.cargar_datos()
    
    def crear_interfaz(self):
        # Panel principal (sin sidebar, ya está en main.py)
        self.crear_panel_principal(self)



    def crear_panel_principal(self, parent):
        """Panel principal con apartados"""
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        panel.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        
        ctk.CTkLabel(info_frame1, text="📋 Total", font=("Segoe UI", 13), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.total_label = ctk.CTkLabel(info_frame1, text="1", 
                    font=("Segoe UI", 28, "bold"), text_color="#333333", anchor="w")
        self.total_label.pack(anchor="w")
        
        # Tarjeta 2: Activos
        card2 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        
        info_frame2 = ctk.CTkFrame(card2, fg_color="transparent")
        info_frame2.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(info_frame2, text="Activos", font=("Segoe UI", 13), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.activos_label = ctk.CTkLabel(info_frame2, text="0", 
                    font=("Segoe UI", 28, "bold"), text_color="#333333", anchor="w")
        self.activos_label.pack(anchor="w")
        
        # Tarjeta 3: Completados
        card3 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card3.grid(row=0, column=2, padx=5, sticky="ew")
        
        info_frame3 = ctk.CTkFrame(card3, fg_color="transparent")
        info_frame3.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(info_frame3, text="✅ Completados", font=("Segoe UI", 13), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.completados_label = ctk.CTkLabel(info_frame3, text="0", 
                    font=("Segoe UI", 28, "bold"), text_color="#4CAF50", anchor="w")
        self.completados_label.pack(anchor="w")
        
        # Tarjeta 4: Cancelados
        card4 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card4.grid(row=0, column=3, padx=5, sticky="ew")
        
        info_frame4 = ctk.CTkFrame(card4, fg_color="transparent")
        info_frame4.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(info_frame4, text="🚫 Cancelados", font=("Segoe UI", 13), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.cancelados_label = ctk.CTkLabel(info_frame4, text="1", 
                    font=("Segoe UI", 28, "bold"), text_color="#E53935", anchor="w")
        self.cancelados_label.pack(anchor="w")
        
        # Tarjeta 5: Pendiente
        card5 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card5.grid(row=0, column=4, padx=5, sticky="ew")
        
        info_frame5 = ctk.CTkFrame(card5, fg_color="transparent")
        info_frame5.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(info_frame5, text="⏱ Pendiente", font=("Segoe UI", 13), 
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
        try:
            from controllers.apartados import obtener_estadisticas_apartados
            stats = obtener_estadisticas_apartados()
            
            self.total_label.configure(text=str(stats.get('total', 0)))
            self.activos_label.configure(text=str(stats.get('activos', 0)))
            self.completados_label.configure(text=str(stats.get('completados', 0)))
            self.cancelados_label.configure(text=str(stats.get('cancelados', 0)))
            self.pendiente_label.configure(text=f"${float(stats.get('pendiente_total', 0)):,.2f}")
        except Exception as e:
            print(f"Error al actualizar estadísticas: {e}")
            # Valores por defecto si hay error
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
        fila = ctk.CTkFrame(parent, fg_color="white", height=50)
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
            font=("Segoe UI", 13),
            text_color="#333333",
            width=180,
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Total
        total = float(apartado.get("total", 0))
        ctk.CTkLabel(
            fila,
            text=f"${total:.2f}",
            font=("Segoe UI", 13),
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
            font=("Segoe UI", 13),
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
        
        # Botón Eliminar
        ctk.CTkButton(
            acciones_frame,
            text="🗑️",
            fg_color="transparent",
            text_color="#F44336",
            hover_color="#FFEBEE",
            width=35,
            height=35,
            font=("Segoe UI", 16),
            command=lambda a=apartado: self.eliminar_apartado(a)
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
        # Crear ventana de nuevo apartado
        apartado_window = ctk.CTkToplevel(self)
        apartado_window.title("Nuevo Apartado")
        apartado_window.geometry("600x700")
        apartado_window.transient(self)
        apartado_window.grab_set()
        
        # Centrar ventana
        apartado_window.update_idletasks()
        x = (apartado_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (apartado_window.winfo_screenheight() // 2) - (700 // 2)
        apartado_window.geometry(f"600x700+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(apartado_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="📋 Nuevo Apartado",
            font=("Segoe UI", 20, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Información del cliente
        ctk.CTkLabel(
            form_frame,
            text="Información del Cliente",
            font=("Segoe UI", 14, "bold"),
            text_color="#E91E63"
        ).pack(anchor="w", pady=(0, 10))
        
        # Nombre del cliente
        ctk.CTkLabel(form_frame, text="Nombre del Cliente:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        cliente_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre completo", height=40, font=("Segoe UI", 13))
        cliente_entry.pack(fill="x", pady=(0, 15))
        
        # Teléfono
        ctk.CTkLabel(form_frame, text="Teléfono:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        telefono_entry = ctk.CTkEntry(form_frame, placeholder_text="10 dígitos", height=40, font=("Segoe UI", 13))
        telefono_entry.pack(fill="x", pady=(0, 15))
        
        # Información del apartado
        ctk.CTkLabel(
            form_frame,
            text="Información del Apartado",
            font=("Segoe UI", 14, "bold"),
            text_color="#E91E63"
        ).pack(anchor="w", pady=(10, 10))
        
        # Total
        ctk.CTkLabel(form_frame, text="Total del Apartado:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        total_entry = ctk.CTkEntry(form_frame, placeholder_text="$0.00", height=40, font=("Segoe UI", 13))
        total_entry.pack(fill="x", pady=(0, 15))
        
        # Anticipo
        ctk.CTkLabel(form_frame, text="Anticipo:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        anticipo_entry = ctk.CTkEntry(form_frame, placeholder_text="$0.00", height=40, font=("Segoe UI", 13))
        anticipo_entry.pack(fill="x", pady=(0, 15))
        
        # Fecha límite con calendario
        ctk.CTkLabel(form_frame, text="Fecha Límite:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        
        fecha_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fecha_frame.pack(fill="x", pady=(0, 15))
        
        fecha_entry = ctk.CTkEntry(fecha_frame, placeholder_text="DD/MM/AAAA", height=40, font=("Segoe UI", 13))
        fecha_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botón para abrir calendario
        def abrir_calendario():
            try:
                from tkcalendar import Calendar
                import tkinter as tk
                
                cal_window = ctk.CTkToplevel(apartado_window)
                cal_window.title("Seleccionar Fecha")
                cal_window.geometry("300x300")
                cal_window.transient(apartado_window)
                cal_window.grab_set()
                
                # Centrar ventana
                cal_window.update_idletasks()
                x = (cal_window.winfo_screenwidth() // 2) - (300 // 2)
                y = (cal_window.winfo_screenheight() // 2) - (300 // 2)
                cal_window.geometry(f"300x300+{x}+{y}")
                
                # Calendario
                cal = Calendar(cal_window, selectmode='day', date_pattern='dd/mm/yyyy')
                cal.pack(fill="both", expand=True, padx=10, pady=10)
                
                def seleccionar_fecha():
                    fecha_entry.delete(0, 'end')
                    fecha_entry.insert(0, cal.get_date())
                    cal_window.destroy()
                
                ctk.CTkButton(
                    cal_window,
                    text="Seleccionar",
                    command=seleccionar_fecha,
                    fg_color="#E91E63",
                    hover_color="#C2185B"
                ).pack(pady=10)
                
            except ImportError:
                messagebox.showinfo("Calendario", "Instala tkcalendar: pip install tkcalendar")
        
        ctk.CTkButton(
            fecha_frame,
            text="📅",
            width=50,
            height=40,
            fg_color="#E91E63",
            hover_color="#C2185B",
            font=("Segoe UI", 18),
            command=abrir_calendario
        ).pack(side="left")
        
        # Descripción
        ctk.CTkLabel(form_frame, text="Descripción del Producto:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        descripcion_entry = ctk.CTkTextbox(form_frame, height=80, font=("Segoe UI", 13))
        descripcion_entry.pack(fill="x", pady=(0, 15))
        
        # Resumen con cálculo automático
        resumen_frame = ctk.CTkFrame(form_frame, fg_color="#E8F5E9", corner_radius=10)
        resumen_frame.pack(fill="x", pady=(10, 0))
        
        resumen_content = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        resumen_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            resumen_content,
            text="💰 Cuánta feria tiene que dar:",
            font=("Segoe UI", 13, "bold"),
            text_color="#2E7D32",
            anchor="w"
        ).pack(anchor="w")
        
        saldo_label = ctk.CTkLabel(
            resumen_content,
            text="$0.00",
            font=("Segoe UI", 24, "bold"),
            text_color="#2E7D32",
            anchor="w"
        )
        saldo_label.pack(anchor="w", pady=(5, 0))
        
        # Función para calcular saldo automáticamente
        def calcular_saldo(*args):
            try:
                total = float(total_entry.get() or 0)
                anticipo = float(anticipo_entry.get() or 0)
                saldo = total - anticipo
                saldo_label.configure(text=f"${saldo:,.2f}")
                
                if saldo < 0:
                    saldo_label.configure(text_color="#E53935")
                    resumen_frame.configure(fg_color="#FFEBEE")
                elif saldo == 0:
                    saldo_label.configure(text_color="#2E7D32")
                    resumen_frame.configure(fg_color="#E8F5E9")
                else:
                    saldo_label.configure(text_color="#2E7D32")
                    resumen_frame.configure(fg_color="#E8F5E9")
            except:
                saldo_label.configure(text="$0.00")
        
        # Vincular eventos para cálculo automático
        total_entry.bind("<KeyRelease>", calcular_saldo)
        anticipo_entry.bind("<KeyRelease>", calcular_saldo)
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def guardar_apartado():
            cliente = cliente_entry.get().strip()
            telefono = telefono_entry.get().strip()
            total = total_entry.get().strip()
            anticipo = anticipo_entry.get().strip()
            fecha = fecha_entry.get().strip()
            descripcion = descripcion_entry.get("1.0", "end-1c").strip()
            
            if not cliente or not telefono or not total or not anticipo:
                messagebox.showwarning("Datos incompletos", "Por favor completa todos los campos obligatorios")
                return
            
            try:
                from database.db import crear_conexion
                from datetime import datetime
                
                total_float = float(total)
                anticipo_float = float(anticipo)
                saldo = total_float - anticipo_float
                
                if anticipo_float > total_float:
                    messagebox.showwarning("Error", "El anticipo no puede ser mayor al total")
                    return
                
                # Crear o buscar cliente
                conn = crear_conexion()
                cursor = conn.cursor()
                
                # Buscar si el cliente ya existe
                cursor.execute("SELECT id_cliente FROM clientes WHERE telefono = %s", (telefono,))
                cliente_existente = cursor.fetchone()
                
                if cliente_existente:
                    id_cliente = cliente_existente[0]
                    # Actualizar nombre si cambió
                    cursor.execute("UPDATE clientes SET nombre = %s WHERE id_cliente = %s", (cliente, id_cliente))
                else:
                    # Crear nuevo cliente
                    cursor.execute(
                        "INSERT INTO clientes (nombre, telefono, correo) VALUES (%s, %s, %s)",
                        (cliente, telefono, "")
                    )
                    id_cliente = cursor.lastrowid
                
                # Parsear fecha límite
                fecha_limite = None
                if fecha:
                    try:
                        fecha_limite = datetime.strptime(fecha, "%d/%m/%Y").date()
                    except:
                        try:
                            fecha_limite = datetime.strptime(fecha, "%Y-%m-%d").date()
                        except:
                            pass
                
                # Crear apartado
                cursor.execute("""
                    INSERT INTO apartados (id_cliente, total, anticipo, saldo, fecha_limite, estado)
                    VALUES (%s, %s, %s, %s, %s, 'Pendiente')
                """, (id_cliente, total_float, anticipo_float, saldo, fecha_limite))
                
                id_apartado = cursor.lastrowid
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo(
                    "Apartado Registrado",
                    f"✅ Apartado #{id_apartado} registrado exitosamente:\n\n"
                    f"Cliente: {cliente}\n"
                    f"Total: ${total_float:,.2f}\n"
                    f"Anticipo: ${anticipo_float:,.2f}\n"
                    f"Saldo: ${saldo:,.2f}\n"
                    f"Fecha límite: {fecha if fecha else 'No especificada'}"
                )
                apartado_window.destroy()
                self.cargar_datos()
                
            except ValueError:
                messagebox.showerror("Error", "Total y anticipo deben ser números válidos")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el apartado:\n{str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Apartado",
            fg_color="#F06292",
            hover_color="#E91E63",
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=guardar_apartado
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=45,
            font=("Segoe UI", 12),
            command=apartado_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))
    
    def ver_apartado(self, apartado):
        """Ver detalles del apartado"""
        try:
            detalle = obtener_apartado_detalle(apartado["id_apartado"])
            
            # Crear ventana de detalles más grande
            dialog = ctk.CTkToplevel(self)
            dialog.title(f"Detalle del Apartado #{apartado['id_apartado']}")
            dialog.geometry("700x800")
            dialog.transient(self)
            dialog.grab_set()
            
            # Centrar ventana
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
            y = (dialog.winfo_screenheight() // 2) - (800 // 2)
            dialog.geometry(f"700x800+{x}+{y}")
            
            # Contenido con scroll
            scroll_frame = ctk.CTkScrollableFrame(dialog, fg_color="white")
            scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título
            ctk.CTkLabel(
                scroll_frame,
                text=f"Detalle del Apartado #{apartado['id_apartado']}",
                font=("Segoe UI", 22, "bold"),
                text_color="#333333"
            ).pack(pady=(0, 20))
            
            # Información del Cliente
            ctk.CTkLabel(
                scroll_frame,
                text="Información del Cliente",
                font=("Segoe UI", 16, "bold"),
                text_color="#333333"
            ).pack(anchor="w", pady=(0, 10))
            
            info_frame = ctk.CTkFrame(scroll_frame, fg_color="#F5F5F5", corner_radius=10)
            info_frame.pack(fill="x", pady=(0, 15))
            
            # Obtener información del cliente desde la base de datos
            from database.db import crear_conexion
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.nombre, c.telefono, c.correo as email 
                FROM clientes c
                JOIN apartados a ON c.id_cliente = a.id_cliente
                WHERE a.id_apartado = %s
            """, (apartado['id_apartado'],))
            cliente_info = cursor.fetchone()
            conn.close()
            
            if cliente_info:
                # Nombre con icono
                nombre_row = ctk.CTkFrame(info_frame, fg_color="transparent")
                nombre_row.pack(fill="x", padx=15, pady=(10, 5))
                ctk.CTkLabel(nombre_row, text="👤", font=("Segoe UI", 16)).pack(side="left", padx=(0, 10))
                ctk.CTkLabel(nombre_row, text=cliente_info.get("nombre", "N/A"), 
                            font=("Segoe UI", 14, "bold"), text_color="#333333").pack(side="left")
                
                # Teléfono con icono
                if cliente_info.get("telefono"):
                    tel_row = ctk.CTkFrame(info_frame, fg_color="transparent")
                    tel_row.pack(fill="x", padx=15, pady=5)
                    ctk.CTkLabel(tel_row, text="📞", font=("Segoe UI", 14)).pack(side="left", padx=(0, 10))
                    ctk.CTkLabel(tel_row, text=cliente_info.get("telefono"), 
                                font=("Segoe UI", 12), text_color="#666666").pack(side="left")
                
                # Email con icono
                if cliente_info.get("email"):
                    email_row = ctk.CTkFrame(info_frame, fg_color="transparent")
                    email_row.pack(fill="x", padx=15, pady=(5, 10))
                    ctk.CTkLabel(email_row, text="📧", font=("Segoe UI", 14)).pack(side="left", padx=(0, 10))
                    ctk.CTkLabel(email_row, text=cliente_info.get("email"), 
                                font=("Segoe UI", 12), text_color="#666666").pack(side="left")
            else:
                ctk.CTkLabel(info_frame, text=apartado.get("cliente_nombre", "N/A"), 
                            font=("Segoe UI", 14, "bold"), text_color="#333333").pack(padx=15, pady=10)
            
            # Resumen financiero
            resumen_frame = ctk.CTkFrame(scroll_frame, fg_color="#FFF0F5", corner_radius=10)
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
            
            # Productos Apartados
            ctk.CTkLabel(scroll_frame, text="Productos Apartados", font=("Segoe UI", 16, "bold"), 
                        text_color="#333333").pack(anchor="w", pady=(10, 10))
            
            if detalle and "productos" in detalle:
                for prod in detalle["productos"]:
                    prod_frame = ctk.CTkFrame(scroll_frame, fg_color="#F9F9F9", corner_radius=8)
                    prod_frame.pack(fill="x", pady=3)
                    
                    # Nombre y cantidad
                    left_frame = ctk.CTkFrame(prod_frame, fg_color="transparent")
                    left_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
                    
                    ctk.CTkLabel(
                        left_frame,
                        text=prod.get('nombre', 'N/A'),
                        font=("Segoe UI", 13, "bold"),
                        text_color="#333333"
                    ).pack(anchor="w")
                    
                    ctk.CTkLabel(
                        left_frame,
                        text=f"{prod.get('cantidad', 0)} x ${prod.get('precio', 0):.2f}",
                        font=("Segoe UI", 11),
                        text_color="#666666"
                    ).pack(anchor="w")
                    
                    # Precio total
                    ctk.CTkLabel(
                        prod_frame,
                        text=f"${prod.get('subtotal', 0):.2f}",
                        font=("Segoe UI", 14, "bold"),
                        text_color="#E91E63"
                    ).pack(side="right", padx=15, pady=10)
            
            # Historial de Pagos
            ctk.CTkLabel(scroll_frame, text="Historial de Pagos", font=("Segoe UI", 16, "bold"), 
                        text_color="#333333").pack(anchor="w", pady=(15, 10))
            
            # Obtener historial de pagos (anticipo inicial)
            pagos_frame = ctk.CTkFrame(scroll_frame, fg_color="#F9F9F9", corner_radius=8)
            pagos_frame.pack(fill="x", pady=(0, 15))
            
            # Pago inicial (anticipo)
            pago_row = ctk.CTkFrame(pagos_frame, fg_color="transparent")
            pago_row.pack(fill="x", padx=15, pady=10)
            
            fecha_apartado = apartado.get('fecha_apartado', apartado.get('fecha_creacion', 'N/A'))
            if isinstance(fecha_apartado, str):
                fecha_str = fecha_apartado.split()[0] if ' ' in fecha_apartado else fecha_apartado
            else:
                fecha_str = str(fecha_apartado)
            
            ctk.CTkLabel(
                pago_row,
                text=f"{fecha_str} - Efectivo",
                font=("Segoe UI", 12),
                text_color="#666666"
            ).pack(side="left")
            
            ctk.CTkLabel(
                pago_row,
                text=f"${apartado.get('anticipo', 0):.2f}",
                font=("Segoe UI", 12, "bold"),
                text_color="#4CAF50"
            ).pack(side="right")
            
            # Fechas importantes
            fechas_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            fechas_frame.pack(fill="x", pady=(10, 15))
            
            # Fecha de Apartado
            fecha_apart_frame = ctk.CTkFrame(fechas_frame, fg_color="#E3F2FD", corner_radius=8)
            fecha_apart_frame.pack(side="left", expand=True, fill="x", padx=(0, 5))
            
            ctk.CTkLabel(
                fecha_apart_frame,
                text="Fecha de Apartado",
                font=("Segoe UI", 11),
                text_color="#666666"
            ).pack(pady=(10, 2))
            
            ctk.CTkLabel(
                fecha_apart_frame,
                text=fecha_str,
                font=("Segoe UI", 13, "bold"),
                text_color="#333333"
            ).pack(pady=(0, 10))
            
            # Fecha Límite
            fecha_limite_frame = ctk.CTkFrame(fechas_frame, fg_color="#FFF3E0", corner_radius=8)
            fecha_limite_frame.pack(side="left", expand=True, fill="x", padx=(5, 0))
            
            ctk.CTkLabel(
                fecha_limite_frame,
                text="Fecha Límite",
                font=("Segoe UI", 11),
                text_color="#666666"
            ).pack(pady=(10, 2))
            
            fecha_limite = apartado.get('fecha_limite', 'N/A')
            if isinstance(fecha_limite, str):
                fecha_lim_str = fecha_limite.split()[0] if ' ' in fecha_limite else fecha_limite
            else:
                fecha_lim_str = str(fecha_limite)
            
            ctk.CTkLabel(
                fecha_limite_frame,
                text=fecha_lim_str,
                font=("Segoe UI", 13, "bold"),
                text_color="#333333"
            ).pack(pady=(0, 10))
            
            # Botones de acción
            buttons_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=(10, 0))
            
            # Botón Editar
            ctk.CTkButton(
                buttons_frame,
                text="✏️ Editar",
                fg_color="#2196F3",
                hover_color="#1976D2",
                height=45,
                font=("Segoe UI", 13, "bold"),
                corner_radius=10,
                command=lambda: self.editar_apartado(apartado, dialog)
            ).pack(side="left", expand=True, fill="x", padx=(0, 5))
            
            # Botón Cerrar
            ctk.CTkButton(
                buttons_frame,
                text="Cerrar",
                fg_color="#E91E63",
                hover_color="#C2185B",
                height=40,
                font=("Segoe UI", 12, "bold"),
                command=dialog.destroy
            ).pack(side="left", expand=True, fill="x", padx=(5, 0))
            
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
    
    def eliminar_apartado(self, apartado):
        """Eliminar apartado permanentemente"""
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que deseas eliminar el apartado #{apartado['id_apartado']}?\n\n"
            f"Cliente: {apartado.get('cliente_nombre', 'N/A')}\n"
            f"Total: ${apartado.get('total', 0):.2f}\n\n"
            f"⚠️ Esta acción eliminará el apartado permanentemente y no se puede deshacer.",
            icon='warning'
        )
        
        if not respuesta:
            return
        
        try:
            from database.db import crear_conexion
            
            conn = crear_conexion()
            if not conn:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
            
            cursor = conn.cursor()
            
            # Eliminar apartado
            cursor.execute(
                "DELETE FROM apartados WHERE id_apartado = %s",
                (apartado['id_apartado'],)
            )
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo(
                "Apartado Eliminado",
                f"El apartado #{apartado['id_apartado']} ha sido eliminado correctamente"
            )
            
            # Recargar datos
            self.cargar_datos()
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el apartado:\n{str(e)}"
            )

    def editar_apartado(self, apartado, dialog_anterior=None):
        """Editar apartado existente"""
        # Cerrar el diálogo anterior si existe
        if dialog_anterior:
            dialog_anterior.destroy()
        
        # Crear ventana de edición
        edit_window = ctk.CTkToplevel(self)
        edit_window.title(f"Editar Apartado #{apartado['id_apartado']}")
        edit_window.geometry("600x700")
        edit_window.transient(self)
        edit_window.grab_set()
        
        # Centrar ventana
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (700 // 2)
        edit_window.geometry(f"600x700+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(edit_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text=f"✏️ Editar Apartado #{apartado['id_apartado']}",
            font=("Segoe UI", 20, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Información del cliente
        ctk.CTkLabel(
            form_frame,
            text="Información del Cliente",
            font=("Segoe UI", 14, "bold"),
            text_color="#E91E63"
        ).pack(anchor="w", pady=(0, 10))
        
        # Nombre del cliente
        ctk.CTkLabel(form_frame, text="Nombre del Cliente:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        cliente_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre completo", height=40, font=("Segoe UI", 13))
        cliente_entry.pack(fill="x", pady=(0, 15))
        cliente_entry.insert(0, apartado.get("cliente_nombre", ""))
        
        # Teléfono
        ctk.CTkLabel(form_frame, text="Teléfono:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        telefono_entry = ctk.CTkEntry(form_frame, placeholder_text="10 dígitos", height=40, font=("Segoe UI", 13))
        telefono_entry.pack(fill="x", pady=(0, 15))
        telefono_entry.insert(0, apartado.get("cliente_telefono", ""))
        
        # Información del apartado
        ctk.CTkLabel(
            form_frame,
            text="Información del Apartado",
            font=("Segoe UI", 14, "bold"),
            text_color="#E91E63"
        ).pack(anchor="w", pady=(10, 10))
        
        # Total
        ctk.CTkLabel(form_frame, text="Total del Apartado:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        total_entry = ctk.CTkEntry(form_frame, placeholder_text="$0.00", height=40, font=("Segoe UI", 13))
        total_entry.pack(fill="x", pady=(0, 15))
        total_entry.insert(0, str(apartado.get("total", 0)))
        
        # Anticipo
        ctk.CTkLabel(form_frame, text="Anticipo:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        anticipo_entry = ctk.CTkEntry(form_frame, placeholder_text="$0.00", height=40, font=("Segoe UI", 13))
        anticipo_entry.pack(fill="x", pady=(0, 15))
        anticipo_entry.insert(0, str(apartado.get("anticipo", 0)))
        
        # Fecha límite con calendario
        ctk.CTkLabel(form_frame, text="Fecha Límite:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        
        fecha_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fecha_frame.pack(fill="x", pady=(0, 15))
        
        fecha_entry = ctk.CTkEntry(fecha_frame, placeholder_text="DD/MM/AAAA", height=40, font=("Segoe UI", 13))
        fecha_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        if apartado.get("fecha_limite"):
            fecha_entry.insert(0, apartado.get("fecha_limite"))
        
        # Botón para abrir calendario
        def abrir_calendario():
            try:
                from tkcalendar import Calendar
                
                cal_window = ctk.CTkToplevel(edit_window)
                cal_window.title("Seleccionar Fecha")
                cal_window.geometry("300x300")
                cal_window.transient(edit_window)
                cal_window.grab_set()
                
                # Centrar ventana
                cal_window.update_idletasks()
                x = (cal_window.winfo_screenwidth() // 2) - (300 // 2)
                y = (cal_window.winfo_screenheight() // 2) - (300 // 2)
                cal_window.geometry(f"300x300+{x}+{y}")
                
                # Calendario
                cal = Calendar(cal_window, selectmode='day', date_pattern='dd/mm/yyyy')
                cal.pack(fill="both", expand=True, padx=10, pady=10)
                
                def seleccionar_fecha():
                    fecha_entry.delete(0, 'end')
                    fecha_entry.insert(0, cal.get_date())
                    cal_window.destroy()
                
                ctk.CTkButton(
                    cal_window,
                    text="Seleccionar",
                    command=seleccionar_fecha,
                    fg_color="#E91E63",
                    hover_color="#C2185B"
                ).pack(pady=10)
                
            except ImportError:
                messagebox.showinfo("Calendario", "Instala tkcalendar: pip install tkcalendar")
        
        ctk.CTkButton(
            fecha_frame,
            text="📅",
            width=50,
            height=40,
            fg_color="#E91E63",
            hover_color="#C2185B",
            font=("Segoe UI", 18),
            command=abrir_calendario
        ).pack(side="left")
        
        # Notas (opcional - si quieres agregar notas al apartado)
        # ctk.CTkLabel(form_frame, text="Notas:", font=("Segoe UI", 13), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        # descripcion_entry = ctk.CTkTextbox(form_frame, height=80, font=("Segoe UI", 13))
        # descripcion_entry.pack(fill="x", pady=(0, 15))
        
        # Resumen con cálculo automático
        resumen_frame = ctk.CTkFrame(form_frame, fg_color="#E8F5E9", corner_radius=10)
        resumen_frame.pack(fill="x", pady=(10, 0))
        
        resumen_content = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        resumen_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            resumen_content,
            text="💰 Cuánta feria tiene que dar:",
            font=("Segoe UI", 13, "bold"),
            text_color="#2E7D32",
            anchor="w"
        ).pack(anchor="w")
        
        saldo_label = ctk.CTkLabel(
            resumen_content,
            text=f"${apartado.get('saldo', 0):.2f}",
            font=("Segoe UI", 24, "bold"),
            text_color="#2E7D32",
            anchor="w"
        )
        saldo_label.pack(anchor="w", pady=(5, 0))
        
        # Función para calcular saldo automáticamente
        def calcular_saldo(*args):
            try:
                total = float(total_entry.get() or 0)
                anticipo = float(anticipo_entry.get() or 0)
                saldo = total - anticipo
                saldo_label.configure(text=f"${saldo:,.2f}")
                
                if saldo < 0:
                    saldo_label.configure(text_color="#E53935")
                    resumen_frame.configure(fg_color="#FFEBEE")
                elif saldo == 0:
                    saldo_label.configure(text_color="#2E7D32")
                    resumen_frame.configure(fg_color="#E8F5E9")
                else:
                    saldo_label.configure(text_color="#2E7D32")
                    resumen_frame.configure(fg_color="#E8F5E9")
            except:
                saldo_label.configure(text="$0.00")
        
        # Vincular eventos para cálculo automático
        total_entry.bind("<KeyRelease>", calcular_saldo)
        anticipo_entry.bind("<KeyRelease>", calcular_saldo)
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def guardar_cambios():
            cliente = cliente_entry.get().strip()
            telefono = telefono_entry.get().strip()
            total = total_entry.get().strip()
            anticipo = anticipo_entry.get().strip()
            fecha = fecha_entry.get().strip()
            
            if not cliente or not telefono or not total or not anticipo:
                messagebox.showwarning("Datos incompletos", "Por favor completa todos los campos obligatorios")
                return
            
            try:
                from database.db import crear_conexion
                
                total_float = float(total)
                anticipo_float = float(anticipo)
                saldo = total_float - anticipo_float
                
                if anticipo_float > total_float:
                    messagebox.showwarning("Error", "El anticipo no puede ser mayor al total")
                    return
                
                conn = crear_conexion()
                cursor = conn.cursor()
                
                # Actualizar apartado
                cursor.execute(
                    """UPDATE apartados 
                       SET total = %s, anticipo = %s, saldo = %s, fecha_limite = %s
                       WHERE id_apartado = %s""",
                    (total_float, anticipo_float, saldo, fecha, apartado['id_apartado'])
                )
                
                # Actualizar cliente
                cursor.execute(
                    """UPDATE clientes 
                       SET nombre = %s, telefono = %s
                       WHERE id_cliente = %s""",
                    (cliente, telefono, apartado.get('id_cliente'))
                )
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", f"✅ Apartado #{apartado['id_apartado']} actualizado correctamente")
                edit_window.destroy()
                self.cargar_datos()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el apartado:\n{str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Cambios",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=45,
            font=("Segoe UI", 13, "bold"),
            command=guardar_cambios
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#757575",
            hover_color="#616161",
            height=45,
            font=("Segoe UI", 13, "bold"),
            command=edit_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))
