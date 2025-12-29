import psycopg
from contextlib import contextmanager
from psycopg.rows import dict_row

from app.domain.entities import Event
from app.domain.errors import SoldOut
from app.usecases.ports import EventRepository


class PostgresEventRepository(EventRepository):
    def __init__(self, dsn: str):
        self.dsn = dsn

    @contextmanager
    def _conn(self):
        with psycopg.connect(self.dsn, row_factory=dict_row) as conn:
            yield conn

    def add(self, event: Event):
        with self._conn() as conn, conn.transaction():
            conn.execute(
                """
                INSERT INTO events (id, total_stock, available_stock, reserved_count)
                VALUES (%s,%s,%s,%s)
                ON CONFLICT (id) DO NOTHING
                """,
                (event.id, event.total_stock, event.available_stock, event.reserved_count),
            )

    def get(self, event_id: str):
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM events WHERE id=%s", (event_id,)
            ).fetchone()
            return Event(**row) if row else None

    def save(self, event: Event):
        with self._conn() as conn, conn.transaction():
            row = conn.execute(
                """
                UPDATE events
                SET available_stock = available_stock - 1,
                    reserved_count = reserved_count + 1
                WHERE id=%s AND available_stock > 0
                RETURNING *
                """,
                (event.id,),
            ).fetchone()

            if not row:
                raise SoldOut()

            event.available_stock = row["available_stock"]
            event.reserved_count = row["reserved_count"]
