from app.domain.entities import Event

class CreateEvent:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, event_id: str, stock: int):
        event = Event.create(event_id, stock)
        self.repo.add(event)
        return event
