import os
import httpx

from sqlalchemy.orm import Session

from models import Booking
from schemas import CreateBooking


EVENT_SERVICE_URL = os.getenv(
    "EVENT_SERVICE_URL",
    "http://event-service:8001"
)


def create_booking(
    db: Session,
    booking_data: CreateBooking
):
    reserve_url = (
        f"{EVENT_SERVICE_URL}/events/"
        f"{booking_data.event_id}/reserve"
    )

    response = httpx.post(
        reserve_url,
        json={
            "number_of_seats": booking_data.number_of_seats
        }
    )

    if response.status_code == 404:
        return None, "EVENT_NOT_FOUND"

    if response.status_code == 400:
        error_detail = response.json().get("detail")
        return None, error_detail

    if response.status_code != 200:
        return None, "EVENT_SERVICE_ERROR"

    booking = Booking(
        event_id=booking_data.event_id,
        user_name=booking_data.user_name,
        number_of_seats=booking_data.number_of_seats,
        status="CONFIRMED"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking, None


def get_all_bookings(db: Session):
    return db.query(Booking).all()

def get_bookings_by_user(
    db: Session,
    user_name: str
):
    return (
        db.query(Booking)
        .filter(Booking.user_name == user_name)
        .all()
    )