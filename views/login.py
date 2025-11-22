import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageOps
import os, configparser
from database.db import crear_conexion
from views.main import MainApp
from views.recover import RecoverWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Iniciar sesión")
        self.root.geometry("620x600")
        self.root.configure(bg="#020823")

        # ====== Estilos ======
        style = ttk.Style()
        style.configure("Pink.TButton", font=("Segoe UI", 11, "bold"),
                        foreground="#fff", background="#E48CA6")
        style.map("Pink.TButton", background=[("active", "#D97393")])
        style.configure("Card.TFrame", background="#d9d9d9")
        style.configure("Card.TLabel", background="#d9d9d9")

        # ====== Contenedor principal ======
        wrap = ttk.Frame(root, padding=20)
        wrap.pack(fill="both", expand=True)

        container = ttk.Frame(wrap, style="Card.TFrame", padding=(30, 30))
        container.place(relx=0.5, rely=0.5, anchor="center", width=520, height=520)

        # ====== Logo ======
        base_dir = os.path.dirname(os.path.dirname(__file__))
        candidates = [
            os.path.join(base_dir, "logo_bici.jpeg"),
            os.path.join(base_dir, "logo.jpeg"),
            os.path.join(base_dir, "logo.png"),
            os.path.join(base_dir, "WhatsApp Image 2025-11-20 at 10.25.27 AM.jpeg"),
        ]
        img_obj = None
        for p in candidates:
            try:
                img_obj = Image.open(p).convert("RGBA")
                break
            except Exception:
                continue
        try:
            base = (img_obj or Image.new("RGBA", (90, 90), (255,255,255,255))).resize((90, 90))
            mask = Image.new("L", (90, 90), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 90, 90), fill=255)
            rounded = ImageOps.fit(base, (90, 90), centering=(0.5, 0.5))
            rounded.putalpha(mask)
            bg = Image.new("RGBA", (96, 96), (238, 238, 238, 255))
            bg.paste(rounded, (3, 3), rounded)
            border = ImageDraw.Draw(bg)
            border.ellipse((1, 1, 95, 95), outline=(200, 200, 200, 255), width=2)
            self.logo = ImageTk.PhotoImage(bg)
            tk.Label(container, image=self.logo, bg="#d9d9d9").pack(pady=(0, 6))
        except Exception:
            ttk.Label(container, text="Boutique POS", font=("Segoe UI", 18, "bold"),
                      style="Card.TLabel").pack(pady=10)

        # ====== Marca ======
        biz = self.obtener_config_negocio()
        brand = ttk.Frame(container, style="Card.TFrame")
        brand.pack(pady=8)

        parts = biz.get("name", "Boutique POS").split()
        if parts:
            ttk.Label(brand, text=parts[0], font=("Segoe UI", 20, "bold"),
                      style="Card.TLabel").pack(side="left")
        if len(parts) >= 2:
            ttk.Label(brand, text=f" {parts[1]} ", font=("Segoe Script", 20, "italic"),
                      foreground="#D97393", style="Card.TLabel").pack(side="left")
        if len(parts) >= 3:
            ttk.Label(brand, text=parts[2], font=("Segoe UI", 20, "bold"),
                      style="Card.TLabel").pack(side="left")

        ttk.Label(container, text="Iniciar sesión para continuar",
                  font=("Segoe UI", 10), style="Card.TLabel").pack(pady=(0, 10))

        # ====== Usuario ======
        ttk.Label(container, text="Correo electrónico", style="Card.TLabel").pack(anchor="w", pady=(10, 4))
        self.user_entry = ttk.Entry(container, font=("Segoe UI", 12))
        self.user_entry.pack(fill="x")
        self._placeholder(self.user_entry, "tu@gmail.com")

        # ====== Contraseña ======
        ttk.Label(container, text="Contraseña", style="Card.TLabel").pack(anchor="w", pady=(12, 4))
        pass_row = ttk.Frame(container, style="Card.TFrame")
        pass_row.pack(fill="x")
        self.pass_entry = ttk.Entry(pass_row, show="*", font=("Segoe UI", 12))
        self.pass_entry.pack(side="left", fill="x", expand=True)
        self.show_pass = tk.BooleanVar(value=False)
        ttk.Button(pass_row, text="👁", width=3, command=self.toggle_password).pack(side="right", padx=6)

        # ====== Botón login ======
        ttk.Button(container, text="Iniciar Sesión", style="Pink.TButton",
                   command=self.login).pack(pady=20, fill="x")

        # ====== Link recuperar ======
        link = ttk.Label(container, text="¿Olvidaste tu contraseña?", foreground="#D97393", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: RecoverWindow(self.root))

    # ====== Lógica de login ======
    def login(self):
        usuario = self.user_entry.get()
        password = self.pass_entry.get()

        conn = crear_conexion()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s LIMIT 1", (usuario,))
        user = cursor.fetchone()
        conn.close()

        if user:
            pwd_field = 'contraseña' if 'contraseña' in user else ('password' if 'password' in user else None)
            if not pwd_field or str(user.get(pwd_field, '')) != password:
                messagebox.showerror("Error", "Credenciales incorrectas")
                return
            self.root.destroy()
            app = MainApp(user)
            app.mainloop()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def toggle_password(self):
        self.show_pass.set(not self.show_pass.get())
        self.pass_entry.configure(show=("" if self.show_pass.get() else "*"))

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

    def obtener_config_negocio(self):
        cfg = configparser.ConfigParser()
        root = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root, "mysql_config.ini")
        cfg.read(path, encoding="utf-8")
        return {
            "name": cfg.get("business", "name", fallback="Janet Rosa Bici"),
            "address": cfg.get("business", "address", fallback=""),
            "phone": cfg.get("business", "phone", fallback="")
        }
