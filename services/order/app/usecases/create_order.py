import uuid
from app.adapters.kafka_producer import publish_reserve_requested

class CreateOrder:
    def execute(self, event_id: str, user_id: str, idempotency_key: str) -> str:
        order_id = str(uuid.uuid4())

        publish_reserve_requested(
            order_id=order_id,
            event_id_ref=event_id,
            user_id=user_id,
        )

        return order_id
