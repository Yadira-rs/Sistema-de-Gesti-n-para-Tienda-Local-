"""
Script de prueba para el formulario de Nuevo Usuario
Ejecuta este archivo para probar el formulario independientemente
"""
import customtkinter as ctk
from views.nuevo_usuario_form import NuevoUsuarioForm

def test_callback(datos):
    print("Datos recibidos del formulario:")
    print(f"  - Nombre completo: {datos['nombre_completo']}")
    print(f"  - Email: {datos['email']}")
    print(f"  - Contraseña: {datos['password']}")
    print(f"  - Rol: {datos['rol']}")
    print(f"  - Usuario activo: {datos['activo']}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.withdraw()  # Ocultar ventana principal
    
    # Abrir el formulario
    form = NuevoUsuarioForm(root, on_create=test_callback)
    
    root.mainloop()
