import customtkinter as ctk

class NuevoUsuarioForm(ctk.CTkToplevel):
    """
    Ventana emergente para crear un nuevo usuario.
    """
    def __init__(self, parent, on_create=None):
        super().__init__(parent)
        self.title("Nuevo Usuario")
        self.geometry("550x650")
        self.transient(parent)
        self.grab_set()

        self.on_create = on_create

        # --- Panel principal ---
        main = ctk.CTkFrame(self, fg_color="white")
        main.pack(fill="both", expand=True, padx=30, pady=30)

        # Título
        ctk.CTkLabel(
            main, 
            text="Nuevo usuario", 
            font=("Segoe UI", 24, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 30))

        # Nombre completo
        ctk.CTkLabel(
            main, 
            text="Nombre completo", 
            anchor="w",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(fill="x", padx=10, pady=(10, 5))
        self.nombre_completo = ctk.CTkEntry(
            main, 
            placeholder_text="Ej: María García",
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.nombre_completo.pack(fill="x", padx=10)

        # Email
        ctk.CTkLabel(
            main, 
            text="Email", 
            anchor="w",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(fill="x", padx=10, pady=(15, 5))
        self.email = ctk.CTkEntry(
            main, 
            placeholder_text="usuario@rosabici.com",
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.email.pack(fill="x", padx=10)

        # Contraseña
        ctk.CTkLabel(
            main, 
            text="Contraseña", 
            anchor="w",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(fill="x", padx=10, pady=(15, 5))
        self.password = ctk.CTkEntry(
            main, 
            placeholder_text="••••••••••••••••••••",
            show="*",
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.password.pack(fill="x", padx=10)

        # Rol
        ctk.CTkLabel(
            main, 
            text="Rol", 
            anchor="w",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(fill="x", padx=10, pady=(15, 5))
        self.rol = ctk.CTkComboBox(
            main, 
            values=["Vendedor", "Administrador", "Cajero"],
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.rol.set("Vendedor")
        self.rol.pack(fill="x", padx=10)

        # Mensaje informativo
        info_frame = ctk.CTkFrame(main, fg_color="#E3F2FD", corner_radius=10)
        info_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️  acceso limitado, solo puede realizar ventas , consultas , apartado y\n     consultar el catálogo de productos",
            font=("Segoe UI", 11),
            text_color="#1976D2",
            justify="left"
        ).pack(padx=15, pady=12)

        # Checkbox Usuario activo
        self.usuario_activo = ctk.CTkCheckBox(
            main,
            text="Usuario activo",
            font=("Segoe UI", 12),
            text_color="#666666"
        )
        self.usuario_activo.pack(padx=10, pady=(15, 20), anchor="w")

        # Botones
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(20, 0))

        ctk.CTkButton(
            btn_frame, 
            text="Crear usuario", 
            fg_color="#FF0000",
            hover_color="#CC0000",
            height=45,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            command=self.crear_usuario
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame, 
            text="Cancelar", 
            fg_color="white",
            hover_color="#F0F0F0",
            text_color="#666666",
            border_width=2,
            border_color="#CCCCCC",
            height=45,
            width=180,
            corner_radius=10,
            font=("Segoe UI", 13),
            command=self.destroy
        ).pack(side="left", padx=10)

    def crear_usuario(self):
        """Recopila los datos y los pasa al callback on_create."""
        datos = {
            "nombre_completo": self.nombre_completo.get(),
            "email": self.email.get(),
            "password": self.password.get(),
            "rol": self.rol.get(),
            "activo": self.usuario_activo.get()
        }
        if self.on_create:
            self.on_create(datos)
        self.destroy()