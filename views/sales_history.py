import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser, tempfile
from pathlib import Path
from controllers.ventas import resumen_ventas, listar_ventas, exportar_ventas_csv
from datetime import datetime, timedelta
from controllers.ventas import obtener_ticket

class SalesHistoryView(ttk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user
        header = ttk.Frame(self); header.pack(fill="x", padx=8, pady=6)
        ttk.Label(header, text="Historial de Ventas", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Button(header, text="Exportar", command=self.exportar).pack(side="right")
        controls = ttk.Frame(self); controls.pack(fill="x", padx=8, pady=6)
        ttk.Label(controls, text="Buscar por ticket...").pack(side="left")
        self.search = ttk.Entry(controls, width=22); self.search.pack(side="left", padx=6)
        self._placeholder(self.search, "Buscar por ticket...")
        self.rango = ttk.Combobox(controls, values=["Todas las fechas","Hoy","Últimos 7 días","Este mes","Rango manual"], width=18, state="readonly")
        self.rango.current(0); self.rango.pack(side="left", padx=6)
        self.start = ttk.Entry(controls, width=10); self.start.pack(side="left")
        self.end = ttk.Entry(controls, width=10); self.end.pack(side="left", padx=4)
        ttk.Label(controls, text="Método").pack(side="left")
        self.metodo = ttk.Combobox(controls, values=["Todos","Efectivo","Tarjeta","Transferencia"], width=15, state="readonly")
        self.metodo.current(0); self.metodo.pack(side="left", padx=6)
        ttk.Button(controls, text="Aplicar", command=self.refresh).pack(side="left", padx=6)
        

        cards = ttk.Frame(self); cards.pack(fill="x", padx=8)
        try:
            data = resumen_ventas()
            self.card_total = ttk.Label(cards, text=f"Total Ventas: {data['total_ventas']}", padding=8); self.card_total.pack(side="left", padx=6)
            self.card_ingreso = ttk.Label(cards, text=f"Ingreso Total: ${data['ingreso_total']:.2f}", padding=8); self.card_ingreso.pack(side="left", padx=6)
            self.card_promedio = ttk.Label(cards, text=f"Promedio Venta: ${data['promedio']:.2f}", padding=8); self.card_promedio.pack(side="left", padx=6)
            self.card_prod = ttk.Label(cards, text=f"Productos vendidos: {data['productos_vendidos']}", padding=8); self.card_prod.pack(side="left", padx=6)
        except Exception:
            self.card_total = ttk.Label(cards, text="Sin conexión", padding=8); self.card_total.pack(side="left", padx=6)
            self.card_ingreso = ttk.Label(cards, text="", padding=8); self.card_ingreso.pack(side="left", padx=6)
            self.card_promedio = ttk.Label(cards, text="", padding=8); self.card_promedio.pack(side="left", padx=6)
            self.card_prod = ttk.Label(cards, text="", padding=8); self.card_prod.pack(side="left", padx=6)

        self.list_container = ttk.Frame(self); self.list_container.pack(fill="both", expand=True, padx=8, pady=8)
        self.refresh()

    def _compute_range(self):
        choice = self.rango.get()
        if choice == "Hoy":
            d = datetime.now().date().isoformat(); return d, d
        if choice == "Últimos 7 días":
            end = datetime.now().date(); start = end - timedelta(days=6); return start.isoformat(), end.isoformat()
        if choice == "Este mes":
            end = datetime.now().date(); start = end.replace(day=1); return start.isoformat(), end.isoformat()
        if choice == "Rango manual":
            s = self.start.get().strip() or None; e = self.end.get().strip() or None; return s, e
        return None, None

    def filtrar(self):
        q = self.search.get().strip()
        s,e = self._compute_range()
        rows = [v for v in listar_ventas(start_date=s, end_date=e, metodo=self.metodo.get()) if (not q or q == str(v["id_venta"]))]
        self._render(rows)

    def refresh(self):
        s,e = self._compute_range()
        m = self.metodo.get()
        try:
            rows = listar_ventas(start_date=s, end_date=e, metodo=m)
        except Exception:
            rows = []
        self._render(rows)
        try:
            d = resumen_ventas(start_date=s, end_date=e, metodo=(None if m=="Todos" else m))
            self.card_total.config(text=f"Total Ventas: {d['total_ventas']}")
            self.card_ingreso.config(text=f"Ingreso Total: ${float(d['ingreso_total']):.2f}")
            self.card_promedio.config(text=f"Promedio Venta: ${float(d['promedio']):.2f}")
            self.card_prod.config(text=f"Productos vendidos: {d['productos_vendidos']}")
        except Exception:
            pass

    def exportar(self):
        s,e = self._compute_range()
        m = self.metodo.get()
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="ventas_export.csv", filetypes=[("CSV","*.csv")])
        if not path:
            return
        exportar_ventas_csv(path, start_date=s, end_date=e, metodo=m if m!="Todos" else None)
        messagebox.showinfo("Exportar", f"Archivo guardado: {path}")

    def _render(self, rows):
        for w in self.list_container.winfo_children():
            w.destroy()
        if not rows:
            ttk.Label(self.list_container, text="No se encontraron ventas", padding=12).pack()
            return
        for v in rows:
            row = ttk.Frame(self.list_container, padding=12)
            row.pack(fill="x", pady=4)
            left = ttk.Frame(row); left.pack(side="left", fill="x", expand=True)
            right = ttk.Frame(row); right.pack(side="right")
            metodo = v.get("metodo_pago") or "-"
            ttk.Label(left, text=f"Ticket #{v['id_venta']} ", font=("Segoe UI", 11, "bold")).pack(side="left")
            chip = tk.Label(left, text=metodo, bg="#D1F5DC" if metodo=="Efectivo" else ("#D6E4FF" if metodo=="Tarjeta" else "#FFE9CC"), fg="#1A7F37" if metodo=="Efectivo" else ("#11367A" if metodo=="Tarjeta" else "#8A4B0B"))
            chip.pack(side="left", padx=6)
            fecha_txt = datetime.strptime(str(v['fecha']), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y, %I:%M %p") if isinstance(v['fecha'], str) else str(v['fecha'])
            sub = ttk.Label(row, text=f"{fecha_txt}   {int(v.get('items_count') or 0)} productos")
            sub.pack(anchor="w")
            ttk.Label(right, text=f"${float(v['total']):.2f}", font=("Segoe UI", 11, "bold")).pack()
            ttk.Button(right, text="Imprimir", command=lambda vid=v['id_venta']: self.imprimir_ticket(vid)).pack(pady=2)

    def imprimir_ticket(self, id_venta):
        ticket = obtener_ticket(id_venta)
        if not ticket:
            messagebox.showerror("Ticket", "No se encontró el ticket")
            return
        html = self._generar_html(ticket)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        tmp.write(html.encode("utf-8")); tmp.close()
        webbrowser.open(Path(tmp.name).as_uri())

    def _generar_html(self, ticket):
        lines = []
        for item in ticket.get("items", []):
            qty = int(item["cantidad"]) ; subtotal = float(item["precio"]) * qty
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
.total{{text-align:right;font-weight:700;margin-top:8px}}
.thanks{{text-align:center;margin-top:10px}}
</style></head><body>
<div class='wrap'>
<div class='title'>Ticket #{ticket['id_venta']}</div>
<div class='sub'>Método: {ticket['metodo']}</div>
<div class='sep'></div>
{''.join(lines)}
<div class='sep'></div>
<div class='total'>Total: ${ticket['total']:.2f}</div>
<div class='thanks'>¡Gracias por su compra!<br>Vuelva pronto</div>
</div>
<script>window.onload=function(){{setTimeout(()=>window.print(),300)}}</script>
</body></html>
"""

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