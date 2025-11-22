import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from controllers.products import obtener_productos, ajustar_stock

class InventarioView(ttk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user
        ttk.Label(self, text="Gestión de Inventario", font=("Segoe UI", 16, "bold")).pack(pady=8)
        self.cards = ttk.Frame(self); self.cards.pack(fill="x", padx=8)
        self.card_total = ttk.Label(self.cards, text="Total Productos: 0", padding=8); self.card_total.pack(side="left", padx=6)
        self.card_stock = ttk.Label(self.cards, text="Stock Total: 0", padding=8); self.card_stock.pack(side="left", padx=6)
        self.card_stock_bajo = ttk.Label(self.cards, text="Stock Bajo: 0", padding=8); self.card_stock_bajo.pack(side="left", padx=6)
        self.card_valor = ttk.Label(self.cards, text="Valor Total: $0.00", padding=8); self.card_valor.pack(side="left", padx=6)

        filtros = ttk.Frame(self); filtros.pack(fill="x", padx=8, pady=4)
        ttk.Label(filtros, text="Buscar producto...").pack(side="left")
        self.search = ttk.Entry(filtros, width=30); self.search.pack(side="left", padx=6)
        ttk.Button(filtros, text="Filtrar", command=self.filtrar).pack(side="left")

        cols = ("codigo","producto","categoria","precio","stock","valor","accion")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=16)
        for c,t in zip(cols, ["Código","Producto","Categoría","Precio","Stock Actual","Valor Total","Acción"]):
            self.tabla.heading(c, text=t)
        self.tabla.pack(fill="both", expand=True, padx=8, pady=8)
        ttk.Button(self, text="Ajustar selección", command=self.ajustar).pack(pady=6)
        self.cargar()

    def cargar(self):
        self.tabla.delete(*self.tabla.get_children())
        productos = obtener_productos()
        total_prod = len(productos); stock_total = 0; stock_bajo = 0; valor_total = 0
        for p in productos:
            stock_total += int(p["stock"]) if p["stock"] is not None else 0
            valor = float(p["precio"]) * int(p["stock"])
            valor_total += valor
            if int(p["stock"]) <= 5:
                stock_bajo += 1
            self.tabla.insert("", tk.END, values=(p.get("id_producto"), p.get("nombre"), "-", f"${p['precio']:.2f}", p.get("stock"), f"${valor:.2f}", "Ajustar"))
        self.card_total.config(text=f"Total Productos: {total_prod}")
        self.card_stock.config(text=f"Stock Total: {stock_total}")
        self.card_stock_bajo.config(text=f"Stock Bajo: {stock_bajo}")
        self.card_valor.config(text=f"Valor Total: ${valor_total:.2f}")

    def filtrar(self):
        term = self.search.get().strip().lower()
        if not term:
            self.cargar(); return
        self.tabla.delete(*self.tabla.get_children())
        for p in obtener_productos():
            if term in p["nombre"].lower():
                valor = float(p["precio"]) * int(p["stock"]) 
                self.tabla.insert("", tk.END, values=(p.get("id_producto"), p.get("nombre"), "-", f"${p['precio']:.2f}", p.get("stock"), f"${valor:.2f}", "Ajustar"))

    def ajustar(self):
        sel = self.tabla.focus()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un producto para ajustar"); return
        vals = self.tabla.item(sel, "values")
        pid = int(vals[0])
        cantidad = simpledialog.askinteger("Cantidad", "Cantidad a ajustar:", minvalue=1)
        if not cantidad:
            return
        tipo = simpledialog.askstring("Tipo", "Tipo (Entrada/Salida)", initialvalue="Entrada")
        if tipo not in ("Entrada","Salida"):
            messagebox.showerror("Tipo", "Tipo inválido"); return
        if ajustar_stock(pid, cantidad, tipo):
            messagebox.showinfo("Inventario", "Stock ajustado")
            self.cargar()