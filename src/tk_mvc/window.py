import tkinter as tk


class BaseWindow(tk.Frame):
    """
    All windows in tk_mvc derive from BaseWindow. It is simply a Frame that View will place inside a TopLevel
    upon creation.
    """

    def __init__(self, view, parent):
        super().__init__(parent)
        self._view = view
