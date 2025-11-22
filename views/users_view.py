import tkinter as tk
from tkinter import ttk, messagebox
from controllers.users import listar_usuarios, crear_usuario

class UsersWindow(ttk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user
        header = ttk.Frame(self); header.pack(fill="x", padx=8, pady=6)
        ttk.Label(header, text="Gestión de Usuario", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Button(header, text="+ Nuevo Usuario", command=self.nuevo).pack(side="right")

        cards = ttk.Frame(self); cards.pack(fill="x", padx=8)
        try:
            data = self._metrics()
            ttk.Label(cards, text=f"Total: {data['total']}", padding=8).pack(side="left", padx=6)
            ttk.Label(cards, text=f"Admins: {data['admins']}", padding=8).pack(side="left", padx=6)
            ttk.Label(cards, text=f"Cajeros: {data['cajeros']}", padding=8).pack(side="left", padx=6)
            ttk.Label(cards, text=f"Empleados: {data['empleados']}", padding=8).pack(side="left", padx=6)
        except Exception:
            ttk.Label(cards, text="Sin conexión a la base de datos", padding=8).pack(side="left", padx=6)

        filtros = ttk.Frame(self); filtros.pack(fill="x", padx=8, pady=6)
        ttk.Label(filtros, text="Buscar por usuario...").pack(side="left")
        self.search = ttk.Entry(filtros, width=22); self.search.pack(side="left", padx=6)
        ttk.Button(filtros, text="Filtrar", command=self.filtrar).pack(side="left")

        self.tabla = ttk.Treeview(self, columns=("id", "usuario", "rol"), show="headings", height=14)
        for col, text in [("id", "ID"), ("usuario", "Usuario"), ("rol", "Rol")]:
            self.tabla.heading(col, text=text)
        self.tabla.pack(fill="both", expand=True, padx=8, pady=8)
        try:
            self.cargar()
        except Exception:
            ttk.Label(self, text="No se pudieron cargar usuarios", padding=8).pack()

    def _metrics(self):
        rows = listar_usuarios();
        total = len(rows)
        admins = sum(1 for r in rows if r['rol'] == 'Administrador')
        cajeros = sum(1 for r in rows if r['rol'] == 'Cajero')
        empleados = sum(1 for r in rows if r['rol'] == 'Empleado')
        return {"total": total, "admins": admins, "cajeros": cajeros, "empleados": empleados}

    def cargar(self):
        self.tabla.delete(*self.tabla.get_children())
        for u in listar_usuarios():
            self.tabla.insert("", tk.END, values=(u["id_usuario"], u["usuario"], u["rol"]))

    def filtrar(self):
        q = self.search.get().strip().lower(); self.tabla.delete(*self.tabla.get_children())
        for u in listar_usuarios():
            if not q or q in u["usuario"].lower():
                self.tabla.insert("", tk.END, values=(u["id_usuario"], u["usuario"], u["rol"]))

    def nuevo(self):
        win = tk.Toplevel(self)
        win.title("Nuevo Usuario"); win.geometry("460x380")
        frm = ttk.Frame(win, padding=16); frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Nombre de usuario").grid(row=0, column=0, sticky="w", pady=4)
        e_user = ttk.Entry(frm); e_user.grid(row=0, column=1, sticky="ew")
        ttk.Label(frm, text="Contraseña").grid(row=1, column=0, sticky="w", pady=4)
        e_pass = ttk.Entry(frm, show="*"); e_pass.grid(row=1, column=1, sticky="ew")
        ttk.Label(frm, text="Rol").grid(row=2, column=0, sticky="w", pady=4)
        rol = tk.StringVar(value="Cajero")
        ttk.Combobox(frm, textvariable=rol, values=["Administrador","Cajero","Empleado"], state="readonly").grid(row=2, column=1, sticky="ew")
        ttk.Label(frm, text="Pregunta").grid(row=3, column=0, sticky="w", pady=4)
        e_preg = ttk.Entry(frm); e_preg.grid(row=3, column=1, sticky="ew")
        ttk.Label(frm, text="Respuesta").grid(row=4, column=0, sticky="w", pady=4)
        e_resp = ttk.Entry(frm); e_resp.grid(row=4, column=1, sticky="ew")
        frm.columnconfigure(1, weight=1)
        def save():
            u = e_user.get().strip(); p = e_pass.get().strip()
            if not u or not p:
                messagebox.showwarning("Datos", "Usuario y contraseña son obligatorios"); return
            crear_usuario(u, p, rol.get(), e_preg.get().strip(), e_resp.get().strip())
            messagebox.showinfo("Usuarios", "Usuario creado")
            win.destroy(); self.cargar()
        ttk.Button(frm, text="Crear usuario", command=save).grid(row=5, column=0, columnspan=2, pady=12)