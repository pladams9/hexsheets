from typing import Any, Dict, Optional


class Event:
    """
    Basic event class.
    """
    def __init__(self, event_type: str = 'GenericEvent', data: Optional[Dict[str, Any]] = None) -> None:
        self.type = event_type

        if data is None:
            self.data = {}
        else:
            self.data = data

    def __repr__(self) -> str:
        return ''.join(['Event<', self.type, '> ', str(self.data)])
