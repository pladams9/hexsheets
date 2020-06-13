import tkinter as tk
from typing import List, Dict, Callable, Any, Tuple, Iterator, Type
from .event import Event
from .window import BaseWindow

LoopHookCallback = Callable[[], None]
ObserverCallback = Callable[[Any], None]


class ViewError(Exception):
    pass


class View:
    """
    View is a concrete class that provides a layer between tkinter and a controller class. View owns the tk root window
    and starts its mainloop.

    Custom window classes are passed to View to be created and then shown/hidden as directed.

    Windows can trigger Events through View that will be handled by a controller class. The controller class hooks into
    the program loop through add_loop_hook. Windows also add observers to View which are triggered when a controller
    updates those values.
    """

    def __init__(self) -> None:
        self._tk_root = tk.Tk()
        self._tk_root.overrideredirect(1)
        self._tk_root.withdraw()

        self._observers: Dict[str, ObserverCallback] = {}
        self._events: List[Event] = []
        self._windows: Dict[str, tk.Toplevel] = {}
        self._loop_hooks: List[Tuple[LoopHookCallback, int]] = []

    def start_mainloop(self) -> None:
        for func, interval in self._loop_hooks:
            self._tk_root.after(interval, lambda: self._run_loop_hook(func, interval))
        self._tk_root.mainloop()

    def add_loop_hook(self, func: LoopHookCallback, interval: int) -> None:
        self._loop_hooks.append((func, interval))

    def _run_loop_hook(self, func: LoopHookCallback, interval: int) -> None:
        func()
        self._tk_root.after(interval, lambda: self._run_loop_hook(func, interval))

    def add_observer(self, name: str, callback: ObserverCallback) -> None:
        self._observers[name] = callback

    def set_value(self, name: str, value: Any) -> None:
        self._observers[name](value)

    def add_event(self, event: Event) -> None:
        self._events.append(event)

    def get_events(self, n: int = 0) -> Iterator[Event]:
        """
        Yields the next n events. If n == 0, yields all events.
        """
        if n == 0:
            n = len(self._events)
        for i in range(n):
            if len(self._events) > 0:
                yield self._events.pop(0)
            else:
                yield None

    def add_window(self, window_name: str, window_cls: Type[BaseWindow], *args, **kwargs) -> None:
        if window_name not in self._windows:
            new_window = tk.Toplevel(self._tk_root)
            new_window.withdraw()
            window_cls(self, new_window, *args, **kwargs)
            self._windows[window_name] = new_window
        else:
            raise ViewError('Window name already exists.')

    def show_window(self, window_name: str) -> None:
        if window_name in self._windows:
            self._windows[window_name].deiconify()

    def hide_window(self, window_name: str) -> None:
        if window_name in self._windows:
            self._windows[window_name].withdraw()
