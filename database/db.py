from tkinter import messagebox

def crear_conexion():
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="boutique_db"
        )
        return conn
    except Exception as e:
        print("❌ Error al conectar BD:", e)
        messagebox.showerror("Error de BD", "No se pudo conectar a la base de datos.")
        return None
