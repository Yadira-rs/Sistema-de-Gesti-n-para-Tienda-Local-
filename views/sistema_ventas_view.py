import customtkinter as ctk
from tkinter import messagebox
from controllers.products import obtener_productos

class SistemaVentas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Janet Rosa Bici - Sistema de ventas")
        self.geometry("1000x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue") # "pink" no es un tema por defecto

        self.carrito = []
        self.metodo_pago = ctk.StringVar(value="Efectivo")

        self.crear_interfaz()

    def crear_interfaz(self):
        # Menú lateral
        menu = ctk.CTkFrame(self, width=200)
        menu.pack(side="left", fill="y")

        ctk.CTkLabel(menu, text="Janet Rosa Bici", font=("Arial", 18, "bold")).pack(pady=(20, 0))
        ctk.CTkLabel(menu, text="Sistema de ventas", font=("Arial", 14)).pack(pady=(0, 20))

        for opcion in ["Dashboard", "Punto de Venta", "Apartado", "Productos", "Inventario", "Ventas", "Usuarios"]:
            ctk.CTkButton(menu, text=opcion, width=180).pack(pady=5)

        ctk.CTkLabel(menu, text="").pack(pady=10)
        ctk.CTkLabel(menu, text="Administrador", font=("Arial", 14, "bold")).pack(pady=(20, 0))
        ctk.CTkLabel(menu, text="admin@janet.com", font=("Arial", 12)).pack()

        # Panel principal
        panel = ctk.CTkFrame(self)
        panel.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        # Filtro de categoría
        ctk.CTkLabel(panel, text="Todas las Categorías", font=("Arial", 16)).pack(pady=5)

        # Catálogo de productos
        catalogo = ctk.CTkScrollableFrame(panel)
        catalogo.pack(side="left", expand=True, fill="both", padx=10)

        productos = obtener_productos() # Carga de productos desde la base de datos

        for producto in productos:
            frame = ctk.CTkFrame(catalogo)
            frame.pack(fill="x", pady=5)

            nombre = producto.get("nombre", "N/A")
            precio = float(producto.get("precio", 0.0))
            stock = int(producto.get("stock", 0))

            ctk.CTkLabel(frame, text=f"{nombre} - ${precio:.2f} (Stock: {stock})", anchor="w").pack(side="left", padx=10)
            ctk.CTkButton(frame, text="Agregar", command=lambda p=producto: self.agregar_al_carrito(p)).pack(side="right", padx=10)

        # Carrito de compras
        carrito_frame = ctk.CTkFrame(panel, width=250)
        carrito_frame.pack(side="right", fill="y", padx=10)

        ctk.CTkLabel(carrito_frame, text="Carrito de Compras", font=("Arial", 16)).pack(pady=10)
        self.carrito_lista = ctk.CTkLabel(carrito_frame, text="(Vacío)")
        self.carrito_lista.pack()

        # Métodos de pago
        ctk.CTkLabel(carrito_frame, text="Método de pago:", font=("Arial", 14)).pack(pady=(20, 5))
        for metodo in ["Efectivo", "Tarjeta", "Transferencia"]:
            ctk.CTkRadioButton(carrito_frame, text=metodo, variable=self.metodo_pago, value=metodo).pack(anchor="w", padx=20)

        # Total y botón
        self.total_label = ctk.CTkLabel(carrito_frame, text="Total: $0.00", font=("Arial", 16, "bold"))
        self.total_label.pack(pady=10)

        ctk.CTkButton(carrito_frame, text="Procesar Venta", command=self.procesar_venta).pack(pady=10)

    def agregar_al_carrito(self, producto):
        self.carrito.append(producto)
        self.actualizar_carrito()

    def actualizar_carrito(self):
        texto = ""
        total = 0
        for p in self.carrito:
            texto += f"{p.get('nombre', 'N/A')} - ${float(p.get('precio', 0.0)):.2f}\n"
            total += float(p.get("precio", 0.0))
        self.carrito_lista.configure(text=texto)
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def procesar_venta(self):
        metodo = self.metodo_pago.get()
        total = sum(float(p.get("precio", 0.0)) for p in self.carrito)
        messagebox.showinfo("Venta procesada", f"Venta de ${total:.2f} con {metodo}")

if __name__ == "__main__":
    app = SistemaVentas()
    app.mainloop()