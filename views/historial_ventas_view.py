import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from controllers.ventas import listar_ultimas_ventas
from database.db import crear_conexion

class HistorialVentasView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.user = user
        self.ventas = []
        self.pack(fill="both", expand=True)
        
        self.crear_interfaz()
        self.cargar_ventas()
    
    def crear_interfaz(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 5))
        
        # Título
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="📊 Historial de Ventas",
            font=("Segoe UI", 20, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Consulta todas las ventas realizadas",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(anchor="w")
        
        # Botones en la esquina derecha
        buttons_frame = ctk.CTkFrame(header, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Botón actualizar
        ctk.CTkButton(
            buttons_frame,
            text="🔄 Actualizar",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=40,
            width=130,
            font=("Segoe UI", 12, "bold"),
            command=self.cargar_ventas
        ).pack(side="left", padx=(0, 10))
        
        # Botón borrar historial
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Borrar Historial",
            fg_color="#F44336",
            hover_color="#D32F2F",
            height=40,
            width=160,
            font=("Segoe UI", 12, "bold"),
            command=self.borrar_historial
        ).pack(side="left")
        
        # Estadísticas
        self.crear_estadisticas()
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10, height=45)
        search_frame.pack(fill="x", padx=20, pady=(10, 5))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 16)).pack(side="left", padx=10)
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por ID de venta...",
            border_width=0,
            fg_color="white",
            font=("Segoe UI", 11)
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filtrar_ventas())
        
        # Lista de ventas
        self.ventas_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.ventas_scroll.pack(fill="both", expand=True, padx=20, pady=(5, 10))
    
    def crear_estadisticas(self):
        """Crear tarjetas de estadísticas"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=(5, 10))
        
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total Ventas
        card1 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card1.grid(row=0, column=0, padx=5, sticky="ew")
        
        icon_frame1 = ctk.CTkFrame(card1, fg_color="#E3F2FD", corner_radius=8, width=50, height=50)
        icon_frame1.pack(side="left", padx=15, pady=15)
        icon_frame1.pack_propagate(False)
        ctk.CTkLabel(icon_frame1, text="🛒", font=("Segoe UI", 24)).pack(expand=True)
        
        info_frame1 = ctk.CTkFrame(card1, fg_color="transparent")
        info_frame1.pack(side="left", fill="both", expand=True, pady=15)
        ctk.CTkLabel(info_frame1, text="Total Ventas", font=("Segoe UI", 12), text_color="#666666", anchor="w").pack(anchor="w")
        self.total_ventas_label = ctk.CTkLabel(info_frame1, text="0", font=("Segoe UI", 20, "bold"), text_color="#333333", anchor="w")
        self.total_ventas_label.pack(anchor="w")
        
        # Ingresos Totales
        card2 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        
        icon_frame2 = ctk.CTkFrame(card2, fg_color="#E8F5E9", corner_radius=8, width=50, height=50)
        icon_frame2.pack(side="left", padx=15, pady=15)
        icon_frame2.pack_propagate(False)
        ctk.CTkLabel(icon_frame2, text="💰", font=("Segoe UI", 24)).pack(expand=True)
        
        info_frame2 = ctk.CTkFrame(card2, fg_color="transparent")
        info_frame2.pack(side="left", fill="both", expand=True, pady=15)
        ctk.CTkLabel(info_frame2, text="Ingresos Totales", font=("Segoe UI", 12), text_color="#666666", anchor="w").pack(anchor="w")
        self.ingresos_label = ctk.CTkLabel(info_frame2, text="$0.00", font=("Segoe UI", 20, "bold"), text_color="#4CAF50", anchor="w")
        self.ingresos_label.pack(anchor="w")
        
        # Productos Vendidos
        card3 = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=10)
        card3.grid(row=0, column=2, padx=5, sticky="ew")
        
        icon_frame3 = ctk.CTkFrame(card3, fg_color="#FFF3E0", corner_radius=8, width=50, height=50)
        icon_frame3.pack(side="left", padx=15, pady=15)
        icon_frame3.pack_propagate(False)
        ctk.CTkLabel(icon_frame3, text="📦", font=("Segoe UI", 24)).pack(expand=True)
        
        info_frame3 = ctk.CTkFrame(card3, fg_color="transparent")
        info_frame3.pack(side="left", fill="both", expand=True, pady=15)
        ctk.CTkLabel(info_frame3, text="Productos Vendidos", font=("Segoe UI", 12), text_color="#666666", anchor="w").pack(anchor="w")
        self.productos_label = ctk.CTkLabel(info_frame3, text="0", font=("Segoe UI", 20, "bold"), text_color="#FF9800", anchor="w")
        self.productos_label.pack(anchor="w")
    
    def cargar_ventas(self):
        """Cargar ventas desde la base de datos"""
        try:
            self.ventas = listar_ultimas_ventas(100)  # Últimas 100 ventas
            self.actualizar_estadisticas()
            self.mostrar_ventas(self.ventas)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las ventas: {str(e)}")
            self.ventas = []
    
    def actualizar_estadisticas(self):
        """Actualizar estadísticas"""
        total_ventas = len(self.ventas)
        ingresos_totales = sum(float(v.get("total", 0)) for v in self.ventas)
        
        # Contar productos vendidos
        total_productos = 0
        for venta in self.ventas:
            detalles = self.obtener_detalle_venta(venta.get("id_venta"))
            total_productos += sum(d.get("cantidad", 0) for d in detalles)
        
        self.total_ventas_label.configure(text=str(total_ventas))
        self.ingresos_label.configure(text=f"${ingresos_totales:,.2f}")
        self.productos_label.configure(text=str(total_productos))
    
    def mostrar_ventas(self, ventas):
        """Mostrar ventas en la lista"""
        for widget in self.ventas_scroll.winfo_children():
            widget.destroy()
        
        for venta in ventas:
            self.crear_tarjeta_venta(venta)
    
    def crear_tarjeta_venta(self, venta):
        """Crear tarjeta de venta con detalle de productos"""
        # Tarjeta principal
        card = ctk.CTkFrame(self.ventas_scroll, fg_color="white", corner_radius=8)
        card.pack(fill="x", pady=2)
        
        # Header de la venta
        header = ctk.CTkFrame(card, fg_color="#F5F5F5", corner_radius=8)
        header.pack(fill="x", padx=10, pady=8)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=10, pady=6)
        
        # ID y fecha
        left_info = ctk.CTkFrame(header_content, fg_color="transparent")
        left_info.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            left_info,
            text=f"🧾 Venta #{venta.get('id_venta', 'N/A')}",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333",
            anchor="w"
        ).pack(anchor="w")
        
        fecha = venta.get("fecha", datetime.now())
        if isinstance(fecha, datetime):
            fecha_str = fecha.strftime("%d/%m/%Y %H:%M")
        else:
            fecha_str = str(fecha)
        
        ctk.CTkLabel(
            left_info,
            text=f"📅 {fecha_str}",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(3, 0))
        
        # Total
        total = float(venta.get("total", 0))
        ctk.CTkLabel(
            header_content,
            text=f"${total:,.2f}",
            font=("Segoe UI", 20, "bold"),
            text_color="#E91E63"
        ).pack(side="right")
        
        # Frame para botones
        btn_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # Botón ver ticket
        btn_ticket = ctk.CTkButton(
            btn_frame,
            text="🎫 Ver Ticket",
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            width=100,
            height=32,
            font=("Segoe UI", 10, "bold"),
            corner_radius=8
        )
        btn_ticket.configure(command=lambda v=venta: self.ver_ticket_venta(v))
        btn_ticket.pack(side="left", padx=(0, 5))
        
        # Botón generar factura
        btn_factura = ctk.CTkButton(
            btn_frame,
            text="📄 Factura",
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=90,
            height=32,
            font=("Segoe UI", 10, "bold"),
            corner_radius=8
        )
        btn_factura.configure(command=lambda v=venta: self.generar_factura(v))
        btn_factura.pack(side="left", padx=(0, 5))
        
        # Botón borrar ticket
        btn_borrar = ctk.CTkButton(
            btn_frame,
            text="🗑️",
            fg_color="#F44336",
            hover_color="#D32F2F",
            width=40,
            height=32,
            font=("Segoe UI", 14),
            corner_radius=8
        )
        btn_borrar.configure(command=lambda v=venta: self.borrar_ticket(v))
        btn_borrar.pack(side="left")
        
        # Método de pago
        metodo = venta.get("metodo_pago", "Efectivo")
        metodo_icon = {"Efectivo": "💵", "Tarjeta": "💳", "Transferencia": "📱"}.get(metodo, "💵")
        
        metodo_badge = ctk.CTkFrame(header_content, fg_color="#E3F2FD", corner_radius=8)
        metodo_badge.pack(side="right", padx=(0, 10))
        
        ctk.CTkLabel(
            metodo_badge,
            text=f"{metodo_icon} {metodo}",
            font=("Segoe UI", 10, "bold"),
            text_color="#2196F3"
        ).pack(padx=10, pady=5)
        
        # Productos vendidos
        productos_frame = ctk.CTkFrame(card, fg_color="transparent")
        productos_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            productos_frame,
            text="Productos:",
            font=("Segoe UI", 11, "bold"),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        # Obtener detalle de productos
        detalles = self.obtener_detalle_venta(venta.get("id_venta"))
        
        if detalles:
            for detalle in detalles:
                self.crear_fila_producto(productos_frame, detalle)
        else:
            ctk.CTkLabel(
                productos_frame,
                text="No hay detalles disponibles",
                font=("Segoe UI", 12),
                text_color="#999999"
            ).pack(anchor="w")
    
    def crear_fila_producto(self, parent, detalle):
        """Crear fila de producto vendido"""
        fila = ctk.CTkFrame(parent, fg_color="#F9F9F9", corner_radius=8)
        fila.pack(fill="x", pady=2)
        
        content = ctk.CTkFrame(fila, fg_color="transparent")
        content.pack(fill="x", padx=12, pady=8)
        
        # Nombre del producto
        nombre = detalle.get("nombre_producto", "Producto")
        ctk.CTkLabel(
            content,
            text=f"• {nombre}",
            font=("Segoe UI", 12),
            text_color="#333333",
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        # Cantidad
        cantidad = detalle.get("cantidad", 0)
        ctk.CTkLabel(
            content,
            text=f"x{cantidad}",
            font=("Segoe UI", 10, "bold"),
            text_color="#666666"
        ).pack(side="left", padx=10)
        
        # Precio unitario
        precio = float(detalle.get("precio_unitario", 0))
        ctk.CTkLabel(
            content,
            text=f"${precio:.2f}",
            font=("Segoe UI", 12),
            text_color="#999999"
        ).pack(side="left", padx=5)
        
        # Subtotal
        subtotal = precio * cantidad
        ctk.CTkLabel(
            content,
            text=f"${subtotal:.2f}",
            font=("Segoe UI", 10, "bold"),
            text_color="#E91E63"
        ).pack(side="left")
    
    def obtener_detalle_venta(self, id_venta):
        """Obtener detalle de productos de una venta"""
        try:
            conn = crear_conexion()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            
            # Intentar con detalle_ventas (plural)
            try:
                cursor.execute("""
                    SELECT 
                        dv.cantidad,
                        dv.subtotal / dv.cantidad as precio_unitario,
                        p.nombre as nombre_producto,
                        p.precio
                    FROM detalle_ventas dv
                    LEFT JOIN productos p ON dv.id_producto = p.id_producto
                    WHERE dv.id_venta = %s
                """, (id_venta,))
                
                detalles = cursor.fetchall()
                
                if detalles:
                    conn.close()
                    return detalles
            except:
                pass
            
            # Intentar con detalle_venta (singular) como alternativa
            try:
                cursor.execute("""
                    SELECT 
                        dv.cantidad,
                        dv.precio_unitario,
                        p.nombre as nombre_producto
                    FROM detalle_venta dv
                    LEFT JOIN productos p ON dv.id_producto = p.id_producto
                    WHERE dv.id_venta = %s
                """, (id_venta,))
                
                detalles = cursor.fetchall()
                conn.close()
                return detalles
            except:
                pass
            
            conn.close()
            return []
            
        except Exception as e:
            print(f"Error al obtener detalle de venta: {e}")
            return []
    
    def filtrar_ventas(self):
        """Filtrar ventas por búsqueda"""
        termino = self.search_entry.get().lower()
        
        if not termino:
            self.mostrar_ventas(self.ventas)
            return
        
        ventas_filtradas = [
            v for v in self.ventas
            if termino in str(v.get("id_venta", "")).lower()
        ]
        
        self.mostrar_ventas(ventas_filtradas)
    
    def generar_factura(self, venta):
        """Generar factura de una venta"""
        try:
            print(f"DEBUG: Generando factura para venta {venta.get('id_venta')}")
            
            # Obtener detalles de la venta
            detalles = self.obtener_detalle_venta(venta.get("id_venta"))
            print(f"DEBUG: Detalles para factura: {len(detalles)} items")
            
            # Preparar datos para la factura
            items = []
            subtotal = 0
            
            for detalle in detalles:
                cantidad = int(detalle.get('cantidad', 1))
                precio_unitario = float(detalle.get('precio_unitario', 0))
                importe = cantidad * precio_unitario
                subtotal += importe
                
                items.append({
                    'nombre': detalle.get('nombre_producto', 'Producto'),
                    'descripcion': detalle.get('nombre_producto', 'Producto'),
                    'cantidad': cantidad,
                    'precio': precio_unitario,
                    'importe': importe
                })
            
            # IVA 16% 
            iva = subtotal * 0.16
            total_calculado = subtotal + iva
            
            # Usar el total real de la venta
            total_real = float(venta.get('total', total_calculado))
            
            factura_data = {
                'id_venta': str(venta.get('id_venta')),
                'folio': f"FAC-{venta.get('id_venta')}",
                'fecha': venta.get('fecha', datetime.now()),
                'items': items,
                'subtotal': subtotal,
                'iva': iva,
                'total': total_real,
                'pago': total_real,
                'cambio': 0,
                'metodo_pago': venta.get('metodo_pago', 'Efectivo'),
                'descuento': float(venta.get('descuento', 0)),
                'cliente': {
                    'nombre': 'Cliente Mostrador',
                    'direccion': 'Conocido',
                    'telefono': ''
                }
            }
            
            print(f"DEBUG: Datos de la factura: {factura_data}")
            
            # Mostrar factura
            from views.factura_view import FacturaView
            factura_window = FacturaView(self, factura_data)
            
        except Exception as e:
            print(f"ERROR en generar_factura: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo generar la factura: {str(e)}")
    
    def ver_ticket_venta(self, venta):
        """Ver ticket de una venta del historial"""
        try:
            print(f"DEBUG: Abriendo ticket para venta {venta.get('id_venta')}")
            
            # Obtener detalles de la venta
            detalles = self.obtener_detalle_venta(venta.get("id_venta"))
            print(f"DEBUG: Detalles obtenidos: {len(detalles)} items")
            
            # Preparar datos para el ticket
            items = []
            for detalle in detalles:
                precio_unitario = float(detalle.get('precio_unitario', 0))
                cantidad = int(detalle.get('cantidad', 1))
                
                items.append({
                    'nombre': detalle.get('nombre_producto', 'Producto'),
                    'cantidad': cantidad,
                    'precio': precio_unitario,
                    'importe': precio_unitario * cantidad
                })
            
            print(f"DEBUG: Items preparados: {items}")
            
            # Usar el total real de la venta (no recalcular)
            total_real = float(venta.get('total', 0))
            
            ticket_data = {
                'id_venta': venta.get('id_venta'),
                'fecha': venta.get('fecha', datetime.now()),
                'items': items,
                'total': total_real,
                'metodo': venta.get('metodo_pago', 'Efectivo'),
                'descuento': float(venta.get('descuento', 0))
            }
            
            print(f"DEBUG: Datos del ticket: {ticket_data}")
            
            # Mostrar ticket
            from views.ticket_venta_view import TicketVentaView
            ticket_window = TicketVentaView(self, ticket_data)
            
        except Exception as e:
            print(f"ERROR en ver_ticket_venta: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo mostrar el ticket:\n{str(e)}")


    
    def borrar_historial(self):
        """Borrar todo el historial de ventas con confirmación"""
        # Confirmación con advertencia fuerte
        respuesta = messagebox.askyesno(
            "⚠️ ADVERTENCIA - Borrar Historial",
            "¿Estás COMPLETAMENTE SEGURO de que deseas borrar TODO el historial de ventas?\n\n"
            "⚠️ ESTA ACCIÓN NO SE PUEDE DESHACER ⚠️\n\n"
            "Se eliminarán:\n"
            "• Todas las ventas registradas\n"
            "• Todos los detalles de productos vendidos\n"
            "• Todo el historial de transacciones\n\n"
            "Esta acción es PERMANENTE e IRREVERSIBLE.",
            icon='warning'
        )
        
        if not respuesta:
            return
        
        # Segunda confirmación
        respuesta2 = messagebox.askyesno(
            "⚠️ ÚLTIMA CONFIRMACIÓN",
            "Esta es tu última oportunidad para cancelar.\n\n"
            "¿Realmente deseas ELIMINAR TODO el historial de ventas?\n\n"
            "Esta acción es IRREVERSIBLE.",
            icon='warning'
        )
        
        if not respuesta2:
            return
        
        try:
            from database.db import crear_conexion
            
            conn = crear_conexion()
            cursor = conn.cursor()
            
            # Eliminar detalles de ventas primero (por la clave foránea)
            cursor.execute("DELETE FROM detalle_ventas")
            detalles_eliminados = cursor.rowcount
            
            # Eliminar ventas
            cursor.execute("DELETE FROM ventas")
            ventas_eliminadas = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo(
                "✅ Historial Borrado",
                f"Historial eliminado exitosamente:\n\n"
                f"• {ventas_eliminadas} ventas eliminadas\n"
                f"• {detalles_eliminados} detalles eliminados\n\n"
                f"El historial está ahora vacío."
            )
            
            # Recargar la vista
            self.cargar_ventas()
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo borrar el historial:\n{str(e)}"
            )

    
    def borrar_ticket(self, venta):
        """Borrar un ticket/venta individual"""
        id_venta = venta.get('id_venta')
        total = venta.get('total', 0)
        fecha = venta.get('fecha', 'N/A')
        
        # Confirmación
        respuesta = messagebox.askyesno(
            "⚠️ Confirmar Eliminación",
            f"¿Estás seguro de que deseas eliminar esta venta?\n\n"
            f"Venta #{id_venta}\n"
            f"Fecha: {fecha}\n"
            f"Total: ${total:,.2f}\n\n"
            f"Esta acción no se puede deshacer.",
            icon='warning'
        )
        
        if not respuesta:
            return
        
        try:
            from database.db import crear_conexion
            
            conn = crear_conexion()
            cursor = conn.cursor()
            
            # Eliminar detalles de la venta primero
            cursor.execute("DELETE FROM detalle_ventas WHERE id_venta = %s", (id_venta,))
            
            # Eliminar la venta
            cursor.execute("DELETE FROM ventas WHERE id_venta = %s", (id_venta,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo(
                "✅ Venta Eliminada",
                f"La venta #{id_venta} ha sido eliminada exitosamente."
            )
            
            # Recargar la vista
            self.cargar_ventas()
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar la venta:\n{str(e)}"
            )
