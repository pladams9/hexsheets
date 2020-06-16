from tkinter import Frame
from tk_mvc import View

class WindowPart(Frame):
    """
    The WindowPart class is a helper for splitting up windows into multiple files. Derived classes should override the
    _build method, and the Window in question can add the WindowPart the same way they would a frame (with the exception
    that a View must passed to it).
    """

    def __init__(self, view: View, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._view = view
        self._build()

    def _build(self):
        """
        Any widgets that need to be created as part of the WindowPart should be added in the derived class's _build.
        """
        pass
