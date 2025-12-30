from shared.events.ticket_events import TicketReserveRequested

def publish_reserve_requested(order_id: str, event_id_ref: str, user_id: str):
    event = TicketReserveRequested.new(
        order_id=order_id,
        event_id_ref=event_id_ref,
        user_id=user_id,
        quantity=1,
    )
    # TODO: send to Kafka
