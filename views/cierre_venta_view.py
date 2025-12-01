import customtkinter as ctk

class CierreVentaView(ctk.CTkFrame):
    def __init__(self, parent, total=280.00):
        super().__init__(parent)
        self.total = total
        self.efectivo = ctk.DoubleVar(value=0.0)
        self.otros = ctk.DoubleVar(value=0.0)
        self.cambio = ctk.DoubleVar(value=0.0)

        self.pack(fill="both", expand=True)
        self.sidebar()
        self.panel_principal()

    def sidebar(self):
        sidebar = ctk.CTkFrame(self, width=180)
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(sidebar, text="Cierre de Venta", font=("Segoe UI", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(sidebar, text="Administrador de Almacén", font=("Segoe UI", 12)).pack()
        ctk.CTkLabel(sidebar, text="admin@jrossabici.com", font=("Segoe UI", 10), text_color="gray").pack()

    def panel_principal(self):
        panel = ctk.CTkFrame(self)
        panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(panel, text="Cierre de Venta", font=("Segoe UI", 20, "bold")).pack(pady=10)

        # Tipo de venta
        ctk.CTkLabel(panel, text="Tipo de Venta:", font=("Segoe UI", 14)).pack(anchor="w")
        ctk.CTkLabel(panel, text="Ticket", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

        # Total
        ctk.CTkLabel(panel, text=f"Total: ${self.total:.2f}", font=("Segoe UI", 14)).pack(anchor="w", pady=(10, 5))

        # Efectivo
        ctk.CTkLabel(panel, text="Efectivo:", font=("Segoe UI", 14)).pack(anchor="w")
        ctk.CTkEntry(panel, textvariable=self.efectivo).pack(fill="x", pady=5)

        # Otros métodos
        ctk.CTkLabel(panel, text="Débito / Crédito / Transferencia:", font=("Segoe UI", 14)).pack(anchor="w")
        ctk.CTkEntry(panel, textvariable=self.otros).pack(fill="x", pady=5)

        # Pago total y cambio
        self.pago_label = ctk.CTkLabel(panel, text="Pago Total: $0.00", font=("Segoe UI", 14))
        self.pago_label.pack(anchor="w", pady=(10, 0))

        self.cambio_label = ctk.CTkLabel(panel, text="Su Cambio: $0.00", font=("Segoe UI", 14))
        self.cambio_label.pack(anchor="w", pady=(0, 10))

        # Botones
        botones = ctk.CTkFrame(panel)
        botones.pack(pady=20)

        ctk.CTkButton(botones, text="Cobrar", command=self.calcular_cambio).pack(side="left", padx=10)
        ctk.CTkButton(botones, text="Cerrar", command=self.master.destroy).pack(side="left", padx=10)

    def calcular_cambio(self):
        efectivo = self.efectivo.get()
        otros = self.otros.get()
        pago_total = efectivo + otros
        cambio = pago_total - self.total if pago_total >= self.total else 0.0

        self.pago_label.configure(text=f"Pago Total: ${pago_total:.2f}")
        self.cambio_label.configure(text=f"Su Cambio: ${cambio:.2f}")