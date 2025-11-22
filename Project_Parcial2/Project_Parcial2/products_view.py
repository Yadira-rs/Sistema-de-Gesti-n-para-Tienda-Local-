import tkinter as tk
from tkinter import messagebox, ttk
from products_controller import ver_productos, agregar_producto, actualizar_producto, eliminar_producto

class ProductsApp:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Bienvenido {username}")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.crear_elementos()
        self.ver_productos()
        self.root.mainloop()

    def crear_elementos(self):
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        tk.Label(frame_botones, text=f"¡Hola {self.username}!", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Button(frame_botones, text="Agregar producto", command=self.agregar_producto, width=20).pack(pady=5)
        tk.Button(frame_botones, text="Actualizar producto", command=self.actualizar_producto, width=20).pack(pady=5)
        tk.Button(frame_botones, text="Eliminar producto", command=self.eliminar_producto, width=20).pack(pady=5)
        tk.Button(frame_botones, text="Cerrar sesión", command=self.cerrar_sesion, width=20).pack(pady=10)

        tk.Label(self.root, text="Lista de productos", font=("Arial", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Marca", "Precio", "Stock"), show="headings", height=10)
        for col in ("ID", "Nombre", "Marca", "Precio", "Stock"):
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    def ver_productos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        productos = ver_productos()
        for p in productos:
            self.tree.insert("", tk.END, values=p)

    def agregar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Producto")
        ventana.geometry("300x300")

        campos = ["Nombre", "Marca", "Precio", "Stock"]
        entradas = {}

        for campo in campos:
            tk.Label(ventana, text=campo).pack(pady=5)
            entrada = tk.Entry(ventana)
            entrada.pack(pady=5)
            entradas[campo] = entrada

        def guardar():
            nombre = entradas["Nombre"].get().strip()
            marca = entradas["Marca"].get().strip()
            try:
                precio = float(entradas["Precio"].get().strip())
                stock = int(entradas["Stock"].get().strip())
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser número decimal y stock entero")
                return

            if agregar_producto(nombre, marca, precio, stock):
                messagebox.showinfo("Éxito", "Producto agregado correctamente")
                self.ver_productos()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto")

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

    def actualizar_producto(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Selecciona un producto")
            return

        valores = self.tree.item(seleccion, "values")
        id_producto = valores[0]

        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar Producto")
        ventana.geometry("300x300")

        campos = ["Nombre", "Marca", "Precio", "Stock"]
        entradas = {}

        for i, campo in enumerate(campos, start=1):
            tk.Label(ventana, text=campo).pack(pady=5)
            entrada = tk.Entry(ventana)
            entrada.insert(0, valores[i])
            entrada.pack(pady=5)
            entradas[campo] = entrada

        def guardar():
            nombre = entradas["Nombre"].get().strip()
            marca = entradas["Marca"].get().strip()
            try:
                precio = float(entradas["Precio"].get().strip())
                stock = int(entradas["Stock"].get().strip())
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser número decimal y stock entero")
                return

            if actualizar_producto(id_producto, nombre, marca, precio, stock):
                messagebox.showinfo("Actualizado", "Producto actualizado correctamente")
                self.ver_productos()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto")

        tk.Button(ventana, text="Actualizar", command=guardar).pack(pady=10)

    def eliminar_producto(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Selecciona un producto")
            return

        valores = self.tree.item(seleccion, "values")
        id_producto = valores[0]

        confirmacion = messagebox.askyesno("¿Eliminar?", "¿Estás segura de eliminar este producto?")
        if confirmacion:
            if eliminar_producto(id_producto):
                messagebox.showinfo("Eliminado", "Producto eliminado correctamente")
                self.ver_productos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")

    def cerrar_sesion(self):
        self.root.destroy()

if __name__ == "__main__":
    ProductsApp("admin")