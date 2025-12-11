import customtkinter as ctk
from tkinter import messagebox
from controllers.products import agregar_producto, codigo_disponible, codigo_barras_disponible

class NuevoProductoFormMejorado(ctk.CTkToplevel):
    """
    Ventana emergente para crear un nuevo producto con código de barras.
    """
    def __init__(self, parent, on_create=None):
        super().__init__(parent)
        self.title("Nuevo Producto")
        self.geometry("600x650")
        self.transient(parent)
        self.grab_set()

        self.on_create = on_create

        # --- Panel principal ---
        main = ctk.CTkFrame(self, fg_color="white")
        main.pack(fill="both", expand=True, padx=30, pady=30)

        # Título
        ctk.CTkLabel(
            main, 
            text="Nuevo Producto", 
            font=("Segoe UI", 24, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 15))
        
        # Qué poner en cada campo
        campos_frame = ctk.CTkFrame(main, fg_color="#FFF3E0", corner_radius=8)
        campos_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        ctk.CTkLabel(
            campos_frame,
            text="📝 Qué poner en cada campo:",
            font=("Segoe UI", 11, "bold"),
            text_color="#F57C00"
        ).pack(anchor="w", padx=15, pady=(8, 2))
        
        campos_items = [
            "• Código: BLUSA001 (opcional)",
            "• Código de Barras: escanear o generar automático",
            "• Nombre: Blusa Rosa Talla M (*obligatorio)",
            "• Precio: 299.50 (*obligatorio)",
            "• Stock: 25 (*obligatorio)"
        ]
        
        for item in campos_items:
            ctk.CTkLabel(
                campos_frame,
                text=item,
                font=("Segoe UI", 9),
                text_color="#FF8F00",
                anchor="w"
            ).pack(anchor="w", padx=25, pady=1)
        
        ctk.CTkFrame(campos_frame, height=5, fg_color="transparent").pack()

        # Código
        ctk.CTkLabel(
            main, 
            text="Código (SKU)", 
            anchor="w",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(fill="x", padx=10, pady=(10, 5))
        self.codigo = ctk.CTkEntry(
            main, 
            placeholder_text="Ej: VEST-001",
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.codigo.pack(fill="x", padx=10)

        # Código de Barras
        ctk.CTkLabel(
            main, 
            text="Código de Barras (único)", 
            anchor="w",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(fill="x", padx=10, pady=(15, 5))
        
        barcode_frame = ctk.CTkFrame(main, fg_color="transparent")
        barcode_frame.pack(fill="x", padx=10)
        
        self.codigo_barras = ctk.CTkEntry(
            barcode_frame, 
            placeholder_text="Escanear o ingresar código de barras",
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.codigo_barras.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(
            barcode_frame,
            text="Auto",
            width=80,
            height=45,
            fg_color="#FF9800",
            hover_color="#F57C00",
            corner_radius=10,
            font=("Segoe UI", 11),
            command=self.generar_codigo_barras_auto
        ).pack(side="right")

        # Nombre del producto
        nombre_label_frame = ctk.CTkFrame(main, fg_color="transparent")
        nombre_label_frame.pack(fill="x", padx=10, pady=(15, 5))
        
        ctk.CTkLabel(
            nombre_label_frame, 
            text="Nombre del Producto", 
            anchor="w",
            font=("Segoe UI", 12, "bold"),
            text_color="#666666"
        ).pack(side="left")
        
        ctk.CTkLabel(
            nombre_label_frame, 
            text="*", 
            font=("Segoe UI", 12, "bold"),
            text_color="#E53935"
        ).pack(side="left", padx=(2, 0))
        self.nombre = ctk.CTkEntry(
            main, 
            placeholder_text="Ej: Vestido Floral Primavera",
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.nombre.pack(fill="x", padx=10)

        # Descripción
        ctk.CTkLabel(
            main, 
            text="Descripción", 
            anchor="w",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(fill="x", padx=10, pady=(15, 5))
        self.descripcion = ctk.CTkEntry(
            main, 
            placeholder_text="Descripción breve del producto",
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.descripcion.pack(fill="x", padx=10)



        # Precio y Stock en la misma fila
        row_frame = ctk.CTkFrame(main, fg_color="transparent")
        row_frame.pack(fill="x", padx=10, pady=(15, 0))

        # Precio
        precio_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        precio_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        precio_label_frame = ctk.CTkFrame(precio_frame, fg_color="transparent")
        precio_label_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(
            precio_label_frame, 
            text="Precio", 
            anchor="w",
            font=("Segoe UI", 12, "bold"),
            text_color="#666666"
        ).pack(side="left")
        
        ctk.CTkLabel(
            precio_label_frame, 
            text="*", 
            font=("Segoe UI", 12, "bold"),
            text_color="#E53935"
        ).pack(side="left", padx=(2, 0))
        self.precio = ctk.CTkEntry(
            precio_frame, 
            placeholder_text="0.00",
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.precio.pack(fill="x")

        # Stock
        stock_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        stock_frame.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        stock_label_frame = ctk.CTkFrame(stock_frame, fg_color="transparent")
        stock_label_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(
            stock_label_frame, 
            text="Stock Inicial", 
            anchor="w",
            font=("Segoe UI", 12, "bold"),
            text_color="#666666"
        ).pack(side="left")
        
        ctk.CTkLabel(
            stock_label_frame, 
            text="*", 
            font=("Segoe UI", 12, "bold"),
            text_color="#E53935"
        ).pack(side="left", padx=(2, 0))
        self.stock = ctk.CTkEntry(
            stock_frame, 
            placeholder_text="0",
            height=45,
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 12)
        )
        self.stock.pack(fill="x")

        # Botones
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(30, 0))

        ctk.CTkButton(
            btn_frame, 
            text="Crear Producto", 
            fg_color="#E91E63",
            hover_color="#C2185B",
            height=50,
            width=200,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            command=self.crear_producto
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame, 
            text="Cancelar", 
            fg_color="white",
            hover_color="#F0F0F0",
            text_color="#666666",
            border_width=2,
            border_color="#CCCCCC",
            height=50,
            width=200,
            corner_radius=10,
            font=("Segoe UI", 13),
            command=self.destroy
        ).pack(side="left", padx=10)

    def generar_codigo_barras_auto(self):
        """Generar código de barras automático"""
        import random
        # Generar código temporal (se generará el definitivo al guardar)
        codigo_temp = f"750{random.randint(1000000000, 9999999999)}"
        self.codigo_barras.delete(0, 'end')
        self.codigo_barras.insert(0, codigo_temp)

    def crear_producto(self):
        """Validar y crear el producto"""
        # Validar campos con mensajes específicos
        nombre = self.nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Campo obligatorio", "El nombre del producto es obligatorio.\n\nEjemplo: 'Blusa Rosa Talla M'")
            self.nombre.focus()
            return
        
        if len(nombre) < 2:
            messagebox.showwarning("Nombre muy corto", "El nombre debe tener al menos 2 caracteres.")
            self.nombre.focus()
            return

        # Validar precio
        precio_str = self.precio.get().strip()
        if not precio_str:
            messagebox.showwarning("Campo obligatorio", "El precio es obligatorio.\n\nEjemplo: 299.50")
            self.precio.focus()
            return
            
        try:
            precio = float(precio_str)
            if precio < 0:
                messagebox.showwarning("Precio inválido", "El precio no puede ser negativo.\n\nIngresa un valor como: 299.50")
                self.precio.focus()
                return
            if precio > 999999:
                messagebox.showwarning("Precio muy alto", "El precio es demasiado alto.\n\nVerifica que sea correcto.")
                self.precio.focus()
                return
        except ValueError:
            messagebox.showwarning("Precio inválido", "El precio debe ser un número válido.\n\nEjemplos correctos:\n• 299.50\n• 1500\n• 25.99")
            self.precio.focus()
            return

        # Validar stock
        stock_str = self.stock.get().strip()
        if not stock_str:
            messagebox.showwarning("Campo obligatorio", "El stock inicial es obligatorio.\n\nEjemplo: 25")
            self.stock.focus()
            return
            
        try:
            stock = int(stock_str)
            if stock < 0:
                messagebox.showwarning("Stock inválido", "El stock no puede ser negativo.\n\nIngresa un número entero como: 25")
                self.stock.focus()
                return
            if stock > 999999:
                messagebox.showwarning("Stock muy alto", "El stock es demasiado alto.\n\nVerifica que sea correcto.")
                self.stock.focus()
                return
        except ValueError:
            messagebox.showwarning("Stock inválido", "El stock debe ser un número entero.\n\nEjemplos correctos:\n• 25\n• 100\n• 0")
            self.stock.focus()
            return

        codigo = self.codigo.get().strip()
        codigo_barras = self.codigo_barras.get().strip()
        descripcion = self.descripcion.get().strip()
        id_categoria = None  # Sin categorías

        # Validar código único
        if codigo and not codigo_disponible(codigo):
            messagebox.showwarning("Código duplicado", "El código SKU ya existe")
            return

        # Validar código de barras único
        if codigo_barras and not codigo_barras_disponible(codigo_barras):
            messagebox.showwarning("Código de barras duplicado", "El código de barras ya existe")
            return

        # Crear producto
        if agregar_producto(nombre, descripcion, precio, stock, codigo, codigo_barras, id_categoria):
            messagebox.showinfo("Éxito", f"Producto '{nombre}' creado correctamente")
            
            # Notificar nuevo producto
            try:
                from utils.notificaciones import notificar_nuevo_producto
                notificar_nuevo_producto()
            except:
                pass
            
            if self.on_create:
                self.on_create()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el producto")


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    form = NuevoProductoFormMejorado(root)
    root.mainloop()
