import customtkinter as ctk
from tkinter import messagebox

class PantallaCobro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cobrar venta - Janet Rosa Bici")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue") # "pink" no es un tema por defecto

        self.carrito = [
            {"nombre": "The Ordinary Peeling Solution", "precio": 280.0, "stock": 12}
        ]
        self.metodo_pago = ctk.StringVar(value="Efectivo")

        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        titulo = ctk.CTkLabel(self, text="Resumen del carrito", font=("Arial", 20))
        titulo.pack(pady=10)

        # Lista de productos
        for producto in self.carrito:
            item = ctk.CTkLabel(self, text=f"{producto['nombre']} - ${producto['precio']} (Stock: {producto['stock']})")
            item.pack(pady=2)

        # Total
        total = sum(p["precio"] for p in self.carrito)
        self.total_label = ctk.CTkLabel(self, text=f"Total: ${total:.2f}", font=("Arial", 18, "bold"))
        self.total_label.pack(pady=10)

        # Métodos de pago
        metodo_label = ctk.CTkLabel(self, text="Método de pago:")
        metodo_label.pack(pady=(20, 5))

        opciones = ["Efectivo", "Tarjeta", "Transferencia"]
        for opcion in opciones:
            radio = ctk.CTkRadioButton(self, text=opcion, variable=self.metodo_pago, value=opcion)
            radio.pack(anchor="w", padx=100)

        # Botón procesar
        boton = ctk.CTkButton(self, text="Procesar Venta", command=self.procesar_venta)
        boton.pack(pady=30)

    def procesar_venta(self):
        metodo = self.metodo_pago.get()
        messagebox.showinfo("Venta procesada", f"Venta realizada con {metodo}")

if __name__ == "__main__":
    app = PantallaCobro()
    app.mainloop()