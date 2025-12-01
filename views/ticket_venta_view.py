import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

class TicketVentaView(ctk.CTkToplevel):
    """
    Ventana de ticket de venta
    """
    def __init__(self, parent, venta_data):
        super().__init__(parent)
        self.title("Ticket de Venta")
        self.geometry("400x700")
        self.transient(parent)
        self.grab_set()
        
        self.venta_data = venta_data
        
        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"400x700+{x}+{y}")
        
        self.crear_ticket()
    
    def crear_ticket(self):
        """Crear el diseño del ticket"""
        # Contenedor principal
        main = ctk.CTkFrame(self, fg_color="white")
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Scroll frame para el contenido
        scroll = ctk.CTkScrollableFrame(main, fg_color="white")
        scroll.pack(fill="both", expand=True)
        
        # Logo y nombre del negocio
        ctk.CTkLabel(
            scroll,
            text="🚲",
            font=("Segoe UI", 40),
            text_color="#E91E63"
        ).pack(pady=(10, 5))
        
        # Nombre del negocio
        title_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        title_frame.pack()
        
        ctk.CTkLabel(
            title_frame,
            text="Janet ",
            font=("Brush Script MT", 24),
            text_color="#333333"
        ).pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Rosa ",
            font=("Brush Script MT", 24),
            text_color="#E91E63"
        ).pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Bici",
            font=("Brush Script MT", 24),
            text_color="#333333"
        ).pack(side="left")
        
        ctk.CTkLabel(
            scroll,
            text="Sistema de Ventas",
            font=("Segoe UI", 10),
            text_color="#666666"
        ).pack(pady=(0, 10))
        
        # Línea separadora
        ctk.CTkFrame(scroll, height=2, fg_color="#E0E0E0").pack(fill="x", padx=20, pady=10)
        
        # Información del ticket
        info_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # Número de ticket
        ticket_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        ticket_row.pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            ticket_row,
            text="Ticket:",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(side="left")
        
        ctk.CTkLabel(
            ticket_row,
            text=f"#{self.venta_data.get('id_venta', 'N/A')}",
            font=("Segoe UI", 11, "bold"),
            text_color="#333333"
        ).pack(side="right")
        
        # Fecha y hora
        fecha_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        fecha_row.pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            fecha_row,
            text="Fecha:",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(side="left")
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        ctk.CTkLabel(
            fecha_row,
            text=fecha_actual,
            font=("Segoe UI", 11),
            text_color="#333333"
        ).pack(side="right")
        
        # Método de pago
        metodo_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        metodo_row.pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            metodo_row,
            text="Método de pago:",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(side="left")
        
        ctk.CTkLabel(
            metodo_row,
            text=self.venta_data.get('metodo', 'Efectivo'),
            font=("Segoe UI", 11),
            text_color="#333333"
        ).pack(side="right")
        
        # Línea separadora
        ctk.CTkFrame(scroll, height=2, fg_color="#E0E0E0").pack(fill="x", padx=20, pady=15)
        
        # Productos
        ctk.CTkLabel(
            scroll,
            text="PRODUCTOS",
            font=("Segoe UI", 12, "bold"),
            text_color="#333333"
        ).pack(anchor="w", padx=20, pady=(0, 10))
        
        # Lista de productos
        productos_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        productos_frame.pack(fill="x", padx=20)
        
        for item in self.venta_data.get('items', []):
            self.crear_item_producto(productos_frame, item)
        
        # Línea separadora
        ctk.CTkFrame(scroll, height=2, fg_color="#E0E0E0").pack(fill="x", padx=20, pady=15)
        
        # Totales
        totales_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        totales_frame.pack(fill="x", padx=20)
        
        # Subtotal
        subtotal = sum(item['precio'] * item['cantidad'] for item in self.venta_data.get('items', []))
        
        subtotal_row = ctk.CTkFrame(totales_frame, fg_color="transparent")
        subtotal_row.pack(fill="x", pady=3)
        
        ctk.CTkLabel(
            subtotal_row,
            text="Subtotal:",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(side="left")
        
        ctk.CTkLabel(
            subtotal_row,
            text=f"${subtotal:.2f}",
            font=("Segoe UI", 11),
            text_color="#333333"
        ).pack(side="right")
        
        # Descuento (si aplica)
        descuento = self.venta_data.get('descuento', 0)
        if descuento > 0:
            descuento_row = ctk.CTkFrame(totales_frame, fg_color="transparent")
            descuento_row.pack(fill="x", pady=3)
            
            ctk.CTkLabel(
                descuento_row,
                text="Descuento:",
                font=("Segoe UI", 11),
                text_color="#FF9800"
            ).pack(side="left")
            
            ctk.CTkLabel(
                descuento_row,
                text=f"- ${descuento:.2f}",
                font=("Segoe UI", 11, "bold"),
                text_color="#FF9800"
            ).pack(side="right")
        
        # Total
        total_row = ctk.CTkFrame(totales_frame, fg_color="#FFF0F5", corner_radius=8)
        total_row.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(
            total_row,
            text="TOTAL:",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(side="left", padx=15, pady=12)
        
        ctk.CTkLabel(
            total_row,
            text=f"${self.venta_data.get('total', 0):.2f}",
            font=("Segoe UI", 18, "bold"),
            text_color="#E91E63"
        ).pack(side="right", padx=15, pady=12)
        
        # Mensaje de agradecimiento
        ctk.CTkLabel(
            scroll,
            text="¡Gracias por su compra!",
            font=("Segoe UI", 12, "bold"),
            text_color="#333333"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            scroll,
            text="Vuelva pronto",
            font=("Segoe UI", 10),
            text_color="#666666"
        ).pack(pady=(0, 20))
        
        # Botones
        buttons_frame = ctk.CTkFrame(main, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkButton(
            buttons_frame,
            text="🖨 Imprimir",
            fg_color="#2196F3",
            hover_color="#1976D2",
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=self.imprimir_ticket
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            buttons_frame,
            text="Cerrar",
            fg_color="#E91E63",
            hover_color="#C2185B",
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=self.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))
    
    def crear_item_producto(self, parent, item):
        """Crear fila de producto en el ticket"""
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", pady=3)
        
        # Nombre y cantidad
        nombre_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        nombre_frame.pack(fill="x")
        
        nombre = item.get('nombre', 'Producto')
        cantidad = item.get('cantidad', 1)
        
        ctk.CTkLabel(
            nombre_frame,
            text=f"{cantidad}x {nombre}",
            font=("Segoe UI", 11),
            text_color="#333333",
            anchor="w"
        ).pack(side="left")
        
        # Precio
        precio_unitario = item.get('precio', 0)
        subtotal = precio_unitario * cantidad
        
        precio_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        precio_frame.pack(fill="x")
        
        ctk.CTkLabel(
            precio_frame,
            text=f"${precio_unitario:.2f} c/u",
            font=("Segoe UI", 9),
            text_color="#999999"
        ).pack(side="left", padx=(20, 0))
        
        ctk.CTkLabel(
            precio_frame,
            text=f"${subtotal:.2f}",
            font=("Segoe UI", 11, "bold"),
            text_color="#333333"
        ).pack(side="right")
    
    def imprimir_ticket(self):
        """Imprimir o guardar el ticket"""
        try:
            # Generar archivo de texto del ticket
            filename = f"ticket_{self.venta_data.get('id_venta', 'temp')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 40 + "\n")
                f.write("        JANET ROSA BICI\n")
                f.write("      Sistema de Ventas\n")
                f.write("=" * 40 + "\n\n")
                
                f.write(f"Ticket: #{self.venta_data.get('id_venta', 'N/A')}\n")
                f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f"Método: {self.venta_data.get('metodo', 'Efectivo')}\n")
                f.write("-" * 40 + "\n\n")
                
                f.write("PRODUCTOS:\n")
                f.write("-" * 40 + "\n")
                
                for item in self.venta_data.get('items', []):
                    nombre = item.get('nombre', 'Producto')
                    cantidad = item.get('cantidad', 1)
                    precio = item.get('precio', 0)
                    subtotal = precio * cantidad
                    
                    f.write(f"{cantidad}x {nombre}\n")
                    f.write(f"   ${precio:.2f} c/u = ${subtotal:.2f}\n")
                
                f.write("-" * 40 + "\n")
                
                subtotal_total = sum(item['precio'] * item['cantidad'] for item in self.venta_data.get('items', []))
                f.write(f"Subtotal: ${subtotal_total:.2f}\n")
                
                descuento = self.venta_data.get('descuento', 0)
                if descuento > 0:
                    f.write(f"Descuento: -${descuento:.2f}\n")
                
                f.write(f"\nTOTAL: ${self.venta_data.get('total', 0):.2f}\n")
                f.write("=" * 40 + "\n")
                f.write("\n   ¡Gracias por su compra!\n")
                f.write("        Vuelva pronto\n")
                f.write("=" * 40 + "\n")
            
            messagebox.showinfo("Ticket guardado", f"Ticket guardado en:\n{filename}\n\nPuedes imprimirlo desde tu editor de texto.")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el ticket: {str(e)}")


if __name__ == "__main__":
    # Datos de prueba
    venta_test = {
        'id_venta': 123,
        'total': 580.00,
        'metodo': 'Efectivo',
        'descuento': 20.00,
        'items': [
            {'nombre': 'Blusa Rosa', 'cantidad': 2, 'precio': 199.00},
            {'nombre': 'Pantalón Negro', 'cantidad': 1, 'precio': 299.00}
        ]
    }
    
    root = ctk.CTk()
    root.withdraw()
    ticket = TicketVentaView(root, venta_test)
    root.mainloop()
