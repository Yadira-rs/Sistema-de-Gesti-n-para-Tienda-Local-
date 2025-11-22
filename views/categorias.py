import tkinter as tk
from tkinter import ttk
from controllers.products import obtener_categorias
from views.category_view import CategoryView

class CategoriasView(ttk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user
        ttk.Label(self, text="Categorías", font=("Segoe UI", 16, "bold")).pack(pady=8)
        grid = ttk.Frame(self); grid.pack(fill="both", expand=True, padx=8, pady=8)
        cats = obtener_categorias()
        for i, c in enumerate(cats):
            b = ttk.Button(grid, text=c["nombre"], command=lambda cid=c["id_categoria"]: self.open_category(cid))
            b.grid(row=i//3, column=i%3, padx=8, pady=8, sticky="ew")

    def open_category(self, id_categoria):
        for w in self.winfo_children():
            if isinstance(w, ttk.Frame):
                pass
        view = CategoryView(self.master, self.user, id_categoria)
        view.pack(fill="both", expand=True)