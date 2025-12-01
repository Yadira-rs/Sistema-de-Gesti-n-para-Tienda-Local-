import customtkinter as ctk
from tkinter import messagebox

class ClienteForm(ctk.CTkToplevel):
    """
    Ventana emergente para capturar los datos de un cliente
    para un nuevo apartado.
    """
    def __init__(self, parent, on_create=None):
        super().__init__(parent)
        self.title("Nuevo Apartado - Cliente")
        self.geometry("400x400")
        self.transient(parent)
        self.grab_set()

        ctk.set_appearance_mode("light")
        # Usando un tema válido para evitar errores.
        ctk.set_default_color_theme("blue")

        self.on_create = on_create

        ctk.CTkLabel(self, text="Nuevo Apartado", font=("Segoe UI", 20, "bold")).pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Ingresa los datos del cliente", font=("Segoe UI", 14)).pack(pady=(0, 20))

        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre *")
        self.nombre.pack(fill="x", padx=40, pady=8)

        self.telefono = ctk.CTkEntry(self, placeholder_text="Teléfono *")
        self.telefono.pack(fill="x", padx=40, pady=8)

        self.email = ctk.CTkEntry(self, placeholder_text="Email (opcional)")
        self.email.pack(fill="x", padx=40, pady=8)

        ctk.CTkButton(self, text="Crear y Continuar", command=self.crear_cliente).pack(pady=20)
        ctk.CTkButton(self, text="Cancelar", fg_color="gray", command=self.destroy).pack()

    def crear_cliente(self):
        """Valida los datos y llama al callback on_create."""
        nombre = self.nombre.get().strip()
        telefono = self.telefono.get().strip()

        if not nombre or not telefono:
            messagebox.showwarning("Campos incompletos", "El nombre y el teléfono son obligatorios.", parent=self)
            return

        cliente = {
            "nombre": nombre,
            "telefono": telefono,
            "email": self.email.get().strip()
        }
        if self.on_create:
            self.on_create(cliente)
        self.destroy()