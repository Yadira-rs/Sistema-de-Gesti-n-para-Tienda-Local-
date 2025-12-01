import customtkinter as ctk
from tkinter import messagebox
from controllers.clientes_controller import obtener_clientes

class NuevoCredito(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Janet Rosa Bici - Nuevo Crédito")
        self.geometry("800x500")
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

        ctk.CTkLabel(panel, text="Nuevo Crédito", font=("Arial", 20, "bold")).pack(pady=(0, 10))
        ctk.CTkLabel(panel, text="Registra una nueva venta a crédito", font=("Arial", 14)).pack(pady=(0, 20))

        # Campos del formulario
        clientes = obtener_clientes()
        nombres_clientes = [cliente[1] for cliente in clientes] if clientes else ["No hay clientes"]
        
        self.cliente = ctk.CTkComboBox(panel, values=nombres_clientes, width=300)
        self.cliente.set("Seleccionar un cliente")
        self.monto = ctk.CTkEntry(panel, placeholder_text="Monto Total", width=300)
        self.dias = ctk.CTkEntry(panel, placeholder_text="Días de Crédito", width=300)
        self.notas = ctk.CTkTextbox(panel, width=300, height=80)

        for widget in [self.cliente, self.monto, self.dias, self.notas]:
            widget.pack(pady=10)

        # Advertencia
        advertencia = ctk.CTkLabel(
            panel,
            text="⚠️ Para créditos con productos específicos, usa el Punto de Venta y selecciona 'Venta de Crédito'",
            text_color="yellow",
            wraplength=400,
            font=("Arial", 12)
        )
        advertencia.pack(pady=10)

        # Botón
        ctk.CTkButton(panel, text="Crear Crédito", fg_color="red", hover_color="darkred", command=self.crear_credito).pack(pady=20)

    def crear_credito(self):
        cliente = self.cliente.get()
        monto = self.monto.get()
        dias = self.dias.get()

        if cliente == "Seleccionar un cliente" or not monto or not dias:
            messagebox.showerror("Error", "Por favor completa los campos obligatorios.")
            return

        messagebox.showinfo("Crédito creado", f"Crédito registrado para {cliente} por ${monto}")

if __name__ == "__main__":
    app = NuevoCredito()
    app.mainloop()