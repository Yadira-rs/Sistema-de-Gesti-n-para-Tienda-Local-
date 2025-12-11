import customtkinter as ctk
from tkinter import messagebox
from database.db import crear_conexion

class ClientesView(ctk.CTkFrame):
    """Vista de gestión de clientes"""
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.pack(fill="both", expand=True)
        self.user = user
        self.clientes = []
        
        self.crear_interfaz()
        self.cargar_clientes()
    
    def crear_interfaz(self):
        """Crear interfaz de clientes"""
        # Contenedor principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header,
            text="👥 Gestión de Clientes",
            font=("Segoe UI", 28, "bold"),
            text_color="#333333"
        ).pack(side="left")
        
        # Botón nuevo cliente
        ctk.CTkButton(
            header,
            text="➕ Nuevo Cliente",
            height=45,
            corner_radius=15,
            fg_color="#E91E63",
            hover_color="#C2185B",
            font=("Segoe UI", 14, "bold"),
            command=self.nuevo_cliente
        ).pack(side="right")
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(main_container, fg_color="white", corner_radius=15, height=55)
        search_frame.pack(fill="x", pady=(0, 20))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 18)).pack(side="left", padx=15)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar cliente por nombre, teléfono o email...",
            border_width=0,
            fg_color="white",
            font=("Segoe UI", 14)
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", lambda e: self.buscar_clientes())
        
        # Contenedor de tabla
        table_container = ctk.CTkFrame(main_container, fg_color="white", corner_radius=15)
        table_container.pack(fill="both", expand=True)
        
        # Header de tabla
        header_frame = ctk.CTkFrame(table_container, fg_color="#F5F5F5", corner_radius=15)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        headers = ["ID", "Nombre Completo", "Teléfono", "Email", "Acciones"]
        widths = [60, 300, 120, 200, 150]
        
        for header, width in zip(headers, widths):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Segoe UI", 13, "bold"),
                text_color="#333333",
                width=width
            ).pack(side="left", padx=10, pady=15)
        
        # Área de contenido scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(table_container, fg_color="white")
        self.scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)
    
    def cargar_clientes(self):
        """Cargar clientes desde la base de datos"""
        try:
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_cliente, nombre, telefono, correo as email
                FROM clientes
                ORDER BY nombre
            """)
            self.clientes = cursor.fetchall()
            conn.close()
            
            self.mostrar_clientes()
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los clientes:\n{str(e)}")
    
    def mostrar_clientes(self, clientes=None):
        """Mostrar clientes en la tabla"""
        # Limpiar contenido
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        clientes_mostrar = clientes if clientes is not None else self.clientes
        
        if not clientes_mostrar:
            ctk.CTkLabel(
                self.scroll_frame,
                text="📋 No hay clientes registrados",
                font=("Segoe UI", 16),
                text_color="#999999"
            ).pack(expand=True, pady=100)
            return
        
        # Mostrar cada cliente
        for cliente in clientes_mostrar:
            self.crear_fila_cliente(cliente)
    
    def crear_fila_cliente(self, cliente):
        """Crear una fila para un cliente"""
        row = ctk.CTkFrame(self.scroll_frame, fg_color="white")
        row.pack(fill="x", pady=2, padx=5)
        
        widths = [60, 150, 150, 120, 200, 150]
        
        # ID
        ctk.CTkLabel(
            row,
            text=str(cliente['id_cliente']),
            font=("Segoe UI", 12),
            width=widths[0]
        ).pack(side="left", padx=10)
        
        # Nombre Completo
        ctk.CTkLabel(
            row,
            text=cliente['nombre'] or "-",
            font=("Segoe UI", 12, "bold"),
            text_color="#333333",
            width=widths[1],
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Teléfono
        ctk.CTkLabel(
            row,
            text=cliente['telefono'] or "-",
            font=("Segoe UI", 12),
            text_color="#666666",
            width=widths[2]
        ).pack(side="left", padx=10)
        
        # Email
        email_text = cliente.get('email', "-") or "-"
        if len(email_text) > 25:
            email_text = email_text[:22] + "..."
        
        ctk.CTkLabel(
            row,
            text=email_text,
            font=("Segoe UI", 12),
            text_color="#666666",
            width=widths[3],
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(row, fg_color="transparent", width=widths[4])
        actions_frame.pack(side="left", padx=10)
        actions_frame.pack_propagate(False)
        
        # Botón editar
        ctk.CTkButton(
            actions_frame,
            text="✏️",
            width=35,
            height=35,
            corner_radius=10,
            fg_color="#2196F3",
            hover_color="#1976D2",
            font=("Segoe UI", 14),
            command=lambda c=cliente: self.editar_cliente(c)
        ).pack(side="left", padx=2)
        
        # Botón eliminar
        ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=35,
            height=35,
            corner_radius=10,
            fg_color="#F44336",
            hover_color="#D32F2F",
            font=("Segoe UI", 14),
            command=lambda c=cliente: self.eliminar_cliente(c)
        ).pack(side="left", padx=2)
    
    def buscar_clientes(self):
        """Buscar clientes por texto"""
        texto = self.search_entry.get().lower().strip()
        
        if not texto:
            self.mostrar_clientes()
            return
        
        clientes_filtrados = [
            c for c in self.clientes
            if texto in (c['nombre'] or "").lower()
            or texto in (c['telefono'] or "").lower()
            or texto in (c.get('email', "") or "").lower()
        ]
        
        self.mostrar_clientes(clientes_filtrados)
    
    def nuevo_cliente(self):
        """Abrir formulario para nuevo cliente"""
        self.abrir_formulario_cliente()
    
    def editar_cliente(self, cliente):
        """Editar un cliente existente"""
        self.abrir_formulario_cliente(cliente)
    
    def abrir_formulario_cliente(self, cliente=None):
        """Abrir formulario de cliente (nuevo o editar)"""
        # Crear ventana
        form_window = ctk.CTkToplevel(self)
        form_window.title("Editar Cliente" if cliente else "Nuevo Cliente")
        form_window.geometry("500x600")
        form_window.transient(self)
        form_window.grab_set()
        
        # Centrar ventana
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (form_window.winfo_screenheight() // 2) - (600 // 2)
        form_window.geometry(f"500x600+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(form_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Título
        titulo = "✏️ Editar Cliente" if cliente else "➕ Nuevo Cliente"
        ctk.CTkLabel(
            main_frame,
            text=titulo,
            font=("Segoe UI", 22, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 25))
        
        # Formulario
        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Nombre Completo
        ctk.CTkLabel(form_frame, text="Nombre Completo: *", font=("Segoe UI", 13, "bold"), 
                    text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre completo del cliente", 
                                    height=45, font=("Segoe UI", 13))
        nombre_entry.pack(fill="x", pady=(0, 15))
        if cliente:
            nombre_entry.insert(0, cliente['nombre'] or "")
        
        # Teléfono con validación
        ctk.CTkLabel(form_frame, text="Teléfono: * (10 dígitos)", font=("Segoe UI", 13, "bold"), 
                    text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        telefono_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 6181234567", 
                                     height=45, font=("Segoe UI", 13))
        telefono_entry.pack(fill="x", pady=(0, 15))
        
        # Validación: solo números y máximo 10 dígitos
        def validar_telefono(event):
            texto = telefono_entry.get()
            # Eliminar cualquier caracter que no sea número
            texto_limpio = ''.join(filter(str.isdigit, texto))
            # Limitar a 10 dígitos
            if len(texto_limpio) > 10:
                texto_limpio = texto_limpio[:10]
            # Actualizar el campo si cambió
            if texto != texto_limpio:
                telefono_entry.delete(0, 'end')
                telefono_entry.insert(0, texto_limpio)
        
        telefono_entry.bind('<KeyRelease>', validar_telefono)
        
        if cliente:
            telefono_entry.insert(0, cliente['telefono'] or "")
        
        # Email (correo)
        ctk.CTkLabel(form_frame, text="Email:", font=("Segoe UI", 13, "bold"), 
                    text_color="#666666", anchor="w").pack(anchor="w", pady=(0, 5))
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="correo@ejemplo.com", 
                                  height=45, font=("Segoe UI", 13))
        email_entry.pack(fill="x", pady=(0, 15))
        if cliente:
            email_entry.insert(0, cliente.get('email', "") or "")
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def guardar():
            nombre = nombre_entry.get().strip()
            telefono = telefono_entry.get().strip()
            email = email_entry.get().strip()
            
            if not nombre or not telefono:
                messagebox.showwarning("Datos incompletos", 
                                     "Nombre y teléfono son obligatorios")
                return
            
            # Validar que el teléfono tenga exactamente 10 dígitos
            if len(telefono) != 10 or not telefono.isdigit():
                messagebox.showwarning("Teléfono inválido", 
                                     "El teléfono debe tener exactamente 10 dígitos numéricos")
                return
            
            try:
                conn = crear_conexion()
                cursor = conn.cursor()
                
                if cliente:
                    # Actualizar (sin dirección)
                    cursor.execute("""
                        UPDATE clientes 
                        SET nombre = %s, telefono = %s, correo = %s
                        WHERE id_cliente = %s
                    """, (nombre, telefono, email, cliente['id_cliente']))
                    mensaje = "Cliente actualizado correctamente"
                else:
                    # Insertar (sin dirección)
                    cursor.execute("""
                        INSERT INTO clientes (nombre, telefono, correo)
                        VALUES (%s, %s, %s)
                    """, (nombre, telefono, email))
                    mensaje = "Cliente registrado correctamente"
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", f"✅ {mensaje}")
                form_window.destroy()
                self.cargar_clientes()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el cliente:\n{str(e)}")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Guardar",
            fg_color="#4CAF50",
            hover_color="#45a049",
            height=50,
            font=("Segoe UI", 14, "bold"),
            command=guardar
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            height=50,
            font=("Segoe UI", 14),
            command=form_window.destroy
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))
    
    def eliminar_cliente(self, cliente):
        """Eliminar un cliente"""
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar al cliente?\n\n"
            f"{cliente['nombre']}\n"
            f"Teléfono: {cliente['telefono']}\n\n"
            f"Esta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                conn = crear_conexion()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (cliente['id_cliente'],))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "✅ Cliente eliminado correctamente")
                self.cargar_clientes()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente:\n{str(e)}")
