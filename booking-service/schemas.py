from pydantic import BaseModel


class CreateBooking(BaseModel):
    event_id: int
    user_name: str
    number_of_seats: int


class BookingResponse(BaseModel):
    id: int
    event_id: int
    user_name: str
    number_of_seats: int
    status: str