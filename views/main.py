import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from views.dashboard import DashboardView
from views.products_view import ProductsView
from views.inventario import InventarioView
from views.apartado import ApartadoView
from views.ventas_view import VentasView
from views.sales_history import SalesHistoryView
from views.users_view import UsersWindow as UsuariosView
from views.categorias import CategoriasView

class MainApp(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title("Boutique Rosa Janet - Panel")
        self.geometry("1200x700")
        self.user = user

        self.configure(bg="#F8F8F8")

        self.setup_style()

        # ---- Panel lateral ----
        self.sidebar = tk.Frame(self, bg="#FDE2E4", width=230)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self, bg="#F8F8F8")
        self.content.pack(side="right", fill="both", expand=True)

        self.create_menu()
        self.create_brand()

        self.show_view(DashboardView)

    # -----------------------------------------------------
    def create_menu(self):

        menu_items = [
            ("Dashboard", DashboardView),
            ("Punto de Venta", VentasView),
            ("Ventas", SalesHistoryView),
            ("Apartado", ApartadoView),
            ("Productos", ProductsView),
            ("Inventario", InventarioView),
            ("Usuarios", UsuariosView),
            ("Categorías", CategoriasView),
        ]

        for text, view in menu_items:
            btn = ttk.Button(
                self.sidebar,
                text=text,
                style="Sidebar.TButton",
                command=lambda v=view: self.show_view(v)
            )
            btn.pack(fill="x", padx=10, pady=4)

    # -----------------------------------------------------
    def show_view(self, view_class):
        for widget in self.content.winfo_children():
            widget.destroy()
        try:
            view = view_class(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            fallback = ttk.Frame(self.content)
            fallback.pack(fill="both", expand=True)
            ttk.Label(fallback, text="No se pudo cargar la vista", font=("Segoe UI", 14, "bold")).pack(pady=10)
            ttk.Label(fallback, text=str(e)).pack()
            ttk.Button(fallback, text="Reintentar", command=lambda: self.show_view(view_class)).pack(pady=8)

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

    def create_brand(self):
        top = ttk.Frame(self.sidebar)
        top.pack(fill="x", padx=8, pady=8)
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "WhatsApp Image 2025-11-20 at 10.25.27 AM.jpeg")
        try:
            img = Image.open(path).resize((60, 60))
            self.brand_logo = ImageTk.PhotoImage(img)
            tk.Label(top, image=self.brand_logo, bg="#FDE2E4").pack(side="left")
        except Exception:
            pass
        ttk.Label(top, text="Janet Rosa Bici", font=("Segoe UI", 13, "bold")).pack(side="left", padx=8)
