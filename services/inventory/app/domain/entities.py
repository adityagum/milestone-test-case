from dataclasses import dataclass
from .errors import InvalidStock, SoldOut

@dataclass
class Event:
    id: str
    total_stock: int
    available_stock: int
    reserved_count: int = 0

    @staticmethod
    def create(event_id: str, stock: int):
        if stock < 0:
            raise InvalidStock()
        return Event(event_id, stock, stock)

    def reserve_one(self):
        if self.available_stock <= 0:
            raise SoldOut()
        self.available_stock -= 1
        self.reserved_count += 1
