"""
Controlador de Comprobantes de Venta - Diseño Elegante
Janet Rosa Bici - Sistema de Ventas
"""

from datetime import datetime
import os
import tempfile
import webbrowser
import base64

def generar_comprobante_venta(venta, productos):
    """Generar factura con diseño elegante"""
    try:
        # Calcular totales
        subtotal = sum(float(p.get('precio_unitario', 0)) * int(p.get('cantidad', 1)) for p in productos)
        descuento = float(venta.get('descuento', 0))
        iva = subtotal * 0.16  # IVA 16%
        total = float(venta.get('total', 0))
        
        # Generar filas de productos
        filas_html = ""
        for producto in productos:
            cantidad = producto.get('cantidad', 1)
            nombre = producto.get('nombre', 'Producto')
            precio = float(producto.get('precio_unitario', 0))
            importe = cantidad * precio
            
            filas_html += f"""
            <tr class="producto-row">
                <td class="cantidad">{cantidad}</td>
                <td class="descripcion">{nombre}</td>
                <td class="precio">${precio:,.2f}</td>
                <td class="total">${importe:,.2f}</td>
            </tr>
            """
        
        # Fecha
        fecha = venta.get('fecha', datetime.now())
        if isinstance(fecha, str):
            fecha_str = fecha
        else:
            fecha_str = fecha.strftime("%d de %B de %Y")
        
        # Obtener logo en base64
        logo_html = '<div class="logo">🚲</div>'
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image_path = os.path.join(base_path, "WhatsApp Image 2025-12-02 at 11.52.41 AM.jpeg")
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read()).decode('utf-8')
                    # Ajustar tamaño del logo en impresión
                    logo_html = f'<img src="data:image/jpeg;base64,{b64_string}" alt="Logo" style="max-height: 100px; max-width: 200px; margin-bottom: 10px;">'
        except Exception as e:
            print(f"No se pudo cargar logo para impresión: {e}")

        # HTML con diseño elegante
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Factura #{venta.get('id_venta', 'N/A')}</title>
    <style>
        @page {{ margin: 2cm; }}
        @media print {{ .no-print {{ display: none; }} }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', 'Arial', sans-serif;
            color: #666;
            background: #f5f5f5;
            padding: 40px 20px;
        }}
        
        .factura-container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 50px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 40px;
            padding-bottom: 30px;
        }}
        
        .logo-section {{
            flex: 1;
        }}
        
        .logo {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        
        .business-name {{
            font-family: 'Brush Script MT', cursive;
            font-size: 32px;
            font-style: italic;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .rosa {{ color: #E91E63; }}
        
        .business-info {{
            font-size: 13px;
            color: #999;
            line-height: 1.6;
        }}
        
        .factura-info {{
            text-align: right;
        }}
        
        .factura-title {{
            font-family: 'Brush Script MT', cursive;
            font-size: 48px;
            font-style: italic;
            color: #666;
            margin-bottom: 15px;
        }}
        
        .factura-details {{
            font-size: 13px;
            color: #999;
            line-height: 1.8;
        }}
        
        .factura-number {{
            font-weight: bold;
            color: #333;
        }}
        
        .productos-table {{
            width: 100%;
            margin: 40px 0;
            border-collapse: collapse;
        }}
        
        .productos-table thead {{
            background: #5a5a5a;
            color: white;
        }}
        
        .productos-table th {{
            padding: 15px;
            text-align: left;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .productos-table th.cantidad {{ width: 15%; text-align: center; }}
        .productos-table th.descripcion {{ width: 40%; }}
        .productos-table th.precio {{ width: 22.5%; text-align: right; }}
        .productos-table th.total {{ width: 22.5%; text-align: right; }}
        
        .producto-row {{
            background: #f5f5f5;
        }}
        
        .producto-row:nth-child(even) {{
            background: #e8e8e8;
        }}
        
        .producto-row td {{
            padding: 15px;
            font-size: 14px;
            color: #666;
        }}
        
        .producto-row .cantidad {{
            text-align: center;
            font-weight: bold;
        }}
        
        .producto-row .precio {{
            text-align: right;
        }}
        
        .producto-row .total {{
            text-align: right;
            font-weight: bold;
            color: #333;
        }}
        
        .footer-section {{
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
        }}
        
        .cliente-info {{
            flex: 1;
        }}
        
        .cliente-title {{
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            font-size: 14px;
        }}
        
        .cliente-details {{
            font-size: 13px;
            color: #999;
            line-height: 1.6;
        }}
        
        .totales {{
            width: 300px;
            text-align: right;
        }}
        
        .total-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            font-size: 15px;
            color: #666;
        }}
        
        .total-row.subtotal {{
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .total-row.final {{
            border-top: 2px solid #333;
            padding-top: 15px;
            margin-top: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        
        .total-row .label {{
            font-weight: 600;
        }}
        
        .notas {{
            margin-top: 50px;
            padding-top: 30px;
            border-top: 1px solid #e0e0e0;
        }}
        
        .notas-title {{
            font-family: 'Brush Script MT', cursive;
            font-size: 24px;
            font-style: italic;
            color: #666;
            margin-bottom: 15px;
        }}
        
        .notas-content {{
            background: #333;
            color: white;
            padding: 20px;
            border-radius: 8px;
            font-size: 13px;
            line-height: 1.6;
        }}
        
        .print-button {{
            text-align: center;
            margin: 30px 0;
        }}
        
        .print-button button {{
            background: #E91E63;
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(233, 30, 99, 0.3);
        }}
        
        .print-button button:hover {{
            background: #C2185B;
        }}
    </style>
</head>
<body>
    <div class="print-button no-print">
        <button onclick="window.print()">🖨 Imprimir Factura</button>
    </div>
    
    <div class="factura-container">
        <div class="header">
            <div class="logo-section">
                {logo_html}
                <div class="business-name">
                    Janet <span class="rosa">Rosa</span> Bici
                </div>
                <div class="business-info">
                    Sistema de Ventas<br>
                    Tel: 555-1234-567
                </div>
            </div>
            
            <div class="factura-info">
                <div class="factura-title">Factura</div>
                <div class="factura-details">
                    <div class="factura-number">Nº: {venta.get('id_venta', 'N/A'):04d}</div>
                    <div>{fecha_str}</div>
                    <div>Nº de cuenta: {venta.get('id_venta', 'N/A'):04d}</div>
                </div>
            </div>
        </div>
        
        <table class="productos-table">
            <thead>
                <tr>
                    <th class="cantidad">Cantidad</th>
                    <th class="descripcion">Descripción</th>
                    <th class="precio">Precio unitario</th>
                    <th class="total">Total</th>
                </tr>
            </thead>
            <tbody>
                {filas_html}
            </tbody>
        </table>
        
        <div class="footer-section">
            <div class="cliente-info">
                <div class="cliente-title">Cliente: {venta.get('cliente', 'Público General')}</div>
                <div class="cliente-details">
                    Método de pago: {venta.get('metodo_pago', 'Efectivo')}<br>
                    Atendió: {venta.get('usuario', 'Vendedor')}
                </div>
            </div>
            
            <div class="totales">
                <div class="total-row subtotal">
                    <span class="label">Subtotal</span>
                    <span>${subtotal:,.2f}</span>
                </div>
                <div class="total-row">
                    <span class="label">IVA (16%)</span>
                    <span>${iva:,.2f}</span>
                </div>
                {f'<div class="total-row"><span class="label">Descuento</span><span>-${descuento:,.2f}</span></div>' if descuento > 0 else ''}
                <div class="total-row final">
                    <span class="label">Total</span>
                    <span>${total:,.2f}</span>
                </div>
            </div>
        </div>
        
        <div class="notas">
            <div class="notas-title">Notas</div>
            <div class="notas-content">
                Gracias por su compra. Este comprobante es válido como constancia de compra.
                Para cualquier aclaración, favor de presentar este documento.
                Janet Rosa Bici - Sistema de Ventas
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return html_content
        
    except Exception as e:
        print(f"Error al generar comprobante: {e}")
        return None

def guardar_y_abrir_comprobante(venta, productos):
    """Guardar comprobante y abrirlo en navegador"""
    try:
        html_content = generar_comprobante_venta(venta, productos)
        if not html_content:
            return None
        
        # Crear archivo temporal
        fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"factura_{venta.get('id_venta', 'N/A')}_{fecha_archivo}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Abrir en navegador
        webbrowser.open('file://' + os.path.abspath(filename))
        
        return filename
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def generar_comprobante_pdf(venta, productos):
    """Generar comprobante en PDF (requiere weasyprint)"""
    try:
        html_content = generar_comprobante_venta(venta, productos)
        if not html_content:
            return None
        
        try:
            from weasyprint import HTML
            fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_file = f"factura_{venta.get('id_venta', 'N/A')}_{fecha_archivo}.pdf"
            HTML(string=html_content).write_pdf(pdf_file)
            return pdf_file
        except ImportError:
            return guardar_y_abrir_comprobante(venta, productos)
            
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return None
