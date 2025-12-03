import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.users import listar_usuarios, crear_usuario

from views.nuevo_usuario_form import NuevoUsuarioForm

class UsersView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.user = user
        self.pack(fill="both", expand=True)
        
        # Verificar si es administrador para habilitar funciones de edición
        rol = self.user.get("rol", "") if self.user else ""
        self.es_admin = (rol == "Administrador" or rol == "Admin")
        
        self.usuarios_originales = []
        self.crear_interfaz()
        self.cargar_usuarios()

    def crear_interfaz(self):
        # Panel principal
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = ctk.CTkFrame(main, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        # Título y descripción
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Gestión de Usuario",
            font=("Segoe UI", 24, "bold"),
            text_color="#2C2C2C"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Administra los usuarios del sistema",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(anchor="w")
        
        # Botón nuevo usuario (solo para administradores)
        if self.es_admin:
            ctk.CTkButton(
                header,
                text="+ Nuevo Usuario",
                fg_color="#E91E63",
                hover_color="#C2185B",
                height=40,
                font=("Segoe UI", 12, "bold"),
                corner_radius=8,
                command=self.nuevo
            ).pack(side="right")
        else:
            ctk.CTkLabel(
                header,
                text="👁️ Modo Solo Lectura",
                font=("Segoe UI", 12, "bold"),
                text_color="#666666"
            ).pack(side="right", padx=10)
        
        # Mensaje de recuperación
        info_frame = ctk.CTkFrame(main, fg_color="#E3F2FD", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 15))
        
        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            info_content,
            text="🔑",
            font=("Segoe UI", 20)
        ).pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(info_content, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            text_frame,
            text="Recuperación de Contraseñas",
            font=("Segoe UI", 12, "bold"),
            text_color="#1976D2",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame,
            text='¿Olvidaste la contraseña? Tú al ser administrador puedes restaurar las contraseñas utilizando el botón "olvide mi contraseña" en el inicio de sesión',
            font=("Segoe UI", 12),
            text_color="#1976D2",
            anchor="w",
            wraplength=700
        ).pack(anchor="w")
        
        # Tarjetas de estadísticas
        self.crear_tarjetas_estadisticas(main)
        
        # Filtros
        self.crear_filtros(main)
        
        # Tabla de usuarios
        self.crear_tabla_usuarios(main)
    
    def crear_tarjetas_estadisticas(self, parent):
        """Crear tarjetas de estadísticas"""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 15))
        
        self.stats_cards = {}
        
        stats = [
            ("Total", "👥", "#E91E63", "total"),
            ("Activos", "✓", "#4CAF50", "activos"),
            ("Admins", "🛡️", "#FF5252", "admins"),
            ("Vendedores", "👤", "#2196F3", "vendedores")
        ]
        
        for titulo, icono, color, key in stats:
            card = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
            card.pack(side="left", expand=True, fill="x", padx=5)
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(padx=20, pady=15)
            
            # Icono
            ctk.CTkLabel(
                content,
                text=icono,
                font=("Segoe UI", 24),
                text_color=color
            ).pack(side="left", padx=(0, 15))
            
            # Texto
            text_frame = ctk.CTkFrame(content, fg_color="transparent")
            text_frame.pack(side="left")
            
            ctk.CTkLabel(
                text_frame,
                text=titulo,
                font=("Segoe UI", 13),
                text_color="#666666"
            ).pack(anchor="w")
            
            label = ctk.CTkLabel(
                text_frame,
                text="0",
                font=("Segoe UI", 20, "bold"),
                text_color="#2C2C2C"
            )
            label.pack(anchor="w")
            
            self.stats_cards[key] = label
    
    def crear_filtros(self, parent):
        """Crear barra de filtros"""
        filtros_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(0, 15))
        
        # Búsqueda
        search_frame = ctk.CTkFrame(filtros_frame, fg_color="white", corner_radius=8, height=45)
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Segoe UI", 16)
        ).pack(side="left", padx=12)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por nombre o email...",
            border_width=0,
            fg_color="white",
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filtrar_usuarios())
        
        # Filtro de rol
        self.rol_var = ctk.StringVar(value="Todos los roles")
        rol_menu = ctk.CTkOptionMenu(
            filtros_frame,
            variable=self.rol_var,
            values=["Todos los roles", "Administrador", "Cajero", "Empleado", "Vendedor"],
            fg_color="white",
            button_color="#E91E63",
            button_hover_color="#C2185B",
            dropdown_fg_color="white",
            width=180,
            height=45,
            corner_radius=8,
            font=("Segoe UI", 13),
            command=lambda x: self.filtrar_usuarios()
        )
        rol_menu.pack(side="left", padx=(0, 10))
        
        # Filtro de estado
        self.estado_var = ctk.StringVar(value="Todos los Estados")
        estado_menu = ctk.CTkOptionMenu(
            filtros_frame,
            variable=self.estado_var,
            values=["Todos los Estados", "Activo", "Inactivo"],
            fg_color="white",
            button_color="#E91E63",
            button_hover_color="#C2185B",
            dropdown_fg_color="white",
            width=180,
            height=45,
            corner_radius=8,
            font=("Segoe UI", 13),
            command=lambda x: self.filtrar_usuarios()
        )
        estado_menu.pack(side="left")
    
    def crear_tabla_usuarios(self, parent):
        """Crear tabla de usuarios"""
        # Contenedor de la tabla
        tabla_container = ctk.CTkFrame(parent, fg_color="transparent")
        tabla_container.pack(fill="both", expand=True)
        
        # Headers
        headers_frame = ctk.CTkFrame(tabla_container, fg_color="white", corner_radius=10)
        headers_frame.pack(fill="x", pady=(0, 5))
        
        headers = [
            ("Usuario", 0.15),
            ("Email", 0.2),
            ("Contraseña", 0.15),
            ("Rol", 0.12),
            ("Estado", 0.12),
            ("Fecha Creación", 0.18),
            ("Acciones", 0.08)
        ]
        
        for header, weight in headers:
            ctk.CTkLabel(
                headers_frame,
                text=header,
                font=("Segoe UI", 11, "bold"),
                text_color="#666666",
                anchor="w"
            ).pack(side="left", expand=True, fill="x", padx=15, pady=12)
        
        # Scroll frame para usuarios
        self.usuarios_scroll = ctk.CTkScrollableFrame(
            tabla_container,
            fg_color="transparent"
        )
        self.usuarios_scroll.pack(fill="both", expand=True)

    def cargar_usuarios(self):
        """Cargar usuarios desde la base de datos"""
        try:
            self.usuarios_originales = listar_usuarios()
            self.actualizar_estadisticas()
            self.mostrar_usuarios(self.usuarios_originales)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los usuarios: {str(e)}")
            self.usuarios_originales = []
    
    def actualizar_estadisticas(self):
        """Actualizar las tarjetas de estadísticas"""
        total = len(self.usuarios_originales)
        activos = sum(1 for u in self.usuarios_originales if u.get('activo', True))
        admins = sum(1 for u in self.usuarios_originales if u.get('rol') == 'Administrador')
        vendedores = sum(1 for u in self.usuarios_originales if u.get('rol') == 'Vendedor')
        
        self.stats_cards['total'].configure(text=str(total))
        self.stats_cards['activos'].configure(text=str(activos))
        self.stats_cards['admins'].configure(text=str(admins))
        self.stats_cards['vendedores'].configure(text=str(vendedores))
    
    def mostrar_usuarios(self, usuarios):
        """Mostrar usuarios en la tabla"""
        # Limpiar tabla
        for widget in self.usuarios_scroll.winfo_children():
            widget.destroy()
        
        # Mostrar cada usuario
        for usuario in usuarios:
            self.crear_fila_usuario(self.usuarios_scroll, usuario)
    
    def crear_fila_usuario(self, parent, usuario):
        """Crear fila de usuario"""
        fila = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, height=70)
        fila.pack(fill="x", pady=3)
        fila.pack_propagate(False)
        
        container = ctk.CTkFrame(fila, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Usuario
        user_frame = ctk.CTkFrame(container, fg_color="transparent")
        user_frame.pack(side="left", expand=True, fill="x")
        
        ctk.CTkLabel(
            user_frame,
            text=usuario.get('usuario', 'N/A'),
            font=("Segoe UI", 13),
            text_color="#2C2C2C",
            anchor="w"
        ).pack(anchor="w")
        
        # Email
        email_frame = ctk.CTkFrame(container, fg_color="transparent")
        email_frame.pack(side="left", expand=True, fill="x")
        
        email = usuario.get('email', 'N/A')
        if len(email) > 25:
            email = email[:22] + "..."
        
        ctk.CTkLabel(
            email_frame,
            text=email,
            font=("Segoe UI", 12),
            text_color="#2C2C2C",
            anchor="w"
        ).pack(anchor="w")
        
        # Contraseña con botón mostrar/ocultar
        password_frame = ctk.CTkFrame(container, fg_color="transparent")
        password_frame.pack(side="left", expand=True, fill="x")
        
        # Obtener contraseña
        password = usuario.get('contraseña', usuario.get('password', '****'))
        
        # Label para mostrar contraseña (oculta por defecto)
        password_label = ctk.CTkLabel(
            password_frame,
            text="••••••••",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        )
        password_label.pack(side="left", padx=(0, 5))
        
        # Botón para mostrar/ocultar (solo para administradores)
        def toggle_password():
            # Verificar que el usuario actual sea administrador
            rol_actual = self.user.get('rol', '') if self.user else ''
            if rol_actual not in ['Administrador', 'Admin']:
                messagebox.showwarning(
                    "Acceso Denegado",
                    "Solo los administradores pueden ver las contraseñas de otros usuarios."
                )
                return
            
            if password_label.cget("text") == "••••••••":
                password_label.configure(text=str(password))
                toggle_btn.configure(text="🙈")
            else:
                password_label.configure(text="••••••••")
                toggle_btn.configure(text="👁️")
        
        # Verificar si el usuario actual es administrador para mostrar el botón
        rol_actual = self.user.get('rol', '') if self.user else ''
        es_admin = rol_actual in ['Administrador', 'Admin']
        
        toggle_btn = ctk.CTkButton(
            password_frame,
            text="👁️" if es_admin else "🔒",
            width=30,
            height=24,
            fg_color="transparent",
            text_color="#E91E63" if es_admin else "#999999",
            hover_color="#FFE4E1" if es_admin else "#F5F5F5",
            font=("Segoe UI", 12),
            command=toggle_password
        )
        toggle_btn.pack(side="left")
        
        # Tooltip visual para no administradores
        if not es_admin:
            toggle_btn.configure(cursor="not-allowed")
        
        # Rol (badge)
        rol_frame = ctk.CTkFrame(container, fg_color="transparent")
        rol_frame.pack(side="left", expand=True, padx=5)
        
        rol = usuario.get('rol', 'N/A')
        rol_color = {
            'Administrador': '#FF5252',
            'Cajero': '#2196F3',
            'Empleado': '#FF9800',
            'Vendedor': '#9C27B0'
        }.get(rol, '#666666')
        
        rol_badge = ctk.CTkLabel(
            rol_frame,
            text=rol,
            font=("Segoe UI", 9, "bold"),
            text_color="white",
            fg_color=rol_color,
            corner_radius=12,
            width=90,
            height=24
        )
        rol_badge.pack()
        
        # Estado (badge)
        estado_frame = ctk.CTkFrame(container, fg_color="transparent")
        estado_frame.pack(side="left", expand=True, padx=5)
        
        activo = usuario.get('activo', True)
        estado_text = "Activo" if activo else "Inactivo"
        estado_color = "#4CAF50" if activo else "#F44336"
        
        estado_badge = ctk.CTkLabel(
            estado_frame,
            text=estado_text,
            font=("Segoe UI", 9, "bold"),
            text_color="white",
            fg_color=estado_color,
            corner_radius=12,
            width=70,
            height=24
        )
        estado_badge.pack()
        
        # Fecha de creación
        fecha_frame = ctk.CTkFrame(container, fg_color="transparent")
        fecha_frame.pack(side="left", expand=True, fill="x")
        
        fecha = datetime.now().strftime("%d/%m/%Y")
        ctk.CTkLabel(
            fecha_frame,
            text=fecha,
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w")
        
        # Botones de acción
        acciones_frame = ctk.CTkFrame(container, fg_color="transparent")
        acciones_frame.pack(side="left")
        
        # Botón ver ingresos (solo para vendedores)
        if usuario.get('rol') in ['Vendedor', 'Cajero', 'Empleado']:
            ctk.CTkButton(
                acciones_frame,
                text="💰",
                width=35,
                height=28,
                fg_color="transparent",
                text_color="#4CAF50",
                hover_color="#E8F5E9",
                font=("Segoe UI", 14),
                command=lambda u=usuario: self.ver_ingresos_vendedor(u)
            ).pack(side="left", padx=2)
        
        # Botón editar
        ctk.CTkButton(
            acciones_frame,
            text="✏️",
            width=35,
            height=28,
            fg_color="transparent",
            text_color="#2196F3",
            hover_color="#E3F2FD",
            font=("Segoe UI", 14),
            command=lambda u=usuario: self.editar_usuario(u)
        ).pack(side="left", padx=2)
    
    def filtrar_usuarios(self):
        """Filtrar usuarios según búsqueda, rol y estado"""
        termino = self.search_entry.get().lower()
        rol_filtro = self.rol_var.get()
        estado_filtro = self.estado_var.get()
        
        usuarios_filtrados = self.usuarios_originales.copy()
        
        # Filtro de búsqueda
        if termino:
            usuarios_filtrados = [
                u for u in usuarios_filtrados
                if termino in u.get('usuario', '').lower() or
                   termino in u.get('email', '').lower() or
                   termino in u.get('nombre_completo', '').lower()
            ]
        
        # Filtro de rol
        if rol_filtro != "Todos los roles":
            usuarios_filtrados = [
                u for u in usuarios_filtrados
                if u.get('rol') == rol_filtro
            ]
        
        # Filtro de estado
        if estado_filtro != "Todos los Estados":
            activo = estado_filtro == "Activo"
            usuarios_filtrados = [
                u for u in usuarios_filtrados
                if u.get('activo', True) == activo
            ]
        
        self.mostrar_usuarios(usuarios_filtrados)
    
    def nuevo(self):
        """Abrir formulario para crear nuevo usuario"""
        def handle_creacion(datos):
            nombre = datos.get("nombre_completo", "").strip()
            email = datos.get("email", "").strip()
            password = datos.get("password", "").strip()
            rol = datos.get("rol", "Vendedor")
            
            if not nombre or not email or not password:
                messagebox.showwarning("Datos incompletos", "Nombre, email y contraseña son obligatorios.")
                return
            
            try:
                crear_usuario(
                    nombre_completo=nombre,
                    email=email,
                    contraseña=password,
                    rol=rol,
                    activo=True,
                    pregunta=datos.get("pregunta", "").strip(),
                    respuesta=datos.get("respuesta", "").strip()
                )
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                self.cargar_usuarios()  # Recargar lista
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el usuario: {str(e)}")
        
        form = NuevoUsuarioForm(self, on_create=handle_creacion)
    
    def editar_usuario(self, usuario):
        """Editar información de un usuario"""
        # Verificar permisos
        if not self.es_admin:
            messagebox.showwarning(
                "Acceso Denegado",
                "Solo los administradores pueden editar usuarios"
            )
            return
        
        # Crear ventana de edición
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Editar Usuario")
        edit_window.geometry("400x300")
        edit_window.transient(self)
        edit_window.grab_set()
        
        # Centrar ventana
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (300 // 2)
        edit_window.geometry(f"400x300+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(edit_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text=f"Editar Usuario: {usuario.get('usuario', 'N/A')}",
            font=("Segoe UI", 16, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 20))
        
        # Campo de contraseña
        ctk.CTkLabel(
            main_frame,
            text="Nueva Contraseña:",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Dejar vacío para no cambiar",
            height=40,
            font=("Segoe UI", 12)
        )
        password_entry.pack(fill="x", pady=(0, 15))
        
        # Campo de rol
        ctk.CTkLabel(
            main_frame,
            text="Rol:",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        rol_var = ctk.StringVar(value=usuario.get('rol', 'Vendedor'))
        rol_menu = ctk.CTkOptionMenu(
            main_frame,
            variable=rol_var,
            values=["Administrador", "Cajero", "Empleado", "Vendedor"],
            height=40,
            font=("Segoe UI", 12)
        )
        rol_menu.pack(fill="x", pady=(0, 20))
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def guardar_cambios():
            try:
                from database.db import crear_conexion
                
                conn = crear_conexion()
                if not conn:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                    return
                
                cursor = conn.cursor()
                
                # Actualizar rol
                cursor.execute(
                    "UPDATE usuarios SET rol = %s WHERE id_usuario = %s",
                    (rol_var.get(), usuario.get('id_usuario'))
                )
                
                # Actualizar contraseña si se proporcionó
                nueva_password = password_entry.get().strip()
                if nueva_password:
                    cursor.execute(
                        "UPDATE usuarios SET contraseña = %s WHERE id_usuario = %s",
                        (nueva_password, usuario.get('id_usuario'))
                    )
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                edit_window.destroy()
                self.cargar_usuarios()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el usuario:\n{str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="Guardar",
            fg_color="#E91E63",
            hover_color="#C2185B",
            height=40,
            font=("Segoe UI", 12, "bold"),
            command=guardar_cambios
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=40,
            font=("Segoe UI", 12),
            command=edit_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))
        

    def ver_ingresos_vendedor(self, usuario):
        """Ver ingresos y estadísticas de un vendedor"""
        # Crear ventana de ingresos
        ingresos_window = ctk.CTkToplevel(self)
        ingresos_window.title(f"Ingresos - {usuario.get('nombre_completo', usuario.get('usuario', 'N/A'))}")
        ingresos_window.geometry("900x700")
        ingresos_window.transient(self)
        ingresos_window.grab_set()
        
        # Centrar ventana
        ingresos_window.update_idletasks()
        x = (ingresos_window.winfo_screenwidth() // 2) - (900 // 2)
        y = (ingresos_window.winfo_screenheight() // 2) - (700 // 2)
        ingresos_window.geometry(f"900x700+{x}+{y}")
        
        # Contenido principal
        main_frame = ctk.CTkFrame(ingresos_window, fg_color="#F5F5F5")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=30, pady=20)
        
        # Avatar y nombre
        avatar_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        avatar_frame.pack(side="left")
        
        # Avatar circular
        rol = usuario.get('rol', 'Vendedor')
        avatar_color = {
            'Vendedor': '#9C27B0',
            'Cajero': '#2196F3',
            'Empleado': '#FF9800'
        }.get(rol, '#9C27B0')
        
        avatar = ctk.CTkFrame(avatar_frame, fg_color=avatar_color, corner_radius=40, width=80, height=80)
        avatar.pack()
        avatar.pack_propagate(False)
        
        inicial = usuario.get('nombre_completo', usuario.get('usuario', 'V'))[0].upper()
        ctk.CTkLabel(
            avatar,
            text=inicial,
            font=("Segoe UI", 32, "bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Info del vendedor
        info_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        info_frame.pack(side="left", padx=20)
        
        ctk.CTkLabel(
            info_frame,
            text=usuario.get('nombre_completo', usuario.get('usuario', 'N/A')),
            font=("Segoe UI", 20, "bold"),
            text_color="#2C2C2C",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=f"👤 {rol}",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=f"📧 {usuario.get('email', 'N/A')}",
            font=("Segoe UI", 13),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        # Contenido scrollable
        scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Obtener estadísticas del vendedor
        try:
            from database.db import crear_conexion
            
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            
            id_usuario = usuario.get('id_usuario')
            
            # Estadísticas generales
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_ventas,
                    COALESCE(SUM(total), 0) as ingresos_totales,
                    COALESCE(AVG(total), 0) as promedio_venta,
                    COALESCE(MAX(total), 0) as venta_maxima
                FROM ventas
                WHERE id_usuario = %s
            """, (id_usuario,))
            stats = cursor.fetchone()
            
            # Ventas del mes actual
            cursor.execute("""
                SELECT COALESCE(SUM(total), 0) as ingresos_mes
                FROM ventas
                WHERE id_usuario = %s 
                AND YEAR(fecha) = YEAR(CURDATE())
                AND MONTH(fecha) = MONTH(CURDATE())
            """, (id_usuario,))
            mes_actual = cursor.fetchone()
            
            # Ventas de hoy
            cursor.execute("""
                SELECT COALESCE(SUM(total), 0) as ingresos_hoy
                FROM ventas
                WHERE id_usuario = %s 
                AND DATE(fecha) = CURDATE()
            """, (id_usuario,))
            hoy = cursor.fetchone()
            
            conn.close()
            
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            stats = {'total_ventas': 0, 'ingresos_totales': 0, 'promedio_venta': 0, 'venta_maxima': 0}
            mes_actual = {'ingresos_mes': 0}
            hoy = {'ingresos_hoy': 0}
        
        # Tarjetas de estadísticas
        stats_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        stats_container.pack(fill="x", pady=(0, 20))
        
        stats_container.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Tarjeta 1: Ingresos Totales
        card1 = ctk.CTkFrame(stats_container, fg_color="white", corner_radius=15)
        card1.grid(row=0, column=0, padx=5, sticky="ew")
        
        ctk.CTkLabel(
            card1,
            text="💰 Ingresos Totales",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card1,
            text=f"${float(stats['ingresos_totales']):,.2f}",
            font=("Segoe UI", 24, "bold"),
            text_color="#4CAF50"
        ).pack(pady=(0, 20))
        
        # Tarjeta 2: Ventas del Mes
        card2 = ctk.CTkFrame(stats_container, fg_color="white", corner_radius=15)
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        
        ctk.CTkLabel(
            card2,
            text="📅 Ingresos del Mes",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card2,
            text=f"${float(mes_actual['ingresos_mes']):,.2f}",
            font=("Segoe UI", 24, "bold"),
            text_color="#2196F3"
        ).pack(pady=(0, 20))
        
        # Tarjeta 3: Ventas de Hoy
        card3 = ctk.CTkFrame(stats_container, fg_color="white", corner_radius=15)
        card3.grid(row=0, column=2, padx=5, sticky="ew")
        
        ctk.CTkLabel(
            card3,
            text="🕐 Ingresos de Hoy",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card3,
            text=f"${float(hoy['ingresos_hoy']):,.2f}",
            font=("Segoe UI", 24, "bold"),
            text_color="#FF9800"
        ).pack(pady=(0, 20))
        
        # Segunda fila de estadísticas
        stats_container2 = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        stats_container2.pack(fill="x", pady=(0, 20))
        
        stats_container2.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total de ventas
        card4 = ctk.CTkFrame(stats_container2, fg_color="white", corner_radius=15)
        card4.grid(row=0, column=0, padx=5, sticky="ew")
        
        ctk.CTkLabel(
            card4,
            text="📊 Total de Ventas",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card4,
            text=str(stats['total_ventas']),
            font=("Segoe UI", 24, "bold"),
            text_color="#9C27B0"
        ).pack(pady=(0, 20))
        
        # Promedio por venta
        card5 = ctk.CTkFrame(stats_container2, fg_color="white", corner_radius=15)
        card5.grid(row=0, column=1, padx=5, sticky="ew")
        
        ctk.CTkLabel(
            card5,
            text="📈 Promedio por Venta",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card5,
            text=f"${float(stats['promedio_venta']):,.2f}",
            font=("Segoe UI", 24, "bold"),
            text_color="#00BCD4"
        ).pack(pady=(0, 20))
        
        # Venta máxima
        card6 = ctk.CTkFrame(stats_container2, fg_color="white", corner_radius=15)
        card6.grid(row=0, column=2, padx=5, sticky="ew")
        
        ctk.CTkLabel(
            card6,
            text="🏆 Venta Máxima",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card6,
            text=f"${float(stats['venta_maxima']):,.2f}",
            font=("Segoe UI", 24, "bold"),
            text_color="#FF5722"
        ).pack(pady=(0, 20))
        
        # Historial de ventas recientes
        historial_frame = ctk.CTkFrame(scroll_frame, fg_color="white", corner_radius=15)
        historial_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            historial_frame,
            text="📋 Últimas 10 Ventas",
            font=("Segoe UI", 16, "bold"),
            text_color="#2C2C2C"
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Obtener últimas ventas
        try:
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    id_venta,
                    fecha,
                    total,
                    metodo_pago
                FROM ventas
                WHERE id_usuario = %s
                ORDER BY fecha DESC
                LIMIT 10
            """, (id_usuario,))
            
            ventas = cursor.fetchall()
            conn.close()
            
            if ventas:
                # Header de tabla
                header_row = ctk.CTkFrame(historial_frame, fg_color="#F5F5F5")
                header_row.pack(fill="x", padx=20, pady=(0, 5))
                
                headers = [("Ticket", 0.15), ("Fecha", 0.35), ("Método", 0.25), ("Total", 0.25)]
                for header, weight in headers:
                    ctk.CTkLabel(
                        header_row,
                        text=header,
                        font=("Segoe UI", 11, "bold"),
                        text_color="#666666",
                        anchor="w"
                    ).pack(side="left", expand=True, fill="x", padx=10, pady=8)
                
                # Scroll para ventas
                ventas_scroll = ctk.CTkScrollableFrame(historial_frame, fg_color="transparent", height=200)
                ventas_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                
                for venta in ventas:
                    venta_row = ctk.CTkFrame(ventas_scroll, fg_color="white", height=40)
                    venta_row.pack(fill="x", pady=2)
                    venta_row.pack_propagate(False)
                    
                    # Ticket
                    ctk.CTkLabel(
                        venta_row,
                        text=f"#{venta['id_venta']}",
                        font=("Segoe UI", 10, "bold"),
                        text_color="#E91E63",
                        anchor="w"
                    ).pack(side="left", expand=True, fill="x", padx=10)
                    
                    # Fecha
                    fecha_str = venta['fecha'].strftime("%d/%m/%Y %H:%M") if venta['fecha'] else "N/A"
                    ctk.CTkLabel(
                        venta_row,
                        text=fecha_str,
                        font=("Segoe UI", 12),
                        text_color="#666666",
                        anchor="w"
                    ).pack(side="left", expand=True, fill="x", padx=10)
                    
                    # Método
                    ctk.CTkLabel(
                        venta_row,
                        text=venta.get('metodo_pago', 'N/A'),
                        font=("Segoe UI", 12),
                        text_color="#666666",
                        anchor="w"
                    ).pack(side="left", expand=True, fill="x", padx=10)
                    
                    # Total
                    ctk.CTkLabel(
                        venta_row,
                        text=f"${float(venta['total']):,.2f}",
                        font=("Segoe UI", 10, "bold"),
                        text_color="#4CAF50",
                        anchor="w"
                    ).pack(side="left", expand=True, fill="x", padx=10)
            else:
                ctk.CTkLabel(
                    historial_frame,
                    text="📭 No hay ventas registradas",
                    font=("Segoe UI", 12),
                    text_color="#999999"
                ).pack(pady=40)
                
        except Exception as e:
            print(f"Error al obtener ventas: {e}")
            ctk.CTkLabel(
                historial_frame,
                text="❌ Error al cargar ventas",
                font=("Segoe UI", 12),
                text_color="#E53935"
            ).pack(pady=40)
        
        # Botón cerrar
        ctk.CTkButton(
            main_frame,
            text="Cerrar",
            fg_color="#E91E63",
            hover_color="#C2185B",
            height=45,
            font=("Segoe UI", 13, "bold"),
            command=ingresos_window.destroy
        ).pack(fill="x", padx=20, pady=(0, 20))
