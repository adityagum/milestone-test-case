from fastapi import APIRouter, Header
from app.usecases.create_order import CreateOrder

router = APIRouter()

@router.post("/orders/reserve")
def reserve(
    event_id: str,
    x_user_id: str = Header(...),
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    order_id = CreateOrder().execute(
        event_id_ref=event_id,
        user_id=x_user_id,
        idempotency_key=idempotency_key,
    )
    return {"order_id": order_id, "status": "pending"}
