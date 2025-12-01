import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw, ImageFont
import webbrowser, tempfile
from pathlib import Path
import platform
import configparser
import os
from controllers.ventas import (
    buscar_producto,
    agregar_al_carrito,
    finalizar_venta,
    obtener_carrito,
    set_cantidad,
    eliminar_item,
)
from controllers.products import obtener_productos, obtener_categorias, obtener_productos_por_categoria, buscar_productos, obtener_productos_favoritos, obtener_productos_stock_bajo, crear_categoria


class VentasView(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.metodo = tk.StringVar(value="Efectivo")
        self.quick_filter = None
        self.build_ui()

    def build_ui(self):
        # Configurar colores y estilos
        self.configure(bg="#F5F5F5")
        
        # Header con título
        header = tk.Frame(self, bg="#F5F5F5")
        header.pack(fill="x", padx=20, pady=(10, 5))
        
        tk.Label(
            header,
            text="Punto de Venta",
            font=("Segoe UI", 20, "bold"),
            bg="#F5F5F5",
            fg="#333333"
        ).pack(side="left")

        # Contenedor principal
        body = tk.Frame(self, bg="#F5F5F5")
        body.pack(fill="both", expand=True, padx=10, pady=5)

        # Panel izquierdo (productos)
        left = tk.Frame(body, bg="#F5F5F5")
        left.pack(side="left", fill="both", expand=True, padx=(10, 5))
        
        # Panel derecho (carrito)
        right = tk.Frame(body, bg="white", width=350)
        right.pack(side="right", fill="y", padx=(5, 10))
        right.pack_propagate(False)

        # Barra de búsqueda
        search_frame = tk.Frame(left, bg="white", height=50)
        search_frame.pack(fill="x", pady=(0, 10))
        search_frame.pack_propagate(False)
        
        tk.Label(search_frame, text="🔍", font=("Segoe UI", 16), bg="white").pack(side="left", padx=10)
        
        self.entry_codigo = tk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            bg="white",
            fg="#666666",
            relief="flat",
            bd=0
        )
        self.entry_codigo.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.entry_codigo.bind("<Return>", self.agregar_por_codigo)
        self.entry_codigo.bind("<KP_Enter>", self.agregar_por_codigo)
        self.entry_codigo.bind("<KeyRelease>", lambda e: self.cargar_grid())
        self._placeholder(self.entry_codigo, "Buscar productos por Nombre, Código o Categoría...")
        
        # Filtros de categorías
        categorias_frame = tk.Frame(left, bg="#F5F5F5")
        categorias_frame.pack(fill="x", pady=(0, 10))
        
        categorias = ["Todas las Categorías", "Vestidos", "Blusas", "Pantalones", "Serum", "Cremas", "Dulces", "short"]
        
        for i, cat in enumerate(categorias):
            btn = tk.Button(
                categorias_frame,
                text=cat,
                font=("Segoe UI", 10),
                bg="#F06292" if i == 0 else "#E0E0E0",
                fg="white" if i == 0 else "#666666",
                relief="flat",
                padx=15,
                pady=8,
                cursor="hand2",
                command=lambda c=cat: self.filtrar_categoria(c)
            )
            btn.pack(side="left", padx=3)
        
        self.categoria_actual = "Todas las Categorías"

        # Grid de productos a la izquierda
        self.grid = ttk.Frame(left)
        self.grid.pack(fill="both", expand=True)
        self.cargar_grid()

        # Panel de carrito a la derecha
        self.cart_panel = ttk.Frame(right)
        self.cart_panel.pack(fill="y")
        ttk.Label(self.cart_panel, text="Carrito de Compras", font=("Segoe UI", 12, "bold")).pack(pady=4)
        self.cart_items_container = ttk.Frame(self.cart_panel)
        self.cart_items_container.pack(fill="y")

        ttk.Label(right, text="Método de pago", font=("Segoe UI", 12, "bold")).pack(pady=(10, 4))
        pagos = ttk.Frame(right)
        pagos.pack(fill="x")
        for m in ("Efectivo", "Tarjeta", "Transferencia"):
            ttk.Radiobutton(pagos, text=m, variable=self.metodo, value=m, style="Pay.TRadiobutton").pack(side="left", padx=4)

        self.lbl_total = ttk.Label(right, text="Total: $0.00", font=("Segoe UI", 14, "bold"))
        self.lbl_total.pack(pady=10)

        ttk.Button(right, text="Procesar Venta", style="Primary.TButton", command=self.finalizar).pack(fill="x")

    def agregar_por_codigo(self, event=None):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            return

        producto = buscar_producto(codigo)

        if not producto:
            messagebox.showerror("No encontrado", f"No existe el producto con código: {codigo}")
        else:
            agregar_al_carrito(producto, 1)  # Cantidad por defecto = 1
            self.actualizar_tabla()

        self.entry_codigo.delete(0, tk.END)
        try:
            self.entry_codigo.focus_set()
        except Exception:
            pass

    def actualizar_tabla(self):
        for w in self.cart_items_container.winfo_children():
            w.destroy()
        carrito = obtener_carrito()
        total = 0
        for item in carrito:
            subtotal = float(item["precio"]) * int(item["cantidad"])
            total += subtotal
            row = ttk.Frame(self.cart_items_container)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=item["nombre"], width=30).pack(side="left")
            controls = ttk.Frame(row)
            controls.pack(side="right")
            ttk.Button(controls, text="-", width=3, command=lambda pid=item["id_producto"], q=item["cantidad"]: (set_cantidad(pid, max(0, int(q)-1)), self.actualizar_tabla())).pack(side="left")
            ttk.Label(controls, text=str(item["cantidad"]), width=3).pack(side="left")
            ttk.Button(controls, text="+", width=3, command=lambda pid=item["id_producto"], q=item["cantidad"]: (set_cantidad(pid, int(q)+1), self.actualizar_tabla())).pack(side="left")
            ttk.Button(controls, text="🗑", width=3, command=lambda pid=item["id_producto"]: (eliminar_item(pid), self.actualizar_tabla())).pack(side="left", padx=4)
            ttk.Label(row, text=f"${subtotal:.2f}", width=10).pack(side="right")
        self.lbl_total.config(text=f"Total: ${total:.2f}")

    def cargar_grid(self):
        for w in self.grid.winfo_children():
            w.destroy()
        
        # Obtener productos
        productos = obtener_productos()
        
        # Filtrar por búsqueda
        q = self.entry_codigo.get().strip()
        if q and q.lower() not in ("buscar productos por nombre, código o categoría...", ""):
            try:
                productos = buscar_productos(q)
            except Exception:
                pass
        
        # Mostrar productos en grid 3 columnas
        for i, p in enumerate(productos[:9]):
            # Tarjeta de producto
            card = tk.Frame(self.grid, bg="white", relief="solid", bd=1, width=200, height=280)
            card.grid(row=i//3, column=i%3, padx=8, pady=8, sticky="nsew")
            card.grid_propagate(False)
            
            # Placeholder de imagen (cuadro gris)
            img_frame = tk.Frame(card, bg="#F0F0F0", height=140)
            img_frame.pack(fill="x", padx=10, pady=10)
            img_frame.pack_propagate(False)
            
            tk.Label(
                img_frame,
                text="📦",
                font=("Segoe UI", 50),
                bg="#F0F0F0",
                fg="#CCCCCC"
            ).pack(expand=True)
            
            # Nombre del producto
            nombre = p.get("nombre", "Producto")
            tk.Label(
                card,
                text=nombre[:25] + "..." if len(nombre) > 25 else nombre,
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="#333333",
                wraplength=180
            ).pack(padx=10, pady=(0, 5))
            
            # Precio
            precio = float(p.get('precio', 0))
            tk.Label(
                card,
                text=f"${precio:.2f}",
                font=("Segoe UI", 14, "bold"),
                bg="white",
                fg="#E91E63"
            ).pack()
            
            # Stock
            stock = int(p.get('stock', 0))
            tk.Label(
                card,
                text=f"Stock: {stock}",
                font=("Segoe UI", 9),
                bg="white",
                fg="#666666"
            ).pack(pady=(0, 10))
            
            # Botón agregar
            btn = tk.Button(
                card,
                text="Agregar",
                font=("Segoe UI", 10, "bold"),
                bg="#4CAF50",
                fg="white",
                relief="flat",
                cursor="hand2",
                command=lambda prod=p: (agregar_al_carrito(prod, 1), self.actualizar_tabla())
            )
            btn.pack(fill="x", padx=10, pady=(0, 10))
        
        # Configurar columnas
        for c in range(3):
            self.grid.columnconfigure(c, weight=1)
    
    def filtrar_categoria(self, categoria):
        """Filtrar por categoría"""
        self.categoria_actual = categoria
        # Aquí puedes implementar el filtro real por categoría
        self.cargar_grid()

    def set_quick_filter(self, kind):
        self.quick_filter = kind
        self.selected_cat = None
        self.cargar_grid()

    def _placeholder(self, entry, text):
        def on_focus_in(e):
            if entry.get() == text:
                entry.delete(0, tk.END)
        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, text)
        entry.insert(0, text)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def finalizar(self):
        carrito = obtener_carrito()
        if len(carrito) == 0:
            messagebox.showwarning("Carrito vacío", "Agrega productos primero")
            return
        confirmado = messagebox.askyesno("Confirmar venta", "¿Deseas finalizar la venta?")
        if not confirmado:
            return
        ticket = finalizar_venta(self.user.get("id_usuario"), self.metodo.get())
        if not ticket:
            messagebox.showerror("Error", "No fue posible guardar la venta.")
            return
        self.actualizar_tabla()
        self.mostrar_ticket(ticket)
        try:
            p = self.guardar_pdf(ticket, auto=True)
            if p and platform.system() == "Windows":
                try:
                    os.startfile(p, "print")
                except Exception:
                    pass
        except Exception:
            pass

    def mostrar_ticket(self, ticket):
        win = tk.Toplevel(self)
        win.title("Venta Completa")
        win.geometry("520x480")
        cont = ttk.Frame(win, padding=16)
        cont.pack(fill="both", expand=True)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "WhatsApp Image 2025-11-20 at 10.25.27 AM.jpeg")
        try:
            img = Image.open(logo_path).resize((70, 70))
            win.logo = ImageTk.PhotoImage(img)
            tk.Label(cont, image=win.logo).pack()
        except Exception:
            pass
        ttk.Label(cont, text="Venta Completada", font=("Segoe UI", 15, "bold")).pack(pady=4)
        info = ttk.Frame(cont)
        info.pack(fill="x", pady=8)
        biz = self.obtener_config_negocio()
        ttk.Label(info, text=f"{biz['name']}\n{biz['address']}\nTel: {biz['phone']}", justify="center").pack(anchor="center")
        sep1 = ttk.Separator(cont, orient="horizontal"); sep1.pack(fill="x", pady=8)
        meta = ttk.Frame(cont); meta.pack(fill="x")
        ttk.Label(meta, text=f"Ticket #: {ticket['id_venta']}").pack(anchor="w")
        ttk.Label(meta, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y, %I:%M:%S %p')}").pack(anchor="w")
        ttk.Label(meta, text=f"Método: {ticket['metodo']}").pack(anchor="w")
        sep2 = ttk.Separator(cont, orient="horizontal"); sep2.pack(fill="x", pady=8)
        items_box = ttk.Frame(cont)
        items_box.pack(fill="x")
        for item in ticket.get("items", []):
            subtotal = float(item["precio"]) * int(item["cantidad"])
            row = ttk.Frame(items_box)
            row.pack(fill="x", pady=4)
            left = ttk.Frame(row)
            left.pack(side="left", fill="x", expand=True)
            ttk.Label(left, text=item["nombre"]).pack(anchor="w")
            ttk.Label(left, text=f"{int(item['cantidad'])} x ${float(item['precio']):.2f}", foreground="#666").pack(anchor="w")
            ttk.Label(row, text=f"${subtotal:.2f}").pack(side="right")
        ttk.Label(cont, text=f"Total: ${ticket['total']:.2f}", font=("Segoe UI", 13, "bold"), foreground="#B2334A").pack(pady=10)
        ttk.Label(cont, text="¡Gracias por su compra!\nVuelva pronto", justify="center").pack()
        buttons = ttk.Frame(cont); buttons.pack(fill="x", pady=6)
        ttk.Button(buttons, text="Guardar PDF", command=lambda: self.guardar_pdf(ticket)).pack(side="left")
        ttk.Button(buttons, text="Imprimir", command=lambda: self.imprimir_ticket(ticket)).pack(side="left", padx=6)
        ttk.Button(buttons, text="Cerrar", command=win.destroy).pack(side="right")

    def imprimir_ticket(self, ticket):
        html = self._generar_html(ticket)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        tmp.write(html.encode("utf-8")); tmp.close()
        webbrowser.open(Path(tmp.name).as_uri())

    def _generar_html(self, ticket):
        lines = []
        biz = self.obtener_config_negocio()
        for item in ticket.get("items", []):
            qty = int(item["cantidad"])
            subtotal = float(item["precio"]) * qty
            lines.append(f"<div class=\"row\"><div class=\"name\">{item['nombre']}</div><div class=\"qty\">1 x ${float(item['precio']):.2f}</div><div class=\"price\">${subtotal:.2f}</div></div>")
        return f"""
<!doctype html>
<html><head><meta charset='utf-8'><title>Ticket de Venta</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;color:#000;}}
.wrap{{width:380px;margin:20px auto;}}
.title{{font-size:22px;font-weight:700;text-align:center;margin-bottom:6px;}}
.sub{{text-align:center;color:#333;}}
.sep{{border-top:1px dotted #888;margin:10px 0;}}
.row{{display:flex;align-items:center;margin:6px 0;}}
.name{{flex:1}}
.qty{{width:120px;text-align:left;color:#444}}
.price{{width:80px;text-align:right}}
.total{{text-align:right;font-weight:700;margin-top:8px;color:#B2334A}}
.thanks{{text-align:center;margin-top:10px}}
</style></head><body>
<div class='wrap'>
<div class='title'>{biz['name']}</div>
<div class='sub'>{biz['address']}<br>Tel: {biz['phone']}</div>
<div class='sep'></div>
<div><b>Ticket #:</b> {ticket['id_venta']}<br><b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y, %I:%M:%S %p')}<br><b>Método:</b> {ticket['metodo']}</div>
<div class='sep'></div>
{''.join(lines)}
<div class='sep'></div>
<div class='total'>Total: ${ticket['total']:.2f}</div>
<div class='thanks'>¡Gracias por su compra!<br>Vuelva pronto</div>
</div>
<script>window.onload=function(){{setTimeout(()=>window.print(),300)}}</script>
</body></html>
"""

    def guardar_pdf(self, ticket, auto=False):
        default_name = f"ticket_{ticket['id_venta']}.pdf"
        path = None
        if auto:
            path = os.path.join(os.getcwd(), default_name)
        else:
            path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=default_name, filetypes=[("PDF","*.pdf")])
        if not path:
            return None
        W, H = 580, 800
        img = Image.new("RGB", (W, H), "white")
        draw = ImageDraw.Draw(img)
        y = 20
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "WhatsApp Image 2025-11-20 at 10.25.27 AM.jpeg")
        try:
            logo = Image.open(logo_path).resize((80,80))
            img.paste(logo, (W//2-40, y))
            y += 90
        except Exception:
            pass
        font = ImageFont.load_default()
        biz2 = self.obtener_config_negocio()
        draw.text((20, y), "Venta Completa", fill="black", font=font); y += 20
        draw.text((20, y), biz2['name'], fill="black", font=font); y += 16
        draw.text((20, y), biz2['address'], fill="black", font=font); y += 16
        draw.text((20, y), f"Tel: {biz2['phone']}", fill="black", font=font); y += 24
        draw.line((20, y, W-20, y), fill="#cccccc"); y += 10
        draw.text((20, y), f"Ticket#: {ticket['id_venta']}", fill="black", font=font); y += 16
        draw.text((20, y), f"Fecha: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}", fill="black", font=font); y += 16
        draw.text((20, y), f"Método: {ticket['metodo']}", fill="black", font=font); y += 16
        draw.line((20, y, W-20, y), fill="#cccccc"); y += 10
        draw.text((20, y), "Producto", fill="black", font=font)
        draw.text((350, y), "Cant", fill="black", font=font)
        draw.text((450, y), "Precio", fill="black", font=font)
        y += 18
        for item in ticket.get("items", []):
            name = str(item["nombre"])[:28]
            qty = int(item["cantidad"])
            subtotal = float(item["precio"]) * qty
            draw.text((20, y), name, fill="black", font=font)
            draw.text((350, y), f"x {qty}", fill="black", font=font)
            draw.text((450, y), f"${subtotal:.2f}", fill="black", font=font)
            y += 18
        y += 8
        draw.line((20, y, W-20, y), fill="#cccccc"); y += 10
        draw.text((20, y), f"Total: ${ticket['total']:.2f}", fill="#B2334A", font=font)
        img.save(path, "PDF")
        if not auto:
            messagebox.showinfo("Ticket", f"PDF guardado en:\n{path}")
        return path

    def obtener_config_negocio(self):
        cfg = configparser.ConfigParser()
        root = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root, "mysql_config.ini")
        cfg.read(path, encoding="utf-8")
        name = cfg.get("business", "name", fallback="Boutique POS")
        address = cfg.get("business", "address", fallback="Dirección")
        phone = cfg.get("business", "phone", fallback="(000) 000-0000")
        return {"name": name, "address": address, "phone": phone}
        img.save(path, "PDF")
        if not auto:
            messagebox.showinfo("Ticket", f"PDF guardado en:\n{path}")
