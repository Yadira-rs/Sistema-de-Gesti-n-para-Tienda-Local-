import customtkinter as ctk
from tkinter import simpledialog, messagebox
from controllers.products import obtener_productos, ajustar_stock, productos_count, stock_total_sum

class InventarioView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user
        self.pack(fill="both", expand=True)

        # Título
        ctk.CTkLabel(self, text="Gestión de Inventario", font=("Segoe UI", 20, "bold")).pack(pady=10, padx=20, anchor="w")

        # Frame para las tarjetas de resumen
        self.resumen_frame = ctk.CTkFrame(self)
        self.resumen_frame.pack(fill="x", padx=20, pady=10)

        # Filtros
        filtros_frame = ctk.CTkFrame(self)
        filtros_frame.pack(fill="x", padx=20, pady=5)
        self.search_entry = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar producto por nombre...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.filtrar_productos)

        # Tabla
        self.tabla_frame = ctk.CTkScrollableFrame(self)
        self.tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_inventario()

    def cargar_inventario(self, filtro=None):
        """Carga o recarga los datos del inventario en la UI."""
        # Limpiar widgets anteriores
        for widget in self.resumen_frame.winfo_children():
            widget.destroy()
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        productos = obtener_productos()

        if filtro:
            productos = [p for p in productos if filtro.lower() in p.get("nombre", "").lower()]

        # --- Calcular y mostrar resumen ---
        total_productos = len(productos)
        stock_total = sum(p.get("stock", 0) for p in productos)
        stock_bajo = sum(1 for p in productos if p.get("stock", 0) < 10)
        valor_total = sum(p.get("precio", 0) * p.get("stock", 0) for p in productos)

        resumen_data = [
            f"Total Productos: {total_productos}",
            f"Stock Total: {stock_total} unidades",
            f"Stock Bajo: {stock_bajo} productos",
            f"Valor Total: ${valor_total:.2f}"
        ]
        for i, txt in enumerate(resumen_data):
            ctk.CTkLabel(self.resumen_frame, text=txt, font=("Segoe UI", 14)).grid(row=0, column=i, padx=10, pady=5, sticky="w")

        # --- Llenar tabla ---
        headers = ["Código", "Producto", "Precio", "Stock Actual", "Valor Total", "Acción"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.tabla_frame, text=h, font=("Segoe UI", 12, "bold")).grid(row=0, column=i, padx=5, pady=5, sticky="w")

        for p in productos:
            r = productos.index(p) + 1
            fila = [
                p.get("codigo", "-"),
                p.get("nombre", "-"),
                f"${p.get('precio', 0):.2f}",
                f"{p.get('stock', 0)} unidades",
                f"${p.get('precio', 0) * p.get('stock', 0):.2f}"
            ]
            for c, val in enumerate(fila):
                ctk.CTkLabel(self.tabla_frame, text=val).grid(row=r, column=c, padx=5, pady=5, sticky="w")

            ctk.CTkButton(self.tabla_frame, text="Ajustar", width=80, command=lambda prod=p: self.ajustar_producto(prod)).grid(row=r, column=len(fila), padx=5)

    def filtrar_productos(self, event=None):
        """Filtra los productos en la tabla según el texto de búsqueda."""
        filtro = self.search_entry.get()
        self.cargar_inventario(filtro)

    def ajustar_producto(self, producto):
        """Abre diálogos para ajustar el stock de un producto."""
        cantidad = simpledialog.askinteger("Ajustar Stock", f"Cantidad para {producto['nombre']}:", parent=self, minvalue=0)
        if not cantidad:
            return
        
        tipo = simpledialog.askstring("Tipo de Ajuste", "Tipo (Entrada / Salida):", parent=self)
        if tipo and tipo.lower() in ["entrada", "salida"]:
            if ajustar_stock(producto['id_producto'], cantidad, tipo.capitalize()):
                messagebox.showinfo("Éxito", "Stock ajustado correctamente.")
                self.cargar_inventario(self.search_entry.get())
            else:
                messagebox.showerror("Error", "No se pudo ajustar el stock.")
        else:
            messagebox.showwarning("Tipo inválido", "El tipo de ajuste debe ser 'Entrada' o 'Salida'.")