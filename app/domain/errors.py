class DomainError(Exception):
    pass

class InvalidStock(DomainError):
    pass

class SoldOut(DomainError):
    pass

class EventNotFound(DomainError):
    pass
