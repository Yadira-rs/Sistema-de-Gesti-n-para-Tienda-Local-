import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from controllers.products import productos_count, stock_total_sum, stock_bajo_list
from controllers.ventas import ventas_hoy_total, resumen_ventas, listar_ultimas_ventas, ingresos_mes_total, ventas_diarias

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # --- Cargar datos de los controladores ---
        resumen = resumen_ventas()
        stock_bajo = stock_bajo_list(5) # Limitar a 5 para no saturar
        ultimas_ventas = listar_ultimas_ventas(5)
        v_hoy = ventas_hoy_total()
        p_count = productos_count()
        s_sum = stock_total_sum()

        # --- Área principal ---
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main, text="Bienvenido al sistema de punto de venta", font=("Segoe UI", 18, "bold")).pack(pady=10, anchor="w")

        # Tarjetas resumen
        resumen_frame = ctk.CTkFrame(main)
        resumen_frame.pack(fill="x", pady=10)

        resumen_data = [
            f"Ventas Hoy\n${v_hoy:.2f}",
            f"Total Ventas\n{resumen.get('total_ventas', 0)}",
            f"Productos\n{p_count}",
            f"Stock Total\n{s_sum}"
        ]

        for txt in resumen_data:
            ctk.CTkLabel(resumen_frame, text=txt, corner_radius=10,
                         fg_color="#E3A8C5", text_color="black",
                         font=("Segoe UI", 14, "bold"),
                         padx=20, pady=12).pack(side="left", padx=8, expand=True, fill="x")

        # Stock Bajo
        ctk.CTkLabel(main, text="Productos con Stock Bajo", font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(20, 5))
        stock_frame = ctk.CTkFrame(main, fg_color="transparent")
        stock_frame.pack(fill="x")
        for p in stock_bajo:
            txt = f"{p.get('nombre', '?')} : {p.get('stock', 0)} unidades - ${float(p.get('precio', 0)):.2f}"
            ctk.CTkLabel(stock_frame, text=txt, fg_color="#5E4B56", corner_radius=8,
                         padx=6, pady=4).pack(fill="x", pady=3)

        # Últimas Ventas
        ctk.CTkLabel(main, text="Últimas Ventas", font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(20, 5))
        ventas_frame = ctk.CTkFrame(main, fg_color="transparent")
        ventas_frame.pack(fill="x")
        for v in ultimas_ventas:
            fecha_str = str(v.get('fecha', ''))
            txt = f"Venta #{v.get('id_venta', '?')}: {fecha_str} - ${float(v.get('total', 0)):.2f}"
            ctk.CTkLabel(ventas_frame, text=txt).pack(anchor="w", padx=10)
