import uuid
from shared.events.ticket_events import TicketReserveRequested
from app.adapters.kafka_producer import publish_reserve_requested
from app.adapters.redis_client import redis_client

class CreateOrder:
    def execute(self, event_id_ref: str, user_id: str, idempotency_key: str) -> str:
        idem_key = f"order:{user_id}:{idempotency_key}"
        cached = redis_client.idem_get(idem_key)
        if cached:
            return cached["order_id"]

        order_id = str(uuid.uuid4())

        event = TicketReserveRequested.new(
            order_id=order_id,
            event_id_ref=event_id_ref,
            user_id=user_id,
            quantity=1,
        )
        publish_reserve_requested(event)

        redis_client.idem_set(idem_key, {"order_id": order_id})
        return order_id
