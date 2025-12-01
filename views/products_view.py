import customtkinter as ctk
from tkinter import messagebox
from controllers.products import obtener_productos, agregar_producto
from views.nuevo_producto_form import NuevoProductoForm

class ProductsView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="transparent")
        self.user = user
        self.pack(fill="both", expand=True)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(header, text="Productos", font=("Segoe UI", 18, "bold")).pack(side="left")
        ctk.CTkButton(header, text="Nuevo Producto", command=self.abrir_formulario_nuevo).pack(side="right")

        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_tabla_productos()

    def cargar_tabla_productos(self):
        """Carga o recarga los productos en la tabla."""
        # Limpiar el frame de la tabla antes de volver a dibujar
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        productos = obtener_productos()

        columns = ("nombre", "codigo", "tipo", "precio", "stock")

        # Encabezados
        for i, col in enumerate(columns):
            ctk.CTkLabel(self.tabla_frame, text=col.upper(), font=("Segoe UI", 12, "bold")).grid(row=0, column=i, padx=10, pady=5, sticky="w")

        # Filas de datos
        for r, p in enumerate(productos, start=1):
            # Asegurarse de que las claves existan o usar un valor por defecto
            fila = [
                p.get("nombre", "-"),
                p.get("codigo", "-"),
                p.get("tipo", "-"),
                f"${float(p.get('precio', 0)):.2f}",
                str(p.get("stock", 0))
            ]
            for c, val in enumerate(fila):
                ctk.CTkLabel(self.tabla_frame, text=val).grid(row=r, column=c, padx=10, pady=5, sticky="w")

    def abrir_formulario_nuevo(self):
        """Abre la ventana para crear un nuevo producto."""
        def handle_creacion(datos):
            try:
                # Llama al controlador para agregar el producto a la BD
                agregar_producto(
                    nombre=datos["nombre"],
                    descripcion=f'{datos["tipo"]} {datos["talla"]}', # Combinamos tipo y talla como descripción
                    precio=float(datos["precio"]),
                    stock=int(datos["stock"]),
                    codigo=datos["codigo"] or None
                )
                messagebox.showinfo("Éxito", "Producto creado correctamente.")
                self.cargar_tabla_productos() # Recargar la tabla
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el producto:\n{e}")

        # Crea y muestra la ventana del formulario, pasando la función de callback
        form_window = NuevoProductoForm(self, on_create=handle_creacion)
