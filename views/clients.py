import tkinter as tk
from tkinter import ttk, messagebox
from controllers.clientes_controller import agregar_cliente, obtener_clientes


class ClientsWindow:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user

        self.frame = tk.Frame(self.parent, bg="#ffffff")
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame,
            text="👥 Módulo de Clientes",
            font=("Arial", 18, "bold"),
            bg="#ffffff"
        ).pack(pady=10)

        self._crear_formulario()
        self._crear_tabla()

        # Cargar clientes al iniciar
        self.cargar_clientes()

    # ==========================
    #  FORMULARIO DE CLIENTES
    # ==========================
    def _crear_formulario(self):
        form_frame = tk.Frame(self.frame, bg="#ffffff")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nombre:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.nombre = tk.Entry(form_frame, width=40)
        self.nombre.grid(row=0, column=1)

        tk.Label(form_frame, text="Teléfono:", bg="#ffffff").grid(row=1, column=0, padx=5, pady=5)
        self.telefono = tk.Entry(form_frame, width=40)
        self.telefono.grid(row=1, column=1)

        tk.Label(form_frame, text="Correo:", bg="#ffffff").grid(row=2, column=0, padx=5, pady=5)
        self.correo = tk.Entry(form_frame, width=40)
        self.correo.grid(row=2, column=1)

        tk.Button(
            form_frame,
            text="Guardar Cliente",
            command=self.guardar_cliente,
            bg="#4CAF50",
            fg="white",
            padx=10
        ).grid(row=3, columnspan=2, pady=10)

    # ==========================
    #        TABLA
    # ==========================
    def _crear_tabla(self):
        tabla_frame = tk.Frame(self.frame, bg="#ffffff")
        tabla_frame.pack(fill="both", expand=True, pady=10)

        columnas = ("ID", "Nombre", "Telefono", "Correo")

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=10
        )
        self.tabla.pack(side="left", fill="both", expand=True)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150, anchor="center")

        scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        scroll.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scroll.set)

    # ==========================
    #   FUNCIONES DE CRUD
    # ==========================
    def guardar_cliente(self):
        nombre = self.nombre.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()

        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return

        if agregar_cliente(nombre, telefono, correo):
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")

            # Limpia los campos
            self.nombre.delete(0, tk.END)
            self.telefono.delete(0, tk.END)
            self.correo.delete(0, tk.END)

            self.cargar_clientes()
        else:
            messagebox.showerror("Error", "No se pudo guardar el cliente")

    def cargar_clientes(self):
        self.tabla.delete(*self.tabla.get_children())
        clientes = obtener_clientes()

        for cliente in clientes:
            self.tabla.insert("", tk.END, values=cliente)
