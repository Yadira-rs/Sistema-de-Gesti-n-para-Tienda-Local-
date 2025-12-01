import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.users import listar_usuarios, crear_usuario

from views.nuevo_usuario_form import NuevoUsuarioForm
class UsersView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user
        self.pack(fill="both", expand=True)

        # --- Cargar datos ---
        usuarios = listar_usuarios()
        resumen = self._metrics(usuarios)

        # --- Panel principal ---
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        header = ctk.CTkFrame(main, fg_color="transparent")
        header.pack(fill="x", pady=10)
        ctk.CTkLabel(header, text="Gestión de Usuario", font=("Segoe UI", 20, "bold")).pack(side="left")
        ctk.CTkButton(header, text="+ Nuevo Usuario", fg_color="#D76B74", command=self.nuevo).pack(side="right")

        # Resumen
        resumen_frame = ctk.CTkFrame(main)
        resumen_frame.pack(fill="x", pady=10)

        resumen_labels = [
            f"Total: {resumen['total']}",
            f"Admins: {resumen['admins']}",
            f"Cajeros: {resumen['cajeros']}",
            f"Empleados: {resumen['empleados']}"
        ]
        for txt in resumen_labels:
            ctk.CTkLabel(resumen_frame, text=txt, font=("Segoe UI", 14)).pack(side="left", padx=10, pady=5, expand=True)

        # Mensaje de recuperación
        ctk.CTkLabel(main, text="¿Olvidaste la contraseña?", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 5))
        ctk.CTkLabel(main, text="Tú, al ser administrador, puedes restaurar las contraseñas utilizando el botón 'olvide mi contraseña' en el inicio de sesión.",
                     wraplength=800, justify="left", text_color="gray").pack(anchor="w")

        # Tabla de usuarios
        tabla = ctk.CTkScrollableFrame(main)
        tabla.pack(fill="both", expand=True, pady=20)

        headers = ["ID Usuario", "Usuario", "Rol"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(tabla, text=h, font=("Segoe UI", 12, "bold")).grid(row=0, column=i, padx=10, pady=5, sticky="w")

        for r, u in enumerate(usuarios, start=1):
            ctk.CTkLabel(tabla, text=u.get("id_usuario", "")).grid(row=r, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(tabla, text=u.get("usuario", "")).grid(row=r, column=1, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(tabla, text=u.get("rol", "")).grid(row=r, column=2, padx=10, pady=5, sticky="w")

    def _metrics(self, rows):
        """Calcula las métricas de resumen de usuarios."""
        total = len(rows)
        admins = sum(1 for r in rows if r.get('rol') == 'Administrador')
        cajeros = sum(1 for r in rows if r.get('rol') == 'Cajero')
        empleados = sum(1 for r in rows if r.get('rol') == 'Empleado')
        return {"total": total, "admins": admins, "cajeros": cajeros, "empleados": empleados}

    def nuevo(self):
        """Abre la ventana para crear un nuevo usuario (lógica existente)."""
        def handle_creacion(datos):
            usuario = datos["usuario"].strip()
            password = datos["password"].strip()
            if not usuario or not password:
                messagebox.showwarning("Datos incompletos", "Usuario y contraseña son obligatorios.", parent=self)
                return
            
            crear_usuario(
                usuario,
                password,
                datos["rol"],
                datos["pregunta"].strip(),
                datos["respuesta"].strip()
            )
            messagebox.showinfo("Usuarios", "Usuario creado correctamente.", parent=self)
            # Para recargar la vista, se necesitaría una función de recarga en UsersView

        form = NuevoUsuarioForm(self, on_create=handle_creacion)
        
