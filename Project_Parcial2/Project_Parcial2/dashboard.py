import tkinter as tk
from user_view import UserApp
from products_view import ProductsApp

class Dashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.crear_menu()

    def crear_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Bienvenido {self.username}", font=("Arial", 20, "bold")).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Gestionar Usuarios", width=20, command=self.abrir_usuarios).pack(pady=5)
        tk.Button(frame, text="Gestionar Productos", width=20, command=self.abrir_productos).pack(pady=5)
        tk.Button(frame, text="Cerrar Sesión", width=20, command=self.cerrar_sesion).pack(pady=20)

    def abrir_usuarios(self):
        self.root.destroy()
        UserApp(self.username)

    def abrir_productos(self):
        self.root.destroy()
        ProductsApp(self.username)

    def cerrar_sesion(self):
        from login_view import LoginApp
        self.root.destroy()
        root = tk.Tk()
        LoginApp(root)
        root.mainloop()