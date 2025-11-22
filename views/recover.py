import tkinter as tk
from tkinter import ttk, messagebox
from controllers.users import recuperar_contraseña

class RecoverWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Recuperación de Contraseña")
        self.geometry("460x360")
        self.configure(bg="#D9D9D9")
        self.resizable(False, False)

        style = ttk.Style(self)
        style.configure("Pink.TButton", font=("Segoe UI", 11, "bold"), foreground="#fff", background="#E48CA6")
        style.map("Pink.TButton", background=[("active", "#D97393")])

        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Recuperación de Contraseña", font=("Segoe UI", 16, "bold")).pack(pady=6)
        ttk.Label(container, text="Información de acceso al sistema", font=("Segoe UI", 10)).pack()

        ttk.Label(container, text="Ingresa tu correo electrónico").pack(anchor="w", pady=(16, 4))
        self.entry_usuario = ttk.Entry(container, font=("Segoe UI", 12))
        self.entry_usuario.pack(fill="x")

        ttk.Label(container, text="Ingresa el código o respuesta").pack(anchor="w", pady=(16, 4))
        self.entry_respuesta = ttk.Entry(container, font=("Segoe UI", 12))
        self.entry_respuesta.pack(fill="x")

        ttk.Label(container, text="Nueva contraseña").pack(anchor="w", pady=(16, 4))
        self.entry_nueva = ttk.Entry(container, show="*", font=("Segoe UI", 12))
        self.entry_nueva.pack(fill="x")

        ttk.Button(container, text="Iniciar Sesión", style="Pink.TButton", command=self.reset).pack(pady=16, fill="x")
        ttk.Button(container, text="Regresar", command=self.destroy).pack(fill="x")

    def reset(self):
        usuario = self.entry_usuario.get().strip()
        respuesta = self.entry_respuesta.get().strip()
        nueva = self.entry_nueva.get().strip()
        if not usuario or not respuesta or not nueva:
            messagebox.showwarning("Datos incompletos", "Completa todos los campos")
            return
        ok, msg = recuperar_contraseña(usuario, respuesta, nueva)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.destroy()
        else:
            messagebox.showerror("Error", msg)