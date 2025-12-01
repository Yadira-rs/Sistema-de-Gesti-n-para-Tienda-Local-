import customtkinter as ctk
from tkinter import messagebox
from controllers.users import recuperar_contraseña

class RecoverWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Recuperación de Contraseña")
        self.geometry("400x500")
        self.transient(master)
        self.grab_set()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue") # "pink" no es un tema por defecto

        self.resizable(False, False)

        # Título y subtítulo
        ctk.CTkLabel(self, text="Recuperación de Contraseña", font=("Segoe UI", 20, "bold")).pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Información de acceso al sistema", font=("Segoe UI", 14)).pack(pady=(0, 20))

        # Campo Usuario
        ctk.CTkLabel(self, text="Ingresa tu nombre de usuario", anchor="w").pack(fill="x", padx=40)
        self.user_entry = ctk.CTkEntry(self, placeholder_text="admin")
        self.user_entry.pack(fill="x", padx=40, pady=8)

        # Campo Respuesta de Seguridad
        ctk.CTkLabel(self, text="Ingresa tu respuesta de seguridad", anchor="w").pack(fill="x", padx=40)
        self.answer_entry = ctk.CTkEntry(self, placeholder_text="Respuesta a tu pregunta secreta")
        self.answer_entry.pack(fill="x", padx=40, pady=8)

        # Campo Nueva Contraseña
        ctk.CTkLabel(self, text="Ingresa tu nueva contraseña", anchor="w").pack(fill="x", padx=40)
        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="••••••••", show="*")
        self.new_password_entry.pack(fill="x", padx=40, pady=8)

        # Botón Restablecer
        ctk.CTkButton(self, text="Restablecer Contraseña", command=self.reset_action).pack(pady=20)

        # Botón Regresar
        ctk.CTkButton(self, text="Regresar", fg_color="gray", command=self.destroy).pack()

    def reset_action(self):
        usuario = self.user_entry.get().strip()
        respuesta = self.answer_entry.get().strip()
        nueva = self.new_password_entry.get().strip()
        if not usuario or not respuesta or not nueva:
            messagebox.showwarning("Datos incompletos", "Completa todos los campos.", parent=self)
            return
        ok, msg = recuperar_contraseña(usuario, respuesta, nueva)
        if ok:
            messagebox.showinfo("Éxito", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self)