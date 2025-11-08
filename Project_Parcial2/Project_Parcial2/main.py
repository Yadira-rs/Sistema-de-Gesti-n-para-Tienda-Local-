# Cuando un proyecto de python se ejecuta, el archivo main.py es el archivo principal o punto de
# entrada, aqui se inicializa la app

from tkinter import Tk
from login_view import LoginApp

def main():
    root = Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()