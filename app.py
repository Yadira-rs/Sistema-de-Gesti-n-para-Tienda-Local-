import tkinter as tk
import customtkinter as ctk
from views.login import LoginWindow

def main():
    """
    Función principal para iniciar la aplicación.
    Crea la ventana raíz y muestra la pantalla de login.
    """
    ctk.deactivate_automatic_dpi_awareness() # Desactiva el listener de DPI para evitar errores
    app = LoginWindow() # LoginWindow es la ventana principal
    app.mainloop() # Ejecutamos el bucle de la aplicación directamente en ella

if __name__ == "__main__":
    main()