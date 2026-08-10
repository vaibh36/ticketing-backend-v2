from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import CreateBooking
from service import create_booking, get_all_bookings, get_bookings_by_user


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("/")
def get_bookings(
    db: Session = Depends(get_db)
):
    return get_all_bookings(db)


@router.post("/")
def add_booking(
    booking_data: CreateBooking,
    db: Session = Depends(get_db)
):
    booking, error = create_booking(
        db,
        booking_data
    )

    if error == "EVENT_NOT_FOUND":
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if error == "Number of seats must be greater than zero":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    if error == "Not enough seats available":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    if error == "EVENT_SERVICE_ERROR":
        raise HTTPException(
            status_code=500,
            detail="Unable to communicate with Event Service"
        )

    return booking

@router.get("/user/{user_name}")
def get_user_bookings(
    user_name: str,
    db: Session = Depends(get_db)
):
    return get_bookings_by_user(
        db,
        user_name
    )