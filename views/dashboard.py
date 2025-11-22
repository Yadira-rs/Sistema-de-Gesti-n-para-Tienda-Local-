import tkinter as tk
from tkinter import ttk
from controllers.products import productos_count, stock_total_sum, stock_bajo_list
from controllers.ventas import ventas_hoy_total, resumen_ventas, listar_ultimas_ventas, ingresos_mes_total, ventas_diarias

class DashboardView(ttk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        ttk.Label(self, text="Dashboard", font=("Segoe UI", 18, "bold")).pack(pady=8, anchor="w")
        cards = ttk.Frame(self); cards.pack(fill="x", padx=8)
        v_hoy = ventas_hoy_total(); res = resumen_ventas()
        ttk.Label(cards, text=f"Ventas Hoy\n${v_hoy:.2f}", padding=12).pack(side="left", padx=8)
        ttk.Label(cards, text=f"Ingreso Mes\n${ingresos_mes_total():.2f}", padding=12).pack(side="left", padx=8)
        ttk.Label(cards, text=f"Total Ventas\n{res['total_ventas']}", padding=12).pack(side="left", padx=8)
        ttk.Label(cards, text=f"Productos\n{productos_count()}", padding=12).pack(side="left", padx=8)
        ttk.Label(cards, text=f"Stock Total\n{stock_total_sum()}", padding=12).pack(side="left", padx=8)

        content = ttk.Frame(self); content.pack(fill="both", expand=True, padx=8, pady=8)
        left = ttk.Frame(content); right = ttk.Frame(content)
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(left, text="Productos con Stock Bajo", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        low = stock_bajo_list(10)
        for p in low:
            ttk.Label(left, text=f"{p['nombre']}  {p['stock']} unidades  ${float(p['precio']):.2f}", padding=6).pack(fill="x")

        ttk.Label(right, text="Últimas Ventas", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tabla = ttk.Treeview(right, columns=("ticket","fecha","total"), show="headings", height=8)
        for c,t in (("ticket","Ticket"),("fecha","Fecha"),("total","Total")):
            tabla.heading(c, text=t)
        tabla.pack(fill="both", expand=True)
        for v in listar_ultimas_ventas(5):
            tabla.insert("", tk.END, values=(v["id_venta"], str(v["fecha"]), f"${float(v['total']):.2f}"))

        ttk.Label(self, text="Ventas diarias", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=8)
        canvas = tk.Canvas(self, height=160, bg="#FFFFFF")
        canvas.pack(fill="x", padx=8, pady=8)
        data = ventas_diarias(7)
        if data:
            max_total = max(float(d["total"]) for d in data) or 1
            bar_width = 40
            spacing = 20
            x = 20
            for d in data:
                h = int((float(d["total"]) / max_total) * 120)
                canvas.create_rectangle(x, 140-h, x+bar_width, 140, fill="#F9D7DD", outline="")
                canvas.create_text(x+bar_width/2, 150, text=str(d["dia"]), angle=45, font=("Segoe UI", 8))
                x += bar_width + spacing