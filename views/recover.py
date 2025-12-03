import customtkinter as ctk
from tkinter import messagebox
from database.db import crear_conexion

class RecoverWindow(ctk.CTkToplevel):
    """Ventana de recuperación de contraseña"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Recuperación de Contraseña")
        self.geometry("600x700")
        self.transient(parent)
        self.grab_set()
        
        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"600x700+{x}+{y}")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Contenedor principal con fondo gris claro
        main_frame = ctk.CTkFrame(self, fg_color="#E8E8E8")
        main_frame.pack(fill="both", expand=True)
        
        # Panel central blanco
        panel = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=20, width=450, height=600)
        panel.place(relx=0.5, rely=0.5, anchor="center")
        panel.pack_propagate(False)
        
        # Header con icono
        header_frame = ctk.CTkFrame(panel, fg_color="transparent")
        header_frame.pack(pady=(40, 10))
        
        # Icono de pregunta en círculo rosa
        icon_frame = ctk.CTkFrame(header_frame, fg_color="#FFE4E1", corner_radius=40, width=80, height=80)
        icon_frame.pack(side="left", padx=(0, 15))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text="?",
            font=("Segoe UI", 40, "bold"),
            text_color="#E91E63"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Títulos
        text_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        text_frame.pack(side="left")
        
        ctk.CTkLabel(
            text_frame,
            text="Recuperación de Contraseña",
            font=("Segoe UI", 18, "bold"),
            text_color="#2C2C2C",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame,
            text="Información de acceso al sistema",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w")
        
        # Contenedor de campos
        fields_frame = ctk.CTkFrame(panel, fg_color="transparent")
        fields_frame.pack(fill="x", padx=50, pady=(30, 0))
        
        # Correo electrónico
        ctk.CTkLabel(
            fields_frame,
            text="Ingresa tu correo electrónico",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        self.email_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="tu@gmail.com",
            height=50,
            corner_radius=25,
            border_width=0,
            fg_color="#F5F5F5",
            font=("Segoe UI", 13)
        )
        self.email_entry.pack(fill="x", pady=(0, 20))
        
        # Código de verificación
        ctk.CTkLabel(
            fields_frame,
            text="Ingresa el código que se envió a tu correo electrónico",
            font=("Segoe UI", 12),
            text_color="#666666",
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        self.code_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="••••••",
            show="•",
            height=50,
            corner_radius=25,
            border_width=0,
            fg_color="#F5F5F5",
            font=("Segoe UI", 13)
        )
        self.code_entry.pack(fill="x", pady=(0, 30))
        
        # Botón Iniciar Sesión (enviar código)
        ctk.CTkButton(
            fields_frame,
            text="Iniciar Sesión",
            height=50,
            corner_radius=25,
            fg_color="#E91E63",
            hover_color="#C2185B",
            font=("Segoe UI", 14, "bold"),
            command=self.verificar_codigo
        ).pack(fill="x", pady=(0, 15))
        
        # Botón Regresar
        ctk.CTkButton(
            fields_frame,
            text="Regresar",
            height=50,
            corner_radius=25,
            fg_color="#E91E63",
            hover_color="#C2185B",
            font=("Segoe UI", 14, "bold"),
            command=self.destroy
        ).pack(fill="x")
    
    def verificar_codigo(self):
        """Verificar código de recuperación"""
        email = self.email_entry.get().strip()
        codigo = self.code_entry.get().strip()
        
        if not email:
            messagebox.showwarning("Campo vacío", "Por favor ingresa tu correo electrónico")
            return
        
        if not codigo:
            messagebox.showwarning("Campo vacío", "Por favor ingresa el código de verificación")
            return
        
        try:
            conn = crear_conexion()
            cur = conn.cursor(dictionary=True)
            
            # Buscar usuario por email
            cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cur.fetchone()
            
            if not usuario:
                messagebox.showerror("Error", "No se encontró un usuario con ese correo electrónico")
                conn.close()
                return
            
            # Mostrar información de acceso incluyendo el correo
            messagebox.showinfo(
                "Información de Acceso Recuperada",
                f"📧 Correo: {usuario.get('email')}\n"
                f"👤 Usuario: {usuario.get('usuario')}\n"
                f"🔑 Contraseña: {usuario.get('contraseña')}\n\n"
                f"💡 Usa tu correo o usuario para iniciar sesión.\n"
                f"⚠️ Por seguridad, cambia tu contraseña después de iniciar sesión."
            )
            
            conn.close()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al recuperar contraseña: {str(e)}")


if __name__ == "__main__":
    # Prueba de la ventana
    root = ctk.CTk()
    root.withdraw()
    recover = RecoverWindow(root)
    root.mainloop()
