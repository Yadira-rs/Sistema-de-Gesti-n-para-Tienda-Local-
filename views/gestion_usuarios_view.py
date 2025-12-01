import customtkinter as ctk
from tkinter import messagebox
from controllers.users import listar_usuarios

class GestionUsuarios(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Janet Rosa Bici - Gestión de Usuario")
        self.geometry("1000x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue") # "pink" no es un tema por defecto

        self.crear_interfaz()

    def crear_interfaz(self):
        # Menú lateral
        menu = ctk.CTkFrame(self, width=200)
        menu.pack(side="left", fill="y")

        ctk.CTkLabel(menu, text="Janet Rosa Bici", font=("Arial", 18, "bold")).pack(pady=(20, 0))
        ctk.CTkLabel(menu, text="Sistema de ventas", font=("Arial", 14)).pack(pady=(0, 20))

        for opcion in ["Dashboard", "Punto de Venta", "Apartado", "Inventario", "Ventas", "Usuarios"]:
            ctk.CTkButton(menu, text=opcion, width=180).pack(pady=5)

        ctk.CTkLabel(menu, text="").pack(pady=10)
        ctk.CTkLabel(menu, text="Administrador", font=("Arial", 14, "bold")).pack(pady=(20, 0))
        ctk.CTkLabel(menu, text="admin@janet.com", font=("Arial", 12)).pack()

        # Panel principal
        panel = ctk.CTkFrame(self)
        panel.pack(side="left", expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(panel, text="Gestión de Usuario", font=("Arial", 20, "bold")).pack(pady=(0, 10))

        # Cargar usuarios desde la base de datos
        usuarios = listar_usuarios()

        # Estadísticas
        estadisticas = ctk.CTkFrame(panel)
        estadisticas.pack(pady=10)

        total = len(usuarios)
        admins = sum(1 for u in usuarios if u.get("rol") == "Administrador")
        cajeros = sum(1 for u in usuarios if u.get("rol") == "Cajero")

        for texto in [f"Total: {total}", f"Admins: {admins}", f"Vendedores: {cajeros}"]:
            ctk.CTkLabel(estadisticas, text=texto, font=("Arial", 14)).pack(side="left", padx=10)

        # Mensaje informativo
        mensaje = (
            "¿Olvidaste tu contraseña?\n"
            "Tú al ser administrador puedes restaurar las contraseñas y cambiarlas\n"
            "utilizando el botón 'olvide mi contraseña' en el inicio de sesión."
        )
        ctk.CTkLabel(panel, text=mensaje, text_color="lightblue", font=("Arial", 12), justify="left").pack(pady=10)

        # Filtros
        filtros = ctk.CTkFrame(panel)
        filtros.pack(pady=10)

        ctk.CTkEntry(filtros, placeholder_text="Buscar usuario...", width=200).pack(side="left", padx=5)
        ctk.CTkComboBox(filtros, values=["Todos", "Admin", "Cajero"], width=150).pack(side="left", padx=5)
        ctk.CTkComboBox(filtros, values=["Todos", "Activo", "Inactivo"], width=150).pack(side="left", padx=5)

        # Tabla de usuarios
        tabla = ctk.CTkScrollableFrame(panel, height=300)
        tabla.pack(fill="x", pady=10)

        encabezado = ctk.CTkFrame(tabla)
        encabezado.pack(fill="x")
        for col in ["Usuario", "Email", "Rol", "Estado", "Fecha Creación"]:
            ctk.CTkLabel(encabezado, text=col, font=("Arial", 13, "bold"), width=180).pack(side="left")

        for u in usuarios:
            fila = ctk.CTkFrame(tabla)
            fila.pack(fill="x", pady=2)
            # Adaptar a los datos reales de la BD y usar valores por defecto para los que no existen
            valores = [u.get("usuario", "N/A"), "No disponible", u.get("rol", "N/A"), "Activo", "No disponible"]
            for valor in valores:
                ctk.CTkLabel(fila, text=valor, width=180).pack(side="left")

        # Botón nuevo usuario
        ctk.CTkButton(panel, text="+ Nuevo Usuario", command=self.crear_usuario).pack(pady=10)

    def crear_usuario(self):
        from views.nuevo_usuario_form import NuevoUsuarioForm
        from controllers.users import crear_usuario
        
        def guardar_usuario(datos):
            try:
                crear_usuario(
                    nombre_completo=datos['nombre_completo'],
                    email=datos['email'],
                    contraseña=datos['password'],
                    rol=datos['rol'],
                    activo=datos['activo']
                )
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                # Recargar la interfaz para mostrar el nuevo usuario
                for widget in self.winfo_children():
                    widget.destroy()
                self.crear_interfaz()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el usuario: {str(e)}")
        
        NuevoUsuarioForm(self, on_create=guardar_usuario)

if __name__ == "__main__":
    app = GestionUsuarios()
    app.mainloop()