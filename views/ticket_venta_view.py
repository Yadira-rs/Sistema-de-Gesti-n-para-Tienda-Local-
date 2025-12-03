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
        """Mostrar opciones de impresión"""
        # Crear ventana de opciones de impresión
        print_dialog = ctk.CTkToplevel(self)
        print_dialog.title("Opciones de Impresión")
        print_dialog.geometry("500x400")
        print_dialog.transient(self)
        print_dialog.grab_set()
        
        # Centrar ventana
        print_dialog.update_idletasks()
        x = (print_dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (print_dialog.winfo_screenheight() // 2) - (400 // 2)
        print_dialog.geometry(f"500x400+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(print_dialog, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="🖨️ Opciones de Impresión",
            font=("Segoe UI", 18, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 20))
        
        # Detectar impresoras
        impresoras = self.detectar_impresoras()
        
        if impresoras:
            ctk.CTkLabel(
                main_frame,
                text="Impresoras disponibles:",
                font=("Segoe UI", 12, "bold"),
                text_color="#666666",
                anchor="w"
            ).pack(anchor="w", pady=(0, 10))
            
            # Lista de impresoras
            impresoras_frame = ctk.CTkScrollableFrame(main_frame, height=150)
            impresoras_frame.pack(fill="x", pady=(0, 15))
            
            self.impresora_seleccionada = ctk.StringVar(value=impresoras[0] if impresoras else "")
            
            for impresora in impresoras:
                radio = ctk.CTkRadioButton(
                    impresoras_frame,
                    text=impresora,
                    variable=self.impresora_seleccionada,
                    value=impresora,
                    font=("Segoe UI", 11)
                )
                radio.pack(anchor="w", pady=5, padx=10)
            
            # Botón imprimir
            ctk.CTkButton(
                main_frame,
                text="🖨️ Imprimir en impresora seleccionada",
                fg_color="#4CAF50",
                hover_color="#45a049",
                height=45,
                font=("Segoe UI", 12, "bold"),
                command=lambda: self.imprimir_en_impresora(print_dialog)
            ).pack(fill="x", pady=(0, 10))
        else:
            ctk.CTkLabel(
                main_frame,
                text="⚠️ No se detectaron impresoras",
                font=("Segoe UI", 12),
                text_color="#FF9800"
            ).pack(pady=20)
        
        # Botón imprimir con navegador (HTML)
        ctk.CTkButton(
            main_frame,
            text="🌐 Abrir en navegador e imprimir",
            fg_color="#FF9800",
            hover_color="#F57C00",
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=lambda: self.imprimir_con_navegador(print_dialog)
        ).pack(fill="x", pady=(0, 10))
        
        # Botón guardar como PDF
        ctk.CTkButton(
            main_frame,
            text="📄 Guardar como PDF",
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=lambda: self.guardar_como_pdf(print_dialog)
        ).pack(fill="x", pady=(0, 10))
        
        # Botón guardar como archivo
        ctk.CTkButton(
            main_frame,
            text="💾 Guardar como archivo de texto",
            fg_color="#2196F3",
            hover_color="#1976D2",
            height=45,
            font=("Segoe UI", 12, "bold"),
            command=lambda: self.guardar_ticket_archivo(print_dialog)
        ).pack(fill="x", pady=(0, 10))
        
        # Botón cancelar
        ctk.CTkButton(
            main_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=40,
            font=("Segoe UI", 11),
            command=print_dialog.destroy
        ).pack(fill="x")
    
    def detectar_impresoras(self):
        """Detectar impresoras disponibles en el sistema"""
        try:
            import win32print
            impresoras = []
            
            # Obtener todas las impresoras
            for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS):
                impresoras.append(printer[2])
            
            return impresoras
        except ImportError:
            # Si no está instalado win32print, intentar con subprocess
            try:
                import subprocess
                result = subprocess.run(['wmic', 'printer', 'get', 'name'], 
                                      capture_output=True, text=True, shell=True)
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    impresoras = [line.strip() for line in lines[1:] if line.strip()]
                    return impresoras
            except:
                pass
            
            return []
        except Exception as e:
            print(f"Error al detectar impresoras: {e}")
            return []
    
    def imprimir_en_impresora(self, dialog):
        """Imprimir ticket en la impresora seleccionada"""
        try:
            impresora = self.impresora_seleccionada.get()
            
            if not impresora:
                messagebox.showwarning("Impresora no seleccionada", "Por favor selecciona una impresora")
                return
            
            # Generar HTML del ticket
            html_content = self.generar_ticket_html()
            
            # Guardar temporalmente
            import tempfile
            import os
            import webbrowser
            
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8')
            temp_file.write(html_content)
            temp_file.close()
            
            # Abrir en navegador para imprimir
            webbrowser.open('file://' + temp_file.name)
            
            messagebox.showinfo(
                "Impresión", 
                f"Se abrió el ticket en tu navegador.\n\n"
                f"Presiona Ctrl+P para imprimir en:\n{impresora}\n\n"
                f"O usa el menú Archivo > Imprimir"
            )
            dialog.destroy()
            
            # Limpiar archivo temporal después de un tiempo
            self.after(30000, lambda: os.unlink(temp_file.name) if os.path.exists(temp_file.name) else None)
            
        except Exception as e:
            messagebox.showerror("Error de impresión", f"No se pudo imprimir el ticket:\n{str(e)}")
    
    def guardar_ticket_archivo(self, dialog):
        """Guardar ticket como archivo de texto"""
        try:
            filename = f"ticket_{self.venta_data.get('id_venta', 'temp')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            contenido = self.generar_contenido_ticket()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            messagebox.showinfo("Ticket guardado", f"Ticket guardado exitosamente en:\n{filename}")
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el ticket:\n{str(e)}")
    
    def generar_contenido_ticket(self):
        """Generar el contenido del ticket en formato texto"""
        contenido = []
        contenido.append("=" * 40)
        contenido.append("        JANET ROSA BICI")
        contenido.append("      Sistema de Ventas")
        contenido.append("=" * 40)
        contenido.append("")
        
        contenido.append(f"Ticket: #{self.venta_data.get('id_venta', 'N/A')}")
        contenido.append(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        contenido.append(f"Método: {self.venta_data.get('metodo', 'Efectivo')}")
        contenido.append("-" * 40)
        contenido.append("")
        
        contenido.append("PRODUCTOS:")
        contenido.append("-" * 40)
        
        for item in self.venta_data.get('items', []):
            nombre = item.get('nombre', 'Producto')
            cantidad = item.get('cantidad', 1)
            precio = item.get('precio', 0)
            subtotal = precio * cantidad
            
            contenido.append(f"{cantidad}x {nombre}")
            contenido.append(f"   ${precio:.2f} c/u = ${subtotal:.2f}")
        
        contenido.append("-" * 40)
        
        subtotal_total = sum(item['precio'] * item['cantidad'] for item in self.venta_data.get('items', []))
        contenido.append(f"Subtotal: ${subtotal_total:.2f}")
        
        descuento = self.venta_data.get('descuento', 0)
        if descuento > 0:
            contenido.append(f"Descuento: -${descuento:.2f}")
        
        contenido.append(f"\nTOTAL: ${self.venta_data.get('total', 0):.2f}")
        contenido.append("=" * 40)
        contenido.append("")
        contenido.append("   ¡Gracias por su compra!")
        contenido.append("        Vuelva pronto")
        contenido.append("=" * 40)
        
        return "\n".join(contenido)
    
    def generar_ticket_html(self):
        """Generar ticket en formato HTML para impresión"""
        subtotal_total = sum(item['precio'] * item['cantidad'] for item in self.venta_data.get('items', []))
        descuento = self.venta_data.get('descuento', 0)
        
        productos_html = ""
        for item in self.venta_data.get('items', []):
            nombre = item.get('nombre', 'Producto')
            cantidad = item.get('cantidad', 1)
            precio = item.get('precio', 0)
            subtotal = precio * cantidad
            
            productos_html += f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{cantidad}x {nombre}</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: right;">${precio:.2f}</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: right; font-weight: bold;">${subtotal:.2f}</td>
            </tr>
            """
        
        descuento_html = ""
        if descuento > 0:
            descuento_html = f"""
            <tr>
                <td colspan="2" style="padding: 8px; text-align: right; color: #FF9800;">Descuento:</td>
                <td style="padding: 8px; text-align: right; color: #FF9800; font-weight: bold;">-${descuento:.2f}</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Ticket #{self.venta_data.get('id_venta', 'N/A')}</title>
            <style>
                @media print {{
                    @page {{ margin: 0.5cm; }}
                    body {{ margin: 0; }}
                }}
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    max-width: 80mm;
                    margin: 20px auto;
                    padding: 20px;
                    background: white;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px dashed #333;
                    padding-bottom: 15px;
                    margin-bottom: 15px;
                }}
                .logo {{
                    font-size: 40px;
                    margin-bottom: 10px;
                }}
                .business-name {{
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .rosa {{
                    color: #E91E63;
                }}
                .subtitle {{
                    font-size: 12px;
                    color: #666;
                }}
                .info {{
                    margin: 15px 0;
                    font-size: 12px;
                }}
                .info-row {{
                    display: flex;
                    justify-content: space-between;
                    margin: 5px 0;
                }}
                .info-label {{
                    color: #666;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                th {{
                    background: #f5f5f5;
                    padding: 8px;
                    text-align: left;
                    font-size: 11px;
                    border-bottom: 2px solid #333;
                }}
                td {{
                    font-size: 11px;
                }}
                .totals {{
                    border-top: 2px dashed #333;
                    padding-top: 10px;
                    margin-top: 10px;
                }}
                .total-row {{
                    display: flex;
                    justify-content: space-between;
                    margin: 5px 0;
                    font-size: 12px;
                }}
                .total-final {{
                    background: #FFF0F5;
                    padding: 10px;
                    border-radius: 5px;
                    margin-top: 10px;
                }}
                .total-final .total-row {{
                    font-size: 16px;
                    font-weight: bold;
                }}
                .total-amount {{
                    color: #E91E63;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    padding-top: 15px;
                    border-top: 2px dashed #333;
                }}
                .thanks {{
                    font-size: 14px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .come-back {{
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">🚲</div>
                <div class="business-name">
                    Janet <span class="rosa">Rosa</span> Bici
                </div>
                <div class="subtitle">Sistema de Ventas</div>
            </div>
            
            <div class="info">
                <div class="info-row">
                    <span class="info-label">Ticket:</span>
                    <strong>#{self.venta_data.get('id_venta', 'N/A')}</strong>
                </div>
                <div class="info-row">
                    <span class="info-label">Fecha:</span>
                    <span>{datetime.now().strftime('%d/%m/%Y %H:%M')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Método:</span>
                    <span>{self.venta_data.get('metodo', 'Efectivo')}</span>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th style="text-align: right;">Precio</th>
                        <th style="text-align: right;">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {productos_html}
                </tbody>
            </table>
            
            <div class="totals">
                <div class="total-row">
                    <span>Subtotal:</span>
                    <span>${subtotal_total:.2f}</span>
                </div>
                {descuento_html}
                <div class="total-final">
                    <div class="total-row">
                        <span>TOTAL:</span>
                        <span class="total-amount">${self.venta_data.get('total', 0):.2f}</span>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <div class="thanks">¡Gracias por su compra!</div>
                <div class="come-back">Vuelva pronto</div>
            </div>
            
            <script>
                // Auto-abrir diálogo de impresión
                window.onload = function() {{
                    setTimeout(function() {{
                        window.print();
                    }}, 500);
                }};
            </script>
        </body>
        </html>
        """
        
        return html
    
    def imprimir_con_navegador(self, dialog):
        """Abrir ticket en navegador para imprimir"""
        try:
            import tempfile
            import os
            import webbrowser
            
            html_content = self.generar_ticket_html()
            
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8')
            temp_file.write(html_content)
            temp_file.close()
            
            webbrowser.open('file://' + temp_file.name)
            
            messagebox.showinfo(
                "Ticket abierto", 
                "El ticket se abrió en tu navegador.\n\n"
                "Se abrirá automáticamente el diálogo de impresión.\n"
                "Si no se abre, presiona Ctrl+P"
            )
            dialog.destroy()
            
            # Limpiar archivo temporal
            self.after(30000, lambda: os.unlink(temp_file.name) if os.path.exists(temp_file.name) else None)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el ticket:\n{str(e)}")
    
    def guardar_como_pdf(self, dialog):
        """Guardar ticket como PDF (requiere navegador)"""
        try:
            import tempfile
            import os
            import webbrowser
            
            html_content = self.generar_ticket_html()
            
            filename = f"ticket_{self.venta_data.get('id_venta', 'temp')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            webbrowser.open('file://' + os.path.abspath(filename))
            
            messagebox.showinfo(
                "Guardar como PDF",
                f"El ticket se abrió en tu navegador.\n\n"
                f"Para guardar como PDF:\n"
                f"1. Presiona Ctrl+P\n"
                f"2. Selecciona 'Guardar como PDF'\n"
                f"3. Haz clic en 'Guardar'\n\n"
                f"Archivo HTML guardado en:\n{filename}"
            )
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF:\n{str(e)}")


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
