import view
import tkinter as tk


class Controller:
    def __init__(self):
        self.model = None
        self.tk_root = tk.Tk()
        self.view = view.View(self.tk_root)

    def start(self):
        self.tk_root.mainloop()
