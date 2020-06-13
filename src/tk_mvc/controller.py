from .view import View
from .event import Event
from typing import Dict
from typing import Callable


class BaseController:
    """
    BaseController defines a relationship with View and provides an event handler loop. This class should be
    derived from before use.
    """

    EVENT_HANDLER_INTERVAL = 100

    def __init__(self) -> None:
        self._view = View()

        self._event_handlers: Dict[str, Callable[[Event], None]] = {}
        self._view.add_loop_hook(self._handle_events, self.EVENT_HANDLER_INTERVAL)

    def start(self) -> None:
        self._view.start_mainloop()

    def _handle_events(self) -> None:
        """
        Processes any events from _view. This function is added into _view's mainloop from __init__.
        """
        for e in self._view.get_events():
            if e.type in self._event_handlers:
                self._event_handlers[e.type](e)

    def _add_event_handlers(self, event_handlers: Dict[str, Callable[[Event], None]]) -> None:
        for event, handler in event_handlers.items():
            self._event_handlers[event] = handler
