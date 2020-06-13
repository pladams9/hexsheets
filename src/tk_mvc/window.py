from tkinter import Frame
from tkinter import Toplevel
from .view import View


class BaseWindow(Frame):
    """
    All windows in tk_mvc derive from BaseWindow. It is simply a Frame that View will place inside a TopLevel
    upon creation.
    """

    def __init__(self, view: View, parent_toplevel: Toplevel) -> None:
        super().__init__(parent_toplevel)
        self._view = view
        self._parent_toplevel = parent_toplevel
