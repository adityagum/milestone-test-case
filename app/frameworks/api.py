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


def rate_limiter(x_user_id: str = Header(default="anonymous")):
    limit = int(os.getenv("RATE_LIMIT_PER_SEC", "20"))
    current_second = int(time.time())

    key = f"rl:{x_user_id}:{current_second}"
    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 1)

    if count > limit:
        raise HTTPException(429, "rate limit exceeded")


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
    x_user_id: str = Header(default="anonymous"),
    _=Depends(rate_limiter),
):
    try:
        event = ReserveTicket(repo).execute(event_id)
        return event.__dict__
    except EventNotFound:
        raise HTTPException(404, "not found")
    except SoldOut:
        return {"status": "sold_out"}


@app.get("/events/{event_id}")
def get_event(event_id: str):
    try:
        event = GetEvent(repo).execute(event_id)
        return event.__dict__
    except EventNotFound:
        raise HTTPException(404, "not found")
