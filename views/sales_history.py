import customtkinter as ctk

class SalesHistoryView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user
        self.pack(fill="both", expand=True)
        self.panel_principal()

    def panel_principal(self):
        panel = ctk.CTkFrame(self)
        panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(panel, text="Historial de Ventas", font=("Segoe UI", 20, "bold")).pack(pady=10)

        # Estadísticas
        stats = [
            ("Total Ventas", "3"),
            ("Ingreso Total", "$550.00"),
            ("Promedio Venta", "$183.33"),
            ("Productos Vendidos", "3")
        ]
        stats_frame = ctk.CTkFrame(panel)
        stats_frame.pack(fill="x", pady=10)
        for label, value in stats:
            ctk.CTkLabel(stats_frame, text=f"{label}: {value}", font=("Segoe UI", 14)).pack(anchor="w")

        # Filtros y búsqueda
        filtros_frame = ctk.CTkFrame(panel)
        filtros_frame.pack(fill="x", pady=10)

        ctk.CTkEntry(filtros_frame, placeholder_text="Buscar por ticket...").pack(side="left", padx=5)
        ctk.CTkComboBox(filtros_frame, values=["Todas las fechas", "Hoy", "Semana", "Mes"]).pack(side="left", padx=5)
        ctk.CTkComboBox(filtros_frame, values=["Todos los métodos", "Efectivo", "Tarjeta", "Transferencia"]).pack(side="left", padx=5)
        ctk.CTkButton(filtros_frame, text="Exportar").pack(side="left", padx=5)

        # Lista de tickets
        tickets = [
            {"id": "#76969815", "fecha": "21/07/2023", "metodo": "Tarjeta", "productos": "1 producto"},
            {"id": "#504836", "fecha": "21/07/2023", "metodo": "Efectivo", "productos": "1 producto"},
            {"id": "#51894725", "fecha": "21/07/2023", "metodo": "Transferencia", "productos": "1 producto"},
        ]

        lista_frame = ctk.CTkFrame(panel)
        lista_frame.pack(fill="both", expand=True, pady=10)

        for ticket in tickets:
            item = ctk.CTkFrame(lista_frame, border_width=1, border_color="gray")
            item.pack(fill="x", pady=5)
            ctk.CTkLabel(item, text=f"Ticket {ticket['id']}", font=("Segoe UI", 14, "bold")).pack(anchor="w")
            ctk.CTkLabel(item, text=f"Fecha: {ticket['fecha']}").pack(anchor="w")
            ctk.CTkLabel(item, text=f"Método: {ticket['metodo']}").pack(anchor="w")
            ctk.CTkLabel(item, text=f"Productos: {ticket['productos']}").pack(anchor="w")
