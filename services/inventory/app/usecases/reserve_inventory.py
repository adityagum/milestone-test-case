from datetime import datetime, timezone
from shared.events.ticket_events import (
    TicketReserved,
    TicketReservationFailed,
)

class ReserveInventory:
    def __init__(self, repo, producer):
        self.repo = repo
        self.producer = producer

    def execute(self, payload: dict) -> None:
        order_id = payload["order_id"]
        event_id = payload["event_id"]

        # 1️⃣ Idempotency guard
        if self.repo.already_processed(order_id):
            return

        # 2️⃣ Atomic reserve
        success = self.repo.reserve_atomic(event_id)

        # 3️⃣ Mark processed
        self.repo.mark_processed(order_id)

        # # 4️⃣ Emit result event
        # now = datetime.now(timezone.utc)

        # if success:
        #     event = TicketReserved(
        #         event_id=event_id,
        #         order_id=order_id,
        #         occurred_at=now,
        #     )
        #     self.producer.publish_reserved(
        #         event.model_dump(mode="json")
        #     )
        # else:
        #     event = TicketReservationFailed(
        #         event_id=event_id,
        #         order_id=order_id,
        #         reason="sold_out",
        #         occurred_at=now,
        #     )
        #     self.producer.publish_failed(
        #         event.model_dump(mode="json")
        #     )
