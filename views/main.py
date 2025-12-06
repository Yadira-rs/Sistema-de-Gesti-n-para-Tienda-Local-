import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import customtkinter as ctk

# Vistas del sistema
from views.dashboard import DashboardView
from views.products_view import ProductsView
from views.gestion_apartados_view import GestionApartadosView
from views.ventas_view import VentasView
from views.historial_ventas_view import HistorialVentasView
from views.users_view import UsersView
from views.gestion_creditos_view import GestionCreditosView
from views.perfil_view import PerfilView

class MainApp(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title("Janet Rosa Bici - Sistema de Ventas")
        self.geometry("1400x800")
        self.user = user

        self.configure(bg="#F5F5F5")

        self.setup_style()

        # ---- Panel lateral ----
        self.sidebar = tk.Frame(self, bg="#FFFFFF", width=230)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self, bg="#F5F5F5")
        self.content.pack(side="right", fill="both", expand=True)

        self.create_brand()
        self.create_menu()
        self.create_user_profile()

        self.show_view(DashboardView)

    # -----------------------------------------------------
    def create_menu(self):
        """Crear menú de navegación"""
        # Diccionario para guardar referencias a los botones
        self.menu_buttons = {}
        self.current_view = None
        
        # Verificar si es administrador
        rol = self.user.get("rol", "")
        email = self.user.get("email", "").lower()
        print("\n" + "="*50)
        print(f"DEBUG - Información del usuario:")
        print(f"Usuario: {self.user.get('nombre', 'Desconocido')}")
        print(f"Email: {email}")
        print(f"Rol: '{rol}'")
        
        # Solo el correo de administrador específico puede ser admin
        es_admin = False
        if rol and email == "janet.rb00@gmail.com":
            rol_lower = str(rol).strip().lower()
            print(f"Rol (en minúsculas): '{rol_lower}'")
            es_admin = "admin" in rol_lower
        
        print(f"¿Es administrador? {es_admin}")
        print("="*50 + "\n")
        
        # Menú base para todos
        menu_items = [
            ("📊", "Dashboard", DashboardView),
            ("🛒", "Punto de Venta", VentasView),
            ("📝", "Apartado", GestionApartadosView),
            ("📦", "Productos", ProductsView),
            ("📋", "Ventas", HistorialVentasView),
            ("💳", "Créditos", GestionCreditosView),
        ]
        
        # Agregar menú de administración si es administrador
        if es_admin:
            menu_items.append(("👥", "Usuarios", UsersView))
            print("DEBUG - Opción 'Usuarios' agregada al menú")  # Para depuración

        for icon, text, view in menu_items:
            # Frame para cada botón
            btn_frame = tk.Frame(self.sidebar, bg="#FFFFFF", cursor="hand2")
            btn_frame.pack(fill="x", padx=8, pady=3)
            
            # Crear botón personalizado
            btn = tk.Frame(btn_frame, bg="#FFFFFF", height=35)
            btn.pack(fill="x")
            btn.pack_propagate(False)
            
            # Contenedor para centrar verticalmente
            content_frame = tk.Frame(btn, bg="#FFFFFF")
            content_frame.place(relx=0, rely=0.5, anchor="w", relwidth=1)
            
            # Configuración de columnas
            content_frame.columnconfigure(0, weight=0, minsize=40)  # Para el ícono
            content_frame.columnconfigure(1, weight=1)  # Para el texto
            
            # Icono
            icon_label = tk.Label(
                content_frame,
                text=icon,
                font=("Segoe UI", 14, "bold"),
                bg="#FFFFFF",
                fg="#333333",
                width=2,
                anchor="center"
            )
            icon_label.grid(row=0, column=0, padx=(10, 5), sticky="")

            # Texto al lado del icono
            text_label = tk.Label(
                content_frame,
                text=text,
                font=("Segoe UI", 12),
                bg="#FFFFFF",
                fg="#333333",
                anchor="w",
                justify="left",
                wraplength=180,
                padx=5
            )
            text_label.grid(row=0, column=1, sticky="w")
            content_frame.grid_columnconfigure(1, weight=1)
            
            # Guardar referencia al botón
            self.menu_buttons[view] = {
                'frame': btn,
                'content': content_frame,
                'icon': icon_label,
                'text': text_label
            }
            
            # Eventos de hover y click
            def on_enter(e, frame=btn, content=content_frame, v=view):
                if self.current_view != v:
                    hover_bg = "#F48FB1"
                    frame.configure(bg=hover_bg)
                    content.configure(bg=hover_bg)
                    for child in content.winfo_children():
                        # Keep icon visible; only change text color on active
                        try:
                            child.configure(bg=hover_bg)
                        except Exception:
                            pass
            
            def on_leave(e, frame=btn, content=content_frame, v=view):
                if self.current_view != v:
                    frame.configure(bg="#FFFFFF")
                    content.configure(bg="#FFFFFF")
                    for child in content.winfo_children():
                        try:
                            child.configure(bg="#FFFFFF")
                            # restore default fg for text/icon
                            child.configure(fg="#333333")
                        except Exception:
                            pass
            
            def on_click(e, v=view):
                self.show_view(v)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.bind("<Button-1>", on_click)
            content_frame.bind("<Enter>", on_enter)
            content_frame.bind("<Leave>", on_leave)
            content_frame.bind("<Button-1>", on_click)
            icon_label.bind("<Enter>", on_enter)
            icon_label.bind("<Leave>", on_leave)
            icon_label.bind("<Button-1>", on_click)
            text_label.bind("<Enter>", on_enter)
            text_label.bind("<Leave>", on_leave)
            text_label.bind("<Button-1>", on_click)

    # -----------------------------------------------------
    def show_view(self, view_class):
        """Mostrar vista en el panel de contenido"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Actualizar el botón activo
        self.update_active_button(view_class)
        
        try:
            view = view_class(self.content, self.user)
            view.pack(fill="both", expand=True)
                
        except Exception as e:
            # Mostrar error
            self.deiconify()  # Asegurar que la ventana principal esté visible
            
            # Limpiar contenido
            for widget in self.content.winfo_children():
                widget.destroy()
            
            fallback = ttk.Frame(self.content)
            fallback.pack(fill="both", expand=True)
            
            ttk.Label(fallback, text="❌ Error al cargar la vista", font=("Segoe UI", 16, "bold"), foreground="red").pack(pady=20)
            
            # Mostrar mensaje de error
            error_frame = ttk.Frame(fallback)
            error_frame.pack(fill="both", expand=True, padx=40, pady=10)
            
            ttk.Label(error_frame, text="Detalles del error:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
            
            error_text = tk.Text(error_frame, height=10, wrap="word", font=("Consolas", 9))
            error_text.pack(fill="both", expand=True)
            error_text.insert("1.0", str(e))
            error_text.config(state="disabled")
            
            # Botones
            btn_frame = ttk.Frame(fallback)
            btn_frame.pack(pady=20)
            
            ttk.Button(btn_frame, text="🔄 Reintentar", command=lambda: self.show_view(view_class)).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="🏠 Volver al Dashboard", command=lambda: self.show_view(DashboardView)).pack(side="left", padx=5)
            
            # Imprimir error en consola para debug
            import traceback
            print("\n" + "="*60)
            print(f"❌ ERROR AL CARGAR VISTA: {view_class.__name__}")
            print("="*60)
            print(f"Error: {e}")
            print("\nTraceback completo:")
            traceback.print_exc()
            print("="*60 + "\n")

    def create_user_profile(self):
        """Crear perfil de usuario al final del menú - Diseño horizontal compacto"""
        # Espaciador para empujar el perfil al fondo
        spacer = tk.Frame(self.sidebar, bg="#FFFFFF")
        spacer.pack(side="bottom", fill="both", expand=True)
        
        # Obtener datos del usuario
        nombre_completo = self.user.get("nombre_completo", self.user.get("usuario", "Administrador"))
        inicial = nombre_completo[0].upper() if nombre_completo else "A"
        rol = self.user.get("rol", "Admin")
        
        # Color según rol (flexible para variaciones)
        rol_lower = rol.lower()
        if "admin" in rol_lower:
            avatar_color = "#E91E63"
            bg_color = "#FCE4EC"
        elif "vendedor" in rol_lower:
            avatar_color = "#9C27B0"
            bg_color = "#F3E5F5"
        else:
            avatar_color = "#4CAF50"
            bg_color = "#E8F5E9"
        
        # Botón de perfil horizontal compacto
        profile_btn = tk.Frame(
            self.sidebar,
            bg=bg_color,
            height=75,
            cursor="hand2"
        )
        profile_btn.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        profile_btn.pack_propagate(False)
        
        # Contenedor interno centrado
        btn_content = tk.Frame(profile_btn, bg=bg_color)
        btn_content.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)
        
        # Avatar circular a la izquierda
        avatar_canvas = tk.Canvas(
            btn_content,
            width=50,
            height=50,
            bg=bg_color,
            highlightthickness=0
        )
        avatar_canvas.pack(side="left", padx=(0, 12))
        
        # Dibujar círculo
        avatar_canvas.create_oval(2, 2, 48, 48, fill=avatar_color, outline="")
        
        # Texto centrado en el círculo
        avatar_canvas.create_text(
            25, 25,
            text=inicial,
            font=("Segoe UI", 20, "bold"),
            fill="white"
        )
        
        # Información del usuario a la derecha
        info_frame = tk.Frame(btn_content, bg=bg_color)
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Nombre (ajustar longitud según ancho disponible)
        nombre_mostrar = nombre_completo
        if len(nombre_completo) > 16:
            nombre_mostrar = nombre_completo[:13] + "..."
        
        nombre_label = tk.Label(
            info_frame,
            text=nombre_mostrar,
            font=("Segoe UI", 11, "bold"),
            bg=bg_color,
            fg="#333333",
            anchor="w"
        )
        nombre_label.pack(anchor="w", pady=(2, 0))
        
        # Rol
        rol_label = tk.Label(
            info_frame,
            text=f" {rol}",
            font=("Segoe UI", 9),
            bg=bg_color,
            fg=avatar_color,
            anchor="w"
        )
        rol_label.pack(anchor="w", pady=(0, 2))
        
        # Hacer clickeable
        def abrir_perfil(event=None):
            self.mostrar_perfil()
        
        for widget in [profile_btn, btn_content, avatar_canvas, 
                       info_frame, nombre_label, rol_label]:
            widget.bind("<Button-1>", abrir_perfil)
        
        # Efecto hover
        def on_enter(e):
            hover_color = {
                "#FCE4EC": "#F8BBD0",
                "#F3E5F5": "#E1BEE7",
                "#E3F2FD": "#BBDEFB",
                "#E8F5E9": "#C8E6C9"
            }.get(bg_color, "#F8BBD0")
            
            profile_btn.configure(bg=hover_color)
            btn_content.configure(bg=hover_color)
            avatar_canvas.configure(bg=hover_color)
            info_frame.configure(bg=hover_color)
            nombre_label.configure(bg=hover_color)
            rol_label.configure(bg=hover_color)
        
        def on_leave(e):
            profile_btn.configure(bg=bg_color)
            btn_content.configure(bg=bg_color)
            avatar_canvas.configure(bg=bg_color)
            info_frame.configure(bg=bg_color)
            nombre_label.configure(bg=bg_color)
            rol_label.configure(bg=bg_color)
        
        for widget in [profile_btn, btn_content, avatar_canvas, 
                       info_frame, nombre_label, rol_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        # Botón de cerrar sesión compacto
        import customtkinter as ctk
        
        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪  Cerrar Sesión",
            height=50,
            corner_radius=15,
            fg_color="#FFFFFF",
            text_color="#E53935",
            hover_color="#FFEBEE",
            border_width=2,
            border_color="#FFCDD2",
            font=("Segoe UI", 13, "bold"),
            command=self.cerrar_sesion
        )
        logout_btn.pack(side="bottom", fill="x", padx=10, pady=(15, 10))
    
    def mostrar_perfil(self):
        """Mostrar ventana de perfil del usuario"""
        import customtkinter as ctk
        
        # Crear ventana modal más grande
        perfil_window = ctk.CTkToplevel(self)
        perfil_window.title("Mi Perfil - Janet Rosa Bici")
        perfil_window.geometry("1000x650")
        perfil_window.transient(self)
        perfil_window.grab_set()
        
        # Centrar ventana
        perfil_window.update_idletasks()
        x = (perfil_window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (perfil_window.winfo_screenheight() // 2) - (650 // 2)
        perfil_window.geometry(f"1000x650+{x}+{y}")
        
        # Usar la nueva vista de perfil moderna
        perfil_view = PerfilView(perfil_window, self.user)
        
        # Sobrescribir el método cerrar_sesion de la vista
        def cerrar_sesion_custom():
            perfil_window.destroy()
            self.cerrar_sesion()
        
        perfil_view.cerrar_sesion = cerrar_sesion_custom
    
    def cerrar_sesion(self, ventana_perfil=None):
        """Cerrar sesión y volver al login"""
        if ventana_perfil:
            ventana_perfil.destroy()
        
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?"):
            self.destroy()
            from views.login import LoginWindow
            app = LoginWindow()
            app.mainloop()
    
    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("vista")
        except Exception:
            pass
        style.configure("Sidebar.TButton", font=("Segoe UI", 11), foreground="#333", padding=12)
        style.map("Sidebar.TButton", background=[("active", "#F9D7DD")])
        # Ajustes para Treeview: evitar el color amarillo por defecto en selección
        style.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF", foreground="#000000")
        style.map("Treeview",
              background=[('selected', '#F9D7DD')],
              foreground=[('selected', '#000000')])
        style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), foreground="#FFFFFF", background="#E48CA6", padding=10)
        style.map("Primary.TButton", background=[["active", "#D97393"]])
        style.configure("Chip.TButton", foreground="#B2334A", background="#F9D7DD", padding=6)
        style.map("Chip.TButton", background=[["active", "#F3C3CC"]])
        style.configure("ChipSelected.TButton", foreground="#FFFFFF", background="#B2334A", padding=6)
        style.map("ChipSelected.TButton", background=[["active", "#99233D"]])
        style.configure("Pay.TRadiobutton", background="#FFFFFF")

    def update_active_button(self, view_class):
        """Actualizar el botón activo en el menú"""
        # Resetear todos los botones
        for view, widgets in self.menu_buttons.items():
            widgets['frame'].configure(bg="#FFFFFF")
            widgets['content'].configure(bg="#FFFFFF")
            widgets['icon'].configure(bg="#FFFFFF", fg="#333333")
            widgets['text'].configure(bg="#FFFFFF", fg="#333333", font=("Segoe UI", 12))
        
        # Resaltar el botón activo
        if view_class in self.menu_buttons:
            self.current_view = view_class
            widgets = self.menu_buttons[view_class]
            widgets['frame'].configure(bg="#E91E63")
            widgets['content'].configure(bg="#E91E63")
            widgets['icon'].configure(bg="#E91E63", fg="white")
            widgets['text'].configure(bg="#E91E63", fg="white", font=("Segoe UI", 12, "bold"))
    
    def create_brand(self):
        """Crear header del menú con logo y título"""
        top = tk.Frame(self.sidebar, bg="#FFFFFF")
        top.pack(fill="x", padx=15, pady=20)
        
        # Logo
        logo_frame = tk.Frame(top, bg="#FFFFFF", width=60, height=60)
        logo_frame.pack(side="left", padx=(0, 10))
        logo_frame.pack_propagate(False)
        
        # Intentar cargar el logo desde diferentes ubicaciones
        logo_paths = [
            "WhatsApp Image 2025-12-02 at 11.52.41 AM.jpeg",
            "logo.png",
            "assets/logo.png",
            "images/logo.png",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "WhatsApp Image 2025-11-20 at 10.25.27 AM.jpeg"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "WhatsApp Image 2025-12-02 at 11.52.41 AM.jpeg")
        ]
        
        logo_loaded = False
        for path in logo_paths:
            try:
                if os.path.exists(path):
                    img = Image.open(path).resize((60, 60), Image.Resampling.LANCZOS)
                    self.brand_logo = ImageTk.PhotoImage(img)
                    tk.Label(logo_frame, image=self.brand_logo, bg="#FFFFFF").pack(expand=True)
                    logo_loaded = True
                    break
            except Exception:
                continue
        
        # Si no se cargó ninguna imagen, usar emoji
        if not logo_loaded:
            tk.Label(logo_frame, text="🚲", font=("Segoe UI", 30), bg="#FFFFFF", fg="#E91E63").pack(expand=True)
        
        # Título (centrado)
        title_frame = tk.Frame(top, bg="#FFFFFF")
        title_frame.pack(side="left", fill="both", expand=True)

        # Center the brand: logo + text stacked and centered
        title_text = tk.Frame(title_frame, bg="#FFFFFF")
        title_text.pack(anchor="center")

        tk.Label(title_text, text="Janet ", font=("Brush Script MT", 18), bg="#FFFFFF", fg="#333333").pack(side="left")
        tk.Label(title_text, text="Rosa ", font=("Brush Script MT", 18), bg="#FFFFFF", fg="#E91E63").pack(side="left")
        tk.Label(title_text, text="Bici", font=("Brush Script MT", 18), bg="#FFFFFF", fg="#333333").pack(side="left")

        tk.Label(title_frame, text="Sistema de ventas", font=("Segoe UI", 9), bg="#FFFFFF", fg="#666666").pack(anchor="center", pady=(2,0))
