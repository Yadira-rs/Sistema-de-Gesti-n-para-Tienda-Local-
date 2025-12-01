import customtkinter as ctk
from tkinter import ttk, messagebox

# Importamos los formularios y controladores necesarios
from views.nuevo_apartado_cliente_form import ClienteForm
from views.apartado_form import ApartadoForm
from controllers.products import obtener_productos
from controllers.clientes_controller import agregar_cliente_y_obtener # Asumo que existe este controlador
from controllers.apartados import crear_apartado_completo

class ApartadoView(ctk.CTkFrame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(header, text="Gestión de Apartados", font=("Segoe UI", 18, "bold")).pack(side="left")
        ctk.CTkButton(header, text="Nuevo Apartado", command=self.iniciar_proceso_apartado).pack(side="right")

        # Tabla para mostrar los apartados existentes
        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.cargar_apartados()

    def cargar_apartados(self):
        """Carga y muestra la lista de apartados en una tabla."""
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()
        
        # Aquí iría la llamada a un controlador para obtener los apartados
        # from controllers.apartados import listar_apartados
        # apartados = listar_apartados()
        
        # Por ahora, mostramos un mensaje.
        ctk.CTkLabel(self.tabla_frame, text="La tabla de apartados se mostrará aquí.").pack(pady=20)

    def iniciar_proceso_apartado(self):
        """Inicia el flujo de creación de un nuevo apartado, empezando por el cliente."""

        # --- PASO 2: Se ejecuta después de que el formulario de cliente se completa ---
        def al_crear_cliente(datos_cliente):
            try:
                # NOTA: Necesitarás un controlador 'clientes_controller.py' con esta función
                cliente_db = agregar_cliente_y_obtener(datos_cliente['nombre'], datos_cliente['telefono'], datos_cliente['email'])
                if not cliente_db:
                    messagebox.showerror("Error de Base de Datos", "No se pudo crear el cliente.", parent=self)
                    return

                # --- PASO 3: Se ejecuta después de agregar los productos ---
                def al_continuar_con_productos(items_apartado):
                    if not items_apartado:
                        messagebox.showwarning("Sin productos", "No se agregaron productos al apartado.", parent=self)
                        return
                    
                    id_apartado = crear_apartado_completo(cliente_db['id_cliente'], items_apartado)
                    if id_apartado:
                        messagebox.showinfo("Éxito", f"Apartado #{id_apartado} creado correctamente.")
                        self.cargar_apartados() # Recargar la lista
                    else:
                        messagebox.showerror("Error", "No se pudo crear el apartado en la base de datos.", parent=self)

                # Abre el formulario para agregar productos
                productos = obtener_productos()
                form_productos = ApartadoForm(self, cliente=cliente_db, productos=productos, on_continue=al_continuar_con_productos)

            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error en el proceso:\n{e}", parent=self)

        # --- PASO 1: Abre el formulario para capturar los datos del cliente ---
        form_cliente = ClienteForm(self, on_create=al_crear_cliente)