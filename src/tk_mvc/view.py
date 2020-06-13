import tkinter as tk


class ViewError(Exception):
    pass


class View:
    def __init__(self):
        self._tk_root = tk.Tk()
        self._tk_root.overrideredirect(1)
        self._tk_root.withdraw()

        self._observers = {}
        self._events = []
        self._windows = {}
        self._loop_hooks = []

    def start_mainloop(self):
        for func, interval in self._loop_hooks:
            self._tk_root.after(interval, lambda: self._run_loop_hook(func, interval))
        self._tk_root.mainloop()

    def add_loop_hook(self, func, interval):
        self._loop_hooks.append((func, interval))

    def _run_loop_hook(self, func, interval):
        func()
        self._tk_root.after(interval, lambda: self._run_loop_hook(func, interval))

    def add_observer(self, name, callback):
        self._observers[name] = callback

    def set_value(self, name, value):
        self._observers[name](value)

    def add_event(self, event):
        self._events.append(event)

    def get_events(self, n: int = 0):
        """Yields the next [n] events."""
        if n == 0:
            n = len(self._events)
        for i in range(n):
            if len(self._events) > 0:
                yield self._events.pop(0)
            else:
                yield None

    def add_window(self, window_name, window_cls, *args, **kwargs):
        if window_name not in self._windows:
            new_window = tk.Toplevel(self._tk_root)
            new_window.withdraw()
            window_cls(self, new_window, *args, **kwargs)
            self._windows[window_name] = new_window
        else:
            raise ViewError('Window name already exists.')

    def show_window(self, window_name):
        if window_name in self._windows:
            self._windows[window_name].deiconify()

    def hide_window(self, window_name):
        if window_name in self._windows:
            self._windows[window_name].withdraw()
