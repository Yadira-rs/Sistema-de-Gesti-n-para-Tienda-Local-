import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class GestionCreditosView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.pack(fill="both", expand=True)
        
        self.user = user or {"nombre_completo": "Administrador", "email": "admin@janet.com"}
        self.creditos = []
        self.tab_actual = "Control de Ventas a Crédito"
        
        self.crear_interfaz()
        self.cargar_datos()
    

    def crear_logo_header(self, parent):
        """Crear header con logo de Janet Rosa Bici"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Logo pequeño a la izquierda
        logo_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_container.pack(side="left", padx=(0, 15))
        
        try:
            # Intentar cargar logo circular pequeño
            logo_paths = [
                "logo_limpio_small.png",  # LOGO LIMPIO
                "assets/logo_limpio_small.png",
                "logo_limpio_small.png",  # IMAGEN ORIGINAL
                "assets/logo_limpio_small.png",
                "logo_limpio_small.png",
                "logo_nuevo_sidebar.png", 
                "WhatsApp Image 2025-12-02 at 11.52.41 AM.jpeg",
                "logo_original.png"
            ]
            
            logo_loaded = False
            for path in logo_paths:
                if os.path.exists(path):
                    try:
                        from PIL import Image
                        img = Image.open(path).resize((40, 40), Image.Resampling.LANCZOS)
                        logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
                        
                        ctk.CTkLabel(
                            logo_container,
                            image=logo_image,
                            text=""
                        ).pack()
                        
                        logo_loaded = True
                        break
                    except Exception:
                        continue
            
            if not logo_loaded:
                # Fallback: emoji de bicicleta
                ctk.CTkLabel(
                    logo_container,
                    text="🚲",
                    font=("Segoe UI", 24),
                    text_color="#E91E63"
                ).pack()
                
        except Exception:
            # Fallback: emoji de bicicleta
            ctk.CTkLabel(
                logo_container,
                text="🚲",
                font=("Segoe UI", 24),
                text_color="#E91E63"
            ).pack()
        
        # Título de la pantalla
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        
        return title_frame

    def crear_interfaz(self):
        # Panel principal (sin sidebar, ya está en main.py)
        self.crear_panel_principal(self)



    def crear_panel_principal(self, parent):
        """Panel principal con créditos"""
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header con título
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header, text="Ventas a Crédito", font=("Segoe UI", 24, "bold"), 
                    text_color="#333333", anchor="w").pack(side="left")
        
        # Tabs de navegación
        self.crear_tabs(panel)
        
        # Contenedor para el contenido de cada tab
        self.content_frame = ctk.CTkFrame(panel, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Mostrar tab inicial
        self.mostrar_tab("Control de Ventas a Crédito")
    
    def crear_tabs(self, parent):
        """Crear pestañas de navegación"""
        tabs_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tabs_frame.pack(fill="x", pady=(0, 10))
        
        tabs = [
            "Control de Ventas a Crédito",
            "Créditos a clientes",
            "Vencidos",
            "Abonos de Hoy",
            "Gestión de Clientes"
        ]
        
        self.tab_buttons = {}
        
        for tab in tabs:
            btn = ctk.CTkButton(
                tabs_frame,
                text=tab,
                fg_color="white" if tab != self.tab_actual else "#E91E63",
                text_color="#666666" if tab != self.tab_actual else "white",
                hover_color="#F8BBD0",
                corner_radius=20,
                height=40,
                font=("Segoe UI", 13),
                command=lambda t=tab: self.cambiar_tab(t)
            )
            btn.pack(side="left", padx=5)
            self.tab_buttons[tab] = btn
    
    def cambiar_tab(self, tab):
        """Cambiar de pestaña"""
        self.tab_actual = tab
        
        # Actualizar estilos de botones
        for tab_name, btn in self.tab_buttons.items():
            if tab_name == tab:
                btn.configure(fg_color="#E91E63", text_color="white")
            else:
                btn.configure(fg_color="white", text_color="#666666")
        
        # Mostrar contenido del tab
        self.mostrar_tab(tab)
    
    def mostrar_tab(self, tab):
        """Mostrar contenido de la pestaña seleccionada"""
        # Limpiar contenido actual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if tab == "Control de Ventas a Crédito":
            self.mostrar_control_creditos()
        elif tab == "Créditos a clientes":
            self.mostrar_creditos_clientes()
        elif tab == "Vencidos":
            self.mostrar_vencidos()
        elif tab == "Abonos de Hoy":
            self.mostrar_abonos_hoy()
        elif tab == "Gestión de Clientes":
            self.mostrar_gestion_clientes()
    
    def mostrar_control_creditos(self):
        """Mostrar control principal de créditos"""
        # Contenedor principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Resumen de créditos (tarjetas superiores)
        self.crear_resumen_creditos(main_container)
        
        # Lista de créditos activos
        self.crear_lista_creditos_activos(main_container)
    
    def crear_resumen_creditos(self, parent):
        """Crear tarjetas de resumen de créditos"""
        resumen_frame = ctk.CTkFrame(parent, fg_color="transparent")
        resumen_frame.pack(fill="x", pady=(0, 20))
        
        # Configurar grid para 4 tarjetas
        resumen_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Obtener datos del resumen
        from controllers.creditos import obtener_resumen_creditos
        resumen = obtener_resumen_creditos()
        
        # Datos de las tarjetas
        tarjetas_data = [
            ("💳", "#E91E63", "Créditos Activos", resumen.get('activos', 0)),
            ("⏰", "#FF9800", "Vencidos", resumen.get('vencidos', 0)),
            ("✅", "#4CAF50", "Pagados", resumen.get('pagados', 0)),
            ("💰", "#2196F3", "Por Cobrar", f"${resumen.get('total_por_cobrar', 0):.2f}")
        ]
        
        for i, (icono, color, titulo, valor) in enumerate(tarjetas_data):
            self.crear_tarjeta_resumen(resumen_frame, i, icono, color, titulo, str(valor))
    
    def crear_tarjeta_resumen(self, parent, column, icono, color, titulo, valor):
        """Crear tarjeta de resumen individual"""
        card_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=8, height=120)
        card_frame.grid(row=0, column=column, padx=10, pady=0, sticky="ew")
        card_frame.grid_propagate(False)
        
        # Contenido de la tarjeta
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono
        icon_frame = ctk.CTkFrame(content_frame, fg_color=color, corner_radius=8, width=50, height=50)
        icon_frame.pack(anchor="w")
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(icon_frame, text=icono, font=("Segoe UI", 24)).pack(expand=True)
        
        # Título
        ctk.CTkLabel(content_frame, text=titulo, font=("Segoe UI", 12), 
                    text_color="#666666").pack(anchor="w", pady=(10, 5))
        
        # Valor
        ctk.CTkLabel(content_frame, text=valor, font=("Segoe UI", 24, "bold"), 
                    text_color="#333333").pack(anchor="w")
    
    def crear_lista_creditos_activos(self, parent):
        """Crear lista de créditos activos con funcionalidades"""
        # Header de la lista
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header_frame, text="Créditos Activos", 
                    font=("Segoe UI", 18, "bold"), text_color="#333333").pack(side="left")
        
        # Botón para nuevo crédito
        ctk.CTkButton(header_frame, text="+ Nuevo Crédito", 
                     fg_color="#E91E63", hover_color="#C2185B",
                     command=self.abrir_nuevo_credito).pack(side="right")
        
        # Contenedor scrollable para la lista
        self.lista_scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent", height=400)
        self.lista_scroll.pack(fill="both", expand=True)
        
        # Cargar créditos activos
        self.cargar_creditos_activos()
    
    def cargar_creditos_activos(self):
        """Cargar y mostrar créditos activos"""
        # Limpiar lista
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
        
        # Obtener créditos activos
        from controllers.creditos import obtener_creditos_activos
        creditos = obtener_creditos_activos()
        
        if not creditos:
            # Mensaje cuando no hay créditos
            empty_frame = ctk.CTkFrame(self.lista_scroll, fg_color="#F8F9FA", corner_radius=8)
            empty_frame.pack(fill="x", pady=20, padx=10)
            
            ctk.CTkLabel(empty_frame, text="📋 No hay créditos activos", 
                        font=("Segoe UI", 14), text_color="#666666").pack(pady=30)
        else:
            # Mostrar cada crédito
            for credito in creditos:
                self.crear_item_credito(self.lista_scroll, credito)
    
    def crear_item_credito(self, parent, credito):
        """Crear item de crédito con funcionalidades completas"""
        # Contenedor principal del item
        item_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=8)
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # Contenido principal
        main_content = ctk.CTkFrame(item_frame, fg_color="transparent")
        main_content.pack(fill="x", padx=20, pady=15)
        
        # Fila superior - ID y estado
        top_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        top_frame.pack(fill="x")
        
        # ID del crédito
        ctk.CTkLabel(top_frame, text=f"Crédito #{credito['id_credito']}", 
                    font=("Segoe UI", 16, "bold"), text_color="#333333").pack(side="left")
        
        # Estado
        estado_color = "#4CAF50" if credito['estado'] == 'Activo' else "#FF9800"
        estado_badge = ctk.CTkFrame(top_frame, fg_color=estado_color, corner_radius=15)
        estado_badge.pack(side="right")
        
        ctk.CTkLabel(estado_badge, text=credito['estado'], 
                    font=("Segoe UI", 10, "bold"), text_color="white").pack(padx=12, pady=4)
        
        # Información del crédito
        info_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        info_frame.pack(fill="x", pady=(10, 0))
        
        # Columna izquierda - Montos
        left_info = ctk.CTkFrame(info_frame, fg_color="transparent")
        left_info.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(left_info, text=f"Total: ${credito['monto_total']:.2f}", 
                    font=("Segoe UI", 12), text_color="#666666").pack(anchor="w")
        ctk.CTkLabel(left_info, text=f"Pagado: ${credito['monto_pagado']:.2f}", 
                    font=("Segoe UI", 12), text_color="#4CAF50").pack(anchor="w")
        ctk.CTkLabel(left_info, text=f"Saldo: ${credito['saldo_pendiente']:.2f}", 
                    font=("Segoe UI", 12, "bold"), text_color="#E91E63").pack(anchor="w")
        
        # Columna derecha - Fechas
        right_info = ctk.CTkFrame(info_frame, fg_color="transparent")
        right_info.pack(side="right")
        
        fecha_credito = credito['fecha_credito'].strftime("%d/%m/%Y") if credito['fecha_credito'] else "N/A"
        fecha_vencimiento = credito['fecha_vencimiento'].strftime("%d/%m/%Y") if credito['fecha_vencimiento'] else "N/A"
        
        ctk.CTkLabel(right_info, text=f"Fecha: {fecha_credito}", 
                    font=("Segoe UI", 11), text_color="#666666").pack(anchor="e")
        ctk.CTkLabel(right_info, text=f"Vence: {fecha_vencimiento}", 
                    font=("Segoe UI", 11), text_color="#666666").pack(anchor="e")
        
        # Días para vencer
        dias_vencer = credito.get('dias_para_vencer', 0)
        color_dias = "#4CAF50" if dias_vencer > 7 else "#FF9800" if dias_vencer > 0 else "#F44336"
        ctk.CTkLabel(right_info, text=f"Días: {dias_vencer}", 
                    font=("Segoe UI", 11, "bold"), text_color=color_dias).pack(anchor="e")
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(15, 0))
        
        # Botón Registrar Abono
        btn_abono = ctk.CTkButton(actions_frame, text="💰 Registrar Abono", 
                                 fg_color="#4CAF50", hover_color="#388E3C",
                                 width=140, height=35,
                                 command=lambda: self.abrir_registrar_abono(credito))
        btn_abono.pack(side="left", padx=(0, 10))
        
        # Botón Ver Historial
        btn_historial = ctk.CTkButton(actions_frame, text="📋 Historial", 
                                     fg_color="#2196F3", hover_color="#1976D2",
                                     width=100, height=35,
                                     command=lambda: self.ver_historial_abonos(credito))
        btn_historial.pack(side="left", padx=(0, 10))
        
        # Botón Cerrar Crédito (solo si saldo es 0 o muy pequeño)
        if credito['saldo_pendiente'] <= 0.01:
            btn_cerrar = ctk.CTkButton(actions_frame, text="✅ Cerrar", 
                                      fg_color="#FF9800", hover_color="#F57C00",
                                      width=80, height=35,
                                      command=lambda: self.cerrar_credito(credito))
            btn_cerrar.pack(side="left")
    
    def abrir_registrar_abono(self, credito):
        """Abrir ventana para registrar abono"""
        ventana = ctk.CTkToplevel(self)
        ventana.title("Registrar Abono")
        ventana.geometry("500x400")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()
        
        # Título
        ctk.CTkLabel(ventana, text="💰 Registrar Abono", 
                    font=("Segoe UI", 24, "bold"), text_color="#4CAF50").pack(pady=20)
        
        # Información del crédito
        info_frame = ctk.CTkFrame(ventana, fg_color="#F8F9FA")
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(info_frame, text=f"Crédito #{credito['id_credito']}", 
                    font=("Segoe UI", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(info_frame, text=f"Saldo Actual: ${credito['saldo_pendiente']:.2f}", 
                    font=("Segoe UI", 14), text_color="#E91E63").pack(pady=(0, 10))
        
        # Formulario
        form_frame = ctk.CTkFrame(ventana)
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Monto del abono
        ctk.CTkLabel(form_frame, text="Monto del Abono:", 
                    font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(20, 5))
        entry_monto = ctk.CTkEntry(form_frame, placeholder_text="0.00", font=("Segoe UI", 14))
        entry_monto.pack(fill="x", padx=20, pady=(0, 15))
        
        # Método de pago
        ctk.CTkLabel(form_frame, text="Método de Pago:", 
                    font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(0, 5))
        combo_metodo = ctk.CTkComboBox(form_frame, values=["Efectivo", "Tarjeta", "Transferencia"])
        combo_metodo.pack(fill="x", padx=20, pady=(0, 15))
        combo_metodo.set("Efectivo")
        
        # Notas
        ctk.CTkLabel(form_frame, text="Notas (opcional):", 
                    font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(0, 5))
        entry_notas = ctk.CTkEntry(form_frame, placeholder_text="Observaciones...")
        entry_notas.pack(fill="x", padx=20, pady=(0, 20))
        
        # Botones
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#666666",
                     command=ventana.destroy).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(btn_frame, text="Registrar Abono", fg_color="#4CAF50",
                     command=lambda: self.procesar_abono(ventana, credito, 
                                                        entry_monto.get(), 
                                                        combo_metodo.get(), 
                                                        entry_notas.get())).pack(side="right")
    
    def procesar_abono(self, ventana, credito, monto_str, metodo, notas):
        """Procesar el registro del abono"""
        try:
            monto = float(monto_str)
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0")
                return
            
            if monto > credito['saldo_pendiente']:
                respuesta = messagebox.askyesno("Advertencia", 
                    f"El abono (${monto:.2f}) es mayor al saldo pendiente (${credito['saldo_pendiente']:.2f}).\n"
                    "¿Desea continuar? El crédito se marcará como pagado.")
                if not respuesta:
                    return
            
            # Registrar el abono
            from controllers.creditos import registrar_abono
            if registrar_abono(credito['id_credito'], monto, metodo, notas):
                ventana.destroy()
                messagebox.showinfo("Éxito", "Abono registrado correctamente")
                
                # Verificar si el crédito se cerró automáticamente
                if monto >= credito['saldo_pendiente']:
                    messagebox.showinfo("Crédito Cerrado", 
                        f"¡El crédito #{credito['id_credito']} ha sido pagado completamente!")
                
                # Recargar la vista
                self.cargar_creditos_activos()
            else:
                messagebox.showerror("Error", "No se pudo registrar el abono")
                
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def ver_historial_abonos(self, credito):
        """Ver historial de abonos del crédito"""
        ventana = ctk.CTkToplevel(self)
        ventana.title("Historial de Abonos")
        ventana.geometry("600x500")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()
        
        # Título
        ctk.CTkLabel(ventana, text=f"📋 Historial - Crédito #{credito['id_credito']}", 
                    font=("Segoe UI", 20, "bold")).pack(pady=20)
        
        # Lista de abonos
        scroll_frame = ctk.CTkScrollableFrame(ventana, height=350)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Obtener abonos del crédito
        from controllers.creditos import obtener_abonos_credito
        try:
            abonos = obtener_abonos_credito(credito['id_credito'])
            
            if not abonos:
                ctk.CTkLabel(scroll_frame, text="No hay abonos registrados", 
                           font=("Segoe UI", 14), text_color="#666666").pack(pady=50)
            else:
                for abono in abonos:
                    self.crear_item_abono(scroll_frame, abono)
        except:
            ctk.CTkLabel(scroll_frame, text="Error al cargar historial", 
                       font=("Segoe UI", 14), text_color="#F44336").pack(pady=50)
        
        # Botón cerrar
        ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
    
    def crear_item_abono(self, parent, abono):
        """Crear item de abono en el historial"""
        item_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=6)
        item_frame.pack(fill="x", pady=3, padx=5)
        
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        
        # Fecha y monto
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x")
        
        fecha = abono['fecha_abono'].strftime("%d/%m/%Y %H:%M") if abono['fecha_abono'] else "N/A"
        ctk.CTkLabel(top_frame, text=fecha, font=("Segoe UI", 12), 
                    text_color="#666666").pack(side="left")
        
        ctk.CTkLabel(top_frame, text=f"${abono['monto_abono']:.2f}", 
                    font=("Segoe UI", 14, "bold"), text_color="#4CAF50").pack(side="right")
        
        # Método y notas
        if abono.get('metodo_pago') or abono.get('notas'):
            bottom_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            bottom_frame.pack(fill="x", pady=(5, 0))
            
            if abono.get('metodo_pago'):
                ctk.CTkLabel(bottom_frame, text=abono['metodo_pago'], 
                           font=("Segoe UI", 11), text_color="#666666").pack(side="left")
            
            if abono.get('notas'):
                ctk.CTkLabel(bottom_frame, text=abono['notas'], 
                           font=("Segoe UI", 11), text_color="#666666").pack(side="right")
    
    def cerrar_credito(self, credito):
        """Cerrar crédito manualmente"""
        respuesta = messagebox.askyesno("Confirmar", 
            f"¿Está seguro de cerrar el crédito #{credito['id_credito']}?\n"
            f"Saldo pendiente: ${credito['saldo_pendiente']:.2f}")
        
        if respuesta:
            try:
                from controllers.creditos import cerrar_credito_manual
                if cerrar_credito_manual(credito['id_credito']):
                    messagebox.showinfo("Éxito", "Crédito cerrado correctamente")
                    self.cargar_creditos_activos()
                else:
                    messagebox.showerror("Error", "No se pudo cerrar el crédito")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
    
    def abrir_nuevo_credito(self):
        """Abrir ventana para crear nuevo crédito"""
        # Reutilizar la funcionalidad del dashboard
        try:
            # Obtener la ventana principal
            main_app = self.winfo_toplevel()
            
            # Crear ventana de nuevo crédito
            self.crear_ventana_nuevo_credito()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir nuevo crédito: {str(e)}")
    
    def crear_ventana_nuevo_credito(self):
        """Crear ventana para nuevo crédito"""
        ventana = ctk.CTkToplevel(self)
        ventana.title("Nuevo Crédito")
        ventana.geometry("500x500")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()
        
        # Título
        ctk.CTkLabel(ventana, text="💳 Nuevo Crédito", 
                    font=("Segoe UI", 24, "bold"), text_color="#E91E63").pack(pady=20)
        
        # Formulario
        form_frame = ctk.CTkFrame(ventana)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cliente
        ctk.CTkLabel(form_frame, text="Cliente:", font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(20, 5))
        entry_cliente = ctk.CTkEntry(form_frame, placeholder_text="Nombre del cliente")
        entry_cliente.pack(fill="x", padx=20, pady=(0, 15))
        
        # Monto
        ctk.CTkLabel(form_frame, text="Monto Total:", font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(0, 5))
        entry_monto = ctk.CTkEntry(form_frame, placeholder_text="0.00")
        entry_monto.pack(fill="x", padx=20, pady=(0, 15))
        
        # Plazo
        ctk.CTkLabel(form_frame, text="Plazo (días):", font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(0, 5))
        entry_plazo = ctk.CTkEntry(form_frame, placeholder_text="30")
        entry_plazo.pack(fill="x", padx=20, pady=(0, 15))
        entry_plazo.insert(0, "30")
        
        # Notas
        ctk.CTkLabel(form_frame, text="Notas:", font=("Segoe UI", 14)).pack(anchor="w", padx=20, pady=(0, 5))
        entry_notas = ctk.CTkEntry(form_frame, placeholder_text="Observaciones...")
        entry_notas.pack(fill="x", padx=20, pady=(0, 20))
        
        # Botones
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#666666",
                     command=ventana.destroy).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(btn_frame, text="Crear Crédito", fg_color="#E91E63",
                     command=lambda: self.procesar_nuevo_credito(ventana, 
                                                               entry_cliente.get(),
                                                               entry_monto.get(),
                                                               entry_plazo.get(),
                                                               entry_notas.get())).pack(side="right")
    
    def procesar_nuevo_credito(self, ventana, cliente, monto_str, plazo_str, notas):
        """Procesar la creación del nuevo crédito"""
        try:
            if not cliente:
                messagebox.showerror("Error", "Ingrese el nombre del cliente")
                return
            
            monto = float(monto_str)
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0")
                return
            
            plazo = int(plazo_str) if plazo_str else 30
            if plazo <= 0:
                messagebox.showerror("Error", "El plazo debe ser mayor a 0")
                return
            
            # Crear el crédito
            from controllers.creditos import crear_credito
            id_credito = crear_credito(None, None, monto, plazo, 0, f"Cliente: {cliente}. {notas}")
            
            if id_credito:
                ventana.destroy()
                messagebox.showinfo("Éxito", f"Crédito #{id_credito} creado correctamente")
                self.cargar_creditos_activos()
            else:
                messagebox.showerror("Error", "No se pudo crear el crédito")
                
        except ValueError:
            messagebox.showerror("Error", "Verifique que los valores numéricos sean correctos")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def mostrar_creditos_clientes(self):
        """Mostrar todos los créditos por cliente"""
        ctk.CTkLabel(self.content_frame, text="Créditos por Cliente", 
                    font=("Segoe UI", 18, "bold")).pack(pady=20)
        # Implementar vista de créditos por cliente
    
    def mostrar_vencidos(self):
        """Mostrar créditos vencidos"""
        ctk.CTkLabel(self.content_frame, text="Créditos Vencidos", 
                    font=("Segoe UI", 18, "bold")).pack(pady=20)
        # Implementar vista de créditos vencidos
    
    def mostrar_abonos_hoy(self):
        """Mostrar abonos del día"""
        ctk.CTkLabel(self.content_frame, text="Abonos de Hoy", 
                    font=("Segoe UI", 18, "bold")).pack(pady=20)
        # Implementar vista de abonos del día
    
    def mostrar_gestion_clientes(self):
        """Mostrar gestión de clientes"""
        ctk.CTkLabel(self.content_frame, text="Gestión de Clientes", 
                    font=("Segoe UI", 18, "bold")).pack(pady=20)
        # Implementar gestión de clientes
    
    def cargar_datos(self):
        """Cargar datos iniciales"""
        pass
        # Contenedor principal dividido
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Panel izquierdo - Tabla
        left_panel = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Header mejorado con botones de acción
        header_frame = ctk.CTkFrame(left_panel, fg_color="#E91E63", corner_radius=10)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)
        
        # Título
        ctk.CTkLabel(
            header_content,
            text="💳 Control de Ventas a Crédito",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        ).pack(side="left")
        
        # Botones de acción en el header
        buttons_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Botón Nuevo Crédito
        ctk.CTkButton(
            buttons_frame,
            text="+ Nuevo",
            fg_color="white",
            text_color="#E91E63",
            hover_color="#F8BBD0",
            corner_radius=8,
            width=80,
            height=35,
            font=("Segoe UI", 11, "bold"),
            command=self.nuevo_credito
        ).pack(side="right", padx=(5, 0))
        
        # Botón Actualizar
        ctk.CTkButton(
            buttons_frame,
            text="🔄",
            fg_color="transparent",
            text_color="white",
            hover_color="#C2185B",
            corner_radius=8,
            width=40,
            height=35,
            font=("Segoe UI", 14),
            command=self.cargar_datos
        ).pack(side="right", padx=(5, 0))
        
        # Área de contenido con filtros
        content_container = ctk.CTkFrame(left_panel, fg_color="transparent")
        content_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Barra de filtros
        filter_frame = ctk.CTkFrame(content_container, fg_color="#F5F5F5", corner_radius=0)
        filter_frame.pack(fill="x", padx=0, pady=0)
        
        filter_content = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_content.pack(fill="x", padx=20, pady=10)
        
        # Filtro por estado
        ctk.CTkLabel(
            filter_content,
            text="Filtrar:",
            font=("Segoe UI", 11, "bold"),
            text_color="#666666"
        ).pack(side="left")
        
        self.filtro_estado = ctk.CTkComboBox(
            filter_content,
            values=["Todos", "Activos", "Vencidos", "Pagados"],
            width=120,
            height=30,
            font=("Segoe UI", 11),
            command=self.filtrar_creditos
        )
        self.filtro_estado.pack(side="left", padx=(10, 0))
        self.filtro_estado.set("Todos")
        
        # Búsqueda
        self.search_entry = ctk.CTkEntry(
            filter_content,
            placeholder_text="Buscar cliente...",
            width=200,
            height=30,
            font=("Segoe UI", 11)
        )
        self.search_entry.pack(side="left", padx=(10, 0))
        self.search_entry.bind("<KeyRelease>", self.buscar_creditos)
        
        # Botón de búsqueda
        ctk.CTkButton(
            filter_content,
            text="🔍",
            fg_color="#E91E63",
            hover_color="#C2185B",
            width=35,
            height=30,
            font=("Segoe UI", 12),
            command=self.buscar_creditos
        ).pack(side="left", padx=(5, 0))
        
        # Área de contenido scrollable
        self.content_scroll = ctk.CTkScrollableFrame(content_container, fg_color="white")
        self.content_scroll.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Cargar créditos
        self.cargar_creditos_tabla()
        
        # Panel derecho - Acciones y Resumen mejorado
        right_panel = ctk.CTkFrame(main_container, fg_color="transparent", width=320)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # Botones de acción principales
        actions_frame = ctk.CTkFrame(right_panel, fg_color="white", corner_radius=10)
        actions_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            actions_frame,
            text="Acciones Rápidas",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        # Botón Nuevo Crédito (principal)
        ctk.CTkButton(
            actions_frame,
            text="💳 Nuevo Crédito",
            fg_color="#E91E63",
            hover_color="#C2185B",
            corner_radius=10,
            height=50,
            font=("Segoe UI", 14, "bold"),
            command=self.nuevo_credito
        ).pack(fill="x", padx=20, pady=(0, 10))
        
        # Botones secundarios en fila
        secondary_buttons = ctk.CTkFrame(actions_frame, fg_color="transparent")
        secondary_buttons.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkButton(
            secondary_buttons,
            text="📊 Reportes",
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=8,
            height=40,
            font=("Segoe UI", 11),
            command=self.generar_reporte
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(
            secondary_buttons,
            text="📤 Exportar",
            fg_color="#FF9800",
            hover_color="#F57C00",
            corner_radius=8,
            height=40,
            font=("Segoe UI", 11),
            command=self.exportar_creditos
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Resumen mejorado
        resumen_frame = ctk.CTkFrame(right_panel, fg_color="white", corner_radius=10)
        resumen_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            resumen_frame,
            text="📈 Resumen Financiero",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        # Cards de resumen
        # Total Por Cobrar
        total_card = ctk.CTkFrame(resumen_frame, fg_color="#E8F5E9", corner_radius=8)
        total_card.pack(fill="x", padx=20, pady=(0, 8))
        
        total_content = ctk.CTkFrame(total_card, fg_color="transparent")
        total_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(total_content, text="💰", font=("Segoe UI", 20), text_color="#4CAF50").pack(side="left")
        
        total_text_frame = ctk.CTkFrame(total_content, fg_color="transparent")
        total_text_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(total_text_frame, text="Total Por Cobrar", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.total_cobrar_label = ctk.CTkLabel(total_text_frame, text="$0.00", 
                    font=("Segoe UI", 16, "bold"), text_color="#4CAF50", anchor="w")
        self.total_cobrar_label.pack(anchor="w")
        
        # Créditos Activos
        activos_card = ctk.CTkFrame(resumen_frame, fg_color="#E3F2FD", corner_radius=8)
        activos_card.pack(fill="x", padx=20, pady=(0, 8))
        
        activos_content = ctk.CTkFrame(activos_card, fg_color="transparent")
        activos_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(activos_content, text="📋", font=("Segoe UI", 20), text_color="#2196F3").pack(side="left")
        
        activos_text_frame = ctk.CTkFrame(activos_content, fg_color="transparent")
        activos_text_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(activos_text_frame, text="Créditos Activos", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.creditos_activos_label = ctk.CTkLabel(activos_text_frame, text="0", 
                    font=("Segoe UI", 16, "bold"), text_color="#2196F3", anchor="w")
        self.creditos_activos_label.pack(anchor="w")
        
        # Créditos Vencidos
        vencidos_card = ctk.CTkFrame(resumen_frame, fg_color="#FFEBEE", corner_radius=8)
        vencidos_card.pack(fill="x", padx=20, pady=(0, 15))
        
        vencidos_content = ctk.CTkFrame(vencidos_card, fg_color="transparent")
        vencidos_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(vencidos_content, text="⚠️", font=("Segoe UI", 20), text_color="#F44336").pack(side="left")
        
        vencidos_text_frame = ctk.CTkFrame(vencidos_content, fg_color="transparent")
        vencidos_text_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(vencidos_text_frame, text="Créditos Vencidos", font=("Segoe UI", 11), 
                    text_color="#666666", anchor="w").pack(anchor="w")
        self.creditos_vencidos_label = ctk.CTkLabel(vencidos_text_frame, text="0", 
                    font=("Segoe UI", 16, "bold"), text_color="#F44336", anchor="w")
        self.creditos_vencidos_label.pack(anchor="w")
        
        # Alertas y notificaciones
        alertas_frame = ctk.CTkFrame(right_panel, fg_color="white", corner_radius=10)
        alertas_frame.pack(fill="x")
        
        ctk.CTkLabel(
            alertas_frame,
            text="🔔 Alertas",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        # Contenedor de alertas
        self.alertas_container = ctk.CTkFrame(alertas_frame, fg_color="transparent")
        self.alertas_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # Cargar alertas
        self.cargar_alertas()
    
    def mostrar_creditos_clientes(self):
        """Mostrar tab de Créditos a clientes - agrupados por cliente"""
        # Contenedor principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=12)
        main_container.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            header,
            text="Créditos por Cliente",
            font=("Segoe UI", 16, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Botón para crear nuevo crédito
        ctk.CTkButton(
            header,
            text="+ Nuevo Crédito",
            fg_color="#E91E63",
            hover_color="#C2185B",
            height=35,
            font=("Segoe UI", 12, "bold"),
            command=self.nuevo_credito
        ).pack(side="right")
        
        # Lista de clientes con créditos
        scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Obtener créditos agrupados por cliente
        try:
            from database.db import crear_conexion
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    c.id_cliente,
                    cl.nombre as cliente_nombre,
                    COUNT(*) as total_creditos,
                    SUM(CASE WHEN c.estado = 'Activo' THEN 1 ELSE 0 END) as activos,
                    SUM(c.saldo_pendiente) as saldo_total
                FROM creditos c
                LEFT JOIN clientes cl ON c.id_cliente = cl.id_cliente
                GROUP BY c.id_cliente, cl.nombre
                ORDER BY saldo_total DESC
            """)
            
            clientes_creditos = cursor.fetchall()
            conn.close()
            
            if not clientes_creditos:
                ctk.CTkLabel(
                    scroll,
                    text="📋 No hay créditos registrados",
                    font=("Segoe UI", 14),
                    text_color="#999999"
                ).pack(expand=True, pady=50)
            else:
                for cliente in clientes_creditos:
                    self.crear_tarjeta_cliente_credito(scroll, cliente)
                    
        except Exception as e:
            ctk.CTkLabel(
                scroll,
                text=f"❌ Error al cargar créditos: {str(e)}",
                font=("Segoe UI", 14),
                text_color="#F44336"
            ).pack(expand=True, pady=50)
    
    def crear_tarjeta_cliente_credito(self, parent, cliente):
        """Crear tarjeta de cliente con sus créditos"""
        card = ctk.CTkFrame(parent, fg_color="#F5F5F5", corner_radius=10)
        card.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)
        
        # Nombre del cliente
        ctk.CTkLabel(
            content,
            text=cliente.get('cliente_nombre', 'Cliente sin nombre'),
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Estadísticas
        stats_frame = ctk.CTkFrame(content, fg_color="transparent")
        stats_frame.pack(side="right")
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Créditos: {cliente.get('total_creditos', 0)} | Activos: {cliente.get('activos', 0)} | Saldo: ${cliente.get('saldo_total', 0):.2f}",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack()
    
    def mostrar_vencidos(self):
        """Mostrar tab de Créditos Vencidos"""
        # Contenedor principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=12)
        main_container.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            header,
            text="⚠️ Créditos Vencidos",
            font=("Segoe UI", 16, "bold"),
            text_color="#F44336"
        ).pack(side="left")
        
        # Lista de créditos vencidos
        scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Obtener créditos vencidos
        try:
            from database.db import crear_conexion
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    c.*,
                    cl.nombre as cliente_nombre,
                    cl.telefono as cliente_telefono,
                    DATEDIFF(NOW(), c.fecha_vencimiento) as dias_vencido
                FROM creditos c
                LEFT JOIN clientes cl ON c.id_cliente = cl.id_cliente
                WHERE c.estado = 'Activo' AND c.fecha_vencimiento < CURDATE()
                ORDER BY c.fecha_vencimiento ASC
            """)
            
            creditos_vencidos = cursor.fetchall()
            conn.close()
            
            if not creditos_vencidos:
                ctk.CTkLabel(
                    scroll,
                    text="✅ No hay créditos vencidos",
                    font=("Segoe UI", 14),
                    text_color="#4CAF50"
                ).pack(expand=True, pady=50)
            else:
                for credito in creditos_vencidos:
                    self.crear_tarjeta_credito_vencido(scroll, credito)
                    
        except Exception as e:
            ctk.CTkLabel(
                scroll,
                text=f"❌ Error al cargar créditos vencidos: {str(e)}",
                font=("Segoe UI", 14),
                text_color="#F44336"
            ).pack(expand=True, pady=50)
    
    def crear_tarjeta_credito_vencido(self, parent, credito):
        """Crear tarjeta de crédito vencido"""
        card = ctk.CTkFrame(parent, fg_color="#FFEBEE", corner_radius=10)
        card.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)
        
        # Info del cliente
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=f"#{credito.get('id_credito')} - {credito.get('cliente_nombre', 'N/A')}",
            font=("Segoe UI", 13, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=f"Vencido hace {credito.get('dias_vencido', 0)} días | Saldo: ${credito.get('saldo_pendiente', 0):.2f}",
            font=("Segoe UI", 11),
            text_color="#F44336"
        ).pack(anchor="w")
        
        # Botón de acción
        ctk.CTkButton(
            content,
            text="Registrar Abono",
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=120,
            height=30,
            font=("Segoe UI", 11),
            command=lambda c=credito: self.registrar_abono(c)
        ).pack(side="right")
        
        # Header con alerta
        header = ctk.CTkFrame(main_container, fg_color="#FFEBEE", corner_radius=10)
        header.pack(fill="x", padx=20, pady=15)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            header_content,
            text="⚠️",
            font=("Segoe UI", 24),
            text_color="#E53935"
        ).pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            text_frame,
            text="Créditos Vencidos",
            font=("Segoe UI", 14, "bold"),
            text_color="#E53935",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame,
            text="Estos créditos han superado su fecha de vencimiento",
            font=("Segoe UI", 12),
            text_color="#C62828",
            anchor="w"
        ).pack(anchor="w")
        
        # Lista de créditos vencidos
        scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Mensaje si no hay vencidos
        ctk.CTkLabel(
            scroll,
            text="✅ No hay créditos vencidos",
            font=("Segoe UI", 14),
            text_color="#4CAF50"
        ).pack(expand=True, pady=50)
    
    def mostrar_abonos_hoy(self):
        """Mostrar tab de Abonos de Hoy"""
        from datetime import datetime
        
        # Contenedor principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=12)
        main_container.pack(fill="both", expand=True)
        
        # Header con fecha
        header = ctk.CTkFrame(main_container, fg_color="#E8F5E9", corner_radius=10)
        header.pack(fill="x", padx=20, pady=15)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            header_content,
            text="💰",
            font=("Segoe UI", 24),
            text_color="#4CAF50"
        ).pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            text_frame,
            text="Abonos de Hoy",
            font=("Segoe UI", 14, "bold"),
            text_color="#2E7D32",
            anchor="w"
        ).pack(anchor="w")
        
        fecha_hoy = datetime.now().strftime("%d de %B de %Y")
        ctk.CTkLabel(
            text_frame,
            text=fecha_hoy,
            font=("Segoe UI", 12),
            text_color="#43A047",
            anchor="w"
        ).pack(anchor="w")
        
        # Resumen del día
        resumen_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        resumen_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        resumen_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Total abonos
        card1 = ctk.CTkFrame(resumen_frame, fg_color="#F5F5F5", corner_radius=10)
        card1.grid(row=0, column=0, padx=5, sticky="ew")
        
        ctk.CTkLabel(card1, text="Total Abonos", font=("Segoe UI", 12), text_color="#666666").pack(pady=(10, 2))
        ctk.CTkLabel(card1, text="0", font=("Segoe UI", 20, "bold"), text_color="#333333").pack(pady=(0, 10))
        
        # Monto total
        card2 = ctk.CTkFrame(resumen_frame, fg_color="#F5F5F5", corner_radius=10)
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        
        ctk.CTkLabel(card2, text="Monto Total", font=("Segoe UI", 12), text_color="#666666").pack(pady=(10, 2))
        ctk.CTkLabel(card2, text="$0.00", font=("Segoe UI", 20, "bold"), text_color="#4CAF50").pack(pady=(0, 10))
        
        # Lista de abonos
        scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Obtener abonos de hoy
        try:
            from controllers.creditos import obtener_abonos_hoy
            abonos_hoy = obtener_abonos_hoy()
            
            if abonos_hoy:
                total_abonos = len(abonos_hoy)
                monto_total = sum(float(abono['monto_abono']) for abono in abonos_hoy)
                
                # Actualizar resumen
                card1.winfo_children()[1].configure(text=str(total_abonos))
                card2.winfo_children()[1].configure(text=f"${monto_total:.2f}")
                
                # Mostrar cada abono
                for abono in abonos_hoy:
                    self.crear_item_abono_hoy(scroll, abono)
            else:
                # Mensaje si no hay abonos
                ctk.CTkLabel(
                    scroll,
                    text="📅 No se registraron abonos hoy",
                    font=("Segoe UI", 14),
                    text_color="#999999"
                ).pack(expand=True, pady=50)
                
        except Exception as e:
            ctk.CTkLabel(
                scroll,
                text=f"❌ Error al cargar abonos: {str(e)}",
                font=("Segoe UI", 14),
                text_color="#F44336"
            ).pack(expand=True, pady=50)
    
    def crear_item_abono_hoy(self, parent, abono):
        """Crear item de abono del día"""
        item_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        item_frame.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(item_frame, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Fila superior - Crédito y monto
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x")
        
        ctk.CTkLabel(
            top_row,
            text=f"Crédito #{abono.get('id_credito')} - Venta #{abono.get('id_venta', 'N/A')}",
            font=("Segoe UI", 13, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Badge de monto
        monto_badge = ctk.CTkFrame(top_row, fg_color="#4CAF50", corner_radius=15)
        monto_badge.pack(side="right")
        
        ctk.CTkLabel(
            monto_badge,
            text=f"${float(abono['monto_abono']):.2f}",
            font=("Segoe UI", 12, "bold"),
            text_color="white"
        ).pack(padx=15, pady=6)
        
        # Fila inferior - Detalles
        bottom_row = ctk.CTkFrame(content, fg_color="transparent")
        bottom_row.pack(fill="x", pady=(8, 0))
        
        # Hora
        hora = abono['fecha_abono'].strftime("%H:%M") if abono['fecha_abono'] else "-"
        ctk.CTkLabel(
            bottom_row,
            text=f"Hora: {hora}",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(side="left")
        
        # Método de pago
        if abono.get('metodo_pago'):
            ctk.CTkLabel(
                bottom_row,
                text=f"Método: {abono['metodo_pago']}",
                font=("Segoe UI", 11),
                text_color="#666666"
            ).pack(side="left", padx=(20, 0))
        
        # Monto total del crédito
        if abono.get('monto_total'):
            ctk.CTkLabel(
                bottom_row,
                text=f"Total crédito: ${float(abono['monto_total']):.2f}",
                font=("Segoe UI", 11),
                text_color="#666666"
            ).pack(side="right")

    def cargar_datos(self):
        """Cargar créditos desde la base de datos"""
        try:
            from controllers.creditos import obtener_creditos, obtener_resumen_creditos
            self.creditos = obtener_creditos()
            self.resumen = obtener_resumen_creditos()
            self.actualizar_resumen()
            
            # Recargar la tabla si existe
            if hasattr(self, 'content_scroll'):
                self.cargar_creditos_tabla()
        except Exception as e:
            print(f"Error al cargar créditos: {e}")
            self.creditos = []
            self.resumen = {
                'total_creditos': 0,
                'activos': 0,
                'vencidos': 0,
                'total_por_cobrar': 0
            }
    
    def cargar_creditos_tabla(self, filtro_estado="Todos", busqueda=""):
        """Cargar créditos en la tabla con filtros"""
        # Limpiar contenido
        for widget in self.content_scroll.winfo_children():
            widget.destroy()
        
        # Aplicar filtros
        creditos_filtrados = self.creditos.copy()
        
        # Filtro por estado
        if filtro_estado != "Todos":
            if filtro_estado == "Activos":
                creditos_filtrados = [c for c in creditos_filtrados if c['estado'] == 'Activo']
            elif filtro_estado == "Vencidos":
                creditos_filtrados = [c for c in creditos_filtrados if c['estado'] == 'Vencido']
            elif filtro_estado == "Pagados":
                creditos_filtrados = [c for c in creditos_filtrados if c['estado'] == 'Pagado']
        
        # Filtro por búsqueda
        if busqueda:
            creditos_filtrados = [
                c for c in creditos_filtrados 
                if busqueda.lower() in str(c.get('cliente_nombre', '')).lower()
            ]
        
        if not creditos_filtrados:
            mensaje = "📋 No hay créditos"
            if filtro_estado != "Todos" or busqueda:
                mensaje += " que coincidan con los filtros"
            
            ctk.CTkLabel(
                self.content_scroll,
                text=mensaje,
                font=("Segoe UI", 14),
                text_color="#999999"
            ).pack(expand=True, pady=100)
            return
        
        # Mostrar créditos filtrados
        for credito in creditos_filtrados:
            self.crear_fila_credito(credito)
    
    def crear_fila_credito(self, credito):
        """Crear una fila para un crédito con diseño limpio y organizado"""
        # Contenedor principal
        row = ctk.CTkFrame(self.content_scroll, fg_color="white", corner_radius=8, height=70)
        row.pack(fill="x", pady=2, padx=10)
        row.pack_propagate(False)
        
        # Contenido principal
        main_content = ctk.CTkFrame(row, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Lado izquierdo - Información principal
        left_side = ctk.CTkFrame(main_content, fg_color="transparent")
        left_side.pack(side="left", fill="both", expand=True)
        
        # Fila superior - ID y descripción
        top_row = ctk.CTkFrame(left_side, fg_color="transparent")
        top_row.pack(fill="x")
        
        # ID del crédito con badge azul
        id_badge = ctk.CTkFrame(top_row, fg_color="#E3F2FD", corner_radius=12, width=60, height=24)
        id_badge.pack(side="left")
        id_badge.pack_propagate(False)
        
        ctk.CTkLabel(
            id_badge,
            text=f"#{credito['id_credito']}",
            font=("Segoe UI", 10, "bold"),
            text_color="#1976D2"
        ).pack(expand=True)
        
        # Descripción del crédito
        venta_text = f"Venta #{credito['id_venta']}" if credito['id_venta'] else "Sin venta"
        ctk.CTkLabel(
            top_row,
            text=venta_text,
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(side="left", padx=(15, 0))
        
        # Fila inferior - Detalles financieros
        bottom_row = ctk.CTkFrame(left_side, fg_color="transparent")
        bottom_row.pack(fill="x", pady=(8, 0))
        
        # Fecha
        fecha = credito['fecha_credito'].strftime("%d/%m/%Y") if credito['fecha_credito'] else "-"
        ctk.CTkLabel(
            bottom_row,
            text=f"📅 {fecha}",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(side="left")
        
        # Separador
        ctk.CTkLabel(
            bottom_row,
            text="•",
            font=("Segoe UI", 11),
            text_color="#E0E0E0"
        ).pack(side="left", padx=(10, 10))
        
        # Total
        monto_total = float(credito['monto_total'])
        ctk.CTkLabel(
            bottom_row,
            text=f"💰 Total: ${monto_total:.2f}",
            font=("Segoe UI", 11),
            text_color="#E91E63"
        ).pack(side="left")
        
        # Separador
        ctk.CTkLabel(
            bottom_row,
            text="•",
            font=("Segoe UI", 11),
            text_color="#E0E0E0"
        ).pack(side="left", padx=(10, 10))
        
        # Pagado
        monto_pagado = float(credito['monto_pagado'])
        ctk.CTkLabel(
            bottom_row,
            text=f"✅ Pagado: ${monto_pagado:.2f}",
            font=("Segoe UI", 11),
            text_color="#4CAF50"
        ).pack(side="left")
        
        # Separador
        ctk.CTkLabel(
            bottom_row,
            text="•",
            font=("Segoe UI", 11),
            text_color="#E0E0E0"
        ).pack(side="left", padx=(10, 10))
        
        # Saldo
        saldo = float(credito['saldo_pendiente'])
        saldo_color = "#F44336" if saldo > 0 else "#4CAF50"
        ctk.CTkLabel(
            bottom_row,
            text=f"❌ Saldo: ${saldo:.2f}" if saldo > 0 else f"✅ Saldo: ${saldo:.2f}",
            font=("Segoe UI", 11, "bold"),
            text_color=saldo_color
        ).pack(side="left")
        
        # Separador
        ctk.CTkLabel(
            bottom_row,
            text="•",
            font=("Segoe UI", 11),
            text_color="#E0E0E0"
        ).pack(side="left", padx=(10, 10))
        
        # Vencimiento
        vence = credito['fecha_vencimiento'].strftime("%d/%m/%Y") if credito['fecha_vencimiento'] else "-"
        vence_color = "#F44336" if credito['estado'] == 'Vencido' else "#666666"
        ctk.CTkLabel(
            bottom_row,
            text=f"⏰ Vence: {vence}",
            font=("Segoe UI", 11),
            text_color=vence_color
        ).pack(side="left")
        
        # Lado derecho - Estado y botones
        right_side = ctk.CTkFrame(main_content, fg_color="transparent", width=200)
        right_side.pack(side="right")
        right_side.pack_propagate(False)
        
        # Estado
        estado_colors = {
            'Activo': '#4CAF50',
            'Vencido': '#F44336', 
            'Pagado': '#2196F3',
            'Cancelado': '#9E9E9E'
        }
        
        estado_badge = ctk.CTkFrame(right_side, fg_color=estado_colors.get(credito['estado'], '#666666'), corner_radius=15)
        estado_badge.pack(anchor="e", pady=(0, 8))
        
        ctk.CTkLabel(
            estado_badge,
            text=credito['estado'],
            font=("Segoe UI", 11, "bold"),
            text_color="white"
        ).pack(padx=15, pady=6)
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(right_side, fg_color="transparent")
        buttons_frame.pack(anchor="e")
        
        # Solo mostrar botón de abono si no está pagado
        if credito['estado'] in ['Activo', 'Vencido'] and saldo > 0:
            ctk.CTkButton(
                buttons_frame,
                text="💰 Abono",
                fg_color="#4CAF50",
                hover_color="#45a049",
                width=80,
                height=30,
                corner_radius=8,
                font=("Segoe UI", 10, "bold"),
                command=lambda c=credito: self.registrar_abono(c)
            ).pack(side="left", padx=(0, 5))
        
        # Botón de detalles
        ctk.CTkButton(
            buttons_frame,
            text="👁️ Ver",
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=70,
            height=30,
            corner_radius=8,
            font=("Segoe UI", 10),
            command=lambda c=credito: self.ver_detalle_credito(c)
        ).pack(side="left")
    
    def actualizar_resumen(self):
        """Actualizar el resumen de créditos"""
        if hasattr(self, 'resumen'):
            self.total_cobrar_label.configure(text=f"${float(self.resumen['total_por_cobrar']):,.2f}")
            self.creditos_activos_label.configure(text=str(self.resumen['activos']))
            self.creditos_vencidos_label.configure(text=str(self.resumen['vencidos']))
    
    def nuevo_credito(self):
        """Abrir formulario para nuevo crédito"""
        # Crear ventana de nuevo crédito
        credito_window = ctk.CTkToplevel(self)
        credito_window.title("Nuevo Crédito")
        credito_window.geometry("550x700")
        credito_window.transient(self)
        credito_window.grab_set()
        
        # Centrar ventana
        credito_window.update_idletasks()
        x = (credito_window.winfo_screenwidth() // 2) - (550 // 2)
        y = (credito_window.winfo_screenheight() // 2) - (700 // 2)
        credito_window.geometry(f"550x700+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(credito_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="💳 Nuevo Crédito",
            font=("Segoe UI", 22, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Cargar clientes de la base de datos
        try:
            from database.db import crear_conexion
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            # Solo seleccionar columnas que existen
            cursor.execute("SELECT id_cliente, nombre, telefono FROM clientes ORDER BY nombre")
            clientes = cursor.fetchall()
            conn.close()
            
            # Crear diccionario de clientes
            clientes_dict = {}
            clientes_nombres = []
            for cliente in clientes:
                nombre_completo = f"{cliente['nombre']} - {cliente['telefono']}"
                clientes_nombres.append(nombre_completo)
                clientes_dict[nombre_completo] = cliente['id_cliente']
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
            clientes_nombres = []
            clientes_dict = {}
        
        # Cliente (ComboBox)
        ctk.CTkLabel(form_frame, text="Cliente: *", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        
        if clientes_nombres:
            cliente_combo = ctk.CTkComboBox(
                form_frame,
                values=clientes_nombres,
                height=45,
                font=("Segoe UI", 13),
                dropdown_font=("Segoe UI", 12),
                button_color="#E91E63",
                button_hover_color="#C2185B",
                border_color="#E0E0E0"
            )
            cliente_combo.pack(fill="x", pady=(0, 15))
            cliente_combo.set("Selecciona un cliente")
        else:
            # Si no hay clientes, mostrar mensaje
            no_clientes_frame = ctk.CTkFrame(form_frame, fg_color="#FFF3E0", corner_radius=10)
            no_clientes_frame.pack(fill="x", pady=(0, 15))
            
            ctk.CTkLabel(
                no_clientes_frame,
                text="⚠️ No hay clientes registrados\nPrimero debes agregar clientes en la sección de Clientes",
                font=("Segoe UI", 12),
                text_color="#F57C00",
                justify="center"
            ).pack(padx=15, pady=15)
            
            cliente_combo = None
        
        # ID Venta (opcional)
        ctk.CTkLabel(form_frame, text="ID Venta (opcional):", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        venta_entry = ctk.CTkEntry(form_frame, placeholder_text="Dejar vacío si no hay venta asociada", height=45, font=("Segoe UI", 13))
        venta_entry.pack(fill="x", pady=(0, 15))
        
        # Monto
        ctk.CTkLabel(form_frame, text="Monto del Crédito: *", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        monto_entry = ctk.CTkEntry(form_frame, placeholder_text="$0.00", height=45, font=("Segoe UI", 13))
        monto_entry.pack(fill="x", pady=(0, 15))
        
        # Plazo
        ctk.CTkLabel(form_frame, text="Plazo (días): *", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        plazo_entry = ctk.CTkEntry(form_frame, placeholder_text="30", height=45, font=("Segoe UI", 13))
        plazo_entry.pack(fill="x", pady=(0, 15))
        plazo_entry.insert(0, "30")
        
        # Fecha de Vencimiento (calculada automáticamente)
        ctk.CTkLabel(form_frame, text="Fecha de Vencimiento:", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        
        from datetime import timedelta
        fecha_vencimiento_default = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
        
        fecha_venc_entry = ctk.CTkEntry(form_frame, placeholder_text="DD/MM/AAAA", height=45, font=("Segoe UI", 13))
        fecha_venc_entry.pack(fill="x", pady=(0, 15))
        fecha_venc_entry.insert(0, fecha_vencimiento_default)
        
        # Función para actualizar fecha de vencimiento cuando cambia el plazo
        def actualizar_fecha_vencimiento(*args):
            try:
                dias = int(plazo_entry.get())
                nueva_fecha = (datetime.now() + timedelta(days=dias)).strftime("%d/%m/%Y")
                fecha_venc_entry.delete(0, "end")
                fecha_venc_entry.insert(0, nueva_fecha)
            except:
                pass
        
        plazo_entry.bind("<KeyRelease>", actualizar_fecha_vencimiento)
        
        # Tasa de interés
        ctk.CTkLabel(form_frame, text="Tasa de Interés (%):", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        tasa_entry = ctk.CTkEntry(form_frame, placeholder_text="0", height=45, font=("Segoe UI", 13))
        tasa_entry.pack(fill="x", pady=(0, 15))
        tasa_entry.insert(0, "0")
        
        # Notas
        ctk.CTkLabel(form_frame, text="Notas:", font=("Segoe UI", 13, "bold"), text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        notas_entry = ctk.CTkTextbox(form_frame, height=100, font=("Segoe UI", 13))
        notas_entry.pack(fill="x", pady=(0, 15))
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def guardar_credito():
            if not cliente_combo or not clientes_nombres:
                messagebox.showwarning("Sin clientes", "Primero debes registrar clientes en el sistema")
                return
            
            cliente_seleccionado = cliente_combo.get()
            monto = monto_entry.get().strip()
            plazo = plazo_entry.get().strip()
            tasa = tasa_entry.get().strip() or "0"
            notas = notas_entry.get("1.0", "end").strip()
            id_venta = venta_entry.get().strip() or None
            
            if cliente_seleccionado == "Selecciona un cliente" or not monto or not plazo:
                messagebox.showwarning("Datos incompletos", "Por favor completa todos los campos obligatorios (*)")
                return
            
            try:
                id_cliente = clientes_dict[cliente_seleccionado]
                monto_float = float(monto.replace("$", "").replace(",", ""))
                plazo_int = int(plazo)
                tasa_float = float(tasa)
                
                # Validar que el id_venta exista si se proporcionó
                if id_venta:
                    from database.db import crear_conexion
                    conn = crear_conexion()
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_venta FROM ventas WHERE id_venta = %s", (id_venta,))
                    venta_existe = cursor.fetchone()
                    conn.close()
                    
                    if not venta_existe:
                        messagebox.showwarning(
                            "Venta no encontrada",
                            f"No existe una venta con ID #{id_venta}.\n\n"
                            f"Puedes dejar el campo vacío para crear un crédito sin venta asociada."
                        )
                        return
                
                # Guardar en la base de datos
                from controllers.creditos import crear_credito
                id_credito = crear_credito(
                    id_venta=id_venta,
                    id_cliente=id_cliente,
                    monto_total=monto_float,
                    plazo_dias=plazo_int,
                    tasa_interes=tasa_float,
                    notas=notas
                )
                
                if id_credito:
                    messagebox.showinfo(
                        "✅ Crédito Registrado",
                        f"Crédito #{id_credito} registrado exitosamente\n\n"
                        f"Cliente: {cliente_seleccionado.split(' - ')[0]}\n"
                        f"Monto: ${monto_float:,.2f}\n"
                        f"Plazo: {plazo_int} días"
                    )
                    credito_window.destroy()
                    self.cargar_datos()  # Recargar la lista
                else:
                    messagebox.showerror("Error", "No se pudo registrar el crédito")
                
            except ValueError:
                messagebox.showerror("Error", "Monto, plazo y tasa deben ser números válidos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Crédito",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=50,
            font=("Segoe UI", 14, "bold"),
            command=guardar_credito
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=50,
            font=("Segoe UI", 14),
            command=credito_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))




    def registrar_abono(self, credito):
        """Abrir ventana para registrar un abono"""
        abono_window = ctk.CTkToplevel(self)
        abono_window.title("Registrar Abono")
        abono_window.geometry("450x600")
        abono_window.transient(self)
        abono_window.grab_set()
        
        # Centrar ventana
        abono_window.update_idletasks()
        x = (abono_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (abono_window.winfo_screenheight() // 2) - (600 // 2)
        abono_window.geometry(f"450x600+{x}+{y}")
        
        # Contenido principal
        main_frame = ctk.CTkFrame(abono_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(
            main_frame,
            text="💰 Registrar Abono",
            font=("Segoe UI", 22, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 20))
        
        # Información del crédito
        info_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5F5", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            info_content,
            text="Información del Crédito",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        # Detalles del crédito
        saldo_actual = float(credito.get('saldo_pendiente', 0))
        monto_total = float(credito.get('monto_total', 0))
        monto_pagado = float(credito.get('monto_pagado', 0))
        
        detalles = [
            f"Crédito #{credito.get('id_credito')}",
            f"Cliente: {credito.get('cliente_nombre', 'N/A')}",
            f"Monto Total: ${monto_total:.2f}",
            f"Pagado: ${monto_pagado:.2f}",
            f"Saldo Pendiente: ${saldo_actual:.2f}"
        ]
        
        for detalle in detalles:
            ctk.CTkLabel(
                info_content,
                text=detalle,
                font=("Segoe UI", 12),
                text_color="#666666"
            ).pack(anchor="w", pady=2)
        
        # Formulario de abono
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Monto del abono
        ctk.CTkLabel(
            form_frame,
            text="Monto del Abono: *",
            font=("Segoe UI", 13, "bold"),
            text_color="#666666"
        ).pack(anchor="w", pady=(0, 5))
        
        monto_abono_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="$0.00",
            height=45,
            font=("Segoe UI", 13)
        )
        monto_abono_entry.pack(fill="x", pady=(0, 15))
        
        # Botones de monto rápido
        quick_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        quick_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            quick_frame,
            text="Montos rápidos:",
            font=("Segoe UI", 11),
            text_color="#999999"
        ).pack(anchor="w", pady=(0, 5))
        
        buttons_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Botones de montos comunes
        montos_rapidos = [100, 200, 500, saldo_actual]  # Incluir saldo completo
        
        for i, monto in enumerate(montos_rapidos):
            if monto > 0:
                texto = f"${monto:.0f}" if monto != saldo_actual else "Pago Total"
                btn = ctk.CTkButton(
                    buttons_frame,
                    text=texto,
                    fg_color="#E0E0E0",
                    text_color="#666666",
                    hover_color="#D0D0D0",
                    width=80,
                    height=30,
                    font=("Segoe UI", 10),
                    command=lambda m=monto: monto_abono_entry.delete(0, "end") or monto_abono_entry.insert(0, str(m))
                )
                btn.pack(side="left", padx=2)
        
        # Método de pago
        ctk.CTkLabel(
            form_frame,
            text="Método de Pago:",
            font=("Segoe UI", 13, "bold"),
            text_color="#666666"
        ).pack(anchor="w", pady=(0, 5))
        
        metodo_combo = ctk.CTkComboBox(
            form_frame,
            values=["Efectivo", "Tarjeta", "Transferencia", "Cheque"],
            height=45,
            font=("Segoe UI", 13)
        )
        metodo_combo.pack(fill="x", pady=(0, 15))
        metodo_combo.set("Efectivo")
        
        # Notas del abono
        ctk.CTkLabel(
            form_frame,
            text="Notas (opcional):",
            font=("Segoe UI", 13, "bold"),
            text_color="#666666"
        ).pack(anchor="w", pady=(0, 5))
        
        notas_abono_entry = ctk.CTkTextbox(
            form_frame,
            height=80,
            font=("Segoe UI", 13)
        )
        notas_abono_entry.pack(fill="x", pady=(0, 20))
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def guardar_abono():
            monto_str = monto_abono_entry.get().strip()
            metodo = metodo_combo.get()
            notas = notas_abono_entry.get("1.0", "end").strip()
            
            if not monto_str:
                messagebox.showwarning("Datos incompletos", "Por favor ingresa el monto del abono")
                return
            
            try:
                monto_abono = float(monto_str.replace("$", "").replace(",", ""))
                
                if monto_abono <= 0:
                    messagebox.showwarning("Monto inválido", "El monto debe ser mayor a $0.00")
                    return
                
                if monto_abono > saldo_actual:
                    messagebox.showwarning(
                        "Monto excesivo",
                        f"El abono (${monto_abono:.2f}) no puede ser mayor al saldo pendiente (${saldo_actual:.2f})"
                    )
                    return
                
                # Registrar el abono
                from controllers.creditos import registrar_abono
                exito = registrar_abono(
                    id_credito=credito['id_credito'],
                    monto_abono=monto_abono,
                    metodo_pago=metodo,
                    notas=notas
                )
                
                if exito:
                    nuevo_saldo = saldo_actual - monto_abono
                    estado_final = "PAGADO COMPLETAMENTE" if nuevo_saldo <= 0 else f"Saldo restante: ${nuevo_saldo:.2f}"
                    
                    messagebox.showinfo(
                        "✅ Abono Registrado",
                        f"Abono registrado exitosamente\n\n"
                        f"Monto: ${monto_abono:.2f}\n"
                        f"Método: {metodo}\n"
                        f"Estado: {estado_final}"
                    )
                    abono_window.destroy()
                    self.cargar_datos()  # Recargar datos
                else:
                    messagebox.showerror("Error", "No se pudo registrar el abono")
                
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar abono: {str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Registrar Abono",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=50,
            font=("Segoe UI", 14, "bold"),
            command=guardar_abono
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=50,
            font=("Segoe UI", 14),
            command=abono_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def ver_detalle_credito(self, credito):
        """Mostrar ventana con detalles completos del crédito"""
        detalle_window = ctk.CTkToplevel(self)
        detalle_window.title(f"Detalle Crédito #{credito['id_credito']}")
        detalle_window.geometry("600x700")
        detalle_window.transient(self)
        detalle_window.grab_set()
        
        # Centrar ventana
        detalle_window.update_idletasks()
        x = (detalle_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (detalle_window.winfo_screenheight() // 2) - (700 // 2)
        detalle_window.geometry(f"600x700+{x}+{y}")
        
        # Contenido principal
        main_frame = ctk.CTkFrame(detalle_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text=f"📋 Crédito #{credito['id_credito']}",
            font=("Segoe UI", 22, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Estado
        estado_colors = {
            'Activo': '#4CAF50',
            'Vencido': '#F44336',
            'Pagado': '#2196F3',
            'Cancelado': '#9E9E9E'
        }
        
        estado_badge = ctk.CTkFrame(header_frame, fg_color=estado_colors.get(credito['estado'], '#666666'), corner_radius=15)
        estado_badge.pack(side="right")
        
        ctk.CTkLabel(
            estado_badge,
            text=credito['estado'],
            font=("Segoe UI", 12, "bold"),
            text_color="white"
        ).pack(padx=15, pady=8)
        
        # Información del crédito
        info_scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        info_scroll.pack(fill="both", expand=True, pady=(0, 15))
        
        # Información general
        general_frame = ctk.CTkFrame(info_scroll, fg_color="#F5F5F5", corner_radius=10)
        general_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            general_frame,
            text="Información General",
            font=("Segoe UI", 16, "bold"),
            text_color="#333333"
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        # Obtener información del cliente
        try:
            from database.db import crear_conexion
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT nombre, telefono, email FROM clientes WHERE id_cliente = %s", (credito.get('id_cliente'),))
            cliente_info = cursor.fetchone()
            conn.close()
        except:
            cliente_info = None
        
        info_items = [
            ("ID Crédito:", f"#{credito['id_credito']}"),
            ("ID Venta:", f"#{credito['id_venta']}" if credito['id_venta'] else "Sin venta asociada"),
            ("Cliente:", cliente_info['nombre'] if cliente_info else "N/A"),
            ("Teléfono:", cliente_info['telefono'] if cliente_info else "N/A"),
            ("Fecha Crédito:", credito['fecha_credito'].strftime("%d/%m/%Y %H:%M") if credito['fecha_credito'] else "-"),
            ("Fecha Vencimiento:", credito['fecha_vencimiento'].strftime("%d/%m/%Y") if credito['fecha_vencimiento'] else "-"),
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=2)
            
            ctk.CTkLabel(item_frame, text=label, font=("Segoe UI", 12, "bold"), text_color="#666666").pack(side="left")
            ctk.CTkLabel(item_frame, text=value, font=("Segoe UI", 12), text_color="#333333").pack(side="right")
        
        # Separador
        ctk.CTkFrame(general_frame, height=1, fg_color="#E0E0E0").pack(fill="x", padx=20, pady=10)
        
        # Información financiera
        monto_total = float(credito['monto_total'])
        monto_pagado = float(credito['monto_pagado'])
        saldo = float(credito['saldo_pendiente'])
        
        financial_items = [
            ("Monto Total:", f"${monto_total:.2f}", "#E91E63"),
            ("Monto Pagado:", f"${monto_pagado:.2f}", "#4CAF50"),
            ("Saldo Pendiente:", f"${saldo:.2f}", "#F44336" if saldo > 0 else "#4CAF50"),
        ]
        
        for label, value, color in financial_items:
            item_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=2)
            
            ctk.CTkLabel(item_frame, text=label, font=("Segoe UI", 12, "bold"), text_color="#666666").pack(side="left")
            ctk.CTkLabel(item_frame, text=value, font=("Segoe UI", 14, "bold"), text_color=color).pack(side="right")
        
        # Notas si existen
        if credito.get('notas'):
            ctk.CTkFrame(general_frame, height=1, fg_color="#E0E0E0").pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                general_frame,
                text="Notas:",
                font=("Segoe UI", 12, "bold"),
                text_color="#666666"
            ).pack(padx=20, anchor="w")
            
            ctk.CTkLabel(
                general_frame,
                text=credito['notas'],
                font=("Segoe UI", 12),
                text_color="#333333",
                wraplength=500,
                justify="left"
            ).pack(padx=20, pady=(5, 15), anchor="w")
        else:
            ctk.CTkFrame(general_frame, height=15, fg_color="transparent").pack()
        
        # Historial de abonos
        abonos_frame = ctk.CTkFrame(info_scroll, fg_color="#F5F5F5", corner_radius=10)
        abonos_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            abonos_frame,
            text="Historial de Abonos",
            font=("Segoe UI", 16, "bold"),
            text_color="#333333"
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        # Obtener abonos
        try:
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM abonos_creditos 
                WHERE id_credito = %s 
                ORDER BY fecha_abono DESC
            """, (credito['id_credito'],))
            abonos = cursor.fetchall()
            conn.close()
        except:
            abonos = []
        
        if abonos:
            for abono in abonos:
                abono_item = ctk.CTkFrame(abonos_frame, fg_color="white", corner_radius=8)
                abono_item.pack(fill="x", padx=20, pady=5)
                
                abono_content = ctk.CTkFrame(abono_item, fg_color="transparent")
                abono_content.pack(fill="x", padx=15, pady=10)
                
                # Fecha y monto
                top_row = ctk.CTkFrame(abono_content, fg_color="transparent")
                top_row.pack(fill="x")
                
                fecha_abono = abono['fecha_abono'].strftime("%d/%m/%Y %H:%M") if abono['fecha_abono'] else "-"
                ctk.CTkLabel(
                    top_row,
                    text=fecha_abono,
                    font=("Segoe UI", 12, "bold"),
                    text_color="#333333"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    top_row,
                    text=f"${float(abono['monto_abono']):.2f}",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#4CAF50"
                ).pack(side="right")
                
                # Método y notas
                if abono.get('metodo_pago') or abono.get('notas'):
                    bottom_row = ctk.CTkFrame(abono_content, fg_color="transparent")
                    bottom_row.pack(fill="x", pady=(5, 0))
                    
                    if abono.get('metodo_pago'):
                        ctk.CTkLabel(
                            bottom_row,
                            text=f"Método: {abono['metodo_pago']}",
                            font=("Segoe UI", 10),
                            text_color="#666666"
                        ).pack(side="left")
                    
                    if abono.get('notas'):
                        ctk.CTkLabel(
                            bottom_row,
                            text=f"Notas: {abono['notas']}",
                            font=("Segoe UI", 10),
                            text_color="#666666"
                        ).pack(side="right")
        else:
            ctk.CTkLabel(
                abonos_frame,
                text="📋 No hay abonos registrados",
                font=("Segoe UI", 12),
                text_color="#999999"
            ).pack(padx=20, pady=20)
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        # Solo mostrar botón de abono si no está pagado
        if credito['estado'] in ['Activo', 'Vencido'] and saldo > 0:
            ctk.CTkButton(
                btn_frame,
                text="💰 Registrar Abono",
                fg_color="#4CAF50",
                hover_color="#45a049",
                height=45,
                font=("Segoe UI", 13, "bold"),
                command=lambda: (detalle_window.destroy(), self.registrar_abono(credito))
            ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cerrar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=45,
            font=("Segoe UI", 13),
            command=detalle_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def mostrar_gestion_clientes(self):
        """Mostrar tab de Gestión de Clientes"""
        from views.clientes_view import ClientesView
        
        # Crear instancia de la vista de clientes dentro del content_frame
        clientes_view = ClientesView(self.content_frame, self.user)
    def filtrar_creditos(self, estado=None):
        """Filtrar créditos por estado"""
        if not estado:
            estado = self.filtro_estado.get()
        
        # Recargar datos con filtro
        self.cargar_creditos_tabla(filtro_estado=estado)
    
    def buscar_creditos(self, event=None):
        """Buscar créditos por nombre de cliente"""
        termino = self.search_entry.get().strip()
        estado = self.filtro_estado.get()
        
        # Recargar datos con búsqueda
        self.cargar_creditos_tabla(filtro_estado=estado, busqueda=termino)
    
    def generar_reporte(self):
        """Generar reporte de créditos"""
        try:
            from utils.exportar_pandas import generar_reporte_creditos
            archivo = generar_reporte_creditos()
            if archivo:
                messagebox.showinfo(
                    "✅ Reporte Generado",
                    f"Reporte guardado como:\n{archivo}"
                )
            else:
                messagebox.showerror("Error", "No se pudo generar el reporte")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def exportar_creditos(self):
        """Exportar créditos a Excel"""
        try:
            from utils.exportar_pandas import exportar_creditos_excel
            archivo = exportar_creditos_excel()
            if archivo:
                messagebox.showinfo(
                    "✅ Exportación Exitosa",
                    f"Créditos exportados a:\n{archivo}"
                )
            else:
                messagebox.showerror("Error", "No se pudo exportar los créditos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def cargar_alertas(self):
        """Cargar alertas de créditos"""
        # Limpiar alertas anteriores
        for widget in self.alertas_container.winfo_children():
            widget.destroy()
        
        try:
            from controllers.creditos import obtener_alertas_creditos
            alertas = obtener_alertas_creditos()
            
            if alertas:
                for alerta in alertas[:3]:  # Mostrar máximo 3 alertas
                    self.crear_alerta_item(alerta)
            else:
                # Sin alertas
                ctk.CTkLabel(
                    self.alertas_container,
                    text="✅ No hay alertas",
                    font=("Segoe UI", 11),
                    text_color="#4CAF50"
                ).pack(pady=10)
                
        except Exception as e:
            ctk.CTkLabel(
                self.alertas_container,
                text="❌ Error cargando alertas",
                font=("Segoe UI", 11),
                text_color="#F44336"
            ).pack(pady=10)
    
    def crear_alerta_item(self, alerta):
        """Crear item de alerta"""
        alerta_frame = ctk.CTkFrame(self.alertas_container, fg_color="#FFF3E0", corner_radius=8)
        alerta_frame.pack(fill="x", pady=2)
        
        content = ctk.CTkFrame(alerta_frame, fg_color="transparent")
        content.pack(fill="x", padx=10, pady=8)
        
        # Icono según tipo
        iconos = {
            'vencido': '🚨',
            'por_vencer': '⏰',
            'sin_abonos': '💰'
        }
        
        icono = iconos.get(alerta.get('tipo', 'info'), '📋')
        
        ctk.CTkLabel(
            content,
            text=icono,
            font=("Segoe UI", 14)
        ).pack(side="left")
        
        ctk.CTkLabel(
            content,
            text=alerta.get('mensaje', 'Alerta'),
            font=("Segoe UI", 10),
            text_color="#E65100",
            wraplength=200
        ).pack(side="left", padx=(8, 0), fill="x", expand=True)