import json
import os
from kafka import KafkaProducer
from shared.events.ticket_events import TicketReserveRequested

_bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "redpanda:9092")
_topic = os.getenv("KAFKA_TOPIC_RESERVE_REQUESTED", "ticket_reserve_requested")

_producer = KafkaProducer(
    bootstrap_servers=_bootstrap,
    value_serializer=lambda v: json.dumps(v.model_dump(mode="json")).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if k else None,
    acks="all",
)

def publish_reserve_requested(event: TicketReserveRequested) -> None:
    _producer.send(
        _topic,
        key=event.order_id,        # key = order_id (partition affinity)
        value=event.model_dump(mode="json"),
    )
    _producer.flush()
