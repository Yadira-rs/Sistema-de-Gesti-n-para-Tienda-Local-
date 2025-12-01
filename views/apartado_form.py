import customtkinter as ctk

class ApartadoForm(ctk.CTkToplevel):
    """
    Ventana emergente para seleccionar productos y cantidades para un nuevo apartado.
    """
    def __init__(self, parent, cliente, productos, on_continue=None):
        super().__init__(parent)
        self.title("Nuevo Apartado - Productos")
        self.geometry("500x500")
        self.transient(parent)
        self.grab_set()

        ctk.set_appearance_mode("light")
        # Usando un tema válido para evitar errores.
        ctk.set_default_color_theme("blue")

        self.on_continue = on_continue
        self.apartado_items = []
        self.productos_disponibles = productos

        ctk.CTkLabel(self, text=f"Cliente: {cliente.get('nombre', 'N/A')}", font=("Segoe UI", 16, "bold")).pack(pady=(20, 10))

        # --- Selección de Producto ---
        self.producto_var = ctk.StringVar()
        self.cantidad_var = ctk.StringVar(value="1")

        ctk.CTkLabel(self, text="Selecciona un producto").pack(pady=(10, 0))
        self.producto_menu = ctk.CTkOptionMenu(self, variable=self.producto_var,
                                               values=[p["nombre"] for p in self.productos_disponibles])
        self.producto_menu.pack(pady=5)

        ctk.CTkLabel(self, text="Cantidad").pack(pady=(10, 0))
        self.cantidad_entry = ctk.CTkEntry(self, textvariable=self.cantidad_var)
        self.cantidad_entry.pack(pady=5)

        ctk.CTkButton(self, text="Agregar Producto", command=self.agregar_producto).pack(pady=10)

        # --- Lista de productos agregados ---
        self.lista_textbox = ctk.CTkTextbox(self, height=150, state="disabled")
        self.lista_textbox.pack(fill="x", padx=20, pady=10)

        # --- Botones de Acción ---
        ctk.CTkButton(self, text="Atrás", fg_color="gray", command=self.destroy).pack(side="left", padx=40, pady=10)
        ctk.CTkButton(self, text="Continuar", command=self.continuar).pack(side="right", padx=40, pady=10)

    def agregar_producto(self):
        """Agrega el producto seleccionado a la lista del apartado."""
        nombre = self.producto_var.get()
        cantidad = self.cantidad_var.get()
        if nombre and cantidad.isdigit() and int(cantidad) > 0:
            self.apartado_items.append({"nombre": nombre, "cantidad": int(cantidad)})
            
            # Actualiza el cuadro de texto
            self.lista_textbox.configure(state="normal")
            self.lista_textbox.insert("end", f"- {nombre} (x{cantidad})\n")
            self.lista_textbox.configure(state="disabled")

    def continuar(self):
        """Cierra la ventana y pasa la lista de productos al callback."""
        if self.on_continue:
            self.on_continue(self.apartado_items)
        self.destroy()