import tkinter as tk
from views.login import LoginWindow
from views.main import MainApp
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Boutique Rosa Janet - Login')
    root.geometry('400x800')

    def on_success(user):
        root.destroy()
        app = MainApp(user)
        app.mainloop()

    LoginWindow(root)
    root.mainloop()
