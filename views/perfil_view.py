import customtkinter as ctk
from tkinter import messagebox

class PerfilView(ctk.CTkFrame):
    """Vista de perfil de usuario - Diseño con formulario y botones laterales"""
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.user = user or {"nombre_completo": "Administrador", "email": "admin@boutique.com", "rol": "Admin"}
        self.pack(fill="both", expand=True)
        self.mostrar_password = False
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Contenedor principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=50, pady=40)
        
        # Obtener color según rol
        rol = self.user.get("rol", "Admin")
        self.avatar_color = {
            'Administrador': '#E91E63',
            'Vendedor': '#9C27B0',
            'Cajero': '#2196F3',
            'Empleado': '#4CAF50'
        }.get(rol, '#E91E63')
        
        self.avatar_bg = {
            'Administrador': '#FCE4EC',
            'Vendedor': '#F3E5F5',
            'Cajero': '#E3F2FD',
            'Empleado': '#E8F5E9'
        }.get(rol, '#FCE4EC')
        
        # Tarjeta de información del usuario (horizontal)
        user_card = ctk.CTkFrame(main_container, fg_color=self.avatar_bg, corner_radius=30, height=200)
        user_card.pack(fill="x", pady=(0, 30))
        user_card.pack_propagate(False)
        
        # Contenedor horizontal para avatar + info
        card_content = ctk.CTkFrame(user_card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=50, pady=40)
        
        # Avatar circular a la izquierda con fondo más oscuro
        avatar_outer = ctk.CTkFrame(
            card_content,
            fg_color="#F8BBD0",  # Rosa más oscuro
            corner_radius=75,
            width=150,
            height=150
        )
        avatar_outer.pack(side="left", padx=(0, 40))
        avatar_outer.pack_propagate(False)
        
        # Inicial del nombre con color verde
        inicial = self.user.get("nombre_completo", "A")[0].upper()
        
        ctk.CTkLabel(
            avatar_outer,
            text=inicial,
            font=("Segoe UI", 70, "bold"),
            text_color="#66BB6A"  # Verde como en la imagen
        ).pack(expand=True)
        
        # Información del usuario a la derecha
        info_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Nombre del usuario
        ctk.CTkLabel(
            info_frame,
            text=self.user.get("nombre_completo", "Usuario"),
            font=("Segoe UI", 36, "bold"),
            text_color=self.avatar_color,
            anchor="w"
        ).pack(anchor="w", pady=(0, 10))
        
        # Rol con icono
        rol_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        rol_frame.pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(
            rol_frame,
            text=f"🛡️  {rol}",
            font=("Segoe UI", 20, "bold"),
            text_color=self.avatar_color,
            anchor="w"
        ).pack(side="left")
        
        # Email
        ctk.CTkLabel(
            info_frame,
            text=self.user.get("email", ""),
            font=("Segoe UI", 18),
            text_color=self.avatar_color,
            anchor="w"
        ).pack(anchor="w")
        
        # Panel de contenido con dos columnas
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.pack(fill="both", expand=True)
        
        # Panel izquierdo - Formulario de edición
        left_panel = ctk.CTkFrame(content_container, fg_color="white", corner_radius=25)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        left_content = ctk.CTkFrame(left_panel, fg_color="transparent")
        left_content.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Título del formulario
        ctk.CTkLabel(
            left_content,
            text="✏️  Editar Información",
            font=("Segoe UI", 22, "bold"),
            text_color="#1A1A1A",
            anchor="w"
        ).pack(anchor="w", pady=(0, 25))
        
        # Campo Nombre con icono
        nombre_frame = ctk.CTkFrame(left_content, fg_color="transparent")
        nombre_frame.pack(fill="x", pady=(0, 18))
        
        ctk.CTkLabel(
            nombre_frame,
            text="👤  Nombre completo",
            font=("Segoe UI", 13, "bold"),
            text_color="#555555",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        self.nombre_entry = ctk.CTkEntry(
            nombre_frame,
            height=52,
            corner_radius=15,
            border_width=0,
            font=("Segoe UI", 15),
            fg_color="#F8F9FA",
            text_color="#2C2C2C"
        )
        self.nombre_entry.pack(fill="x")
        self.nombre_entry.insert(0, self.user.get("nombre_completo", ""))
        
        # Campo Email con icono
        email_frame = ctk.CTkFrame(left_content, fg_color="transparent")
        email_frame.pack(fill="x", pady=(0, 18))
        
        ctk.CTkLabel(
            email_frame,
            text="📧  Correo electrónico",
            font=("Segoe UI", 13, "bold"),
            text_color="#555555",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        self.email_entry = ctk.CTkEntry(
            email_frame,
            height=52,
            corner_radius=15,
            border_width=0,
            font=("Segoe UI", 15),
            fg_color="#F8F9FA",
            text_color="#2C2C2C"
        )
        self.email_entry.pack(fill="x")
        self.email_entry.insert(0, self.user.get("email", ""))
        
        # Campo Contraseña con icono
        password_frame = ctk.CTkFrame(left_content, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 25))
        
        ctk.CTkLabel(
            password_frame,
            text="🔒  Contraseña",
            font=("Segoe UI", 13, "bold"),
            text_color="#555555",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        password_container = ctk.CTkFrame(password_frame, fg_color="transparent")
        password_container.pack(fill="x")
        
        self.password_entry = ctk.CTkEntry(
            password_container,
            height=52,
            corner_radius=15,
            border_width=0,
            font=("Segoe UI", 15),
            fg_color="#F8F9FA",
            text_color="#2C2C2C",
            show="•"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.password_entry.insert(0, "••••••••")
        
        # Botón mostrar/ocultar contraseña
        self.toggle_btn = ctk.CTkButton(
            password_container,
            text="👁",
            width=52,
            height=52,
            corner_radius=15,
            fg_color="#F8F9FA",
            text_color="#666666",
            hover_color="#E8E9EA",
            border_width=0,
            font=("Segoe UI", 20),
            command=self.toggle_password
        )
        self.toggle_btn.pack(side="left")
        
        # Panel derecho - Acciones rápidas
        right_panel = ctk.CTkFrame(content_container, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        # Tarjeta de acciones principales
        actions_card = ctk.CTkFrame(right_panel, fg_color="white", corner_radius=25)
        actions_card.pack(fill="both", expand=True)
        
        actions_content = ctk.CTkFrame(actions_card, fg_color="transparent")
        actions_content.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Título de acciones
        ctk.CTkLabel(
            actions_content,
            text="⚡ Acciones Rápidas",
            font=("Segoe UI", 24, "bold"),
            text_color="#1A1A1A",
            anchor="w"
        ).pack(anchor="w", pady=(0, 30))
        
        # Botón Guardar cambios (destacado en rosa)
        guardar_btn = ctk.CTkButton(
            actions_content,
            text="💾  Guardar Cambios",
            height=70,
            corner_radius=20,
            fg_color="#E91E63",
            hover_color="#C2185B",
            font=("Segoe UI", 18, "bold"),
            text_color="white",
            command=self.guardar_cambios
        )
        guardar_btn.pack(fill="x", pady=(0, 20))
        
        # Separador visual
        separator = ctk.CTkFrame(actions_content, height=1, fg_color="#E8E8E8")
        separator.pack(fill="x", pady=20)
        
        # Grid de botones secundarios (2x2) con diseño mejorado
        grid_frame = ctk.CTkFrame(actions_content, fg_color="transparent")
        grid_frame.pack(fill="x", pady=(0, 20))
        
        # Fila 1
        row1 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 15))
        
        # Botón Editar perfil
        edit_btn = ctk.CTkButton(
            row1,
            text="✏️  Editar Perfil",
            height=65,
            corner_radius=18,
            fg_color="#E3F2FD",
            hover_color="#BBDEFB",
            font=("Segoe UI", 15, "bold"),
            text_color="#1976D2",
            border_width=0,
            command=self.editar_perfil
        )
        edit_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botón Agregar usuario
        add_btn = ctk.CTkButton(
            row1,
            text="➕  Agregar Usuario",
            height=65,
            corner_radius=18,
            fg_color="#E8F5E9",
            hover_color="#C8E6C9",
            font=("Segoe UI", 15, "bold"),
            text_color="#388E3C",
            border_width=0,
            command=self.agregar_perfil
        )
        add_btn.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Fila 2
        row2 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row2.pack(fill="x")
        
        # Botón Eliminar perfil
        delete_btn = ctk.CTkButton(
            row2,
            text="🗑️  Eliminar Perfil",
            height=65,
            corner_radius=18,
            fg_color="#FFEBEE",
            hover_color="#FFCDD2",
            font=("Segoe UI", 15, "bold"),
            text_color="#D32F2F",
            border_width=0,
            command=self.borrar_perfil
        )
        delete_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botón Ayuda
        help_btn = ctk.CTkButton(
            row2,
            text="❓  Ayuda",
            height=65,
            corner_radius=18,
            fg_color="#FFF3E0",
            hover_color="#FFE0B2",
            font=("Segoe UI", 15, "bold"),
            text_color="#F57C00",
            border_width=0,
            command=self.mostrar_ayuda
        )
        help_btn.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Espaciador
        ctk.CTkFrame(actions_content, fg_color="transparent").pack(expand=True)
        
        # Botón Cerrar sesión al final con diseño mejorado
        logout_btn = ctk.CTkButton(
            actions_content,
            text="🚪  Cerrar Sesión",
            height=70,
            corner_radius=20,
            fg_color="#FF5252",
            hover_color="#E53935",
            font=("Segoe UI", 17, "bold"),
            text_color="white",
            border_width=0,
            command=self.cerrar_sesion
        )
        logout_btn.pack(fill="x", pady=(20, 0))
    
    def darken_color(self, hex_color):
        """Oscurecer un color hexadecimal para el efecto hover"""
        # Convertir hex a RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        # Oscurecer 20%
        r = int(r * 0.8)
        g = int(g * 0.8)
        b = int(b * 0.8)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def toggle_password(self):
        """Mostrar/ocultar contraseña"""
        self.mostrar_password = not self.mostrar_password
        
        if self.mostrar_password:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="👁‍🗨")
        else:
            self.password_entry.configure(show="•")
            self.toggle_btn.configure(text="👁")
    
    def editar_perfil(self):
        """Habilitar edición del perfil"""
        messagebox.showinfo("Editar Perfil", "Puedes modificar los campos y luego hacer clic en 'Guardar cambios'")
    
    def borrar_perfil(self):
        """Borrar perfil (solo para administradores)"""
        rol = self.user.get("rol", "").lower()
        if "admin" not in rol:
            messagebox.showwarning("Acceso Denegado", "Solo los administradores pueden borrar perfiles")
            return
        
        respuesta = messagebox.askyesno(
            "Borrar Perfil",
            "⚠️ ¿Estás seguro de que deseas borrar este perfil?\n\nEsta acción no se puede deshacer."
        )
        if respuesta:
            messagebox.showinfo("Función en desarrollo", "La función de borrar perfil estará disponible próximamente")
    
    def agregar_perfil(self):
        """Agregar nuevo perfil (solo para administradores)"""
        rol = self.user.get("rol", "").lower()
        if "admin" not in rol:
            messagebox.showwarning("Acceso Denegado", "Solo los administradores pueden agregar perfiles")
            return
        
        messagebox.showinfo("Agregar Perfil", "Redirigiendo a la sección de Usuarios para agregar un nuevo perfil...")
    
    def mostrar_ayuda(self):
        """Mostrar ayuda sobre el perfil"""
        messagebox.showinfo(
            "Ayuda - Perfil de Usuario",
            "📋 Información del Perfil:\n\n"
            "• Puedes editar tu nombre y correo electrónico\n"
            "• Para cambiar tu contraseña, escribe una nueva\n"
            "• Haz clic en 'Guardar Cambios' para aplicar\n"
            "• El botón 👁 muestra/oculta tu contraseña\n\n"
            "🔐 Permisos:\n"
            "• Solo administradores pueden agregar/eliminar usuarios\n"
            "• Cada usuario puede editar su propio perfil"
        )
    
    def guardar_cambios(self):
        """Guardar cambios del perfil"""
        nombre = self.nombre_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not nombre or not email:
            messagebox.showwarning("Datos incompletos", "Nombre y email son obligatorios")
            return
        
        try:
            from database.db import crear_conexion
            
            conn = crear_conexion()
            if not conn:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
            
            cursor = conn.cursor()
            
            # Actualizar nombre y email
            cursor.execute(
                "UPDATE usuarios SET nombre_completo = %s, email = %s WHERE id_usuario = %s",
                (nombre, email, self.user.get('id_usuario'))
            )
            
            # Actualizar contraseña solo si se modificó
            if password and password != "••••••••":
                cursor.execute(
                    "UPDATE usuarios SET contraseña = %s WHERE id_usuario = %s",
                    (password, self.user.get('id_usuario'))
                )
            
            conn.commit()
            conn.close()
            
            # Actualizar datos del usuario en memoria
            self.user['nombre_completo'] = nombre
            self.user['email'] = email
            
            messagebox.showinfo("Éxito", "✅ Perfil actualizado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el perfil:\n{str(e)}")
    
    def cerrar_sesion(self):
        """Cerrar sesión del usuario"""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?"
        )
        if respuesta:
            # Cerrar la ventana principal y volver al login
            self.master.master.destroy()


if __name__ == "__main__":
    # Prueba de la vista
    root = ctk.CTk()
    root.title("Perfil - Janet Rosa Bici")
    root.geometry("900x600")
    ctk.set_appearance_mode("light")
    
    usuario = {
        "nombre_completo": "Administrador",
        "email": "admin@janet.com"
    }
    
    perfil = PerfilView(root, usuario)
    root.mainloop()
