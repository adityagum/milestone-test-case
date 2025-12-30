from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

class BaseEvent(BaseModel):
    event_version: int = 1
    event_id: str
    occurred_at: datetime

    @classmethod
    def new(cls, **kwargs):
        return cls(
            event_id=str(uuid.uuid4()),
            occurred_at=datetime.now(timezone.utc),
            **kwargs
        )

class TicketReserveRequested(BaseEvent):
    order_id: str
    event_id_ref: str
    user_id: str
    quantity: int
