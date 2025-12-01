# nuevo_apartado_toplevel.py
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os
import platform

# IMPORTS A TU CONTROLADOR DE VENTAS (asegúrate de la ruta correcta)
# Si tu controlador está en controllers/ventas.py:
from controllers.ventas import (
    buscar_producto,
    agregar_al_carrito,
    obtener_carrito,
    eliminar_item,
    vaciar_carrito,
    finalizar_venta
)

# Ajustes visuales
IMAGE_PATH = Path(__file__).parent / "assets" / "logo.png"  # cambia si tienes otra ruta
WINDOW_W = 1100
WINDOW_H = 700

class ApartadoWindow(tk.Toplevel):
    def __init__(self, parent, usuario=None):
        super().__init__(parent)
        self.parent = parent
        self.user = usuario or {}
        self.title("Nuevo Apartado - Boutique Rosa Janet")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.configure(bg="#f1f1f1")
        self.resizable(False, False)

        # Top: campo de búsqueda / escaneo
        top_frame = ttk.Frame(self, padding=8)
        top_frame.pack(fill="x", padx=12, pady=(12,6))

        ttk.Label(top_frame, text="Buscar / Escanear producto (código o nombre):").pack(side="left")
        self.entry_codigo = ttk.Entry(top_frame, width=50)
        self.entry_codigo.pack(side="left", padx=8)
        self.entry_codigo.bind("<Return>", self.on_scan_code)

        btn_add = ttk.Button(top_frame, text="Agregar (Enter)", command=self.on_scan_code)
        btn_add.pack(side="left", padx=6)

        # Middle: lista de items del apartado (usar el mismo carrito global del controlador)
        middle = ttk.Frame(self)
        middle.pack(fill="both", expand=True, padx=12, pady=6)

        # Treeview para mostrar los items
        cols = ("id_producto", "nombre", "cantidad", "precio", "subtotal")
        self.tree = ttk.Treeview(middle, columns=cols, show="headings", height=18)
        self.tree.heading("id_producto", text="ID")
        self.tree.heading("nombre", text="Producto")
        self.tree.heading("cantidad", text="Cant")
        self.tree.heading("precio", text="Precio Unit.")
        self.tree.heading("subtotal", text="Subtotal")
        self.tree.column("id_producto", width=60, anchor="center")
        self.tree.column("nombre", width=360)
        self.tree.column("cantidad", width=60, anchor="center")
        self.tree.column("precio", width=90, anchor="e")
        self.tree.column("subtotal", width=90, anchor="e")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(middle, command=self.tree.yview)
        scrollbar.pack(side="left", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Right side: acciones y resumen
        right = ttk.Frame(self, width=220, padding=8)
        right.pack(side="right", fill="y", padx=12, pady=12)

        self.lbl_total = ttk.Label(right, text="Total: $0.00", font=("Segoe UI", 14, "bold"))
        self.lbl_total.pack(pady=(6,12))

        ttk.Button(right, text="Eliminar seleccionado", command=self.eliminar_seleccionado).pack(fill="x", pady=6)
        ttk.Button(right, text="Vaciar apartado", command=self.vaciar_apartado).pack(fill="x", pady=6)
        ttk.Button(right, text="Convertir a venta", command=self.convertir_a_venta).pack(fill="x", pady=6)

        ttk.Button(right, text="Cerrar", command=self.close_window).pack(fill="x", pady=(20,0))

        # Inicializar tabla con items actuales (usa carrito global del controlador)
        self.refresh_table()

        # foco en input
        self.entry_codigo.focus_set()

    def on_scan_code(self, event=None):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            return
        # buscar producto (por codigo/id/nombre)
        producto = buscar_producto(codigo)
        if not producto:
            messagebox.showerror("No encontrado", f"No existe producto con: {codigo}")
            self.entry_codigo.delete(0, tk.END)
            return
        # agregar_al_carrito reserva stock en BD y agrega al carrito global
        ok = agregar_al_carrito(producto, 1)
        if not ok:
            messagebox.showwarning("Sin stock", "No hay suficiente stock disponible para agregar el producto.")
        self.entry_codigo.delete(0, tk.END)
        self.refresh_table()
        try:
            self.entry_codigo.focus_set()
        except Exception:
            pass

    def refresh_table(self):
        # limpiar tree
        for i in self.tree.get_children():
            self.tree.delete(i)
        carrito = obtener_carrito()
        total = 0.0
        for it in carrito:
            subtotal = float(it["precio"]) * int(it["cantidad"])
            total += subtotal
            self.tree.insert("", "end", values=(it["id_producto"], it["nombre"], it["cantidad"], f"{float(it['precio']):.2f}", f"{subtotal:.2f}"))
        self.lbl_total.config(text=f"Total: ${total:.2f}")

    def eliminar_seleccionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleccionar", "Selecciona un item para eliminar")
            return
        vals = self.tree.item(sel[0], "values")
        pid = int(vals[0])
        # eliminar_item restaurará stock para ese id
        eliminar_item(pid)
        self.refresh_table()

    def vaciar_apartado(self):
        if messagebox.askyesno("Confirmar", "¿Vaciar todo el apartado? Se restaurará el stock reservado."):
            vaciar_carrito()  # si usas controllers.ventas.vaciar_carrito
            self.refresh_table()

    def convertir_a_venta(self):
        carrito = obtener_carrito()
        if not carrito:
            messagebox.showwarning("Vacío", "No hay items para convertir a venta.")
            return
        if not messagebox.askyesno("Confirmar", "¿Deseas convertir este apartado en una venta (se guardará la venta)?"):
            return
        # finalizar_venta usará los items reservados (no descontará doble stock)
        res = finalizar_venta(usuario_id=self.user.get("id_usuario"), metodo="Efectivo")
        if not res:
            messagebox.showerror("Error", "No se pudo crear la venta.")
            return
        # res contiene id_venta y items; abrir el ticket si quieres
        try:
            # si el controlador retorna 'pdf' o 'ticket' agrega aquí el código para abrirlo
            # ejemplo simple: messagebox con id de venta
            messagebox.showinfo("Venta creada", f"Venta #{res['id_venta']} creada. Total: ${res['total']:.2f}")
        except Exception:
            pass
        # refrescar tabla (el carrito se limpia en finalizar_venta)
        self.refresh_table()

    def close_window(self):
        # al cerrar, simplemente destruye la ventana; si quieres restaurar stock automaticamente
        # asegúrate que vaciar_carrito no borre si quieres mantener apartado sin convertir.
        self.destroy()


# helper para integrarlo en la app principal:
def abrir_apartado(parent, usuario=None):
    """
    Llamar desde tu app principal para abrir la ventana de apartado.
    Ejemplo:
        from nuevo_apartado_toplevel import abrir_apartado
        abrir_apartado(root, usuario=current_user)
    """
    # evita abrir múltiples instancias
    for w in parent.winfo_children():
        if isinstance(w, tk.Toplevel) and getattr(w, "title", lambda: "")() == "Nuevo Apartado - Boutique Rosa Janet":
            w.lift()
            return
    ApartadoWindow(parent, usuario=usuario)
