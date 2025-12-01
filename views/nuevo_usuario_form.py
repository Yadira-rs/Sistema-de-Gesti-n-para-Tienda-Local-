import customtkinter as ctk

class NuevoUsuarioForm(ctk.CTkToplevel):
    """
    Ventana emergente para crear un nuevo usuario.
    """
    def __init__(self, parent, on_create=None):
        super().__init__(parent)
        self.title("Nuevo Usuario")
        self.geometry("450x500")
        self.transient(parent)
        self.grab_set()

        self.on_create = on_create

        # --- Panel principal ---
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main, text="Crear Nuevo Usuario", font=("Segoe UI", 20, "bold")).pack(pady=10)

        ctk.CTkLabel(main, text="Nombre de Usuario", anchor="w").pack(fill="x", padx=10)
        self.usuario = ctk.CTkEntry(main, placeholder_text="Ej: mariag")
        self.usuario.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(main, text="Contraseña", anchor="w").pack(fill="x", padx=10)
        self.password = ctk.CTkEntry(main, placeholder_text="••••••••", show="*")
        self.password.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(main, text="Rol", anchor="w").pack(fill="x", padx=10)
        self.rol = ctk.CTkComboBox(main, values=["Administrador", "Cajero", "Empleado"])
        self.rol.set("Cajero") # Valor por defecto
        self.rol.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(main, text="Pregunta de Seguridad", anchor="w").pack(fill="x", padx=10)
        self.pregunta = ctk.CTkEntry(main, placeholder_text="Ej: Nombre de mi primera mascota")
        self.pregunta.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(main, text="Respuesta de Seguridad", anchor="w").pack(fill="x", padx=10)
        self.respuesta = ctk.CTkEntry(main, placeholder_text="Ej: Firulais")
        self.respuesta.pack(fill="x", pady=5, padx=10)

        # Botones
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Crear Usuario", fg_color="#D76B74", command=self.crear_usuario).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="gray", command=self.destroy).pack(side="left", padx=10)

    def crear_usuario(self):
        """Recopila los datos y los pasa al callback on_create."""
        datos = {
            "usuario": self.usuario.get(),
            "password": self.password.get(),
            "rol": self.rol.get(),
            "pregunta": self.pregunta.get(),
            "respuesta": self.respuesta.get()
        }
        if self.on_create:
            self.on_create(datos)
        self.destroy()