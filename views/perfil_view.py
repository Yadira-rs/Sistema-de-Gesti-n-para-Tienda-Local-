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
        # Título de la página
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=40, pady=(30, 20))
        
        ctk.CTkLabel(
            title_frame,
            text="Perfil",
            font=("Segoe UI", 32, "bold"),
            text_color="#2C2C2C",
            anchor="w"
        ).pack(anchor="w")
        
        # Contenedor principal con dos columnas
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Obtener color según rol
        rol = self.user.get("rol", "Admin")
        self.avatar_color = {
            'Administrador': '#E91E63',
            'Vendedor': '#AB47BC',
            'Cajero': '#42A5F5',
            'Empleado': '#66BB6A'
        }.get(rol, '#E91E63')
        
        # Panel izquierdo - Formulario
        left_panel = ctk.CTkFrame(main_container, fg_color="white", corner_radius=20)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        left_content = ctk.CTkFrame(left_panel, fg_color="transparent")
        left_content.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Avatar circular grande
        avatar_frame = ctk.CTkFrame(
            left_content,
            fg_color="#F8BBD0",
            corner_radius=80,
            width=160,
            height=160
        )
        avatar_frame.pack(pady=(0, 30))
        avatar_frame.pack_propagate(False)
        
        # Inicial del nombre
        inicial = self.user.get("nombre_completo", "A")[0].upper()
        
        ctk.CTkLabel(
            avatar_frame,
            text=inicial,
            font=("Segoe UI", 72, "bold"),
            text_color=self.avatar_color
        ).pack(expand=True)
        
        # Campo Nombre
        ctk.CTkLabel(
            left_content,
            text="Nombre",
            font=("Segoe UI", 14, "bold"),
            text_color="#2C2C2C",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        self.nombre_entry = ctk.CTkEntry(
            left_content,
            height=50,
            corner_radius=12,
            border_width=2,
            border_color="#E0E0E0",
            font=("Segoe UI", 14),
            fg_color="white",
            text_color="#666666"
        )
        self.nombre_entry.pack(fill="x", pady=(0, 20))
        self.nombre_entry.insert(0, self.user.get("nombre_completo", ""))
        
        # Campo Correo electrónico
        ctk.CTkLabel(
            left_content,
            text="Correo electrónico",
            font=("Segoe UI", 14, "bold"),
            text_color="#2C2C2C",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        self.email_entry = ctk.CTkEntry(
            left_content,
            height=50,
            corner_radius=12,
            border_width=2,
            border_color="#E0E0E0",
            font=("Segoe UI", 14),
            fg_color="white",
            text_color="#666666"
        )
        self.email_entry.pack(fill="x", pady=(0, 20))
        self.email_entry.insert(0, self.user.get("email", ""))
        
        # Campo Contraseña
        ctk.CTkLabel(
            left_content,
            text="Contraseña",
            font=("Segoe UI", 14, "bold"),
            text_color="#2C2C2C",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        password_container = ctk.CTkFrame(left_content, fg_color="transparent")
        password_container.pack(fill="x", pady=(0, 20))
        
        self.password_entry = ctk.CTkEntry(
            password_container,
            height=50,
            corner_radius=12,
            border_width=2,
            border_color="#E0E0E0",
            font=("Segoe UI", 14),
            fg_color="white",
            text_color="#666666",
            show="•"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.password_entry.insert(0, "••••••••")
        
        # Botón mostrar/ocultar contraseña
        self.toggle_btn = ctk.CTkButton(
            password_container,
            text="👁",
            width=50,
            height=50,
            corner_radius=12,
            fg_color="white",
            text_color="#666666",
            hover_color="#F5F5F5",
            border_width=2,
            border_color="#E0E0E0",
            font=("Segoe UI", 18),
            command=self.toggle_password
        )
        self.toggle_btn.pack(side="left")
        
        # Panel derecho - Botones de acción
        right_panel = ctk.CTkFrame(main_container, fg_color="transparent", width=280)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # Botón Editar perfil
        ctk.CTkButton(
            right_panel,
            text="✏️  Editar perfil",
            height=60,
            corner_radius=15,
            fg_color=self.avatar_color,
            hover_color=self.darken_color(self.avatar_color),
            font=("Segoe UI", 16, "bold"),
            text_color="white",
            command=self.editar_perfil
        ).pack(fill="x", pady=(0, 15))
        
        # Botón Borrar perfil
        ctk.CTkButton(
            right_panel,
            text="🗑️  Borrar perfil",
            height=60,
            corner_radius=15,
            fg_color=self.avatar_color,
            hover_color=self.darken_color(self.avatar_color),
            font=("Segoe UI", 16, "bold"),
            text_color="white",
            command=self.borrar_perfil
        ).pack(fill="x", pady=(0, 15))
        
        # Botón Agregar perfil
        ctk.CTkButton(
            right_panel,
            text="➕  Agregar perfil",
            height=60,
            corner_radius=15,
            fg_color=self.avatar_color,
            hover_color=self.darken_color(self.avatar_color),
            font=("Segoe UI", 16, "bold"),
            text_color="white",
            command=self.agregar_perfil
        ).pack(fill="x", pady=(0, 15))
        
        # Botón Guardar cambios
        ctk.CTkButton(
            right_panel,
            text="💾  Guardar cambios",
            height=60,
            corner_radius=15,
            fg_color=self.avatar_color,
            hover_color=self.darken_color(self.avatar_color),
            font=("Segoe UI", 16, "bold"),
            text_color="white",
            command=self.guardar_cambios
        ).pack(fill="x", pady=(0, 30))
        
        # Botón Cerrar sesión
        ctk.CTkButton(
            right_panel,
            text="➜  Cerrar sesión",
            height=60,
            corner_radius=15,
            fg_color=self.avatar_color,
            hover_color=self.darken_color(self.avatar_color),
            font=("Segoe UI", 16, "bold"),
            text_color="white",
            command=self.cerrar_sesion
        ).pack(fill="x")
    
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
        if self.user.get("rol") not in ["Administrador", "Admin"]:
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
        if self.user.get("rol") not in ["Administrador", "Admin"]:
            messagebox.showwarning("Acceso Denegado", "Solo los administradores pueden agregar perfiles")
            return
        
        messagebox.showinfo("Agregar Perfil", "Redirigiendo a la sección de Usuarios para agregar un nuevo perfil...")
    
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
