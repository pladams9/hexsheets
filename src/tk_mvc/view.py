class View:
    def __init__(self, tk_root):
        self._tk_root = tk_root
        self._observers = {}
        self._events = []

    def add_observer(self, name, callback):
        self._observers[name] = callback

    def set_value(self, name, value):
        self._observers[name](value)

    def add_event(self, event):
        self._events.append(event)

    def get_events(self, n=0):
        if n == 0:
            n = len(self._events)
        for i in range(n):
            if len(self._events) > 0:
                yield self._events.pop(0)
            else:
                yield None
