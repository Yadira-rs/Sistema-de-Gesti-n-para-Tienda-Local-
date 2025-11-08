import tkinter as tk
from tkinter import messagebox, ttk
from database import crear_conexion
from user_controller import eliminar_usuario
from user_controller import *
import mysql.connector  # Asegúrate de tener instalado este módulo o el conector que uses

class UserApp:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Bienvenid@ {username}")
        self.root.geometry("500x500")
        self.root.resizable(True, True)
        self.crear_elementos()
        self.ver_usuarios()
        self.root.mainloop()
        
    def crear_elementos(self):
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=20)

        tk.Label(frame_botones, text=f"¡Hola {self.username}!", font=("Arial", 18, "bold")).pack(pady=15)
        tk.Button(frame_botones, text="Agregar Usuario", command=self.agregar_usuario, width=20).pack(pady=5)    
        tk.Button(frame_botones, text="Actualizar Usuario", command=self.actualizar_usuario, width=20).pack(pady=5)
        tk.Button(frame_botones, text="Eliminar Usuario", command=self.eliminar_usuario, width=20).pack(pady=5)
        tk.Button(frame_botones, text="Cerrar Sesión", command=self.cerrar_sesion, width=20).pack(pady=15)

        tk.Label(self.root, text="Lista de Usuarios", font=("Arial", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Usuario"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    def agregar_usuario(self):
        def guardar():
            u = entry_user.get().strip()
            p = entry_pass.get().strip()
            if not u or not p:
                messagebox.showwarning("Campos vacíos", "Ingrese usuario y contraseña.")
                return
            if agregar_usuarios(u, p):
                messagebox.showinfo("Éxito", f"Usuario '{u}' creado correctamente.")
                self.ver_usuarios()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario.")
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Usuario")
        ventana.geometry("300x200")
        tk.Label(ventana, text="Usuario").pack(pady=5)
        entry_user = tk.Entry(ventana)
        entry_user.pack(pady=5)
        tk.Label(ventana, text="Contraseña").pack(pady=5)
        entry_pass = tk.Entry(ventana, show="*")
        entry_pass.pack(pady=5)
        tk.Button(ventana, text="Crear Usuario", command=guardar).pack(pady=10)

    def ver_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = ver_usuarios()
        for u in usuarios:
            self.tree.insert("", tk.END, values=u)


    def actualizar_usuario(self):
        selecc_usuario = self.tree.focus()
        if not selecc_usuario:
            messagebox.showwarning("Selecciona un usuario")
            return

        values = self.tree.item(selecc_usuario, "values")
        user_id = values[0]

        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar Usuario")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Nuevo Usuario").pack(pady=5)
        entry_user = tk.Entry(ventana)
        entry_user.insert(0, values[1])
        entry_user.pack(pady=5)

        tk.Label(ventana, text="Nueva Contraseña").pack(pady=5)
        entry_pass = tk.Entry(ventana, show="*")
        entry_pass.pack(pady=5)

        def guardar():
            nuevo_usuario = entry_user.get().strip()
            nueva_password = entry_pass.get().strip()
            if actualizar_usuario(user_id, nuevo_usuario, nueva_password):
                messagebox.showinfo("Actualizado", "Usuario actualizado correctamente")
                self.ver_usuarios()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el usuario")

        tk.Button(ventana, text="Actualizar", command=guardar).pack(pady=10)

           
    def eliminar_usuario(self):
        selecc_usuario = self.tree.focus()
        if not selecc_usuario:
            messagebox.showwarning("Por favor, selecciona un usuario")
            return
        
        values = self.tree.item(selecc_usuario, "values")
        user_id = values[0]
        confirmacion = messagebox.askyesno("Seguro que deseas eliminar este usuario?")

        if confirmacion:
            if eliminar_usuario(user_id):
                messagebox.showinfo("Usuario eliminado correctamente")
                self.ver_usuarios()
            else:
                messagebox.showerror("Error, no se pudo eliminar el usuario seleccionado")

    def cerrar_sesion(self):
        self.root.destroy()


# --------------------------
# FUNCIÓN PARA AGREGAR USUARIOS
# --------------------------

def agregar_usuarios(username, password):
    conexion = crear_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (username, password))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al crear un usuario. Tipo de error: {e}")
        return False


if __name__ == "__main__":
    App = UserApp("admin")