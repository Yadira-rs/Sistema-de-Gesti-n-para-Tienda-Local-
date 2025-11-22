import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from controllers.products import obtener_productos_por_categoria

class CategoryView(ttk.Frame):
    def __init__(self, parent, user, id_categoria):
        super().__init__(parent)
        self.user = user
        self.id_categoria = id_categoria
        ttk.Label(self, text="Catálogo", font=("Segoe UI", 16, "bold")).pack(pady=8)
        self.grid = ttk.Frame(self)
        self.grid.pack(fill="both", expand=True, padx=8, pady=8)
        self.cargar()

    def cargar(self):
        for w in self.grid.winfo_children():
            w.destroy()
        prods = obtener_productos_por_categoria(self.id_categoria)
        for i, p in enumerate(prods):
            card = ttk.Frame(self.grid, padding=8)
            card.grid(row=i//4, column=i%4, padx=8, pady=8, sticky="nsew")
            img_path = p.get("imagen_url") or ""
            if img_path and os.path.exists(img_path):
                try:
                    im = Image.open(img_path).resize((120,120))
                    photo = ImageTk.PhotoImage(im)
                    label = tk.Label(card, image=photo)
                    label.image = photo
                    label.pack()
                except Exception:
                    tk.Label(card, text="Imagen", width=18, height=8, bg="#EEE").pack()
            else:
                tk.Label(card, text="Sin imagen", width=18, height=8, bg="#EEE").pack()
            ttk.Label(card, text=p["nombre"], font=("Segoe UI", 11, "bold")).pack(pady=4)
            ttk.Label(card, text=f"${float(p['precio']):.2f}").pack()