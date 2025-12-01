"""
Script de prueba para el ticket de venta
Ejecuta este archivo para ver cómo se ve el ticket
"""
import customtkinter as ctk
from views.ticket_venta_view import TicketVentaView

if __name__ == "__main__":
    # Datos de prueba de una venta
    venta_test = {
        'id_venta': 123,
        'total': 577.00,
        'metodo': 'Efectivo',
        'descuento': 20.00,
        'items': [
            {
                'nombre': 'Blusa Rosa',
                'cantidad': 2,
                'precio': 199.00
            },
            {
                'nombre': 'Pantalón Negro',
                'cantidad': 1,
                'precio': 299.00
            },
            {
                'nombre': 'Vestido Casual',
                'cantidad': 1,
                'precio': 99.00
            }
        ]
    }
    
    root = ctk.CTk()
    root.withdraw()  # Ocultar ventana principal
    
    ticket = TicketVentaView(root, venta_test)
    
    root.mainloop()
