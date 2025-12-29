import pytest
from app.domain.entities import Event
from app.domain.errors import InvalidStock, SoldOut

def test_create_event_stock_cannot_be_negative():
    with pytest.raises(InvalidStock):
        Event.create("E1", -1)

def test_reserve_when_stock_zero_should_fail():
    event = Event.create("E1", 0)
    with pytest.raises(SoldOut):
        event.reserve_one()
