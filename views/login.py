import customtkinter as ctk
from tkinter import messagebox
from database.db import crear_conexion
from views.main import MainApp
from views.recover import RecoverWindow
import os
import json

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Janet Rosa Bici - Login")
        self.geometry("600x700")
        ctk.set_appearance_mode("light")
        
        self.mostrar_password = False
        self.config_file = "login_config.json"
        self.crear_interfaz()
        self.cargar_email_guardado()
    
    def crear_interfaz(self):
        # Contenedor principal con fondo gris claro
        main_frame = ctk.CTkFrame(self, fg_color="#F5F5F5")
        main_frame.pack(fill="both", expand=True)
        
        # Panel central blanco
        panel = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=20, width=450, height=600)
        panel.place(relx=0.5, rely=0.5, anchor="center")
        panel.pack_propagate(False)
        
        # Logo circular
        logo_frame = ctk.CTkFrame(panel, fg_color="white", corner_radius=60, width=120, height=120)
        logo_frame.pack(pady=(40, 10))
        logo_frame.pack_propagate(False)
        
        # Intentar cargar la imagen del logo
        try:
            from PIL import Image
            import os
            
            # Buscar el logo en diferentes ubicaciones posibles
            logo_paths = [
                "logo.png",
                "assets/logo.png",
                "images/logo.png",
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png")
            ]
            
            logo_image = None
            for path in logo_paths:
                if os.path.exists(path):
                    logo_image = ctk.CTkImage(
                        light_image=Image.open(path),
                        dark_image=Image.open(path),
                        size=(100, 100)
                    )
                    break
            
            if logo_image:
                ctk.CTkLabel(
                    logo_frame,
                    image=logo_image,
                    text=""
                ).place(relx=0.5, rely=0.5, anchor="center")
            else:
                # Si no se encuentra la imagen, usar emoji
                ctk.CTkLabel(
                    logo_frame,
                    text="🚲",
                    font=("Segoe UI", 50),
                    text_color="#E91E63"
                ).place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            # Si hay error, usar emoji
            ctk.CTkLabel(
                logo_frame,
                text="🚲",
                font=("Segoe UI", 50),
                text_color="#E91E63"
            ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Título con "Rosa" en color rosa
        title_frame = ctk.CTkFrame(panel, fg_color="transparent")
        title_frame.pack(pady=(10, 5))
        
        ctk.CTkLabel(
            title_frame,
            text="Janet ",
            font=("Brush Script MT", 32),
            text_color="#2C2C2C"
        ).pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Rosa ",
            font=("Brush Script MT", 32),
            text_color="#E91E63"
        ).pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Bici",
            font=("Brush Script MT", 32),
            text_color="#2C2C2C"
        ).pack(side="left")
        
        # Subtítulo
        ctk.CTkLabel(
            panel,
            text="Iniciar sesión para continuar",
            font=("Segoe UI", 13),
            text_color="#666666"
        ).pack(pady=(0, 30))
        
        # Contenedor de campos
        fields_frame = ctk.CTkFrame(panel, fg_color="transparent")
        fields_frame.pack(fill="x", padx=50)
        
        # Correo electrónico
        email_label_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        email_label_frame.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(
            email_label_frame,
            text="Correo electrónico",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(side="left")
        
        # Checkbox para recordar email
        self.recordar_var = ctk.BooleanVar(value=True)
        self.recordar_check = ctk.CTkCheckBox(
            email_label_frame,
            text="Recordar",
            variable=self.recordar_var,
            font=("Segoe UI", 10),
            text_color="#999999",
            fg_color="#E91E63",
            hover_color="#C2185B",
            checkbox_width=18,
            checkbox_height=18
        )
        self.recordar_check.pack(side="right")
        
        self.user_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="tu@gmail.com",
            height=50,
            corner_radius=25,
            border_width=0,
            fg_color="#F5F5F5",
            font=("Segoe UI", 13)
        )
        self.user_entry.pack(fill="x", pady=(0, 20))
        
        # Contraseña
        ctk.CTkLabel(
            fields_frame,
            text="Contraseña",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        password_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 30))
        
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="••••••••",
            show="•",
            height=50,
            corner_radius=25,
            border_width=0,
            fg_color="#F5F5F5",
            font=("Segoe UI", 13)
        )
        self.password_entry.pack(side="left", fill="x", expand=True)
        
        # Botón mostrar/ocultar contraseña
        self.toggle_btn = ctk.CTkButton(
            password_frame,
            text="👁",
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#F5F5F5",
            text_color="#666666",
            hover_color="#E0E0E0",
            font=("Segoe UI", 16),
            command=self.toggle_password
        )
        self.toggle_btn.pack(side="left", padx=(10, 0))
        
        # Botón Iniciar Sesión
        ctk.CTkButton(
            fields_frame,
            text="➜  Iniciar Sesión",
            height=50,
            corner_radius=25,
            fg_color="#E91E63",
            hover_color="#C2185B",
            font=("Segoe UI", 14, "bold"),
            command=self.login_action
        ).pack(fill="x", pady=(0, 20))
        
        # ¿Olvidaste tu contraseña?
        forgot_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        forgot_frame.pack()
        
        ctk.CTkLabel(
            forgot_frame,
            text="ⓘ",
            font=("Segoe UI", 14),
            text_color="#666666"
        ).pack(side="left", padx=(0, 5))
        
        forgot_btn = ctk.CTkButton(
            forgot_frame,
            text="¿Olvidaste tu contraseña?",
            fg_color="transparent",
            text_color="#666666",
            hover_color="white",
            font=("Segoe UI", 12),
            command=self.recover_action
        )
        forgot_btn.pack(side="left")
    
    def toggle_password(self):
        """Mostrar/ocultar contraseña"""
        self.mostrar_password = not self.mostrar_password
        
        if self.mostrar_password:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="👁‍🗨")
        else:
            self.password_entry.configure(show="•")
            self.toggle_btn.configure(text="👁")

    def cargar_email_guardado(self):
        """Cargar el email guardado si existe"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    email_guardado = config.get('email', '')
                    recordar = config.get('recordar', True)
                    
                    if email_guardado and recordar:
                        self.user_entry.insert(0, email_guardado)
                        self.recordar_var.set(True)
        except Exception as e:
            print(f"Error al cargar email guardado: {e}")
    
    def guardar_email(self, email):
        """Guardar el email si el usuario lo desea"""
        try:
            config = {
                'email': email if self.recordar_var.get() else '',
                'recordar': self.recordar_var.get()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar email: {e}")

    def login_action(self):
        usuario = self.user_entry.get()
        password = self.password_entry.get()

        conn = crear_conexion()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos.")
            return

        cursor = conn.cursor(dictionary=True)
        # Buscar por usuario o email
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s OR email=%s LIMIT 1", (usuario, usuario))
        user = cursor.fetchone()
        conn.close()

        # Primero, verificar si el usuario existe
        if not user:
            messagebox.showerror("Error", "Credenciales incorrectas")
            return

        pwd_field = 'contraseña' if 'contraseña' in user else ('password' if 'password' in user else None)
        if not pwd_field or str(user.get(pwd_field, '')) != password:
            messagebox.showerror("Error", "Credenciales incorrectas")
            return
        
        # Guardar email si el usuario lo desea
        self.guardar_email(usuario)
        
        # Si el login es exitoso
        self.destroy() # Cierra la ventana de login
        app = MainApp(user) # Abre la ventana principal
        app.mainloop()

    def recover_action(self):
        """Abrir ventana de recuperación de contraseña"""
        RecoverWindow(self)
