import customtkinter as ctk

class CreditosView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user

        # Configuración de apariencia (se puede centralizar en el futuro)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.main_panel()

    def main_panel(self):
        """Crea el panel principal con las pestañas de créditos."""
        self.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True)

        self.tabs.add("Control de Ventas a Crédito")
        self.tabs.add("Créditos a clientes")
        self.tabs.add("Vencidos")
        self.tabs.add("Abonos de Hoy")

        self.creditos_clientes_tab()

    def creditos_clientes_tab(self):
        """Popula la pestaña 'Créditos a clientes'."""
        tab = self.tabs.tab("Créditos a clientes")

        # Mensaje de gestión de límites
        limites_frame = ctk.CTkFrame(tab)
        limites_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(limites_frame, text="Gestión de Límites de Crédito", font=("Arial", 16)).pack(anchor="w")
        ctk.CTkLabel(limites_frame, text="Configura los límites de créditos disponibles para cada cliente").pack(anchor="w")
        ctk.CTkLabel(limites_frame, text="No hay clientes registrados", text_color="gray").pack(anchor="w")

        # Mensaje de créditos
        creditos_frame = ctk.CTkFrame(tab)
        creditos_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(creditos_frame, text="No se encontraron créditos", text_color="gray").pack()

        # Botones
        botones_frame = ctk.CTkFrame(tab)
        botones_frame.pack(fill="x", pady=10)
        ctk.CTkButton(botones_frame, text="+ Nuevo Crédito").pack(side="left", padx=5)
        ctk.CTkButton(botones_frame, text="Actualizar Lista").pack(side="left", padx=5)

        # Resumen
        resumen_frame = ctk.CTkFrame(tab)
        resumen_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(resumen_frame, text="Resumen de Créditos", font=("Arial", 14)).pack(anchor="w")
        resumen = [
            ("Total Por Cobrar", "$0.00"),
            ("Créditos Activos", "0"),
            ("Créditos Vencidos", "0")
        ]
        for label, valor in resumen:
            ctk.CTkLabel(resumen_frame, text=f"{label}: {valor}").pack(anchor="w")
