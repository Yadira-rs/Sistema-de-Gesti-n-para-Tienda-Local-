import customtkinter as ctk

class VerApartado(ctk.CTkToplevel):
    """
    Ventana emergente para mostrar todos los detalles de un apartado específico.
    """
    def __init__(self, parent, apartado_data):
        super().__init__(parent)
        self.title(f"Detalle del Apartado #{apartado_data.get('id_apartado', 'N/A')}")
        self.geometry("500x600")
        self.transient(parent)
        self.grab_set()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # --- Contenedor principal con scroll ---
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título
        ctk.CTkLabel(scroll_frame, text="Ver Apartado", font=("Segoe UI", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(scroll_frame, text=f"Detalle del Apartado #{apartado_data.get('id_apartado', 'N/A')}", font=("Segoe UI", 14)).pack()

        # Cliente
        cliente = apartado_data.get("cliente", {})
        ctk.CTkLabel(scroll_frame, text="Información del Cliente", font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(scroll_frame, text=cliente.get("nombre", "Sin nombre")).pack()
        ctk.CTkLabel(scroll_frame, text=f"📞 {cliente.get('telefono', 'Sin teléfono')}").pack()
        ctk.CTkLabel(scroll_frame, text=f"📧 {cliente.get('email', 'Sin email')}").pack()

        # Productos
        ctk.CTkLabel(scroll_frame, text="Productos Apartados", font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))
        for p in apartado_data.get("productos", []):
            ctk.CTkLabel(scroll_frame, text=f"- {p.get('nombre', '?')} (x{p.get('cantidad', 0)})").pack()

        # Totales
        total = float(apartado_data.get('total', 0))
        pagado = float(apartado_data.get('pagado', 0))
        ctk.CTkLabel(scroll_frame, text=f"Total: ${total:.2f}", font=("Segoe UI", 12, "bold")).pack(pady=5)
        ctk.CTkLabel(scroll_frame, text=f"Pagado: ${pagado:.2f}", font=("Segoe UI", 12)).pack()
        ctk.CTkLabel(scroll_frame, text=f"Saldo Pendiente: ${total - pagado:.2f}", font=("Segoe UI", 12, "bold"), text_color="orange").pack()

        # Historial de pagos
        ctk.CTkLabel(scroll_frame, text="Historial de Pagos", font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))
        for pago in apartado_data.get("pagos", []):
            ctk.CTkLabel(scroll_frame, text=f"{pago.get('fecha')} - {pago.get('metodo')} ${float(pago.get('monto', 0)):.2f}").pack()

        # Fechas
        ctk.CTkLabel(scroll_frame, text=f"Fecha de Apartado: {apartado_data.get('fecha_apartado', 'N/A')}", font=("Segoe UI", 12)).pack(pady=5)
        ctk.CTkLabel(scroll_frame, text=f"Fecha Límite: {apartado_data.get('fecha_limite', 'N/A')}", font=("Segoe UI", 12)).pack()

        # Botón cerrar
        ctk.CTkButton(self, text="Cerrar", command=self.destroy).pack(pady=10)