import customtkinter as ctk
from datetime import datetime
import tempfile
import os
import webbrowser
from tkinter import messagebox
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.impresion import imprimir_html_directo, abrir_dialogo_impresion, detectar_impresora_predeterminada


class TicketVentaView(ctk.CTkToplevel):
    def __init__(self, parent, venta_data):
        super().__init__(parent)
        self.venta_data = venta_data
        self.title("Ticket de Venta")
        self.geometry("500x750")
        self.transient(parent)
        self.grab_set()
        self._centrar()
        self._crear_ui()
    
    def _centrar(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 250
        y = (self.winfo_screenheight() // 2) - 375
        self.geometry(f"500x750+{x}+{y}")
    
    def _crear_ui(self):
        # Fondo principal
        main = ctk.CTkFrame(self, fg_color="white")
        main.pack(fill="both", expand=True)
        
        # Área de scroll
        scroll = ctk.CTkScrollableFrame(main, fg_color="white")
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Encabezado - Nombre del negocio
        title_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        title_frame.pack(pady=(10, 5))
        
        ctk.CTkLabel(
            title_frame,
            text="Janet ",
            font=("Brush Script MT", 36, "italic"),
            text_color="#333333"
        ).pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Rosa ",
            font=("Brush Script MT", 36, "italic"),
            text_color="#E91E63"
        ).pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Bici",
            font=("Brush Script MT", 36, "italic"),
            text_color="#333333"
        ).pack(side="left")
        
        # Subtítulo
        ctk.CTkLabel(
            scroll,
            text="Sistema de Ventas",
            font=("Segoe UI", 11),
            text_color="#999999"
        ).pack(pady=(0, 15))
        
        # Línea separadora
        ctk.CTkFrame(scroll, height=1, fg_color="#DDDDDD").pack(fill="x", padx=20, pady=15)
        
        # Información del ticket
        info_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        info_frame.pack(fill="x", padx=40, pady=10)
        
        self._fila_info(info_frame, "Ticket:", f"#{self.venta_data.get('id_venta', 'N/A')}")
        self._fila_info(info_frame, "Fecha:", datetime.now().strftime("%d/%m/%Y %H:%M"))
        self._fila_info(info_frame, "Método de pago:", self.venta_data.get('metodo', 'Efectivo'))
        
        # Línea separadora
        ctk.CTkFrame(scroll, height=1, fg_color="#DDDDDD").pack(fill="x", padx=20, pady=15)
        
        # Título PRODUCTOS
        ctk.CTkLabel(
            scroll,
            text="PRODUCTOS",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(anchor="w", padx=40, pady=(10, 15))
        
        # Lista de productos
        productos_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        productos_frame.pack(fill="x", padx=40)
        
        for item in self.venta_data.get('items', []):
            self._producto(productos_frame, item)
        
        # Línea separadora
        ctk.CTkFrame(scroll, height=1, fg_color="#DDDDDD").pack(fill="x", padx=20, pady=20)
        
        # Totales
        totales_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        totales_frame.pack(fill="x", padx=40, pady=10)
        
        subtotal = sum(i['precio'] * i['cantidad'] for i in self.venta_data.get('items', []))
        self._fila_total(totales_frame, "Subtotal:", f"${subtotal:.2f}", "#666666")
        
        desc = self.venta_data.get('descuento', 0)
        if desc > 0:
            self._fila_total(totales_frame, "Descuento:", f"-${desc:.2f}", "#FFA726")
        
        # Espacio antes del total
        ctk.CTkLabel(totales_frame, text="", height=10).pack()
        
        # TOTAL destacado
        total_frame = ctk.CTkFrame(totales_frame, fg_color="transparent")
        total_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            total_frame,
            text="TOTAL:",
            font=("Segoe UI", 18, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        ctk.CTkLabel(
            total_frame,
            text=f"${self.venta_data.get('total', 0):.2f}",
            font=("Segoe UI", 22, "bold"),
            text_color="#E91E63"
        ).pack(side="right")
        
        # Línea separadora
        ctk.CTkFrame(scroll, height=1, fg_color="#DDDDDD").pack(fill="x", padx=20, pady=20)
        
        # Mensaje de agradecimiento
        ctk.CTkLabel(
            scroll,
            text="¡Gracias por su compra!",
            font=("Segoe UI", 13, "bold"),
            text_color="#333333"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            scroll,
            text="Vuelva pronto",
            font=("Segoe UI", 11),
            text_color="#999999"
        ).pack(pady=(0, 20))
        
        # Botones
        buttons_frame = ctk.CTkFrame(main, fg_color="white")
        buttons_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        btn_container = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        btn_container.pack(fill="x")
        
        # Botón Imprimir Directo (verde)
        ctk.CTkButton(
            btn_container,
            text="🖨 Imprimir",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=50,
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            command=self.imprimir_directo
        ).pack(fill="x", pady=(0, 5))
        
        # Botón Cerrar (rosa)
        ctk.CTkButton(
            btn_container,
            text="Cerrar",
            fg_color="#E91E63",
            hover_color="#C2185B",
            height=50,
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            command=self.destroy
        ).pack(fill="x", pady=(5, 0))
    
    def _fila_info(self, parent, label, valor):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=6)
        
        ctk.CTkLabel(
            row,
            text=label,
            font=("Segoe UI", 12),
            text_color="#999999"
        ).pack(side="left")
        
        ctk.CTkLabel(
            row,
            text=valor,
            font=("Segoe UI", 12),
            text_color="#333333"
        ).pack(side="right")
    
    def _producto(self, parent, item):
        # Contenedor del producto
        prod_frame = ctk.CTkFrame(parent, fg_color="transparent")
        prod_frame.pack(fill="x", pady=8)
        
        # Nombre del producto con cantidad
        nombre_label = ctk.CTkLabel(
            prod_frame,
            text=f"{item.get('cantidad', 1)}x {item.get('nombre', 'Producto')}",
            font=("Segoe UI", 12),
            text_color="#333333",
            anchor="w"
        )
        nombre_label.pack(anchor="w")
        
        # Precio unitario y subtotal
        precio_frame = ctk.CTkFrame(prod_frame, fg_color="transparent")
        precio_frame.pack(fill="x", pady=(2, 0))
        
        precio = item.get('precio', 0)
        cantidad = item.get('cantidad', 1)
        subtotal = precio * cantidad
        
        ctk.CTkLabel(
            precio_frame,
            text=f"${precio:.2f} c/u",
            font=("Segoe UI", 10),
            text_color="#AAAAAA"
        ).pack(side="left", padx=(15, 0))
        
        ctk.CTkLabel(
            precio_frame,
            text=f"${subtotal:.2f}",
            font=("Segoe UI", 12, "bold"),
            text_color="#333333"
        ).pack(side="right")
    
    def _fila_total(self, parent, label, valor, color):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            row,
            text=label,
            font=("Segoe UI", 13),
            text_color=color
        ).pack(side="left")
        
        ctk.CTkLabel(
            row,
            text=valor,
            font=("Segoe UI", 13, "bold"),
            text_color=color
        ).pack(side="right")
    
    def imprimir_directo(self):
        '''Imprimir directamente en la impresora predeterminada'''
        try:
            # Detectar impresora
            impresora = detectar_impresora_predeterminada()
            
            if not impresora:
                # Si no hay impresora, abrir en navegador
                respuesta = messagebox.askyesno(
                    "Impresora no detectada",
                    "No se detectó una impresora predeterminada.\n\n¿Desea abrir el ticket en el navegador para imprimir manualmente?",
                    parent=self
                )
                if respuesta:
                    self.ver_en_navegador()
                return
            
            # Generar HTML
            html = self._html()
            
            # Crear archivo temporal
            tf = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8')
            tf.write(html)
            tf.close()
            
            # Intentar imprimir directamente
            exito = abrir_dialogo_impresion(tf.name)
            
            if exito:
                messagebox.showinfo(
                    "Impresión",
                    f"Ticket enviado a la impresora: {impresora}",
                    parent=self
                )
            else:
                # Si falla, abrir en navegador
                webbrowser.open('file://' + tf.name)
            
            # Limpiar después de 30 segundos
            self.after(30000, lambda: os.unlink(tf.name) if os.path.exists(tf.name) else None)
            
        except Exception as e:
            messagebox.showerror(
                "Error de impresión",
                f"No se pudo imprimir el ticket.\n\nError: {str(e)}\n\nIntente usar el botón 'Ver' para abrir en el navegador.",
                parent=self
            )
    
    def ver_en_navegador(self):
        '''Abrir ticket en navegador para imprimir manualmente'''
        try:
            html = self._html()
            tf = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8')
            tf.write(html)
            tf.close()
            webbrowser.open('file://' + tf.name)
            self.after(30000, lambda: os.unlink(tf.name) if os.path.exists(tf.name) else None)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el ticket: {str(e)}", parent=self)
    
    def _html(self):
        items = self.venta_data.get('items', [])
        subtotal = sum(i['precio'] * i['cantidad'] for i in items)
        
        prods_html = ""
        for i in items:
            nombre = i.get("nombre", "Producto")
            cantidad = i.get("cantidad", 1)
            precio = i.get("precio", 0)
            sub = precio * cantidad
            prods_html += f'''
            <div class="producto">
                <div class="prod-nombre">{cantidad}x {nombre}</div>
                <div class="prod-precios">
                    <span class="precio-unit">${precio:.2f} c/u</span>
                    <span class="precio-total">${sub:.2f}</span>
                </div>
            </div>
            '''
        
        desc = self.venta_data.get('descuento', 0)
        desc_html = f'<div class="fila-total desc"><span>Descuento:</span><span>-${desc:.2f}</span></div>' if desc > 0 else ""
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ticket #{self.venta_data.get("id_venta","N/A")}</title>
    <style>
        @media print {{
            @page {{ 
                margin: 0.5cm;
                size: 80mm auto;
            }}
            body {{ margin: 0; }}
            .no-print {{ display: none; }}
        }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 80mm;
            margin: 20px auto;
            padding: 20px;
            background: white;
            color: #333;
        }}
        .header {{
            text-align: center;
            padding-bottom: 15px;
            margin-bottom: 15px;
            border-bottom: 1px solid #ddd;
        }}
        .business-name {{
            font-size: 28px;
            font-weight: bold;
            font-style: italic;
            margin-bottom: 5px;
        }}
        .rosa {{ color: #E91E63; }}
        .subtitle {{
            font-size: 11px;
            color: #999;
            margin-top: 5px;
        }}
        .info {{
            margin: 15px 0;
            padding: 0 10px;
        }}
        .info-row {{
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            font-size: 12px;
        }}
        .info-label {{ color: #999; }}
        .info-value {{ color: #333; }}
        .separador {{
            border-top: 1px solid #ddd;
            margin: 15px 0;
        }}
        .seccion-titulo {{
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin: 15px 0 10px 10px;
        }}
        .productos {{
            padding: 0 10px;
        }}
        .producto {{
            margin: 12px 0;
        }}
        .prod-nombre {{
            font-size: 12px;
            color: #333;
            margin-bottom: 3px;
        }}
        .prod-precios {{
            display: flex;
            justify-content: space-between;
            padding-left: 15px;
        }}
        .precio-unit {{
            font-size: 10px;
            color: #aaa;
        }}
        .precio-total {{
            font-size: 12px;
            font-weight: bold;
            color: #333;
        }}
        .totales {{
            padding: 15px 10px;
        }}
        .fila-total {{
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            font-size: 13px;
            color: #666;
        }}
        .fila-total.desc {{
            color: #FFA726;
            font-weight: bold;
        }}
        .fila-total.final {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-top: 15px;
        }}
        .fila-total.final span:last-child {{
            color: #E91E63;
            font-size: 22px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
        }}
        .thanks {{
            font-size: 13px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        .come-back {{
            font-size: 11px;
            color: #999;
        }}
        .print-button {{
            text-align: center;
            margin: 20px 0;
        }}
        .print-button button {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
        }}
        .print-button button:hover {{
            background: #45a049;
        }}
    </style>
</head>
<body>
    <div class="print-button no-print">
        <button onclick="window.print()">🖨 Imprimir Ticket</button>
    </div>
    
    <div class="header">
        <div class="business-name">
            Janet <span class="rosa">Rosa</span> Bici
        </div>
        <div class="subtitle">Sistema de Ventas</div>
    </div>
    
    <div class="info">
        <div class="info-row">
            <span class="info-label">Ticket:</span>
            <span class="info-value">#{self.venta_data.get("id_venta","N/A")}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Fecha:</span>
            <span class="info-value">{datetime.now().strftime("%d/%m/%Y %H:%M")}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Método de pago:</span>
            <span class="info-value">{self.venta_data.get("metodo","Efectivo")}</span>
        </div>
    </div>
    
    <div class="separador"></div>
    
    <div class="seccion-titulo">PRODUCTOS</div>
    
    <div class="productos">
        {prods_html}
    </div>
    
    <div class="separador"></div>
    
    <div class="totales">
        <div class="fila-total">
            <span>Subtotal:</span>
            <span>${subtotal:.2f}</span>
        </div>
        {desc_html}
        <div class="fila-total final">
            <span>TOTAL:</span>
            <span>${self.venta_data.get("total",0):.2f}</span>
        </div>
    </div>
    
    <div class="separador"></div>
    
    <div class="footer">
        <div class="thanks">¡Gracias por su compra!</div>
        <div class="come-back">Vuelva pronto</div>
    </div>
    
    <script>
        // Auto-imprimir al cargar (opcional, comentado por defecto)
        // window.onload = function() {{
        //     setTimeout(function() {{ window.print(); }}, 500);
        // }};
    </script>
</body>
</html>'''
