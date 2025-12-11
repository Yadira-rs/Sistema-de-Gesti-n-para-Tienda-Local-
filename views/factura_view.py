import customtkinter as ctk
from datetime import datetime
import tempfile
import os
from PIL import Image
import webbrowser
from tkinter import messagebox
from PIL import Image
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.impresion import imprimir_html_directo, abrir_dialogo_impresion, detectar_impresora_predeterminada

class FacturaView(ctk.CTkToplevel):
    def __init__(self, parent, venta_data):
        super().__init__(parent)
        self.venta_data = venta_data
        self.title("Factura - Janet Rosa Bici")
        self.geometry("600x850")
        self.transient(parent)
        self.grab_set()
        self._centrar()
        self._crear_ui()
    
    def _centrar(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 300
        y = (self.winfo_screenheight() // 2) - 425
        self.geometry(f"600x850+{x}+{y}")
    
    def _crear_ui(self):
        # Fondo principal
        main = ctk.CTkFrame(self, fg_color="white")
        main.pack(fill="both", expand=True)
        
        # Área de scroll
        scroll = ctk.CTkScrollableFrame(main, fg_color="white")
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header Grid (Left: Logo/Info, Right: Factura Details)
        header_grid = ctk.CTkFrame(scroll, fg_color="transparent")
        header_grid.pack(fill="x", pady=(0, 20))
        
        # Columna Izquierda (Logo e Info)
        left_header = ctk.CTkFrame(header_grid, fg_color="transparent")
        left_header.pack(side="left", anchor="nw")
        
        # Logo
        logo_frame = ctk.CTkFrame(left_header, fg_color="transparent")
        logo_frame.pack(anchor="w", pady=(0, 5))
        
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image_path = os.path.join(base_path, "WhatsApp Image 2025-12-02 at 11.52.41 AM.jpeg")
            
            if os.path.exists(image_path):
                pil_image = Image.open(image_path)
                # Mantener ratio
                ratio = pil_image.width / pil_image.height
                new_height = 80
                new_width = int(new_height * ratio)
                
                logo_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(new_width, new_height))
                ctk.CTkLabel(logo_frame, text="", image=logo_img).pack(side="top", anchor="center")
            else:
                raise Exception("Logo no encontrado")
        except Exception as e:
            print(f"Error cargando logo: {e}")
            ctk.CTkLabel(
                logo_frame,
                text="🚲", # Emoji de bicicleta
                font=("Segoe UI", 48),
                text_color="#E91E63"
            ).pack(side="top", anchor="center")
        
        ctk.CTkLabel(
            left_header,
            text="Janet Rosa Bici",
            font=("Brush Script MT", 28, "italic"),
            text_color="#E91E63"
        ).pack(anchor="center")
        
        ctk.CTkLabel(
            left_header,
            text="Sistema de Ventas Profesional",
            font=("Segoe UI", 10),
            text_color="#555555"
        ).pack(anchor="center")
        
        # Columna Derecha (Datos Factura)
        right_header = ctk.CTkFrame(header_grid, fg_color="transparent")
        right_header.pack(side="right", anchor="ne")
        
        ctk.CTkLabel(
            right_header,
            text="Factura",
            font=("Brush Script MT", 32, "italic"),
            text_color="#E91E63"
        ).pack(anchor="e")
        
        factura_id = self.venta_data.get('id_venta', '0000').zfill(16)
        factura_id_fmt = " ".join([factura_id[i:i+4] for i in range(0, len(factura_id), 4)])
        
        ctk.CTkLabel(
            right_header,
            text=f"Nº: {factura_id_fmt}",
            font=("Segoe UI", 10, "bold"),
            text_color="#555555"
        ).pack(anchor="e")
        
        ctk.CTkLabel(
            right_header,
            text=datetime.now().strftime("%d de %B de %Y"),
            font=("Segoe UI", 10),
            text_color="#555555"
        ).pack(anchor="e")
        
        # Espaciador
        ctk.CTkFrame(scroll, height=20, fg_color="transparent").pack()

        # Encabezado de productos
        encabezados = ["Cantidad", "Descripción", "Precio unitario", "Total"]
        encabezado_frame = ctk.CTkFrame(scroll, fg_color="#E91E63") # Rosa
        encabezado_frame.pack(fill="x", padx=0, pady=(0, 0))
        
        for i, encabezado in enumerate(encabezados):
            ctk.CTkLabel(
                encabezado_frame,
                text=encabezado,
                font=("Segoe UI", 11, "bold"),
                text_color="white"
            ).grid(row=0, column=i, padx=10, pady=8, sticky="w" if i == 1 else "")
            
        encabezado_frame.grid_columnconfigure(1, weight=1)
        encabezado_frame.grid_columnconfigure(0, weight=0, minsize=60)
        encabezado_frame.grid_columnconfigure(2, weight=0, minsize=100)
        encabezado_frame.grid_columnconfigure(3, weight=0, minsize=80)

        # Lista de productos
        productos_frame = ctk.CTkFrame(scroll, fg_color="#F9F9F9")
        productos_frame.pack(fill="x", padx=0)
        
        for idx, item in enumerate(self.venta_data.get('items', [])):
            self._producto_nuevo(productos_frame, item, idx)
            
        # Sección inferior (Cliente izquierda, Totales derecha)
        bottom_grid = ctk.CTkFrame(scroll, fg_color="transparent")
        bottom_grid.pack(fill="x", pady=20)
        
        # Cliente (Izquierda)
        cliente_frame = ctk.CTkFrame(bottom_grid, fg_color="transparent")
        cliente_frame.pack(side="left", anchor="nw", fill="x", expand=True)
        
        cliente = self.venta_data.get('cliente', {})
        ctk.CTkLabel(cliente_frame, text=f"Cliente: {cliente.get('nombre', 'Cliente Mostrador')}", font=("Segoe UI", 10, "bold"), text_color="#333").pack(anchor="w")
        ctk.CTkLabel(cliente_frame, text=f"Dirección: {cliente.get('direccion', 'Conocido')}", font=("Segoe UI", 10), text_color="#555").pack(anchor="w")

        # Totales (Derecha)
        totales_frame = ctk.CTkFrame(bottom_grid, fg_color="transparent")
        totales_frame.pack(side="right", anchor="ne", padx=(20, 0))
        
        subtotal = self.venta_data.get('subtotal', 0)
        iva = self.venta_data.get('iva', 0)
        total = self.venta_data.get('total', 0)
        
        # Sin envío extra por defecto en proyecto real, o usar lógica existente
        envio = 0
        total_final = total + envio
        
        self._fila_total_nueva(totales_frame, "Subtotal", f"${subtotal:,.2f}")
        self._fila_total_nueva(totales_frame, "IVA (16%)", f"${iva:,.2f}")
        if envio > 0:
            self._fila_total_nueva(totales_frame, "Envío", f"${envio:,.2f}")
        
        # Línea separadora total
        ctk.CTkFrame(totales_frame, height=1, fg_color="#333").pack(fill="x", pady=5)
        
        self._fila_total_nueva(totales_frame, "Total", f"${total_final:,.2f}", bold=True, size=12)

        # Notas y Firma
        footer_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        footer_frame.pack(fill="x", pady=30)
        
        # Notas
        notas_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        notas_frame.pack(side="left", anchor="sw")
        ctk.CTkLabel(notas_frame, text="Gracias por su compra", font=("Brush Script MT", 16, "italic"), text_color="#333").pack(anchor="w")
            
        # Firma
        firma_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        firma_frame.pack(side="right", anchor="se", padx=20)
        ctk.CTkFrame(firma_frame, height=1, width=150, fg_color="#333").pack(pady=(20, 5))
        ctk.CTkLabel(firma_frame, text="Autorizado", font=("Brush Script MT", 14, "italic"), text_color="#333").pack()
        
        # Botones
        buttons_frame = ctk.CTkFrame(main, fg_color="white")
        buttons_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Botón Imprimir
        ctk.CTkButton(
            buttons_frame,
            text="🖨️ Imprimir Factura",
            fg_color="#E91E63", # Rosa
            hover_color="#C2185B",
            height=50,
            corner_radius=4,
            font=("Segoe UI", 14, "bold"),
            command=self._imprimir_factura
        ).pack(fill="x", pady=(0, 10))
        
        # Botón Cerrar
        ctk.CTkButton(
            buttons_frame,
            text="Cerrar",
            fg_color="#9E9E9E",
            hover_color="#757575",
            height=45,
            corner_radius=4,
            font=("Segoe UI", 12, "bold"),
            command=self.destroy
        ).pack(fill="x")

    def _producto_nuevo(self, parent, item, row_num):
        # Color alternado para filas (blanco y gris muy claro)
        bg_color = "#FFFFFF" if row_num % 2 == 0 else "#F5F5F5"
        
        prod_frame = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=0)
        prod_frame.pack(fill="x", pady=0)
        
        # Cantidad
        ctk.CTkLabel(prod_frame, text=f"{item.get('cantidad', 1)}", font=("Segoe UI", 10), text_color="#333", width=60).grid(row=0, column=0, padx=10, pady=5)
        
        # Descripción
        desc_label = ctk.CTkLabel(prod_frame, text=item.get('nombre', 'Producto'), font=("Segoe UI", 10), text_color="#333", anchor="w")
        desc_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Precio
        ctk.CTkLabel(prod_frame, text=f"${float(item.get('precio', 0)):,.2f}", font=("Segoe UI", 10), text_color="#333", width=100, anchor="e").grid(row=0, column=2, padx=10, pady=5)
        
        # Total
        importe = float(item.get('precio', 0)) * int(item.get('cantidad', 1))
        ctk.CTkLabel(prod_frame, text=f"${importe:,.2f}", font=("Segoe UI", 10, "bold"), text_color="#333", width=80, anchor="e").grid(row=0, column=3, padx=10, pady=5)
        
        prod_frame.grid_columnconfigure(1, weight=1)

    def _fila_total_nueva(self, parent, label, valor, bold=False, size=11):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=2)
        font = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
        ctk.CTkLabel(row, text=label, font=font, text_color="#333", anchor="e", width=120).pack(side="left")
        ctk.CTkLabel(row, text=valor, font=font, text_color="#333", anchor="e", width=80).pack(side="right")
    
    def _imprimir_factura(self):
        try:
            # Crear un archivo HTML temporal
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode='w', encoding='utf-8') as f:
                f.write(self._generar_html())
                temp_file = f.name
            
            # Abrir el archivo en el navegador para imprimir
            webbrowser.open('file://' + temp_file)
            
            messagebox.showinfo("Imprimir", "Se abrió la factura en tu navegador.\nUsa Ctrl+P o el menú del navegador para imprimir.")
            
            # Eliminar el archivo temporal después de un tiempo
            self.after(10000, lambda: os.unlink(temp_file) if os.path.exists(temp_file) else None)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la factura: {str(e)}")
    
    def _generar_html(self):
        # Obtener datos de la venta
        cliente = self.venta_data.get('cliente', {})
        items = self.venta_data.get('items', [])
        subtotal = self.venta_data.get('subtotal', 0)
        iva = self.venta_data.get('iva', 0)
        total = self.venta_data.get('total', 0)
        
        # Generar filas de productos
        filas_productos = ""
        for i, item in enumerate(items):
            importe = float(item.get('precio', 0)) * int(item.get('cantidad', 1))
            bg_color = "#FFFFFF" if i % 2 == 0 else "#F5F5F5"
            filas_productos += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding: 10px; text-align: center;">{item.get('cantidad', 1)}</td>
                <td style="padding: 10px;">
                    {item.get('nombre', 'Producto')}
                </td>
                <td style="padding: 10px; text-align: right;">${float(item.get('precio', 0)):,.2f}</td>
                <td style="padding: 10px; text-align: right;">${importe:,.2f}</td>
            </tr>
            """
        
        # Formato de ID
        factura_id = self.venta_data.get('id_venta', '0000').zfill(16)
        factura_id_fmt = " ".join([factura_id[i:i+4] for i in range(0, len(factura_id), 4)])

        # Plantilla HTML de la factura Janet Rosa Bici
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Factura {self.venta_data.get('id_venta', '')}</title>
            <style>
                @page {{
                    margin: 0;
                }}
                
                body {{ 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    margin: 0; 
                    padding: 0;
                    color: #333;
                    background: #f5f5f5;
                }}
                
                .page-container {{
                    max-width: 700px;
                    margin: 20px auto;
                    background: white;
                    border: 6px solid #0066cc;
                    border-radius: 0;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                
                .content {{
                    padding: 25px 30px;
                }}
                
                .header-container {{ 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: flex-start;
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                }}
                
                .logo-section {{
                    flex: 1;
                }}
                
                .logo {{
                    font-size: 35px;
                    margin-bottom: 5px;
                }}
                
                .brand-name {{ 
                    font-family: 'Brush Script MT', cursive; 
                    font-size: 24px; 
                    color: #E91E63; 
                    margin: 0;
                    line-height: 1.2;
                }}
                
                .brand-sub {{ 
                    font-size: 11px; 
                    color: #888;
                    margin-top: 3px;
                }}
                
                .factura-section {{ 
                    text-align: right;
                    flex: 1;
                }}
                
                .factura-title {{ 
                    font-family: 'Brush Script MT', cursive; 
                    font-size: 32px; 
                    color: #E91E63; 
                    margin: 0 0 5px 0;
                    line-height: 1;
                }}
                
                .factura-details {{ 
                    color: #666; 
                    font-size: 11px; 
                    line-height: 1.6;
                }}
                
                .factura-details strong {{
                    color: #333;
                }}
                
                table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin: 15px 0;
                }}
                
                th {{ 
                    background: #E91E63; 
                    color: white; 
                    padding: 10px 8px;
                    text-align: left; 
                    font-weight: bold; 
                    font-size: 11px;
                }}
                
                th:first-child {{
                    text-align: center;
                }}
                
                th:nth-child(3),
                th:nth-child(4) {{
                    text-align: right;
                }}
                
                td {{ 
                    padding: 8px;
                    font-size: 11px;
                    border-bottom: 1px solid #f0f0f0;
                }}
                
                td:first-child {{
                    text-align: center;
                    color: #666;
                }}
                
                td:nth-child(3),
                td:nth-child(4) {{
                    text-align: right;
                }}
                
                tr:hover {{
                    background: #fafafa;
                }}
                
                .footer-section {{ 
                    display: flex; 
                    justify-content: space-between;
                    margin-top: 20px;
                    padding-top: 15px;
                }}
                
                .client-info {{ 
                    flex: 1;
                }}
                
                .client-info strong {{
                    font-size: 11px;
                    color: #333;
                }}
                
                .client-info div {{
                    margin: 5px 0;
                    color: #666;
                    font-size: 10px;
                }}
                
                .totals-info {{ 
                    min-width: 220px;
                    text-align: right;
                }}
                
                .total-row {{ 
                    display: flex; 
                    justify-content: space-between;
                    padding: 5px 0;
                    font-size: 11px;
                    color: #666;
                }}
                
                .total-row span:last-child {{
                    font-weight: 600;
                    color: #333;
                    min-width: 80px;
                    text-align: right;
                }}
                
                .final-total {{ 
                    font-weight: bold; 
                    font-size: 14px;
                    margin-top: 8px;
                    padding-top: 8px;
                    border-top: 2px solid #E91E63;
                    color: #333;
                }}
                
                .final-total span:last-child {{
                    color: #E91E63;
                    font-size: 16px;
                }}
                
                .signature-section {{
                    margin-top: 30px;
                    text-align: right;
                }}
                
                .signature-line {{ 
                    border-bottom: 1px solid #333;
                    width: 150px;
                    margin: 0 0 5px auto;
                }}
                
                .signature-text {{
                    font-family: 'Brush Script MT', cursive;
                    font-size: 13px;
                    color: #666;
                }}
                
                /* Botón de impresión */
                .print-button {{
                    position: fixed;
                    bottom: 30px;
                    right: 30px;
                    background: #E91E63;
                    color: white;
                    border: none;
                    padding: 16px 32px;
                    font-size: 15px;
                    font-weight: bold;
                    border-radius: 8px;
                    cursor: pointer;
                    box-shadow: 0 4px 12px rgba(233, 30, 99, 0.4);
                    transition: all 0.3s;
                    z-index: 1000;
                }}
                
                .print-button:hover {{
                    background: #C2185B;
                    box-shadow: 0 6px 16px rgba(233, 30, 99, 0.5);
                    transform: translateY(-2px);
                }}
                
                /* Ocultar botón al imprimir */
                @media print {{
                    .print-button {{ display: none; }}
                    body {{ 
                        padding: 0;
                        background: white;
                    }}
                    .page-container {{
                        border: none;
                        box-shadow: none;
                        margin: 0;
                    }}
                }}
                
            </style>
        </head>
        <body>
            <button class="print-button" onclick="window.print()">🖨️ Imprimir Factura</button>
            
            <div class="page-container">
                <div class="content">
                    <div class="header-container">
                        <div class="logo-section">
                            <div class="logo">🚲</div>
                            <div class="brand-name">Janet Rosa Bici</div>
                            <div class="brand-sub">Sistema de Ventas Profesional</div>
                        </div>
                        <div class="factura-section">
                            <div class="factura-title">Factura</div>
                            <div class="factura-details">
                                <div><strong>Nº:</strong> {factura_id_fmt}</div>
                                <div>{datetime.now().strftime('%d de %B de %Y')}</div>
                            </div>
                        </div>
                    </div>
                    
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 10%;">Cantidad</th>
                                <th style="width: 50%;">Descripción</th>
                                <th style="width: 20%;">Precio unitario</th>
                                <th style="width: 20%;">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filas_productos}
                        </tbody>
                    </table>
                    
                    <div class="footer-section">
                        <div class="client-info">
                            <strong>Cliente: {cliente.get('nombre', 'Cliente Mostrador')}</strong>
                            <div>Dirección: {cliente.get('direccion', 'Conocido')}</div>
                        </div>
                        
                        <div class="totals-info">
                            <div class="total-row">
                                <span>Subtotal</span>
                                <span>${subtotal:,.2f}</span>
                            </div>
                            <div class="total-row">
                                <span>IVA (16%)</span>
                                <span>${iva:,.2f}</span>
                            </div>
                            <div class="total-row final-total">
                                <span>Total</span>
                                <span>${total:,.2f}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="signature-section">
                        <div class="signature-line"></div>
                        <div class="signature-text">Autorizado</div>
                    </div>
                    
                </div>
            </div>
        </body>
        </html>
        """
        return html
