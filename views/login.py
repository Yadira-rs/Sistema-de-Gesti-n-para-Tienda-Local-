import customtkinter as ctk
from tkinter import messagebox
from database.db import crear_conexion
from views.main import MainApp
from views.recover import RecoverWindow

class LoginWindow(ctk.CTk):
    def __init__(self):
        # Llama al constructor de la clase padre (ctk.CTk) para crear la ventana.
        super().__init__()
        self.title("Janet Rosa Bici - Login")
        self.geometry("400x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue") # "pink" no es un tema por defecto

        # Logo (puedes reemplazar por imagen si tienes el archivo)
        ctk.CTkLabel(self, text="🚲", font=("Segoe UI", 40)).pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Janet Rosa Bici", font=("Segoe UI", 20, "bold")).pack()
        ctk.CTkLabel(self, text="Iniciar sesión para continuar", font=("Segoe UI", 14)).pack(pady=(5, 20))

        # Correo electrónico / Usuario
        ctk.CTkLabel(self, text="Usuario", anchor="w").pack(fill="x", padx=40)
        self.user_entry = ctk.CTkEntry(self, placeholder_text="admin")
        self.user_entry.pack(fill="x", padx=40, pady=8)

        # Contraseña
        ctk.CTkLabel(self, text="Contraseña", anchor="w").pack(fill="x", padx=40)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="••••••••", show="*")
        self.password_entry.pack(fill="x", padx=40, pady=8)

        # Botón iniciar sesión
        ctk.CTkButton(self, text="Iniciar Sesión", command=self.login_action).pack(pady=20)

        # Enlace ¿Olvidaste tu contraseña?
        ctk.CTkButton(self, text="¿Olvidaste tu contraseña?", fg_color="transparent", text_color="gray",
                      hover=False, command=self.recover_action).pack()

    def login_action(self):
        usuario = self.user_entry.get()
        password = self.password_entry.get()

        conn = crear_conexion()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos.")
            return

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s LIMIT 1", (usuario,))
        user = cursor.fetchone()
        conn.close()

        # Primero, verificar si el usuario existe
        if not user:
            messagebox.showerror("Error", "Credenciales incorrectas")
            return

        pwd_field = 'contraseña' if 'contraseña' in user else ('password' if 'password' in user else None)
        if not pwd_field or str(user.get(pwd_field, '')) != password:
            messagebox.showerror("Error", "Credenciales incorrectas")
            return
        
        # Si el login es exitoso
        self.destroy() # Cierra la ventana de login
        app = MainApp(user) # Abre la ventana principal
        app.mainloop()

    def recover_action(self):
        RecoverWindow(self)
