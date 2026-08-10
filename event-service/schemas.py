from pydantic import BaseModel
from typing import Optional

class ReserveSeats(BaseModel):
    number_of_seats: int

class CreateEvent(BaseModel):
    name: str
    total_seats: int


class Event(BaseModel):
    id: int
    name: str
    total_seats: int
    available_seats: int


class UpdateEvent(BaseModel):
    name: Optional[str] = None
    total_seats: Optional[int] = None