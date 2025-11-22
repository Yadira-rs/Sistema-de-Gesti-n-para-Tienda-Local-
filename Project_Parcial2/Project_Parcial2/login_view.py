import tkinter as tk
from tkinter import ttk, messagebox
from auth_controller import validar_creedenciales
from dashboard import Dashboard

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("Sistema de Login")
        self.root.resizable(False, False)
        self.crear_pantalla_login()

    def crear_pantalla_login(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # ---- Pantalla de LOGIN ----
        tk.Label(self.root, text="Bienvenido al Sistema", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self.root, text="Usuario o correo:").pack()
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)
        self.username_entry.insert(1, "Cindy")

        tk.Label(self.root, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, "1234")

        tk.Button(self.root, text="Iniciar sesión", command=self.Login, width=20).pack(pady=20)

    def Login(self):
        usuario = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Faltan datos", "Por favor ingresa usuario y contraseña")
            return

        if validar_creedenciales(usuario, password):
            messagebox.showinfo("Acceso concedido", f"Bienvenido {usuario}")
            # Muestra el panel directamente en la misma ventana
            self.mostrar_panel(usuario)
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")

    def mostrar_panel(self, usuario):
        Dashboard(self.root, usuario)