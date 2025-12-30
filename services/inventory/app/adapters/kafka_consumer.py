from kafka import KafkaConsumer
import json

def build_consumer(bootstrap: str, topic: str):
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap,
        group_id="inventory-service",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
