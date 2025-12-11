import tkinter as tk
import customtkinter as ctk
from views.login import LoginWindow
import sys
import os

def ocultar_consola():
    """Ocultar la ventana de consola en Windows"""
    try:
        import ctypes
        # Obtener el handle de la ventana de consola
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd != 0:
            # Ocultar la ventana de consola
            ctypes.windll.user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE
    except Exception as e:
        # Si hay error, continuar sin ocultar
        pass

def main():
    """
    Función principal para iniciar la aplicación.
    Crea la ventana raíz y muestra la pantalla de login.
    """
    # Ocultar consola automáticamente
    ocultar_consola()
    
    ctk.deactivate_automatic_dpi_awareness() # Desactiva el listener de DPI para evitar errores
    app = LoginWindow() # LoginWindow es la ventana principal
    app.mainloop() # Ejecutamos el bucle de la aplicación directamente en ella

if __name__ == "__main__":
    main()