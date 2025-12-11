import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image
from database.db import crear_conexion

class ClientesView(ctk.CTkFrame):
    """Vista de gestión de clientes - Diseño moderno"""
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.pack(fill="both", expand=True)
        self.user = user
        self.clientes = []
        
        self.crear_interfaz()
        self.cargar_clientes()
    
    def crear_interfaz(self):
        """Crear interfaz moderna de clientes"""
        # Contenedor principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header con logo
        self.crear_header_con_logo(main_container)
        
        # Estadísticas rápidas
        self.crear_estadisticas(main_container)
        
        # Barra de herramientas
        self.crear_barra_herramientas(main_container)
        
        # Contenedor de clientes
        self.crear_contenedor_clientes(main_container)
    
    def crear_header_con_logo(self, parent):
        """Crear header con logo y título"""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        # Logo pequeño
        logo_container = ctk.CTkFrame(header, fg_color="transparent")
        logo_container.pack(side="left", padx=(0, 15))
        
        try:
            logo_paths = [
                "logo_limpio_small.png",  # LOGO LIMPIO pequeño (40px)
                "logo_limpio_header.png",  # Logo limpio para header (50px)
                "logo_limpio_definitivo.png",  # Logo limpio completo
                "assets/logo_limpio_small.png",  # En carpeta assets
                "assets/logo_limpio_header.png",  # En carpeta assets
                "assets/logo_limpio_definitivo.png",  # En carpeta assets
                "logo_final_small.png",  # Fallback imagen original pequeña
                "logo_final_header.png",  # Fallback original header
                "logo_janet_rosa_definitivo.png",  # Fallback original completa
                "assets/logo_final_small.png",  # Fallback en assets
                "assets/logo_final_header.png",  # Fallback en assets
                "assets/logo_janet_rosa_definitivo.png",  # Fallback en assets
                "logo_nuevo_40.png",  # Fallback exacto pequeño
                "logo_nuevo_50.png",  # Fallback exacto mediano
                "logo_janet_rosa_exacto.png",  # Fallback exacto original
                "assets/logo_nuevo_40.png",  # Fallback en assets
                "logo_circular_40.png",  # Fallback anterior
                "logo_circular_50.png", 
                "assets/logo_circular_40.png",
                "assets/logo_circular_50.png",
                "logo_janet_rosa_profesional.png"
            ]
            logo_loaded = False
            
            for path in logo_paths:
                if os.path.exists(path):
                    try:
                        img = Image.open(path).resize((40, 40), Image.Resampling.LANCZOS)
                        logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
                        ctk.CTkLabel(logo_container, image=logo_image, text="").pack()
                        logo_loaded = True
                        break
                    except Exception:
                        continue
            
            if not logo_loaded:
                ctk.CTkLabel(logo_container, text="🚲", font=("Segoe UI", 24), text_color="#E91E63").pack()
        except Exception:
            ctk.CTkLabel(logo_container, text="🚲", font=("Segoe UI", 24), text_color="#E91E63").pack()
        
        # Título y descripción
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            title_frame,
            text="Gestión de Clientes",
            font=("Segoe UI", 28, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Administra la información de tus clientes registrados",
            font=("Segoe UI", 14),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
    
    def crear_estadisticas(self, parent):
        """Crear tarjetas de estadísticas"""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Configurar grid
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total de clientes
        self.crear_tarjeta_estadistica(
            stats_frame, 0, "👥", "#4CAF50", "Total Clientes", "0"
        )
        
        # Clientes con crédito
        self.crear_tarjeta_estadistica(
            stats_frame, 1, "💳", "#FF9800", "Con Crédito", "0"
        )
        
        # Clientes activos (últimos 30 días)
        self.crear_tarjeta_estadistica(
            stats_frame, 2, "⭐", "#2196F3", "Activos", "0"
        )
    
    def crear_tarjeta_estadistica(self, parent, column, icono, color, titulo, valor):
        """Crear una tarjeta de estadística"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, height=100)
        card.grid(row=0, column=column, padx=10, pady=0, sticky="ew")
        card.grid_propagate(False)
        
        # Contenido
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono con fondo de color
        icon_frame = ctk.CTkFrame(content, fg_color=color, corner_radius=8, width=50, height=50)
        icon_frame.pack(anchor="w")
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text=icono,
            font=("Segoe UI", 20),
            text_color="white"
        ).pack(expand=True)
        
        # Título
        ctk.CTkLabel(
            content,
            text=titulo,
            font=("Segoe UI", 11),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(10, 2))
        
        # Valor
        valor_label = ctk.CTkLabel(
            content,
            text=valor,
            font=("Segoe UI", 24, "bold"),
            text_color="#333333",
            anchor="w"
        )
        valor_label.pack(anchor="w")
        
        # Guardar referencia para actualizar
        if column == 0:
            self.total_label = valor_label
        elif column == 1:
            self.credito_label = valor_label
        elif column == 2:
            self.activos_label = valor_label
    
    def crear_barra_herramientas(self, parent):
        """Crear barra de herramientas con búsqueda y botones"""
        toolbar = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, height=70)
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)
        
        # Contenido de la barra
        toolbar_content = ctk.CTkFrame(toolbar, fg_color="transparent")
        toolbar_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Búsqueda
        search_container = ctk.CTkFrame(toolbar_content, fg_color="#F8F9FA", corner_radius=10)
        search_container.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        search_content = ctk.CTkFrame(search_container, fg_color="transparent")
        search_content.pack(fill="both", expand=True, padx=15, pady=10)
        
        ctk.CTkLabel(search_content, text="🔍", font=("Segoe UI", 16)).pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_content,
            placeholder_text="Buscar por nombre, teléfono o email...",
            border_width=0,
            fg_color="transparent",
            font=("Segoe UI", 13)
        )
        self.search_entry.pack(side="left", fill="both", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.buscar_clientes())
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(toolbar_content, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Botón nuevo cliente
        ctk.CTkButton(
            buttons_frame,
            text="➕ Nuevo Cliente",
            height=40,
            width=140,
            corner_radius=10,
            fg_color="#E91E63",
            hover_color="#C2185B",
            font=("Segoe UI", 12, "bold"),
            command=self.nuevo_cliente
        ).pack(side="left", padx=(0, 10))
        
        # Botón exportar
        ctk.CTkButton(
            buttons_frame,
            text="📊 Exportar",
            height=40,
            width=100,
            corner_radius=10,
            fg_color="#4CAF50",
            hover_color="#45A049",
            font=("Segoe UI", 12, "bold"),
            command=self.exportar_clientes
        ).pack(side="left")
    
    def crear_contenedor_clientes(self, parent):
        """Crear contenedor principal de clientes"""
        # Contenedor con título
        container = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        container.pack(fill="both", expand=True)
        
        # Header del contenedor
        header_container = ctk.CTkFrame(container, fg_color="transparent")
        header_container.pack(fill="x", padx=25, pady=(20, 15))
        
        ctk.CTkLabel(
            header_container,
            text="📋 Lista de Clientes",
            font=("Segoe UI", 18, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(side="left")
        
        # Contador de resultados
        self.contador_label = ctk.CTkLabel(
            header_container,
            text="0 clientes",
            font=("Segoe UI", 12),
            text_color="#666666"
        )
        self.contador_label.pack(side="right")
        
        # Área scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(
            container, 
            fg_color="transparent",
            corner_radius=0
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def cargar_clientes(self):
        """Cargar clientes desde la base de datos"""
        try:
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            
            # Cargar clientes básicos
            cursor.execute("""
                SELECT id_cliente, nombre, telefono, correo as email,
                       DATE(fecha_registro) as fecha_registro
                FROM clientes
                ORDER BY nombre
            """)
            self.clientes = cursor.fetchall()
            
            # Cargar estadísticas
            self.cargar_estadisticas(cursor)
            
            conn.close()
            self.mostrar_clientes()
            
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los clientes:\n{str(e)}")
    
    def cargar_estadisticas(self, cursor):
        """Cargar estadísticas de clientes"""
        try:
            # Total de clientes
            cursor.execute("SELECT COUNT(*) as total FROM clientes")
            total = cursor.fetchone()['total']
            self.total_label.configure(text=str(total))
            
            # Clientes con crédito activo
            cursor.execute("""
                SELECT COUNT(DISTINCT cliente_id) as con_credito 
                FROM creditos 
                WHERE estado = 'activo' AND saldo_pendiente > 0
            """)
            result = cursor.fetchone()
            con_credito = result['con_credito'] if result else 0
            self.credito_label.configure(text=str(con_credito))
            
            # Clientes activos (con ventas en últimos 30 días)
            cursor.execute("""
                SELECT COUNT(DISTINCT cliente_id) as activos
                FROM ventas 
                WHERE fecha >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                AND cliente_id IS NOT NULL
            """)
            result = cursor.fetchone()
            activos = result['activos'] if result else 0
            self.activos_label.configure(text=str(activos))
            
        except Exception as e:
            print(f"Error cargando estadísticas: {e}")
            # Valores por defecto en caso de error
            self.total_label.configure(text="0")
            self.credito_label.configure(text="0") 
            self.activos_label.configure(text="0")
    
    def mostrar_clientes(self, clientes=None):
        """Mostrar clientes en cards modernas"""
        # Limpiar contenido
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        clientes_mostrar = clientes if clientes is not None else self.clientes
        
        # Actualizar contador
        total = len(clientes_mostrar)
        if clientes is not None and self.search_entry.get():
            self.contador_label.configure(text=f"{total} de {len(self.clientes)} encontrados")
        else:
            self.contador_label.configure(text=f"{total} clientes")
        
        if not clientes_mostrar:
            self.mostrar_estado_vacio()
            return
        
        # Mostrar clientes en grid de cards
        self.mostrar_clientes_grid(clientes_mostrar)
    
    def mostrar_estado_vacio(self):
        """Mostrar estado vacío mejorado"""
        empty_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        empty_container.pack(fill="both", expand=True, pady=50)
        
        # Icono grande
        ctk.CTkLabel(
            empty_container,
            text="👥",
            font=("Segoe UI", 80),
            text_color="#E0E0E0"
        ).pack(pady=(0, 20))
        
        # Mensaje principal
        mensaje_principal = "No hay clientes registrados" if not self.search_entry.get() else "No se encontraron clientes"
        ctk.CTkLabel(
            empty_container,
            text=mensaje_principal,
            font=("Segoe UI", 20, "bold"),
            text_color="#666666"
        ).pack(pady=(0, 10))
        
        # Mensaje secundario
        if not self.search_entry.get():
            ctk.CTkLabel(
                empty_container,
                text="Comienza agregando tu primer cliente",
                font=("Segoe UI", 14),
                text_color="#999999"
            ).pack(pady=(0, 20))
            
            # Botón de acción
            ctk.CTkButton(
                empty_container,
                text="➕ Agregar Primer Cliente",
                height=45,
                width=200,
                corner_radius=12,
                fg_color="#E91E63",
                hover_color="#C2185B",
                font=("Segoe UI", 14, "bold"),
                command=self.nuevo_cliente
            ).pack()
        else:
            ctk.CTkLabel(
                empty_container,
                text="Intenta con otros términos de búsqueda",
                font=("Segoe UI", 14),
                text_color="#999999"
            ).pack()
    
    def mostrar_clientes_grid(self, clientes):
        """Mostrar clientes en formato grid"""
        # Crear contenedor para el grid
        grid_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        grid_container.pack(fill="both", expand=True)
        
        # Configurar grid (2 columnas)
        grid_container.grid_columnconfigure((0, 1), weight=1)
        
        for i, cliente in enumerate(clientes):
            row = i // 2
            col = i % 2
            self.crear_card_cliente(grid_container, cliente, row, col)
    
    def crear_card_cliente(self, parent, cliente, row, col):
        """Crear card moderna para un cliente"""
        # Card principal
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, height=140)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
        card.grid_propagate(False)
        
        # Contenido de la card
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header de la card
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        # Avatar y nombre
        avatar_container = ctk.CTkFrame(header, fg_color="transparent")
        avatar_container.pack(side="left", fill="x", expand=True)
        
        # Avatar circular
        inicial = (cliente['nombre'] or "?")[0].upper()
        avatar = ctk.CTkFrame(avatar_container, fg_color="#E91E63", corner_radius=20, width=40, height=40)
        avatar.pack(side="left", padx=(0, 12))
        avatar.pack_propagate(False)
        
        ctk.CTkLabel(
            avatar,
            text=inicial,
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        ).pack(expand=True)
        
        # Información del cliente
        info_container = ctk.CTkFrame(avatar_container, fg_color="transparent")
        info_container.pack(side="left", fill="x", expand=True)
        
        # Nombre
        nombre_text = cliente['nombre'] or "Sin nombre"
        if len(nombre_text) > 20:
            nombre_text = nombre_text[:17] + "..."
        
        ctk.CTkLabel(
            info_container,
            text=nombre_text,
            font=("Segoe UI", 16, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        # ID
        ctk.CTkLabel(
            info_container,
            text=f"Cliente #{cliente['id_cliente']}",
            font=("Segoe UI", 11),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))
        
        # Botón de menú
        menu_btn = ctk.CTkButton(
            header,
            text="⋮",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            text_color="#666666",
            hover_color="#F0F0F0",
            font=("Segoe UI", 16, "bold"),
            command=lambda c=cliente: self.mostrar_menu_cliente(c)
        )
        menu_btn.pack(side="right")
        
        # Información de contacto
        contact_frame = ctk.CTkFrame(content, fg_color="transparent")
        contact_frame.pack(fill="x")
        
        # Teléfono
        if cliente['telefono']:
            phone_container = ctk.CTkFrame(contact_frame, fg_color="transparent")
            phone_container.pack(fill="x", pady=(0, 5))
            
            ctk.CTkLabel(
                phone_container,
                text="📞",
                font=("Segoe UI", 12)
            ).pack(side="left", padx=(0, 8))
            
            ctk.CTkLabel(
                phone_container,
                text=cliente['telefono'],
                font=("Segoe UI", 12),
                text_color="#666666",
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
        
        # Email
        email = cliente.get('email', "")
        if email:
            email_container = ctk.CTkFrame(contact_frame, fg_color="transparent")
            email_container.pack(fill="x")
            
            ctk.CTkLabel(
                email_container,
                text="📧",
                font=("Segoe UI", 12)
            ).pack(side="left", padx=(0, 8))
            
            email_text = email if len(email) <= 25 else email[:22] + "..."
            ctk.CTkLabel(
                email_container,
                text=email_text,
                font=("Segoe UI", 12),
                text_color="#666666",
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
        
        # Efecto hover
        def on_enter(event):
            card.configure(fg_color="#F8F9FA")
        
        def on_leave(event):
            card.configure(fg_color="white")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
    
    def mostrar_menu_cliente(self, cliente):
        """Mostrar menú contextual del cliente"""
        # Crear ventana de menú
        menu_window = ctk.CTkToplevel(self)
        menu_window.title("")
        menu_window.geometry("200x150")
        menu_window.transient(self)
        menu_window.grab_set()
        menu_window.configure(fg_color="white")
        
        # Posicionar cerca del cursor
        x = self.winfo_rootx() + 100
        y = self.winfo_rooty() + 100
        menu_window.geometry(f"200x150+{x}+{y}")
        
        # Contenido del menú
        menu_frame = ctk.CTkFrame(menu_window, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Opciones del menú
        opciones = [
            ("✏️ Editar", lambda: [menu_window.destroy(), self.editar_cliente(cliente)]),
            ("📊 Ver Historial", lambda: [menu_window.destroy(), self.ver_historial_cliente(cliente)]),
            ("🗑️ Eliminar", lambda: [menu_window.destroy(), self.eliminar_cliente(cliente)])
        ]
        
        for texto, comando in opciones:
            btn = ctk.CTkButton(
                menu_frame,
                text=texto,
                height=35,
                corner_radius=8,
                fg_color="transparent",
                text_color="#333333",
                hover_color="#F0F0F0",
                font=("Segoe UI", 12),
                anchor="w",
                command=comando
            )
            btn.pack(fill="x", pady=2)
    
    def exportar_clientes(self):
        """Exportar lista de clientes a Excel"""
        try:
            from utils.exportar_pandas import exportar_clientes_excel
            
            if not self.clientes:
                messagebox.showwarning("Sin datos", "No hay clientes para exportar")
                return
            
            # Preparar datos para exportar
            datos_exportar = []
            for cliente in self.clientes:
                datos_exportar.append({
                    'ID': cliente['id_cliente'],
                    'Nombre': cliente['nombre'] or '',
                    'Teléfono': cliente['telefono'] or '',
                    'Email': cliente.get('email', '') or '',
                    'Fecha Registro': cliente.get('fecha_registro', '')
                })
            
            # Exportar
            if exportar_clientes_excel(datos_exportar):
                messagebox.showinfo("Éxito", "✅ Lista de clientes exportada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo exportar la lista de clientes")
                
        except ImportError:
            messagebox.showwarning("Función no disponible", 
                                 "La función de exportar no está disponible")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def ver_historial_cliente(self, cliente):
        """Ver historial de compras del cliente"""
        # Crear ventana de historial
        historial_window = ctk.CTkToplevel(self)
        historial_window.title(f"Historial - {cliente['nombre']}")
        historial_window.geometry("800x600")
        historial_window.transient(self)
        historial_window.grab_set()
        
        # Centrar ventana
        historial_window.update_idletasks()
        x = (historial_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (historial_window.winfo_screenheight() // 2) - (600 // 2)
        historial_window.geometry(f"800x600+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(historial_window, fg_color="#F5F5F5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=12)
        header.pack(fill="x", pady=(0, 20))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            header_content,
            text=f"📊 Historial de {cliente['nombre']}",
            font=("Segoe UI", 20, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_content,
            text=f"Cliente #{cliente['id_cliente']} • {cliente['telefono']}",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(anchor="w", pady=(5, 0))
        
        # Contenido del historial
        content_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=12)
        content_frame.pack(fill="both", expand=True)
        
        # Cargar y mostrar historial
        try:
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            
            # Obtener ventas del cliente
            cursor.execute("""
                SELECT v.id_venta, v.fecha, v.total, v.metodo_pago,
                       COUNT(dv.id_detalle) as items
                FROM ventas v
                LEFT JOIN detalle_ventas dv ON v.id_venta = dv.venta_id
                WHERE v.cliente_id = %s
                GROUP BY v.id_venta
                ORDER BY v.fecha DESC
                LIMIT 50
            """, (cliente['id_cliente'],))
            
            ventas = cursor.fetchall()
            conn.close()
            
            if ventas:
                # Mostrar estadísticas
                stats_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                stats_frame.pack(fill="x", padx=25, pady=20)
                
                total_compras = len(ventas)
                total_gastado = sum(float(v['total']) for v in ventas)
                
                ctk.CTkLabel(
                    stats_frame,
                    text=f"💰 Total gastado: ${total_gastado:.2f} • 🛒 {total_compras} compras",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#4CAF50"
                ).pack(anchor="w")
                
                # Lista de ventas
                scroll_ventas = ctk.CTkScrollableFrame(content_frame, fg_color="transparent")
                scroll_ventas.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                
                for venta in ventas:
                    self.crear_item_historial(scroll_ventas, venta)
            else:
                # Sin historial
                ctk.CTkLabel(
                    content_frame,
                    text="📋 Este cliente aún no tiene compras registradas",
                    font=("Segoe UI", 16),
                    text_color="#666666"
                ).pack(expand=True)
                
        except Exception as e:
            ctk.CTkLabel(
                content_frame,
                text=f"❌ Error al cargar historial: {str(e)}",
                font=("Segoe UI", 14),
                text_color="#F44336"
            ).pack(expand=True)
    
    def crear_item_historial(self, parent, venta):
        """Crear item de historial de venta"""
        item = ctk.CTkFrame(parent, fg_color="white", corner_radius=8)
        item.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(item, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Información de la venta
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Primera línea
        ctk.CTkLabel(
            info_frame,
            text=f"Venta #{venta['id_venta']} • {venta['items']} productos",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        # Segunda línea
        fecha_str = venta['fecha'].strftime("%d/%m/%Y %H:%M") if venta['fecha'] else "Sin fecha"
        ctk.CTkLabel(
            info_frame,
            text=f"📅 {fecha_str} • 💳 {venta['metodo_pago'] or 'Efectivo'}",
            font=("Segoe UI", 11),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(3, 0))
        
        # Total
        total_frame = ctk.CTkFrame(content, fg_color="#E8F5E9", corner_radius=8)
        total_frame.pack(side="right")
        
        ctk.CTkLabel(
            total_frame,
            text=f"${float(venta['total']):.2f}",
            font=("Segoe UI", 14, "bold"),
            text_color="#2E7D32"
        ).pack(padx=15, pady=8)
    
    def buscar_clientes(self):
        """Buscar clientes por texto"""
        texto = self.search_entry.get().lower().strip()
        
        if not texto:
            self.mostrar_clientes()
            return
        
        clientes_filtrados = [
            c for c in self.clientes
            if texto in (c['nombre'] or "").lower()
            or texto in (c['telefono'] or "").lower()
            or texto in (c.get('email', "") or "").lower()
        ]
        
        self.mostrar_clientes(clientes_filtrados)
    
    def nuevo_cliente(self):
        """Abrir formulario para nuevo cliente"""
        self.abrir_formulario_cliente()
    
    def editar_cliente(self, cliente):
        """Editar un cliente existente"""
        self.abrir_formulario_cliente(cliente)
    
    def abrir_formulario_cliente(self, cliente=None):
        """Abrir formulario de cliente (nuevo o editar)"""
        # Crear ventana
        form_window = ctk.CTkToplevel(self)
        form_window.title("Editar Cliente" if cliente else "Nuevo Cliente")
        form_window.geometry("500x600")
        form_window.transient(self)
        form_window.grab_set()
        
        # Centrar ventana
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (form_window.winfo_screenheight() // 2) - (600 // 2)
        form_window.geometry(f"500x600+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(form_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Título
        titulo = "✏️ Editar Cliente" if cliente else "➕ Nuevo Cliente"
        ctk.CTkLabel(
            main_frame,
            text=titulo,
            font=("Segoe UI", 22, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 15))
        
        # Qué poner en cada campo (solo para nuevo cliente)
        if not cliente:
            campos_frame = ctk.CTkFrame(main_frame, fg_color="#E8F5E9", corner_radius=8)
            campos_frame.pack(fill="x", pady=(0, 20))
            
            ctk.CTkLabel(
                campos_frame,
                text="📝 Qué poner en cada campo:",
                font=("Segoe UI", 11, "bold"),
                text_color="#2E7D32"
            ).pack(anchor="w", padx=15, pady=(8, 2))
            
            campos_text = [
                "• Nombre: María García López",
                "• Teléfono: 6181234567 (10 dígitos)",
                "• Email: maria@gmail.com (opcional)"
            ]
            
            for campo in campos_text:
                ctk.CTkLabel(
                    campos_frame,
                    text=campo,
                    font=("Segoe UI", 9),
                    text_color="#388E3C",
                    anchor="w"
                ).pack(anchor="w", padx=25, pady=1)
            
            ctk.CTkFrame(campos_frame, height=5, fg_color="transparent").pack()
        
        # Formulario
        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Nombre Completo
        ctk.CTkLabel(form_frame, text="Nombre Completo: *", font=("Segoe UI", 13, "bold"), 
                    text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre completo del cliente", 
                                    height=45, font=("Segoe UI", 13))
        nombre_entry.pack(fill="x", pady=(0, 15))
        if cliente:
            nombre_entry.insert(0, cliente['nombre'] or "")
        
        # Teléfono con validación
        ctk.CTkLabel(form_frame, text="Teléfono: * (10 dígitos)", font=("Segoe UI", 13, "bold"), 
                    text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        telefono_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 6181234567", 
                                     height=45, font=("Segoe UI", 13))
        telefono_entry.pack(fill="x", pady=(0, 15))
        
        # Validación: solo números y máximo 10 dígitos
        def validar_telefono(event):
            texto = telefono_entry.get()
            # Eliminar cualquier caracter que no sea número
            texto_limpio = ''.join(filter(str.isdigit, texto))
            # Limitar a 10 dígitos
            if len(texto_limpio) > 10:
                texto_limpio = texto_limpio[:10]
            # Actualizar el campo si cambió
            if texto != texto_limpio:
                telefono_entry.delete(0, 'end')
                telefono_entry.insert(0, texto_limpio)
        
        telefono_entry.bind('<KeyRelease>', validar_telefono)
        
        if cliente:
            telefono_entry.insert(0, cliente['telefono'] or "")
        
        # Email (correo)
        ctk.CTkLabel(form_frame, text="Email:", font=("Segoe UI", 13, "bold"), 
                    text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="correo@ejemplo.com", 
                                  height=45, font=("Segoe UI", 13))
        email_entry.pack(fill="x", pady=(0, 15))
        if cliente:
            email_entry.insert(0, cliente.get('email', "") or "")
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def guardar():
            nombre = nombre_entry.get().strip()
            telefono = telefono_entry.get().strip()
            email = email_entry.get().strip()
            
            if not nombre or not telefono:
                messagebox.showwarning("Datos incompletos", 
                                     "Nombre y teléfono son obligatorios")
                return
            
            # Validar que el teléfono tenga exactamente 10 dígitos
            if len(telefono) != 10 or not telefono.isdigit():
                messagebox.showwarning("Teléfono inválido", 
                                     "El teléfono debe tener exactamente 10 dígitos numéricos")
                return
            
            try:
                conn = crear_conexion()
                cursor = conn.cursor()
                
                if cliente:
                    # Actualizar (sin dirección)
                    cursor.execute("""
                        UPDATE clientes 
                        SET nombre = %s, telefono = %s, correo = %s
                        WHERE id_cliente = %s
                    """, (nombre, telefono, email, cliente['id_cliente']))
                    mensaje = "Cliente actualizado correctamente"
                else:
                    # Insertar (sin dirección)
                    cursor.execute("""
                        INSERT INTO clientes (nombre, telefono, correo)
                        VALUES (%s, %s, %s)
                    """, (nombre, telefono, email))
                    mensaje = "Cliente registrado correctamente"
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", f"✅ {mensaje}")
                form_window.destroy()
                self.cargar_clientes()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el cliente:\n{str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Guardar",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=50,
            font=("Segoe UI", 14, "bold"),
            command=guardar
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=50,
            font=("Segoe UI", 14),
            command=form_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))
    
    def eliminar_cliente(self, cliente):
        """Eliminar un cliente"""
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar al cliente?\n\n"
            f"{cliente['nombre']}\n"
            f"Teléfono: {cliente['telefono']}\n\n"
            f"Esta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                conn = crear_conexion()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (cliente['id_cliente'],))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "✅ Cliente eliminado correctamente")
                self.cargar_clientes()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente:\n{str(e)}")
    def buscar_clientes(self):
        """Buscar clientes por texto"""
        texto = self.search_entry.get().lower().strip()
        
        if not texto:
            self.mostrar_clientes()
            return
        
        clientes_filtrados = [
            c for c in self.clientes
            if texto in (c['nombre'] or "").lower()
            or texto in (c['telefono'] or "").lower()
            or texto in (c.get('email', "") or "").lower()
        ]
        
        self.mostrar_clientes(clientes_filtrados)
    
    def nuevo_cliente(self):
        """Abrir formulario para nuevo cliente"""
        self.abrir_formulario_cliente()
    
    def editar_cliente(self, cliente):
        """Editar un cliente existente"""
        self.abrir_formulario_cliente(cliente)
    
    def abrir_formulario_cliente(self, cliente=None):
        """Abrir formulario moderno de cliente"""
        # Crear ventana
        form_window = ctk.CTkToplevel(self)
        form_window.title("Editar Cliente" if cliente else "Nuevo Cliente")
        form_window.geometry("550x650")
        form_window.transient(self)
        form_window.grab_set()
        
        # Centrar ventana
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (550 // 2)
        y = (form_window.winfo_screenheight() // 2) - (650 // 2)
        form_window.geometry(f"550x650+{x}+{y}")
        
        # Contenido principal
        main_frame = ctk.CTkFrame(form_window, fg_color="#F5F5F5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header del formulario
        header = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=12)
        header.pack(fill="x", pady=(0, 20))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=25, pady=20)
        
        # Título con icono
        titulo = "✏️ Editar Cliente" if cliente else "➕ Nuevo Cliente"
        ctk.CTkLabel(
            header_content,
            text=titulo,
            font=("Segoe UI", 24, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        subtitulo = "Modifica la información del cliente" if cliente else "Completa los datos del nuevo cliente"
        ctk.CTkLabel(
            header_content,
            text=subtitulo,
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(anchor="w", pady=(5, 0))
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=12)
        form_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        form_content = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Campos del formulario
        
        # Nombre Completo
        ctk.CTkLabel(
            form_content,
            text="Nombre Completo *",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        nombre_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Ej: María García López",
            height=50,
            font=("Segoe UI", 14),
            corner_radius=10
        )
        nombre_entry.pack(fill="x", pady=(0, 20))
        if cliente:
            nombre_entry.insert(0, cliente['nombre'] or "")
        
        # Teléfono
        ctk.CTkLabel(
            form_content,
            text="Teléfono * (10 dígitos)",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        telefono_frame = ctk.CTkFrame(form_content, fg_color="#F8F9FA", corner_radius=10)
        telefono_frame.pack(fill="x", pady=(0, 20))
        
        telefono_content = ctk.CTkFrame(telefono_frame, fg_color="transparent")
        telefono_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(telefono_content, text="📞", font=("Segoe UI", 16)).pack(side="left", padx=(0, 10))
        
        telefono_entry = ctk.CTkEntry(
            telefono_content,
            placeholder_text="6181234567",
            border_width=0,
            fg_color="transparent",
            font=("Segoe UI", 14)
        )
        telefono_entry.pack(side="left", fill="x", expand=True)
        
        # Validación de teléfono
        def validar_telefono(event):
            texto = telefono_entry.get()
            texto_limpio = ''.join(filter(str.isdigit, texto))
            if len(texto_limpio) > 10:
                texto_limpio = texto_limpio[:10]
            if texto != texto_limpio:
                telefono_entry.delete(0, 'end')
                telefono_entry.insert(0, texto_limpio)
        
        telefono_entry.bind('<KeyRelease>', validar_telefono)
        
        if cliente:
            telefono_entry.insert(0, cliente['telefono'] or "")
        
        # Email
        ctk.CTkLabel(
            form_content,
            text="Email (opcional)",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        email_frame = ctk.CTkFrame(form_content, fg_color="#F8F9FA", corner_radius=10)
        email_frame.pack(fill="x", pady=(0, 20))
        
        email_content = ctk.CTkFrame(email_frame, fg_color="transparent")
        email_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(email_content, text="📧", font=("Segoe UI", 16)).pack(side="left", padx=(0, 10))
        
        email_entry = ctk.CTkEntry(
            email_content,
            placeholder_text="correo@ejemplo.com",
            border_width=0,
            fg_color="transparent",
            font=("Segoe UI", 14)
        )
        email_entry.pack(side="left", fill="x", expand=True)
        
        if cliente:
            email_entry.insert(0, cliente.get('email', "") or "")
        
        # Información de ayuda
        if not cliente:
            help_frame = ctk.CTkFrame(form_content, fg_color="#E3F2FD", corner_radius=10)
            help_frame.pack(fill="x", pady=(0, 20))
            
            help_content = ctk.CTkFrame(help_frame, fg_color="transparent")
            help_content.pack(fill="x", padx=15, pady=12)
            
            ctk.CTkLabel(
                help_content,
                text="💡 Consejos:",
                font=("Segoe UI", 12, "bold"),
                text_color="#1976D2"
            ).pack(anchor="w")
            
            consejos = [
                "• El nombre y teléfono son obligatorios",
                "• El teléfono debe tener exactamente 10 dígitos",
                "• El email es opcional pero recomendado"
            ]
            
            for consejo in consejos:
                ctk.CTkLabel(
                    help_content,
                    text=consejo,
                    font=("Segoe UI", 10),
                    text_color="#1976D2",
                    anchor="w"
                ).pack(anchor="w", pady=1)
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        def guardar():
            nombre = nombre_entry.get().strip()
            telefono = telefono_entry.get().strip()
            email = email_entry.get().strip()
            
            # Validaciones
            if not nombre:
                messagebox.showwarning("Campo requerido", "El nombre es obligatorio")
                nombre_entry.focus()
                return
            
            if not telefono:
                messagebox.showwarning("Campo requerido", "El teléfono es obligatorio")
                telefono_entry.focus()
                return
            
            if len(telefono) != 10 or not telefono.isdigit():
                messagebox.showwarning("Teléfono inválido", 
                                     "El teléfono debe tener exactamente 10 dígitos numéricos")
                telefono_entry.focus()
                return
            
            # Validar email si se proporcionó
            if email and '@' not in email:
                messagebox.showwarning("Email inválido", "El formato del email no es válido")
                email_entry.focus()
                return
            
            try:
                conn = crear_conexion()
                cursor = conn.cursor()
                
                if cliente:
                    # Actualizar
                    cursor.execute("""
                        UPDATE clientes 
                        SET nombre = %s, telefono = %s, correo = %s
                        WHERE id_cliente = %s
                    """, (nombre, telefono, email if email else None, cliente['id_cliente']))
                    mensaje = "Cliente actualizado correctamente"
                else:
                    # Insertar
                    cursor.execute("""
                        INSERT INTO clientes (nombre, telefono, correo, fecha_registro)
                        VALUES (%s, %s, %s, NOW())
                    """, (nombre, telefono, email if email else None))
                    mensaje = "Cliente registrado correctamente"
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", f"✅ {mensaje}")
                form_window.destroy()
                self.cargar_clientes()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el cliente:\n{str(e)}")
        
        # Botón guardar
        ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar Cliente",
            height=50,
            corner_radius=12,
            fg_color="#4CAF50",
            hover_color="#45A049",
            font=("Segoe UI", 14, "bold"),
            command=guardar
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botón cancelar
        ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            height=50,
            corner_radius=12,
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            font=("Segoe UI", 14),
            command=form_window.destroy
        ).pack(side="left", fill="x", expand=True, padx=(10, 0))
    
    def eliminar_cliente(self, cliente):
        """Eliminar un cliente con confirmación mejorada"""
        # Crear ventana de confirmación personalizada
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirmar eliminación")
        confirm_window.geometry("450x300")
        confirm_window.transient(self)
        confirm_window.grab_set()
        
        # Centrar ventana
        confirm_window.update_idletasks()
        x = (confirm_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (confirm_window.winfo_screenheight() // 2) - (300 // 2)
        confirm_window.geometry(f"450x300+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(confirm_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono de advertencia
        ctk.CTkLabel(
            main_frame,
            text="⚠️",
            font=("Segoe UI", 48),
            text_color="#FF9800"
        ).pack(pady=(20, 10))
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="¿Eliminar cliente?",
            font=("Segoe UI", 20, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 10))
        
        # Información del cliente
        info_frame = ctk.CTkFrame(main_frame, fg_color="#F8F9FA", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            info_content,
            text=f"Cliente: {cliente['nombre']}",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_content,
            text=f"Teléfono: {cliente['telefono']}",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))
        
        if cliente.get('email'):
            ctk.CTkLabel(
                info_content,
                text=f"Email: {cliente['email']}",
                font=("Segoe UI", 12),
                text_color="#666666",
                anchor="w"
            ).pack(anchor="w", pady=(2, 0))
        
        # Advertencia
        ctk.CTkLabel(
            main_frame,
            text="Esta acción no se puede deshacer",
            font=("Segoe UI", 12),
            text_color="#F44336"
        ).pack(pady=(0, 20))
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20)
        
        def confirmar_eliminacion():
            try:
                conn = crear_conexion()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (cliente['id_cliente'],))
                conn.commit()
                conn.close()
                
                confirm_window.destroy()
                messagebox.showinfo("Éxito", "✅ Cliente eliminado correctamente")
                self.cargar_clientes()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente:\n{str(e)}")
        
        # Botón eliminar
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Sí, eliminar",
            height=45,
            corner_radius=10,
            fg_color="#F44336",
            hover_color="#D32F2F",
            font=("Segoe UI", 12, "bold"),
            command=confirmar_eliminacion
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botón cancelar
        ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            height=45,
            corner_radius=10,
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            font=("Segoe UI", 12),
            command=confirm_window.destroy
        ).pack(side="left", fill="x", expand=True, padx=(10, 0))