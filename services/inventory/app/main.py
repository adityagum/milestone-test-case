import os

from app.adapters.kafka_consumer import build_consumer
from app.adapters.postgres_repo import InventoryRepository
from app.usecases.reserve_inventory import ReserveInventory

def main():
    consumer = build_consumer(
        os.environ["KAFKA_BOOTSTRAP_SERVERS"],
        os.environ["KAFKA_TOPIC_RESERVE_REQUESTED"],
    )

    repo = InventoryRepository(os.environ["DATABASE_URL"])
    usecase = ReserveInventory(repo)

    for msg in consumer:
        usecase.execute(msg.value)
        consumer.commit()

if __name__ == "__main__":
    main()
