import customtkinter as ctk
from tkinter import messagebox
from database.db import crear_conexion
from utils.resource import resource_path
from views.main import MainApp
from views.recover import RecoverWindow
import os
import json
from PIL import Image, ImageDraw
# import bcrypt  # No necesario para contraseñas en texto plano

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Janet Rosa Bici - Iniciar Sesión")
        self.geometry("1100x700")
        self.minsize(800, 600)
        ctk.set_appearance_mode("light")
        
        self.mostrar_password = False
        self.config_file = "login_config.json"
        
        # Configuración de Grid Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.crear_interfaz()
        self.cargar_email_guardado()
        
    def crear_interfaz(self):
        # Fondo gris claro para toda la ventana
        self.main_frame = ctk.CTkFrame(self, fg_color="#E0E0E0")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Tarjeta central (Card) - MUCHO más ancha como en la imagen
        # En la imagen se ve una tarjeta bastante ancha, ocupando buena parte central
        self.card = ctk.CTkFrame(self.main_frame, fg_color="#F5F5F5", corner_radius=20, width=600)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        
        # Contenedor interno para padding - más espacioso
        self.content = ctk.CTkFrame(self.card, fg_color="transparent")
        self.content.pack(padx=80, pady=60, fill="both", expand=True)
        
        # --- Logo Circular ---
        self.crear_logo(self.content)
        
        # --- Título ---
        ctk.CTkLabel(
            self.content,
            text="Janet Rosa Bici",
            font=("Brush Script MT", 42),
            text_color="#2C2C2C"
        ).pack(pady=(15, 5))
        
        # --- Subtítulo ---
        ctk.CTkLabel(
            self.content,
            text="Iniciar sesión para continuar",
            font=("Segoe UI", 14),
            text_color="#757575"
        ).pack(pady=(0, 35))

        # --- Campos de Entrada ---
        
        # Email
        ctk.CTkLabel(
            self.content,
            text="Correo electrónico",
            font=("Segoe UI", 13, "bold"),
            text_color="#424242",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        self.user_entry = ctk.CTkEntry(
            self.content,
            height=50,  # Un poco más alto
            placeholder_text="tu@gmail.com",
            font=("Segoe UI", 14),
            border_width=0,
            corner_radius=10,
            fg_color="white",
            text_color="#333333"
        )
        self.user_entry.pack(fill="x", pady=(0, 5))
        self.user_entry.bind("<Return>", self.login_action_event)
        

        # Password
        ctk.CTkLabel(
            self.content,
            text="Contraseña",
            font=("Segoe UI", 13, "bold"),
            text_color="#424242",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        # Frame para password + botón ojo
        pass_frame = ctk.CTkFrame(self.content, fg_color="white", corner_radius=10, height=50)
        pass_frame.pack(fill="x", pady=(0, 5))
        pass_frame.pack_propagate(False)
        
        self.password_entry = ctk.CTkEntry(
            pass_frame,
            height=50,
            placeholder_text="••••••••",
            show="•",
            font=("Segoe UI", 14),
            border_width=0,
            corner_radius=10,
            fg_color="white",
            text_color="#333333"
        )
        self.password_entry.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.password_entry.bind("<Return>", self.login_action_event)
        
        self.toggle_btn = ctk.CTkButton(
            pass_frame,
            text="👁",
            width=45,
            height=45,
            fg_color="transparent",
            text_color="#757575",
            hover_color="#F0F0F0",
            corner_radius=10,
            command=self.toggle_password
        )
        self.toggle_btn.pack(side="right", padx=5)
        
        
        # --- Botón Iniciar Sesión ---
        ctk.CTkButton(
            self.content,
            text="→ Iniciar Sesión",
            height=55,
            fg_color="#F06262",  # Color salmón/rosado
            hover_color="#E55353",
            font=("Segoe UI", 15, "bold"),
            corner_radius=27,
            command=self.login_action
        ).pack(fill="x", pady=(0, 25))
        
        # --- Olvidé contraseña ---
        bottom_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        bottom_frame.pack(fill="x")
        
        self.recordar_var = ctk.BooleanVar(value=True)
        
        ctk.CTkButton(
            bottom_frame,
            text="¿Olvidaste tu contraseña?",
            fg_color="transparent",
            text_color="#333333",
            font=("Segoe UI", 13),
            hover_color="#E0E0E0",
            command=self.recover_action
        ).pack(side="top", anchor="center")

    def crear_logo(self, parent):
        # Logo con bicicleta rosa más grande
        logo_container = ctk.CTkFrame(parent, fg_color="transparent")
        logo_container.pack(pady=(0, 20))
        
        # Crear imagen de bicicleta rosa
        try:
            # Cargar el LOGO LIMPIO sin bordes
            logo_paths = [
                "logo_limpio_login.png",  # LOGO LIMPIO para login (250px)
                "logo_limpio_definitivo.png",  # Logo limpio completo
                "logo_limpio_200.png",  # Logo limpio 200px
                "assets/logo_limpio_login.png",  # En carpeta assets
                "assets/logo_limpio_definitivo.png",  # En carpeta assets
                "logo_final_login.png",  # Fallback imagen original
                "logo_janet_rosa_definitivo.png",  # Fallback original completa
                "logo_final_200.png",  # Fallback original 200px
                "assets/logo_final_login.png",  # Fallback en assets
                "assets/logo_janet_rosa_definitivo.png",  # Fallback en assets
                "Captura de pantalla 2025-12-01 234603.png",  # Imagen original directa
                "logo_nuevo_login.png",  # Fallback anterior
                "logo_janet_rosa_exacto.png",  # Fallback exacto
                "logo_nuevo_160.png",  # Fallback mediano
                "assets/logo_nuevo_login.png",  # Fallback en assets
                "logo_login_200.png",  # Fallback anterior
                "logo_circular_160.png",  # Fallback circular
                "assets/logo_login_200.png",  # Fallback en assets
                "assets/logo_circular_160.png",  # Fallback en assets
                "logo_janet_rosa_profesional.png",  # Fallback anterior
                "WhatsApp Image 2025-12-02 at 11.52.41 AM.jpeg",  # Imagen principal
                "janet_rosa_bici_logo_completo.png",  # Fallback creado
                "bicicleta_rosa_logo.png",  # Fallback de bicicleta
                "logo_original.png",  # Respaldo del logo original
                resource_path(os.path.join("assets", "bicicleta_rosa.png")),
                resource_path(os.path.join("assets", "logo_janet_rosa_bici.png")),
                resource_path(os.path.join("assets", "logo.png"))
            ]
            
            logo_image = None
            for path in logo_paths:
                if os.path.exists(path):
                    try:
                        # Si es el LOGO LIMPIO, usar tamaño grande
                        if "limpio_login" in path or "limpio_definitivo" in path:
                            img = Image.open(path)
                            logo_image = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(220, 220)  # Tamaño grande para el logo limpio
                            )
                        elif "limpio_200" in path:
                            img = Image.open(path)
                            logo_image = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(200, 200)  # Tamaño 200px para logo limpio
                            )
                        elif "final_login" in path or "definitivo" in path or "Captura de pantalla" in path:
                            img = Image.open(path)
                            logo_image = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(220, 220)  # Fallback imagen original
                            )
                        elif "final_200" in path:
                            img = Image.open(path)
                            logo_image = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(200, 200)  # Fallback 200px original
                            )
                        elif "nuevo_login" in path or "exacto" in path:
                            img = Image.open(path)
                            logo_image = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(200, 200)  # Fallback para logo exacto
                            )
                        elif "nuevo_160" in path:
                            img = Image.open(path)
                            logo_image = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(160, 160)
                            )
                        elif "login_200" in path or "profesional" in path:
                            img = Image.open(path)
                            logo_image = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(180, 180)
                            )
                        elif "circular" in path:
                            img = Image.open(path)
                            logo_image = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(160, 160)
                            )
                        else:
                            # Crear imagen circular
                            circular_image = self.crear_imagen_circular(path, (160, 160))
                            logo_image = ctk.CTkImage(
                                light_image=circular_image,
                                dark_image=circular_image,
                                size=(160, 160)
                            )
                        break
                    except Exception as e:
                        print(f"Error cargando {path}: {e}")
                        continue
            
            if logo_image:
                # Crear marco transparente para el LOGO LIMPIO
                if "limpio_login" in str(logo_paths[0]) or "limpio_definitivo" in str(logo_paths[0]):
                    # Marco transparente grande para el logo limpio
                    logo_frame = ctk.CTkFrame(logo_container, fg_color="transparent", width=220, height=220)
                    logo_frame.pack()
                    logo_frame.pack_propagate(False)
                elif "final_login" in str(logo_paths[0]) or "definitivo" in str(logo_paths[0]) or "Captura de pantalla" in str(logo_paths[0]):
                    # Marco transparente para imagen original (fallback)
                    logo_frame = ctk.CTkFrame(logo_container, fg_color="transparent", width=220, height=220)
                    logo_frame.pack()
                    logo_frame.pack_propagate(False)
                elif "nuevo_login" in str(logo_paths[0]) or "exacto" in str(logo_paths[0]):
                    # Marco transparente para el logo exacto anterior
                    logo_frame = ctk.CTkFrame(logo_container, fg_color="transparent", width=200, height=200)
                    logo_frame.pack()
                    logo_frame.pack_propagate(False)
                elif "login_200" in str(logo_paths[0]) or "profesional" in str(logo_paths[0]):
                    # Marco más grande para el logo profesional anterior
                    logo_frame = ctk.CTkFrame(logo_container, fg_color="transparent", width=180, height=180)
                    logo_frame.pack()
                    logo_frame.pack_propagate(False)
                else:
                    # Marco circular blanco para otros logos
                    logo_frame = ctk.CTkFrame(logo_container, fg_color="white", corner_radius=80, width=160, height=160)
                    logo_frame.pack()
                    logo_frame.pack_propagate(False)
                
                ctk.CTkLabel(logo_frame, image=logo_image, text="").place(relx=0.5, rely=0.5, anchor="center")
            else:
                # Si no encuentra la imagen, crear bicicleta con texto
                self.crear_logo_texto(logo_container)
                
        except Exception as e:
            print(f"Error general cargando logo: {e}")
            self.crear_logo_texto(logo_container)
    
    def crear_logo_texto(self, parent):
        """Crear logo con texto cuando no hay imagen disponible"""
        # Bicicleta emoji más grande
        ctk.CTkLabel(
            parent,
            text="🚲",
            font=("Segoe UI", 80),
            text_color="#E91E63"
        ).pack(pady=(0, 10))
        
        # Texto JANET ROSA BICI en formato vertical como en la imagen
        texto_frame = ctk.CTkFrame(parent, fg_color="transparent")
        texto_frame.pack()
        
        ctk.CTkLabel(
            texto_frame,
            text="JANET",
            font=("Segoe UI", 24, "bold"),
            text_color="#2C2C2C"
        ).pack()
        
        ctk.CTkLabel(
            texto_frame,
            text="ROSA",
            font=("Segoe UI", 24, "bold"),
            text_color="#2C2C2C"
        ).pack()
        
        ctk.CTkLabel(
            texto_frame,
            text="BICI",
            font=("Segoe UI", 24, "bold"),
            text_color="#2C2C2C"
        ).pack()

    def crear_imagen_circular(self, path, size):
        """Abre una imagen, la redimensiona y la devuelve como un objeto circular."""
        pil_image = Image.open(path).convert("RGBA")
        
        # Redimensionar a cuadrado
        pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
        
        # Crear máscara circular
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        
        # Aplicar máscara
        output = Image.new('RGBA', size, (255, 255, 255, 0))
        output.paste(pil_image, (0, 0), mask)
        
        return output


    def toggle_password(self):
        self.mostrar_password = not self.mostrar_password
        if self.mostrar_password:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="👁‍🗨")
        else:
            self.password_entry.configure(show="•")
            self.toggle_btn.configure(text="👁")

    def cargar_email_guardado(self):
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
        try:
            config = {
                'email': email if self.recordar_var.get() else '',
                'recordar': self.recordar_var.get()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar email: {e}")

    def login_action_event(self, event=None):
        """Manejador de evento para el login con la tecla Enter."""
        self.login_action()

    def login_action(self):
        usuario = self.user_entry.get()
        password = self.password_entry.get()

        if not usuario or not password:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingresa tu correo y contraseña.")
            return

        try:
            with crear_conexion() as conn:
                if conn is None or not conn.is_connected():
                    messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos.")
                    return
                
                with conn.cursor(dictionary=True) as cursor:
                    # Usamos %s como placeholder, estándar para mysql-connector
                    cursor.execute("SELECT * FROM usuarios WHERE email=%s LIMIT 1", (usuario,))
                    user = cursor.fetchone()

            if not user:
                messagebox.showerror("Error de Autenticación", "El correo electrónico no está registrado.")
                return

            # --- Verificación de contraseña en texto plano ---
            # Las contraseñas están almacenadas en texto plano en la base de datos
            password_db = user.get('contraseña', '')
            
            if password == password_db:
                # Contraseña correcta
                self.guardar_email(usuario)
                self.destroy()
                app = MainApp(user)
                app.mainloop()
            else:
                messagebox.showerror("Error de Autenticación", "La contraseña es incorrecta.")
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error durante el inicio de sesión:\n{e}")
            print(f"Error en login_action: {e}")

    def recover_action(self):
        RecoverWindow(self)
