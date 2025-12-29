from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import os
import time

from app.adapters.postgres_repo import PostgresEventRepository
from app.adapters.redis_client import redis_client
from app.usecases.create_event import CreateEvent
from app.usecases.reserve_ticket import ReserveTicket
from app.usecases.get_event import GetEvent
from app.domain.errors import InvalidStock, SoldOut, EventNotFound


class CreateEventBody(BaseModel):
    event_id: str
    stock: int


repo = PostgresEventRepository(os.environ["DATABASE_URL"])
app = FastAPI()


def rate_limiter(x_user_id: str = Header(...)):
    limit = int(os.getenv("RATE_LIMIT_PER_SEC", "20"))
    key = f"rl:{x_user_id}"

    count, allowed = redis_client.rate_limit_hit(key, limit)

    if not allowed:
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    
def idempotency_guard(
    x_user_id: str = Header(...),
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
) -> str:
    key = f"idemp:{x_user_id}:{idempotency_key}"

    cached = redis_client.idem_get(key)
    if cached is not None:
        # short-circuit: kembalikan response lama
        raise HTTPException(status_code=200, detail=cached)

    return key


@app.post("/events")
def create_event(body: CreateEventBody):
    try:
        event = CreateEvent(repo).execute(body.event_id, body.stock)
        return event.__dict__
    except InvalidStock:
        raise HTTPException(400, "invalid stock")


@app.post("/events/{event_id}/reserve")
def reserve(
    event_id: str,
    x_user_id: str = Header(...),
    idemp_key: str = Depends(idempotency_guard),
    _=Depends(rate_limiter),
):
    try:
        event = ReserveTicket(repo).execute(event_id)
        response = event.__dict__

        redis_client.idem_set(idemp_key, response)
        return response

    except EventNotFound:
        raise HTTPException(404, "not found")

    except SoldOut:
        response = {"status": "sold_out"}
        redis_client.idem_set(idemp_key, response)
        return response


@app.get("/events/{event_id}")
def get_event(event_id: str):
    try:
        event = GetEvent(repo).execute(event_id)
        return event.__dict__
    except EventNotFound:
        raise HTTPException(404, "not found")
