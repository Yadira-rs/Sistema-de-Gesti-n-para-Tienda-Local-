import customtkinter as ctk

class LibreriaView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent, fg_color="#F5F5F5")
        self.user = user
        self.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header,
            text="📚 Librería",
            font=("Segoe UI", 24, "bold"),
            text_color="#333333"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Gestión de libros y recursos",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(anchor="w")
        
        # Contenido placeholder
        content = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            content,
            text="🚧 Sección en Construcción 🚧",
            font=("Segoe UI", 20, "bold"),
            text_color="#666666"
        ).place(relx=0.5, rely=0.4, anchor="center")
        
        ctk.CTkLabel(
            content,
            text="Próximamente podrás gestionar el inventario de la librería aquí.",
            font=("Segoe UI", 14),
            text_color="#888888"
        ).place(relx=0.5, rely=0.5, anchor="center")
