from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    total_seats: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    available_seats: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )