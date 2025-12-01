import customtkinter as ctk

class PerfilUsuario(ctk.CTkFrame):
    """
    Una vista de Frame que muestra la información del perfil del usuario
    y proporciona botones para diversas acciones.
    """
    def __init__(self, parent, usuario, on_editar=None, on_borrar=None, on_agregar=None, on_logout=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=40, pady=40)

        # Usa el nombre de usuario si el nombre completo no está disponible
        nombre_usuario = usuario.get("nombre", usuario.get("usuario", "Usuario"))
        email_usuario = usuario.get("email", "No especificado")

        # Icono circular con inicial
        inicial = nombre_usuario[0].upper() if nombre_usuario else 'U'
        ctk.CTkLabel(self, text=inicial, font=("Segoe UI", 40, "bold"),
                     width=80, height=80, corner_radius=40,
                     fg_color="#E3A8C5", text_color="white").pack(pady=10)

        # Campos de perfil
        ctk.CTkLabel(self, text="Nombre", anchor="w").pack(fill="x")
        nombre_entry = ctk.CTkEntry(self, placeholder_text=nombre_usuario)
        nombre_entry.pack(fill="x", pady=5)
        nombre_entry.configure(state="disabled")

        ctk.CTkLabel(self, text="Correo electrónico", anchor="w").pack(fill="x")
        email_entry = ctk.CTkEntry(self, placeholder_text=email_usuario)
        email_entry.pack(fill="x", pady=5)
        email_entry.configure(state="disabled")

        ctk.CTkLabel(self, text="Contraseña", anchor="w").pack(fill="x")
        pass_entry = ctk.CTkEntry(self, placeholder_text="••••••••", show="*")
        pass_entry.pack(fill="x", pady=5)
        pass_entry.configure(state="disabled")

        # Botones de acción
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Editar perfil", fg_color="#D76B74", command=on_editar).pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="Borrar perfil", fg_color="#D76B74", command=on_borrar).pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="Agregar perfil", fg_color="#D76B74", command=on_agregar).pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="Cerrar sesión", fg_color="#5E4B56", command=on_logout).pack(fill="x", pady=15)