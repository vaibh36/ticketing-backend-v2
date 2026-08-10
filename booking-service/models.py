from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    event_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    user_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    number_of_seats: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="CONFIRMED"
    )