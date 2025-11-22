import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.apartados import resumen_apartados, listar_apartados, crear_apartado, cambiar_estado, registrar_anticipo, exportar_apartados_csv

class ApartadoView(ttk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user
        header = ttk.Frame(self); header.pack(fill="x", padx=8, pady=6)
        ttk.Label(header, text="Apartados", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Button(header, text="+ Nuevo Apartado", command=self.nuevo).pack(side="right")

        cards = ttk.Frame(self); cards.pack(fill="x", padx=8)
        try:
            r = resumen_apartados()
            ttk.Label(cards, text=f"Total\n{r['total']}", padding=10).pack(side="left", padx=6)
            ttk.Label(cards, text=f"Activos\n{r['activos']}", padding=10).pack(side="left", padx=6)
            ttk.Label(cards, text=f"Completados\n{r['completados']}", padding=10).pack(side="left", padx=6)
            ttk.Label(cards, text=f"Cancelados\n{r['cancelados']}", padding=10).pack(side="left", padx=6)
            ttk.Label(cards, text=f"Pendiente\n${float(r['pendiente_total']):.2f}", padding=10).pack(side="left", padx=6)
        except Exception:
            ttk.Label(cards, text="Sin conexión", padding=10).pack(side="left", padx=6)

        filtros = ttk.Frame(self); filtros.pack(fill="x", padx=8, pady=6)
        ttk.Label(filtros, text="Buscar por cliente, teléfono o ID...").pack(side="left")
        self.search = ttk.Entry(filtros, width=26); self.search.pack(side="left", padx=6)
        ttk.Label(filtros, text="Desde").pack(side="left")
        self.start = ttk.Entry(filtros, width=12); self.start.pack(side="left", padx=4)
        ttk.Label(filtros, text="Hasta").pack(side="left")
        self.end = ttk.Entry(filtros, width=12); self.end.pack(side="left", padx=4)
        ttk.Label(filtros, text="Estado").pack(side="left")
        self.estado = ttk.Combobox(filtros, values=["Todos","Pendiente","Pagado","Cancelado"], state="readonly", width=15); self.estado.current(0); self.estado.pack(side="left", padx=6)
        ttk.Button(filtros, text="Aplicar", command=self.cargar).pack(side="left")
        ttk.Button(filtros, text="Exportar", command=self.exportar).pack(side="right")

        cols = ("id","cliente","total","anticipo","saldo","fecha","estado")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c,t in zip(cols, ["ID","Cliente","Total","Anticipo","Saldo","Fecha Límite","Estado"]):
            self.tabla.heading(c, text=t)
        self.tabla.pack(fill="both", expand=True, padx=8, pady=8)

        actions = ttk.Frame(self); actions.pack(fill="x", padx=8, pady=6)
        ttk.Button(actions, text="Marcar Pagado", command=lambda: self.set_estado("Pagado")).pack(side="left")
        ttk.Button(actions, text="Cancelar", command=lambda: self.set_estado("Cancelado")).pack(side="left", padx=6)
        ttk.Button(actions, text="Registrar Anticipo", command=self.add_anticipo).pack(side="left", padx=6)

        self.cargar()

    def cargar(self):
        self.tabla.delete(*self.tabla.get_children())
        estado = self.estado.get() if hasattr(self, 'estado') else None
        try:
            rows = listar_apartados(estado=estado, search=self.search.get().strip() if hasattr(self, 'search') else None, start_date=(self.start.get().strip() or None), end_date=(self.end.get().strip() or None))
        except Exception:
            rows = []
        for a in rows:
            self.tabla.insert("", tk.END, values=(a["id_apartado"], a.get("cliente") or "-", f"${float(a['total']):.2f}", f"${float(a.get('anticipo') or 0):.2f}", f"${float(a.get('saldo') or 0):.2f}", str(a.get("fecha_limite") or a["fecha"]), a["estado"]))

    def set_estado(self, estado):
        sel = self.tabla.focus()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un apartado"); return
        pid = int(self.tabla.item(sel, "values")[0])
        cambiar_estado(pid, estado)
        self.cargar()

    def nuevo(self):
        win = tk.Toplevel(self); win.title("Nuevo Apartado"); win.geometry("420x280")
        frm = ttk.Frame(win, padding=16); frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="ID Cliente").grid(row=0, column=0, sticky="w", pady=4)
        e_cliente = ttk.Entry(frm); e_cliente.grid(row=0, column=1, sticky="ew")
        ttk.Label(frm, text="Total").grid(row=1, column=0, sticky="w", pady=4)
        e_total = ttk.Entry(frm); e_total.grid(row=1, column=1, sticky="ew")
        ttk.Label(frm, text="Anticipo").grid(row=2, column=0, sticky="w", pady=4)
        e_anticipo = ttk.Entry(frm); e_anticipo.grid(row=2, column=1, sticky="ew")
        ttk.Label(frm, text="Fecha Límite (YYYY-MM-DD)").grid(row=3, column=0, sticky="w", pady=4)
        e_fecha = ttk.Entry(frm); e_fecha.grid(row=3, column=1, sticky="ew")
        frm.columnconfigure(1, weight=1)
        def save():
            cid = e_cliente.get().strip() or None
            try:
                total = float(e_total.get().strip())
            except Exception:
                messagebox.showerror("Total", "Ingresa un total válido"); return
            anticipo = 0.0
            try:
                anticipo = float((e_anticipo.get().strip() or "0"))
            except Exception:
                messagebox.showerror("Anticipo", "Ingresa un anticipo válido"); return
            fecha_limite = e_fecha.get().strip() or None
            crear_apartado(int(cid) if cid else None, total, anticipo, fecha_limite)
            messagebox.showinfo("Apartados", "Apartado creado")
            win.destroy(); self.cargar()
        ttk.Button(frm, text="Crear", command=save).grid(row=2, column=0, columnspan=2, pady=12)

    def add_anticipo(self):
        sel = self.tabla.focus()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un apartado"); return
        pid = int(self.tabla.item(sel, "values")[0])
        monto = simpledialog.askfloat("Anticipo", "Monto a registrar:")
        if not monto:
            return
        registrar_anticipo(pid, monto)
        self.cargar()

    def exportar(self):
        path = simpledialog.askstring("Exportar", "Ruta del archivo CSV:")
        if not path:
            return
        exportar_apartados_csv(path, estado=self.estado.get(), search=self.search.get().strip() or None, start_date=self.start.get().strip() or None, end_date=self.end.get().strip() or None)
        messagebox.showinfo("Exportar", "Archivo exportado")