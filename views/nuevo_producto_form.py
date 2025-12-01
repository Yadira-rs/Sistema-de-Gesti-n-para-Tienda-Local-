import customtkinter as ctk

class NuevoProductoForm(ctk.CTkToplevel):
    """
    Ventana emergente (Toplevel) para crear un nuevo producto.
    Utiliza callbacks para notificar al padre cuando se crea o cancela.
    """
    def __init__(self, parent, on_create=None):
        super().__init__(parent)
        self.title("Nuevo Producto")
        self.geometry("750x650")
        self.transient(parent) # Mantener la ventana por encima del padre
        self.grab_set() # Bloquear interacción con la ventana principal

        # Colores inspirados en el CSS
        self.configure(fg_color="#f1f1f1")
        self.FG_COLOR_BUTTON_PRIMARY = "#f3d1dc"
        self.TEXT_COLOR_BUTTON_PRIMARY = "#000000"
        self.FG_COLOR_BUTTON_SECONDARY = "#FFFFFF"
        self.TEXT_COLOR_BUTTON_SECONDARY = "#000000"

        self.on_create = on_create

        # --- Contenedor principal ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Título ---
        ctk.CTkLabel(main_frame, text="Productos / Nuevo Producto", font=("Inter", 22, "bold"), text_color="#000").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 5))
        ctk.CTkLabel(main_frame, text="Gestiona el catálogo de productos", font=("Inter", 14), text_color="#c9c3c3").grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 20))

        # --- Campos del Formulario ---
        # Fila 1
        ctk.CTkLabel(main_frame, text="Nombre del producto", font=("Inter", 12), text_color="#000").grid(row=2, column=0, columnspan=4, sticky="w", pady=(0, 5))
        self.nombre = ctk.CTkEntry(main_frame, font=("Inter", 12), border_width=1, border_color="#000", height=40, corner_radius=12)
        self.nombre.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(0, 15))

        # Fila 2
        ctk.CTkLabel(main_frame, text="Código", font=("Inter", 12), text_color="#000").grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.codigo = ctk.CTkEntry(main_frame, font=("Inter", 12), border_width=1, border_color="#000", height=40, corner_radius=12)
        self.codigo.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 15), padx=(0, 10))
        
        # Fila 3
        ctk.CTkLabel(main_frame, text="Precio", font=("Inter", 12), text_color="#000").grid(row=6, column=0, columnspan=4, sticky="w", pady=(0, 5))
        self.precio = ctk.CTkEntry(main_frame, font=("Inter", 12), border_width=1, border_color="#000", height=40, corner_radius=12)
        self.precio.grid(row=7, column=0, columnspan=4, sticky="ew", pady=(0, 15))

        # Fila 4 (Stock, Tipo, Talla, Marca)
        ctk.CTkLabel(main_frame, text="Stock Inicial", font=("Inter", 12), text_color="#000").grid(row=8, column=0, sticky="w", pady=(0, 5))
        self.stock = ctk.CTkEntry(main_frame, font=("Inter", 12), border_width=1, border_color="#000", height=40, corner_radius=12)
        self.stock.grid(row=9, column=0, sticky="ew", pady=(0, 15), padx=(0, 10))

        ctk.CTkLabel(main_frame, text="Tipo de Producto", font=("Inter", 12), text_color="#000").grid(row=8, column=1, sticky="w", pady=(0, 5))
        self.tipo = ctk.CTkEntry(main_frame, font=("Inter", 12), border_width=1, border_color="#000", height=40, corner_radius=12)
        self.tipo.grid(row=9, column=1, sticky="ew", pady=(0, 15), padx=(10, 0))

        ctk.CTkLabel(main_frame, text="Talla", font=("Inter", 12), text_color="#000").grid(row=8, column=2, sticky="w", pady=(0, 5))
        self.talla = ctk.CTkEntry(main_frame, font=("Inter", 12), border_width=1, border_color="#000", height=40, corner_radius=12)
        self.talla.grid(row=9, column=2, sticky="ew", pady=(0, 15), padx=(10, 0))

        ctk.CTkLabel(main_frame, text="Marca", font=("Inter", 12), text_color="#000").grid(row=8, column=3, sticky="w", pady=(0, 5))
        self.marca = ctk.CTkEntry(main_frame, font=("Inter", 12), border_width=1, border_color="#000", height=40, corner_radius=12)
        self.marca.grid(row=9, column=3, sticky="ew", pady=(0, 15), padx=(10, 0))

        # Fila 5
        ctk.CTkLabel(main_frame, text="URL del producto (opcional)", font=("Inter", 12), text_color="#000").grid(row=10, column=0, columnspan=4, sticky="w", pady=(0, 5))
        self.url = ctk.CTkEntry(main_frame, font=("Inter", 12), border_width=1, border_color="#000", height=40, corner_radius=12)
        self.url.grid(row=11, column=0, columnspan=4, sticky="ew", pady=(0, 25))

        # --- Botones de Acción ---
        ctk.CTkButton(main_frame, text="CREAR PRODUCTO", command=self.crear_producto, height=45, corner_radius=12, font=("Inter", 14, "bold"), fg_color=self.FG_COLOR_BUTTON_PRIMARY, text_color=self.TEXT_COLOR_BUTTON_PRIMARY).grid(row=12, column=0, columnspan=2, sticky="ew", padx=(50, 50))
        ctk.CTkButton(main_frame, text="CANCELAR", command=self.destroy, height=45, corner_radius=12, font=("Inter", 14, "bold"), fg_color=self.FG_COLOR_BUTTON_SECONDARY, text_color=self.TEXT_COLOR_BUTTON_SECONDARY, border_width=1, border_color="#000").grid(row=12, column=2, columnspan=2, sticky="ew", padx=(50, 50))

        main_frame.columnconfigure((0, 1, 2, 3), weight=1)

    def crear_producto(self):
        """
        Recopila los datos de los campos y los pasa al callback on_create.
        """
        datos = {
            "nombre": self.nombre.get(),
            "codigo": self.codigo.get(),
            "precio": self.precio.get() or "0",
            "stock": self.stock.get() or "0",
            "tipo": self.tipo.get(),
            "talla": self.talla.get(),
            "marca": self.marca.get(),
            "url": self.url.get()
        }
        if self.on_create:
            self.on_create(datos)
        # self.destroy() # Se destruye en el callback para mostrar mensajes de error/éxito