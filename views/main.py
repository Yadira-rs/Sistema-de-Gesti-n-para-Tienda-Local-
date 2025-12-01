import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import customtkinter as ctk

# Vistas del sistema
from views.dashboard import DashboardView
from views.products_view import ProductsView
from views.apartado import ApartadoView
from views.ventas_view import VentasView
from views.sales_history import SalesHistoryView
from views.users_view import UsersView
from views.categorias import CategoriasView
from views.creditos_view import CreditosView

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
        menu_items = [
            ("📊", "Dashboard", DashboardView),
            ("🛒", "Punto de Venta", VentasView),
            ("📋", "Apartado", ApartadoView),
            ("✓", "Productos", ProductsView),
            ("👥", "Ventas", SalesHistoryView),
            ("👤", "Usuarios", UsersView),
        ]

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
        
        # Separador
        separator = tk.Frame(self.sidebar, bg="#E0E0E0", height=1)
        separator.pack(fill="x", padx=15, pady=20)
        
        # Categorías
        cat_btn = tk.Frame(self.sidebar, bg="#FFFFFF", cursor="hand2")
        cat_btn.pack(fill="x", padx=20, pady=5)
        
        tk.Label(
            cat_btn,
            text="Categorías",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#999999"
        ).pack(side="left")
        
        tk.Label(
            cat_btn,
            text="›",
            font=("Segoe UI", 14),
            bg="#FFFFFF",
            fg="#999999"
        ).pack(side="right")

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
        """Crear perfil de usuario al final del menú"""
        # Espaciador para empujar el perfil al fondo
        spacer = tk.Frame(self.sidebar, bg="#FFFFFF")
        spacer.pack(side="bottom", fill="both", expand=True)
        
        # Frame del perfil (clickeable)
        profile_frame = tk.Frame(self.sidebar, bg="#FFE0E0", height=100, cursor="hand2")
        profile_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        profile_frame.pack_propagate(False)
        
        # Contenido del perfil
        content = tk.Frame(profile_frame, bg="#FFE0E0")
        content.pack(expand=True)
        
        # Icono de usuario
        icon_label = tk.Label(
            content,
            text="👤",
            font=("Segoe UI", 24),
            bg="#FFE0E0",
            fg="#E91E63"
        )
        icon_label.pack()
        
        # Nombre del usuario
        nombre = self.user.get("nombre_completo", self.user.get("usuario", "Administrador"))
        name_label = tk.Label(
            content,
            text=nombre,
            font=("Segoe UI", 11, "bold"),
            bg="#FFE0E0",
            fg="#333333"
        )
        name_label.pack()
        
        # Rol
        rol = self.user.get("rol", "Admin")
        rol_label = tk.Label(
            content,
            text=rol,
            font=("Segoe UI", 9),
            bg="#FFE0E0",
            fg="#666666"
        )
        rol_label.pack()
        
        # Email
        email = self.user.get("email", "admin@janet.com")
        email_label = tk.Label(
            content,
            text=email,
            font=("Segoe UI", 8),
            bg="#FFE0E0",
            fg="#999999"
        )
        email_label.pack()
        
        # Hacer clickeable todo el perfil
        def abrir_perfil(event=None):
            self.mostrar_perfil()
        
        profile_frame.bind("<Button-1>", abrir_perfil)
        content.bind("<Button-1>", abrir_perfil)
        icon_label.bind("<Button-1>", abrir_perfil)
        name_label.bind("<Button-1>", abrir_perfil)
        rol_label.bind("<Button-1>", abrir_perfil)
        email_label.bind("<Button-1>", abrir_perfil)
        
        # Efecto hover
        def on_enter(e):
            profile_frame.configure(bg="#FFD0D0")
            content.configure(bg="#FFD0D0")
            icon_label.configure(bg="#FFD0D0")
            name_label.configure(bg="#FFD0D0")
            rol_label.configure(bg="#FFD0D0")
            email_label.configure(bg="#FFD0D0")
        
        def on_leave(e):
            profile_frame.configure(bg="#FFE0E0")
            content.configure(bg="#FFE0E0")
            icon_label.configure(bg="#FFE0E0")
            name_label.configure(bg="#FFE0E0")
            rol_label.configure(bg="#FFE0E0")
            email_label.configure(bg="#FFE0E0")
        
        profile_frame.bind("<Enter>", on_enter)
        profile_frame.bind("<Leave>", on_leave)
    
    def mostrar_perfil(self):
        """Mostrar ventana de perfil del usuario"""
        import customtkinter as ctk
        
        # Crear ventana modal
        perfil_window = ctk.CTkToplevel(self)
        perfil_window.title("Mi Perfil")
        perfil_window.geometry("450x600")
        perfil_window.transient(self)
        perfil_window.grab_set()
        
        # Centrar ventana
        perfil_window.update_idletasks()
        x = (perfil_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (perfil_window.winfo_screenheight() // 2) - (600 // 2)
        perfil_window.geometry(f"450x600+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(perfil_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Mi Perfil",
            font=("Segoe UI", 24, "bold"),
            text_color="#333333"
        ).pack(pady=(0, 20))
        
        # Icono circular con inicial
        nombre = self.user.get("nombre_completo", self.user.get("usuario", "Administrador"))
        inicial = nombre[0].upper() if nombre else 'A'
        
        icon_frame = ctk.CTkFrame(main_frame, fg_color="#E91E63", corner_radius=50, width=100, height=100)
        icon_frame.pack(pady=(0, 20))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text=inicial,
            font=("Segoe UI", 40, "bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Campos de información
        # Nombre
        ctk.CTkLabel(
            main_frame,
            text="Nombre Completo",
            font=("Segoe UI", 11),
            text_color="#666666",
            anchor="w"
        ).pack(fill="x", pady=(10, 5))
        
        nombre_entry = ctk.CTkEntry(
            main_frame,
            height=40,
            font=("Segoe UI", 12)
        )
        nombre_entry.insert(0, nombre)
        nombre_entry.configure(state="disabled")
        nombre_entry.pack(fill="x")
        
        # Usuario
        ctk.CTkLabel(
            main_frame,
            text="Usuario",
            font=("Segoe UI", 11),
            text_color="#666666",
            anchor="w"
        ).pack(fill="x", pady=(15, 5))
        
        usuario_entry = ctk.CTkEntry(
            main_frame,
            height=40,
            font=("Segoe UI", 12)
        )
        usuario_entry.insert(0, self.user.get("usuario", "admin"))
        usuario_entry.configure(state="disabled")
        usuario_entry.pack(fill="x")
        
        # Email
        ctk.CTkLabel(
            main_frame,
            text="Correo Electrónico",
            font=("Segoe UI", 11),
            text_color="#666666",
            anchor="w"
        ).pack(fill="x", pady=(15, 5))
        
        email_entry = ctk.CTkEntry(
            main_frame,
            height=40,
            font=("Segoe UI", 12)
        )
        email_entry.insert(0, self.user.get("email", "admin@janet.com"))
        email_entry.configure(state="disabled")
        email_entry.pack(fill="x")
        
        # Rol
        ctk.CTkLabel(
            main_frame,
            text="Rol",
            font=("Segoe UI", 11),
            text_color="#666666",
            anchor="w"
        ).pack(fill="x", pady=(15, 5))
        
        rol_entry = ctk.CTkEntry(
            main_frame,
            height=40,
            font=("Segoe UI", 12)
        )
        rol_entry.insert(0, self.user.get("rol", "Administrador"))
        rol_entry.configure(state="disabled")
        rol_entry.pack(fill="x")
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=(30, 0))
        
        ctk.CTkButton(
            buttons_frame,
            text="Cerrar Sesión",
            fg_color="#E53935",
            hover_color="#C62828",
            height=45,
            width=180,
            font=("Segoe UI", 12, "bold"),
            command=lambda: self.cerrar_sesion(perfil_window)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Cerrar",
            fg_color="#E91E63",
            hover_color="#C2185B",
            height=45,
            width=180,
            font=("Segoe UI", 12, "bold"),
            command=perfil_window.destroy
        ).pack(side="left", padx=5)
    
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
        logo_frame = tk.Frame(top, bg="#E3F2FD", width=60, height=60)
        logo_frame.pack(side="left", padx=(0, 10))
        logo_frame.pack_propagate(False)
        
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "WhatsApp Image 2025-11-20 at 10.25.27 AM.jpeg")
        try:
            img = Image.open(path).resize((60, 60))
            self.brand_logo = ImageTk.PhotoImage(img)
            tk.Label(logo_frame, image=self.brand_logo, bg="#E3F2FD").pack(expand=True)
        except Exception:
            tk.Label(logo_frame, text="🚲", font=("Segoe UI", 30), bg="#E3F2FD", fg="#E91E63").pack(expand=True)
        
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
