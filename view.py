import tkinter as tk
import gui.windows


class View:
    def __init__(self, root):
        self.root = root
        self._observers = {}

        # Windows
        self.main_window = gui.windows.MainWindow(self, root)

    def add_observer(self, name, callback):
        def func(*args):
            callback(self.root.getvar(args[0]))
        self._observers[name] = tk.Variable()
        self._observers[name].trace('w', func)

    def set_value(self, name, value):
        self._observers[name].set(value)
