class Event:
    def __init__(self, type='GenericEvent', data=None):
        self.type = type

        if data is None:
            self.data = {}
        else:
            self.data = data

    def __repr__(self):
        return ''.join(['Event<', self.type, '> ', str(self.data)])