from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.adapters.in_memory_repo import InMemoryEventRepository
from app.usecases.create_event import CreateEvent
from app.usecases.reserve_ticket import ReserveTicket
from app.usecases.get_event import GetEvent
from app.domain.errors import InvalidStock, SoldOut, EventNotFound


class CreateEventBody(BaseModel):
    event_id: str
    stock: int


repo = InMemoryEventRepository()
app = FastAPI()

@app.post("/events")
def create_event(body: CreateEventBody):
    try:
        event = CreateEvent(repo).execute(body.event_id, body.stock)
        return event.__dict__
    except InvalidStock:
        raise HTTPException(400, "invalid stock")

@app.post("/events/{event_id}/reserve")
def reserve(event_id: str):
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
