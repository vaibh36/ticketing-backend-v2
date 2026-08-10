from sqlalchemy.orm import Session

from models import Event
from schemas import CreateEvent, UpdateEvent


def get_all_events(db: Session):
    return db.query(Event).all()


def get_event_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def create_event(db: Session, event_data: CreateEvent):
    new_event = Event(
        name=event_data.name,
        total_seats=event_data.total_seats,
        available_seats=event_data.total_seats
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


def update_event(
    db: Session,
    event_id: int,
    event_data: UpdateEvent
):
    event = get_event_by_id(db, event_id)

    if event is None:
        return None

    if event_data.name is not None:
        event.name = event_data.name

    if event_data.total_seats is not None:
        difference = event_data.total_seats - event.total_seats

        event.total_seats = event_data.total_seats
        event.available_seats += difference

    db.commit()
    db.refresh(event)

    return event


def delete_event(db: Session, event_id: int):
    event = get_event_by_id(db, event_id)

    if event is None:
        return None

    db.delete(event)
    db.commit()

    return event

def reserve_seats(
    db: Session,
    event_id: int,
    number_of_seats: int
):
    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .with_for_update()
        .first()
    )

    if event is None:
        return None, "EVENT_NOT_FOUND"

    if number_of_seats <= 0:
        return None, "INVALID_SEAT_COUNT"

    if event.available_seats < number_of_seats:
        return None, "NOT_ENOUGH_SEATS"

    event.available_seats -= number_of_seats

    db.commit()
    db.refresh(event)

    return event, None