from datetime import datetime, timezone
from shared.events.ticket_events import (
    TicketReserved, TicketReservationFailed
)

class ReserveInventory:
    def __init__(self, repo, producer):
        self.repo = repo
        self.producer = producer

    def execute(self, payload: dict):
        order_id = payload["order_id"]
        event_id = payload["event_id"]

        if self.repo.already_processed(order_id):
            return  # idempotent: ignore reprocess

        success = self.repo.reserve_atomic(event_id)

        if success:
            self.repo.mark_processed(order_id)
            self.producer.publish_reserved(
                TicketReserved(
                    event_id=event_id,
                    order_id=order_id,
                    occurred_at=datetime.now(timezone.utc),
                ).model_dump(mode="json")
            )
        else:
            self.producer.publish_failed(
                TicketReservationFailed(
                    event_id=event_id,
                    order_id=order_id,
                    reason="sold_out",
                    occurred_at=datetime.now(timezone.utc),
                ).model_dump(mode="json")
            )
