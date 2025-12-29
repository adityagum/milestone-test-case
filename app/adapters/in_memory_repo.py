class InMemoryEventRepository:
    def __init__(self):
        self._data = {}

    def add(self, event):
        self._data[event.id] = event

    def get(self, event_id):
        return self._data.get(event_id)

    def save(self, event):
        self._data[event.id] = event
