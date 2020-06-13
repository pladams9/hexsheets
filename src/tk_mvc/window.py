from tkinter import Frame
from tkinter import Toplevel


class BaseWindow(Frame):
    """
    All windows in tk_mvc derive from BaseWindow. It is simply a Frame that View will place inside a TopLevel
    upon creation.
    """

    def __init__(self, view, parent_toplevel: Toplevel, *args, **kwargs) -> None:
        super().__init__(parent_toplevel)
        self._view = view
        self._window = parent_toplevel
