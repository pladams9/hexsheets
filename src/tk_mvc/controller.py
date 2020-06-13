import tk_mvc


class Controller:
    EVENT_HANDLER_INTERVAL = 100

    def __init__(self):
        self._view = tk_mvc.View()

        self._event_handlers = {}
        self._view.add_loop_hook(self.handle_events, Controller.EVENT_HANDLER_INTERVAL)

    def start(self):
        self._view.start_mainloop()

    def handle_events(self):
        for e in self._view.get_events():
            if e.type in self._event_handlers:
                self._event_handlers[e.type](e)

    def add_event_handlers(self, event_handlers: dict):
        for event, handler in event_handlers.items():
            self._event_handlers[event] = handler
