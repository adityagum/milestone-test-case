from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

# ======================
# Base Event
# ======================
class BaseEvent(BaseModel):
    event_version: int = 1
    event_id: str
    occurred_at: datetime

    @classmethod
    def new(cls, **kwargs):
        return cls(
            event_id=str(uuid.uuid4()),
            occurred_at=datetime.now(timezone.utc),
            **kwargs,
        )

# ======================
# Events
# ======================
class TicketReserveRequested(BaseEvent):
    order_id: str
    event_id_ref: str
    user_id: str
    quantity: int


class TicketReserved(BaseEvent):
    order_id: str
    event_id_ref: str


class TicketReservationFailed(BaseEvent):
    order_id: str
    event_id_ref: str
    reason: str
