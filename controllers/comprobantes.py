"""
Controlador de Comprobantes de Venta Mejorado
Janet Rosa Bici - Sistema de Ventas
"""

from datetime import datetime
import os
import tempfile
import webbrowser

def generar_comprobante_venta(venta, productos):
    """Generar comprobante de venta mejorado en HTML"""
    try:
        # Calcular totales
        subtotal = sum(float(p.get('precio_unitario', 0)) * int(p.get('cantidad', 1)) for p in productos)
        descuento = float(venta.get('descuento', 0))
        total = float(venta.get('total', 0))
        
        # Generar filas de productos
        filas_html = ""
        for i, producto in enumerate(productos, 1):
            cantidad = producto.get('cantidad', 1)
            nombre = producto.get('nombre', 'Producto')
            precio = float(producto.get('precio_unitario', 0))
            importe = cantidad * precio
            
            filas_html += f"""
            <tr>
                <td class="td-center">{i}</td>
                <td>{nombre}</td>
                <td class="td-center">{cantidad}</td>
                <td class="td-right">${precio:,.2f}</td>
                <td class="td-right td-bold">${importe:,.2f}</td>
            </tr>
            """
        
        # Fecha
        fecha = venta.get('fecha', datetime.now())
        if isinstance(fecha, str):
            fecha_str = fecha
        else:
            fecha_str = fecha.strftime("%d/%m/%Y %H:%M")
        
        # HTML mejorado
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Comprobante #{venta.get('id_venta', 'N/A')}</title>
    <style>
        @page {{ margin: 1.5cm; }}
        @media print {{ .no-print {{ display: none; }} }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            padding: 30px;
            font-size: 13px;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header {{
            text-align: center;
            padding-bottom: 25px;
            margin-bottom: 30px;
            border-bottom: 3px solid #E91E63;
        }}
        
        .business-name {{
            font-size: 36px;
            font-weight: bold;
            font-style: italic;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }}
        
        .rosa {{ color: #E91E63; }}
        
        .subtitle {{
            font-size: 14px;
            color: #999;
            margin-bottom: 15px;
        }}
        
        .doc-title {{
            font-size: 24px;
            font-weight: bold;
            color: #E91E63;
            margin-top: 10px;
            letter-spacing: 2px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            background: #F8F9FA;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        
        .info-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
        }}
        
        .info-label {{
            font-weight: 600;
            color: #666;
        }}
        
        .info-value {{
            color: #333;
            font-weight: 500;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
        }}
        
        th {{
            background: linear-gradient(135deg, #E91E63 0%, #C2185B 100%);
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #E0E0E0;
        }}
        
        tr:hover {{
            background: #FFF0F5;
        }}
        
        .td-center {{ text-align: center; }}
        .td-right {{ text-align: right; }}
        .td-bold {{ font-weight: 600; }}
        
        .totales {{
            background: linear-gradient(135deg, #FFF0F5 0%, #FFE4EC 100%);
            padding: 25px;
            border-radius: 10px;
            margin-top: 25px;
        }}
        
        .total-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            font-size: 15px;
        }}
        
        .total-row.descuento {{
            color: #FF9800;
            font-weight: 600;
        }}
        
        .total-final {{
            font-size: 24px;
            font-weight: bold;
            color: #E91E63;
            border-top: 2px solid #E91E63;
            padding-top: 15px;
            margin-top: 10px;
        }}
        
        .nota {{
            background: #FFF3E0;
            padding: 20px;
            border-radius: 10px;
            margin-top: 25px;
            border-left: 5px solid #FF9800;
        }}
        
        .nota-title {{
            font-weight: bold;
            color: #F57C00;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 25px;
            border-top: 2px solid #E0E0E0;
            color: #999;
            font-size: 12px;
        }}
        
        .footer-title {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .print-btn {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin: 20px auto;
            display: block;
        }}
        
        .print-btn:hover {{
            background: #45a049;
        }}
    </style>
</head>
<body>
    <button class="print-btn no-print" onclick="window.print()">🖨 Imprimir Comprobante</button>
    
    <div class="container">
        <div class="header">
            <div class="business-name">Janet <span class="rosa">Rosa</span> Bici</div>
            <div class="subtitle">Sistema de Ventas</div>
            <div class="doc-title">COMPROBANTE DE VENTA</div>
        </div>
        
        <div class="info-grid">
            <div class="info-item">
                <span class="info-label">Folio:</span>
                <span class="info-value">#{venta.get('id_venta', 'N/A')}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Fecha:</span>
                <span class="info-value">{fecha_str}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Método de Pago:</span>
                <span class="info-value">{venta.get('metodo_pago', 'Efectivo')}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Atendió:</span>
                <span class="info-value">{venta.get('usuario', 'Vendedor')}</span>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th style="width: 5%;">#</th>
                    <th style="width: 45%;">Descripción</th>
                    <th style="width: 15%;" class="td-center">Cantidad</th>
                    <th style="width: 17.5%;" class="td-right">Precio Unit.</th>
                    <th style="width: 17.5%;" class="td-right">Importe</th>
                </tr>
            </thead>
            <tbody>
                {filas_html}
            </tbody>
        </table>
        
        <div class="totales">
            <div class="total-row">
                <span>Subtotal:</span>
                <span>${subtotal:,.2f}</span>
            </div>
            {f'<div class="total-row descuento"><span>Descuento:</span><span>-${descuento:,.2f}</span></div>' if descuento > 0 else ''}
            <div class="total-row total-final">
                <span>TOTAL:</span>
                <span>${total:,.2f}</span>
            </div>
        </div>
        
        <div class="nota">
            <div class="nota-title">📝 Nota Importante</div>
            <p>Este comprobante es válido como constancia de compra. Si requiere factura fiscal (CFDI), 
            solicítela dentro de los próximos 30 días presentando este comprobante.</p>
        </div>
        
        <div class="footer">
            <div class="footer-title">¡Gracias por su compra!</div>
            <p>Janet Rosa Bici - Sistema de Ventas</p>
            <p style="margin-top: 5px;">Este documento no es una factura fiscal</p>
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
        filename = f"comprobante_{venta.get('id_venta', 'N/A')}_{fecha_archivo}.html"
        
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
            pdf_file = f"comprobante_{venta.get('id_venta', 'N/A')}_{fecha_archivo}.pdf"
            HTML(string=html_content).write_pdf(pdf_file)
            return pdf_file
        except ImportError:
            return guardar_y_abrir_comprobante(venta, productos)
            
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return None
