import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class GestionCreditosView(ctk.CTk):
    def __init__(self, usuario=None):
        super().__init__()
        self.title("Janet Rosa Bici - Ventas a Crédito")
        self.geometry("1400x800")
        ctk.set_appearance_mode("light")
        
        self.usuario = usuario or {"nombre_completo": "Administrador", "email": "admin@janet.com"}
        self.creditos = []
        self.tab_actual = "Control de Ventas a Crédito"
        
        self.crear_interfaz()
        self.cargar_datos()
    
    def crear_interfaz(self):
        # Contenedor principal
        main = ctk.CTkFrame(self, fg_color="#F5F5F5")
        main.pack(fill="both", expand=True)
        
        # Sidebar izquierdo
        self.crear_sidebar(main)
        
        # Panel principal
        self.crear_panel_principal(main)

    def crear_sidebar(self, parent):
        """Menú lateral izquierdo"""
        sidebar = ctk.CTkFrame(parent, width=220, fg_color="white")
        sidebar.pack(side="left", fill="y", padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        # Logo y título
        logo_frame = ctk.CTkFrame(sidebar, fg_color="white")
        logo_frame.pack(pady=(20, 10))
        
        ctk.CTkLabel(logo_frame, text="🚲", font=("Segoe UI", 30), text_color="#E91E63").pack()
        
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack()
        
        ctk.CTkLabel(title_frame, text="Janet ", font=("Brush Script MT", 20), text_color="#333333").pack(side="left")
        ctk.CTkLabel(title_frame, text="Rosa ", font=("Brush Script MT", 20), text_color="#E91E63").pack(side="left")
        ctk.CTkLabel(title_frame, text="Bici", font=("Brush Script MT", 20), text_color="#333333").pack(side="left")
        
        ctk.CTkLabel(sidebar, text="Sistema de ventas", font=("Segoe UI", 11), text_color="#666666").pack(pady=(0, 20))
        
        # Menú de navegación
        menu_items = [
            ("📊", "Dashboard"),
            ("🛒", "Punto de Venta"),
            ("📋", "Apartado"),
            ("📦", "Inventario"),
            ("💰", "Ventas"),
            ("👥", "Usuarios")
        ]
        
        for icon, text in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icon}  {text}",
                fg_color="transparent",
                text_color="#333333",
                hover_color="#F8BBD0",
                anchor="w",
                height=40,
                font=("Segoe UI", 12)
            )
            btn.pack(fill="x", padx=10, pady=2)
        
        # Categorías
        ctk.CTkLabel(sidebar, text="Categorías  ›", font=("Segoe UI", 12), text_color="#666666", anchor="w").pack(fill="x", padx=15, pady=(30, 10))
        
        # Usuario info al final
        user_frame = ctk.CTkFrame(sidebar, fg_color="#FFF0F5", corner_radius=10)
        user_frame.pack(side="bottom", fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(user_frame, text="👤", font=("Segoe UI", 20), text_color="#E91E63").pack(pady=(10, 5))
        ctk.CTkLabel(user_frame, text=self.usuario.get("nombre_completo", "Administrador"), 
                    font=("Segoe UI", 12, "bold"), text_color="#333333").pack()
        ctk.CTkLabel(user_frame, text="Admin", font=("Segoe UI", 10), text_color="#666666").pack()
        ctk.CTkLabel(user_frame, text=self.usuario.get("email", "admin@janet.com"), 
                    font=("Segoe UI", 9), text_color="#999999").pack(pady=(0, 10))

    def crear_panel_principal(self, parent):
        """Panel principal con créditos"""
        panel = ctk.CTkFrame(parent, fg_color="#F5F5F5")
        panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
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
            "Abonos de Hoy"
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
                font=("Segoe UI", 11),
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

    def mostrar_control_creditos(self):
        """Mostrar tab de Control de Ventas a Crédito"""
        # Contenedor principal dividido
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Panel izquierdo - Tabla
        left_panel = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Header de la tabla
        header_frame = ctk.CTkFrame(left_panel, fg_color="#F5F5F5")
        header_frame.pack(fill="x", padx=0, pady=0)
        
        headers = ["☑", "#", "Crédito", "Serie", "Venta", "Días", "Vence", "Pasó", "Monto"]
        widths = [40, 60, 100, 80, 80, 60, 100, 60, 100]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Segoe UI", 11, "bold"),
                text_color="#333333",
                width=width
            )
            label.pack(side="left", padx=5, pady=12)
        
        # Área de contenido
        content_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="white")
        content_scroll.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Mensaje si no hay datos
        ctk.CTkLabel(
            content_scroll,
            text="No se registraron abonos hoy",
            font=("Segoe UI", 14),
            text_color="#999999"
        ).pack(expand=True, pady=100)
        
        # Panel derecho - Acciones y Resumen
        right_panel = ctk.CTkFrame(main_container, fg_color="transparent", width=300)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # Botones de acción
        ctk.CTkButton(
            right_panel,
            text="+ Nuevo Crédito",
            fg_color="#F06292",
            hover_color="#E91E63",
            corner_radius=10,
            height=45,
            font=("Segoe UI", 13, "bold"),
            command=self.nuevo_credito
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(
            right_panel,
            text="Actualizar Lista",
            fg_color="white",
            text_color="#666666",
            border_width=2,
            border_color="#E0E0E0",
            hover_color="#F5F5F5",
            corner_radius=10,
            height=45,
            font=("Segoe UI", 12),
            command=self.cargar_datos
        ).pack(fill="x", pady=(0, 20))
        
        # Resumen
        resumen_frame = ctk.CTkFrame(right_panel, fg_color="white", corner_radius=10)
        resumen_frame.pack(fill="x")
        
        ctk.CTkLabel(
            resumen_frame,
            text="Resumen",
            font=("Segoe UI", 14, "bold"),
            text_color="#333333"
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        # Total Por Cobrar
        total_frame = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        total_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(total_frame, text="Total Por Cobrar", font=("Segoe UI", 11), 
                    text_color="#666666").pack(side="left")
        self.total_cobrar_label = ctk.CTkLabel(total_frame, text="$0.00", 
                    font=("Segoe UI", 11, "bold"), text_color="#4CAF50")
        self.total_cobrar_label.pack(side="right")
        
        # Créditos Activos
        activos_frame = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        activos_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(activos_frame, text="Créditos Activos", font=("Segoe UI", 11), 
                    text_color="#666666").pack(side="left")
        self.creditos_activos_label = ctk.CTkLabel(activos_frame, text="0", 
                    font=("Segoe UI", 11, "bold"), text_color="#333333")
        self.creditos_activos_label.pack(side="right")
        
        # Créditos Vencidos
        vencidos_frame = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        vencidos_frame.pack(fill="x", padx=20, pady=(5, 15))
        
        ctk.CTkLabel(vencidos_frame, text="Créditos vencidos", font=("Segoe UI", 11), 
                    text_color="#666666").pack(side="left")
        self.creditos_vencidos_label = ctk.CTkLabel(vencidos_frame, text="0", 
                    font=("Segoe UI", 11, "bold"), text_color="#E53935")
        self.creditos_vencidos_label.pack(side="right")
    
    def mostrar_creditos_clientes(self):
        """Mostrar tab de Créditos a clientes"""
        ctk.CTkLabel(
            self.content_frame,
            text="Créditos a clientes - En desarrollo",
            font=("Segoe UI", 16),
            text_color="#999999"
        ).pack(expand=True)
    
    def mostrar_vencidos(self):
        """Mostrar tab de Vencidos"""
        ctk.CTkLabel(
            self.content_frame,
            text="Créditos vencidos - En desarrollo",
            font=("Segoe UI", 16),
            text_color="#999999"
        ).pack(expand=True)
    
    def mostrar_abonos_hoy(self):
        """Mostrar tab de Abonos de Hoy"""
        ctk.CTkLabel(
            self.content_frame,
            text="Abonos de hoy - En desarrollo",
            font=("Segoe UI", 16),
            text_color="#999999"
        ).pack(expand=True)

    def cargar_datos(self):
        """Cargar créditos desde la base de datos"""
        try:
            from controllers.creditos import obtener_creditos
            self.creditos = obtener_creditos()
            self.actualizar_resumen()
        except Exception as e:
            print(f"Error al cargar créditos: {e}")
            self.creditos = []
    
    def actualizar_resumen(self):
        """Actualizar el resumen de créditos"""
        total_cobrar = sum(float(c.get("monto", 0)) for c in self.creditos)
        activos = len([c for c in self.creditos if c.get("estado") == "Activo"])
        vencidos = len([c for c in self.creditos if c.get("estado") == "Vencido"])
        
        self.total_cobrar_label.configure(text=f"${total_cobrar:,.2f}")
        self.creditos_activos_label.configure(text=str(activos))
        self.creditos_vencidos_label.configure(text=str(vencidos))
    
    def nuevo_credito(self):
        """Abrir formulario para nuevo crédito"""
        messagebox.showinfo("Nuevo Crédito", "Funcionalidad de nuevo crédito en desarrollo")


if __name__ == "__main__":
    app = GestionCreditosView()
    app.mainloop()
