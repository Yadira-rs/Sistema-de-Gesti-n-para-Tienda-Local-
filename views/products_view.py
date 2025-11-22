import tkinter as tk
from tkinter import ttk, messagebox
from controllers.products import agregar_producto, obtener_productos


class ProductsView(ttk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user

        ttk.Label(self, text="📦 Módulo de Productos",
                  font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.crear_formulario()
        self.crear_tabla()
        self.cargar_productos()

    def crear_formulario(self):
        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Nombre:").grid(row=0, column=0, pady=5)
        self.nombre = ttk.Entry(form, width=35)
        self.nombre.grid(row=0, column=1)

        ttk.Label(form, text="Descripción:").grid(row=1, column=0, pady=5)
        self.descripcion = ttk.Entry(form, width=35)
        self.descripcion.grid(row=1, column=1)

        ttk.Label(form, text="Precio:").grid(row=2, column=0, pady=5)
        self.precio = ttk.Entry(form, width=35)
        self.precio.grid(row=2, column=1)

        ttk.Label(form, text="Stock:").grid(row=3, column=0, pady=5)
        self.stock = ttk.Entry(form, width=35)
        self.stock.grid(row=3, column=1)

        ttk.Button(form, text="💾 Guardar Producto",
                   command=self.guardar_producto).grid(row=4, columnspan=2, pady=10)

    def crear_tabla(self):
        columnas = ("ID", "Nombre", "Descripción", "Precio", "Stock")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=12)
        self.tabla.pack(fill="both", expand=True, padx=8)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

    def guardar_producto(self):
        try:
            nombre = self.nombre.get().strip()
            descripcion = self.descripcion.get().strip()
            precio = float(self.precio.get().strip())
            stock = int(self.stock.get().strip())

            if not nombre:
                messagebox.showwarning("Error", "El nombre es obligatorio.")
                return

            if agregar_producto(nombre, descripcion, precio, stock):
                messagebox.showinfo("Éxito", "Producto guardado correctamente 🎉")
                self.limpiar_campos()
                self.cargar_productos()
            else:
                messagebox.showerror("Error", "No se pudo guardar el producto.")

        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser numéricos.")

    def limpiar_campos(self):
        self.nombre.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.stock.delete(0, tk.END)

    def cargar_productos(self):
        self.tabla.delete(*self.tabla.get_children())
        productos = obtener_productos()

        for p in productos:
            self.tabla.insert("", tk.END, values=(
                p["id_producto"],
                p["nombre"],
                p["descripcion"],
                p["precio"],
                p["stock"]
            ))
