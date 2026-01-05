import os

from app.adapters.kafka_consumer import build_consumer
from app.adapters.postgres_repo import InventoryRepository
from app.usecases.reserve_inventory import ReserveInventory

def main():
    print("Inventory consumer starting...", flush=True)

    consumer = build_consumer(
        os.environ["KAFKA_BOOTSTRAP_SERVERS"],
        os.environ["KAFKA_TOPIC_RESERVE_REQUESTED"],
    )

    print("Subscribed to topic, waiting for messages...", flush=True)

    repo = InventoryRepository(os.environ["DATABASE_URL"])
    usecase = ReserveInventory(repo)

    BATCH_SIZE = 10
    processed = 0

    for msg in consumer:
        print("Consumed message:", msg.value, flush=True)

        usecase.execute(msg.value)
        processed += 1

        if processed % BATCH_SIZE == 0:
            consumer.commit()
            print(f"Committed {processed} messages", flush=True)


if __name__ == "__main__":
    main()
