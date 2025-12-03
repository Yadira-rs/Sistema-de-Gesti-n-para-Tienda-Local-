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
        # Menú base para todos
        menu_items = [
            ("📊", "Dashboard", DashboardView),
            ("🛒", "Punto de Venta", VentasView),
            ("☑️", "Apartado", GestionApartadosView),
            ("📦", "Productos", ProductsView),
            ("👥", "Ventas", HistorialVentasView),
            ("💳", "Créditos", GestionCreditosView),
        ]
        
        # Solo agregar "Usuarios" si es Administrador
        rol = self.user.get("rol", "")
        if rol in ["Administrador", "Admin", "administrador", "admin"]:
            menu_items.append(("👤", "Usuarios", UsersView))

        for icon, text, view in menu_items:
            # Frame para cada botón
            btn_frame = tk.Frame(self.sidebar, bg="#FFFFFF", cursor="hand2")
            btn_frame.pack(fill="x", padx=5, pady=2)
            
            # Crear botón personalizado
            btn = tk.Frame(btn_frame, bg="#FFFFFF", height=45)
            btn.pack(fill="x")
            btn.pack_propagate(False)
            
            # Icono
            icon_label = tk.Label(
                btn,
                text=icon,
                font=("Segoe UI", 16),
                bg="#FFFFFF",
                fg="#333333",
                width=3
            )
            icon_label.pack(side="left", padx=(15, 5))
            
            # Texto
            text_label = tk.Label(
                btn,
                text=text,
                font=("Segoe UI", 12),
                bg="#FFFFFF",
                fg="#333333",
                anchor="w"
            )
            text_label.pack(side="left", fill="x", expand=True)
            
            # Eventos de hover y click
            def on_enter(e, frame=btn):
                frame.configure(bg="#F8BBD0")
                for child in frame.winfo_children():
                    child.configure(bg="#F8BBD0")
            
            def on_leave(e, frame=btn):
                frame.configure(bg="#FFFFFF")
                for child in frame.winfo_children():
                    child.configure(bg="#FFFFFF")
            
            def on_click(e, v=view):
                self.show_view(v)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.bind("<Button-1>", on_click)
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
        """Crear perfil de usuario al final del menú - Diseño minimalista"""
        # Espaciador para empujar el perfil al fondo
        spacer = tk.Frame(self.sidebar, bg="#FFFFFF")
        spacer.pack(side="bottom", fill="both", expand=True)
        
        # Tarjeta de información del usuario con fondo rosa suave
        profile_card = tk.Frame(
            self.sidebar, 
            bg="#FCE4EC",
            height=180,
            cursor="hand2"
        )
        profile_card.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        profile_card.pack_propagate(False)
        
        # Contenedor interno con padding
        card_content = tk.Frame(profile_card, bg="#FCE4EC")
        card_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Obtener datos del usuario
        nombre_completo = self.user.get("nombre_completo", self.user.get("usuario", "Administrador"))
        inicial = nombre_completo[0].upper() if nombre_completo else "A"
        rol = self.user.get("rol", "Admin")
        email = self.user.get("email", "admin@boutique.com")
        
        # Color según rol
        if rol == "Administrador" or rol == "Admin":
            avatar_color = "#E91E63"
        elif rol == "Vendedor":
            avatar_color = "#AB47BC"
        elif rol == "Cajero":
            avatar_color = "#42A5F5"
        else:
            avatar_color = "#66BB6A"
        
        # Avatar circular grande
        avatar_frame = tk.Frame(
            card_content,
            bg="#F8BBD0",
            width=70,
            height=70
        )
        avatar_frame.pack(pady=(0, 12))
        avatar_frame.pack_propagate(False)
        
        avatar_label = tk.Label(
            avatar_frame,
            text=inicial,
            font=("Segoe UI", 32, "bold"),
            bg="#F8BBD0",
            fg=avatar_color
        )
        avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Nombre completo
        nombre_label = tk.Label(
            card_content,
            text=nombre_completo if len(nombre_completo) <= 20 else nombre_completo[:17] + "...",
            font=("Segoe UI", 13, "bold"),
            bg="#FCE4EC",
            fg=avatar_color
        )
        nombre_label.pack(pady=(0, 5))
        
        # Badge de rol con icono
        rol_container = tk.Frame(card_content, bg="#FCE4EC")
        rol_container.pack(pady=(0, 8))
        
        rol_icon = tk.Label(
            rol_container,
            text="🛡️",
            font=("Segoe UI", 12),
            bg="#FCE4EC",
            fg=avatar_color
        )
        rol_icon.pack(side="left", padx=(0, 5))
        
        rol_label = tk.Label(
            rol_container,
            text=rol,
            font=("Segoe UI", 11, "bold"),
            bg="#FCE4EC",
            fg=avatar_color
        )
        rol_label.pack(side="left")
        
        # Email
        email_label = tk.Label(
            card_content,
            text=email if len(email) <= 24 else email[:21] + "...",
            font=("Segoe UI", 9),
            bg="#FCE4EC",
            fg=avatar_color
        )
        email_label.pack()
        
        # Hacer clickeable toda la tarjeta para abrir perfil
        def abrir_perfil(event=None):
            self.mostrar_perfil()
        
        # Bind a todos los elementos
        for widget in [profile_card, card_content, avatar_frame, avatar_label, 
                       nombre_label, rol_container, rol_icon, rol_label, email_label]:
            widget.bind("<Button-1>", abrir_perfil)
        
        # Efecto hover
        def on_enter(e):
            profile_card.configure(bg="#F8BBD0")
            card_content.configure(bg="#F8BBD0")
            avatar_label.configure(bg="#F8BBD0")
            nombre_label.configure(bg="#F8BBD0")
            rol_container.configure(bg="#F8BBD0")
            rol_icon.configure(bg="#F8BBD0")
            rol_label.configure(bg="#F8BBD0")
            email_label.configure(bg="#F8BBD0")
        
        def on_leave(e):
            profile_card.configure(bg="#FCE4EC")
            card_content.configure(bg="#FCE4EC")
            avatar_label.configure(bg="#F8BBD0")
            nombre_label.configure(bg="#FCE4EC")
            rol_container.configure(bg="#FCE4EC")
            rol_icon.configure(bg="#FCE4EC")
            rol_label.configure(bg="#FCE4EC")
            email_label.configure(bg="#FCE4EC")
        
        # Bind hover a todos los elementos
        for widget in [profile_card, card_content, avatar_frame, avatar_label, 
                       nombre_label, rol_container, rol_icon, rol_label, email_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        # Botón de cerrar sesión - Diseño minimalista
        logout_btn = tk.Frame(
            self.sidebar, 
            bg="white",
            height=60,
            cursor="hand2",
            relief="solid",
            borderwidth=2,
            highlightbackground="#E0E0E0",
            highlightthickness=2
        )
        logout_btn.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        logout_btn.pack_propagate(False)
        
        logout_content = tk.Frame(logout_btn, bg="white")
        logout_content.pack(expand=True)
        
        logout_icon = tk.Label(
            logout_content,
            text="➜",
            font=("Segoe UI", 20),
            bg="white",
            fg="#546E7A"
        )
        logout_icon.pack(side="left", padx=(0, 10))
        
        logout_text = tk.Label(
            logout_content,
            text="Cerrar Sesión",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#546E7A"
        )
        logout_text.pack(side="left")
        
        # Hacer clickeable
        def cerrar_sesion_click(event=None):
            self.cerrar_sesion()
        
        logout_btn.bind("<Button-1>", cerrar_sesion_click)
        logout_content.bind("<Button-1>", cerrar_sesion_click)
        logout_icon.bind("<Button-1>", cerrar_sesion_click)
        logout_text.bind("<Button-1>", cerrar_sesion_click)
        
        # Efecto hover
        def logout_on_enter(e):
            logout_btn.configure(bg="#ECEFF1")
            logout_content.configure(bg="#ECEFF1")
            logout_icon.configure(bg="#ECEFF1")
            logout_text.configure(bg="#ECEFF1")
        
        def logout_on_leave(e):
            logout_btn.configure(bg="white")
            logout_content.configure(bg="white")
            logout_icon.configure(bg="white")
            logout_text.configure(bg="white")
        
        logout_btn.bind("<Enter>", logout_on_enter)
        logout_btn.bind("<Leave>", logout_on_leave)
        logout_content.bind("<Enter>", logout_on_enter)
        logout_content.bind("<Leave>", logout_on_leave)
        logout_icon.bind("<Enter>", logout_on_enter)
        logout_icon.bind("<Leave>", logout_on_leave)
        logout_text.bind("<Enter>", logout_on_enter)
        logout_text.bind("<Leave>", logout_on_leave)
    
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
            "logo.png",
            "assets/logo.png",
            "images/logo.png",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "WhatsApp Image 2025-11-20 at 10.25.27 AM.jpeg")
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
        
        # Título
        title_frame = tk.Frame(top, bg="#FFFFFF")
        title_frame.pack(side="left", fill="both", expand=True)
        
        # Janet Rosa Bici con Rosa en color rosa
        title_text = tk.Frame(title_frame, bg="#FFFFFF")
        title_text.pack(anchor="w")
        
        tk.Label(title_text, text="Janet ", font=("Brush Script MT", 16), bg="#FFFFFF", fg="#333333").pack(side="left")
        tk.Label(title_text, text="Rosa ", font=("Brush Script MT", 16), bg="#FFFFFF", fg="#E91E63").pack(side="left")
        tk.Label(title_text, text="Bici", font=("Brush Script MT", 16), bg="#FFFFFF", fg="#333333").pack(side="left")
        
        tk.Label(title_frame, text="Sistema de ventas", font=("Segoe UI", 9), bg="#FFFFFF", fg="#666666").pack(anchor="w")
