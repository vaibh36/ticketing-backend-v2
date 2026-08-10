from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import CreateEvent, UpdateEvent, ReserveSeats
from service import (
    create_event,
    get_all_events,
    get_event_by_id,
    update_event,
    delete_event,
    reserve_seats
)


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("/")
def get_events(db: Session = Depends(get_db)):
    return get_all_events(db)


@router.get("/{event_id}")
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = get_event_by_id(db, event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


@router.post("/")
def add_event(
    event_data: CreateEvent,
    db: Session = Depends(get_db)
):
    return create_event(db, event_data)


@router.patch("/{event_id}")
def edit_event(
    event_id: int,
    event_data: UpdateEvent,
    db: Session = Depends(get_db)
):
    event = update_event(
        db,
        event_id,
        event_data
    )

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


@router.delete("/{event_id}")
def remove_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = delete_event(db, event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return {
        "message": "Event deleted successfully",
        "event": event
    }


@router.post("/{event_id}/reserve")
def reserve_event_seats(
    event_id: int,
    data: ReserveSeats,
    db: Session = Depends(get_db)
):
    event, error = reserve_seats(
        db,
        event_id,
        data.number_of_seats
    )

    if error == "EVENT_NOT_FOUND":
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if error == "INVALID_SEAT_COUNT":
        raise HTTPException(
            status_code=400,
            detail="Number of seats must be greater than zero"
        )

    if error == "NOT_ENOUGH_SEATS":
        raise HTTPException(
            status_code=400,
            detail="Not enough seats available"
        )

    return event