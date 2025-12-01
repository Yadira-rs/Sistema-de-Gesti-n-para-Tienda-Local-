import customtkinter as ctk

class MenuLateral(ctk.CTkFrame):
    def __init__(self, master, callback=None):
        super().__init__(master, width=200, corner_radius=0)
        self.pack_propagate(False)
        self.callback = callback  # Para manejar navegación

        self.crear_menu()

    def crear_menu(self):
        # Encabezado
        titulo = ctk.CTkLabel(self, text="Janet Rosa Bici", font=("Arial", 18, "bold"))
        subtitulo = ctk.CTkLabel(self, text="Sistema de ventas", font=("Arial", 14))
        titulo.pack(pady=(20, 0))
        subtitulo.pack(pady=(0, 20))

        # Botones de navegación
        opciones = [
            "Dashboard",
            "Punto de Venta",
            "Apartado",
            "Inventario",
            "Ventas",
            "Usuarios"
        ]

        for opcion in opciones:
            boton = ctk.CTkButton(self, text=opcion, width=180, command=lambda o=opcion: self.navegar(o))
            boton.pack(pady=5)

        # Separador
        ctk.CTkLabel(self, text="").pack(pady=10)

        # Perfil administrador
        perfil = ctk.CTkLabel(self, text="Administrador", font=("Arial", 14, "bold"))
        correo = ctk.CTkLabel(self, text="admin@janet.com", font=("Arial", 12))
        perfil.pack(pady=(20, 0))
        correo.pack()

    def navegar(self, opcion):
        if self.callback:
            self.callback(opcion)
        print(f"Navegando a: {opcion}")

# Ejemplo de uso
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue") # "pink" no es un tema por defecto

    app = ctk.CTk()
    app.geometry("800x600")

    menu = MenuLateral(app)
    menu.pack(side="left", fill="y")

    contenido = ctk.CTkFrame(app)
    contenido.pack(expand=True, fill="both")

    app.mainloop()