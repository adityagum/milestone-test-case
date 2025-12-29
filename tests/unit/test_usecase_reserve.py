import pytest
from app.adapters.in_memory_repo import InMemoryEventRepository
from app.usecases.create_event import CreateEvent
from app.usecases.reserve_ticket import ReserveTicket
from app.domain.errors import SoldOut

def test_reserve_until_sold_out():
    repo = InMemoryEventRepository()
    CreateEvent(repo).execute("E1", 1)

    ReserveTicket(repo).execute("E1")

    with pytest.raises(SoldOut):
        ReserveTicket(repo).execute("E1")
