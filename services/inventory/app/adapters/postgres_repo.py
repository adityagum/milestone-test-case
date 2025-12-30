import psycopg

class InventoryRepository:
    def __init__(self, dsn: str):
        self._dsn = dsn

    def reserve_atomic(self, event_id: str) -> bool:
        with psycopg.connect(self._dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                  UPDATE events
                  SET available_stock = available_stock - 1
                  WHERE event_id = %s AND available_stock > 0
                """, (event_id,))
                return cur.rowcount == 1

    def mark_processed(self, order_id: str) -> None:
        with psycopg.connect(self._dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                  INSERT INTO processed_events(order_id)
                  VALUES (%s)
                  ON CONFLICT DO NOTHING
                """, (order_id,))

    def already_processed(self, order_id: str) -> bool:
        with psycopg.connect(self._dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM processed_events WHERE order_id=%s", (order_id,))
                return cur.fetchone() is not None
