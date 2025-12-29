from app.domain.errors import EventNotFound

class GetEvent:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, event_id: str):
        event = self.repo.get(event_id)
        if not event:
            raise EventNotFound()
        return event
